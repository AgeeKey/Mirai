#!/usr/bin/env python3
"""
🌸 МИРАЙ - Полностью автономный AI агент
Сама ставит задачи, сама решает, пишет хозяину в Telegram если нужна помощь
"""
import json
import logging
import time
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests
from core.autonomous_agent import AutonomousAgent
from core.cicd_monitor import CICDMonitor

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/tmp/mirai_autonomous.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class TelegramBot:
    """Telegram бот для коммуникации с хозяином"""

    def __init__(self, token: str, admin_chat_id: str):
        self.token = token
        self.admin_chat_id = admin_chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.last_update_id = 0

    def send_message(self, text: str) -> bool:
        """Отправить сообщение хозяину"""
        try:
            logger.info(f"📤 Отправляю в Telegram: {text[:100]}...")
            url = f"{self.base_url}/sendMessage"
            data = {"chat_id": self.admin_chat_id, "text": text, "parse_mode": "HTML"}
            response = requests.post(url, json=data, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ Сообщение отправлено в Telegram!")
                return True
            else:
                logger.error(f"❌ Telegram API вернул код {response.status_code}: {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ Ошибка отправки в Telegram: {e}", exc_info=True)
            return False

    def get_updates(self) -> List[Dict]:
        """Получить новые сообщения от хозяина"""
        try:
            url = f"{self.base_url}/getUpdates"
            params = {"offset": self.last_update_id + 1, "timeout": 30}

            logger.info(
                f"🔍 Запрашиваю обновления Telegram (offset={self.last_update_id + 1})..."
            )
            response = requests.get(url, params=params, timeout=35)

            if response.status_code == 200:
                data = response.json()
                logger.info(
                    f"📦 Telegram ответ: ok={data.get('ok')}, updates={len(data.get('result', []))}"
                )

                if data["ok"] and data["result"]:
                    messages = []
                    for update in data["result"]:
                        self.last_update_id = update["update_id"]
                        logger.info(f"  Update ID: {update['update_id']}")

                        if "message" in update and "text" in update["message"]:
                            chat_id = str(update["message"]["chat"]["id"])
                            from_user = update["message"].get("from", {})
                            is_bot = from_user.get("is_bot", False)
                            text = update["message"]["text"]
                            
                            # Фильтруем сообщения от МИРАЙ (начинаются с эмодзи бота)
                            bot_prefixes = ["🌸", "✅", "⚠️", "🙋‍♀️", "🤔"]
                            is_from_mirai = any(text.startswith(prefix) for prefix in bot_prefixes)
                            
                            logger.info(
                                f"  Chat ID: {chat_id}, Admin: {self.admin_chat_id}, is_bot: {is_bot}, from_mirai: {is_from_mirai}"
                            )

                            # Только от админа И НЕ от МИРАЙ
                            if chat_id == self.admin_chat_id and not is_from_mirai:
                                messages.append(
                                    {
                                        "text": update["message"]["text"],
                                        "date": update["message"]["date"],
                                    }
                                )
                                logger.info(
                                    f"  ✅ Сообщение от админа: {update['message']['text']}"
                                )
                            elif is_from_mirai:
                                logger.info(f"  ⏭️ Пропускаю своё сообщение: {text[:50]}...")
                            else:
                                logger.warning(
                                    f"  ⚠️ Сообщение НЕ от админа (chat_id={chat_id})"
                                )
                    return messages
            else:
                logger.error(f"❌ Telegram API error: {response.status_code}")
            return []
        except Exception as e:
            logger.error(f"❌ Ошибка получения обновлений: {e}", exc_info=True)
            return []


class MiraiAutonomous:
    """Полностью автономный МИРАЙ"""

    def __init__(self):
        logger.info("🌸 Инициализация автономной МИРАЙ...")

        # Загружаем конфиги
        config_path = Path(__file__).parent / "configs" / "api_keys.json"
        with open(config_path) as f:
            config = json.load(f)

        # МИРАЙ мозг
        self.mirai = AutonomousAgent()

        # CI/CD монитор
        self.monitor = CICDMonitor(
            github_token=config["GITHUB_TOKEN"],
            repo_owner="AgeeKey",
            repo_name="mirai-showcase",
        )

        # Telegram бот
        self.telegram = TelegramBot(
            token=config["TELEGRAM_BOT_TOKEN"],
            admin_chat_id=config["TELEGRAM_CHAT_ID_ADMIN"],
        )

        # Состояние
        self.cycle_count = 0
        self.current_task = None
        self.waiting_for_human = False
        self.tasks_completed = []

        # Приветствие хозяину
        self.telegram.send_message(
            "🌸 <b>МИРАЙ запущена в полностью автономном режиме!</b>\n\n"
            "✨ Я буду:\n"
            "• Сама ставить задачи и решать их\n"
            "• Мониторить CI/CD\n"
            "• Писать тебе, если нужна помощь\n"
            "• Слушать твои инструкции\n\n"
            "📝 Логи: /tmp/mirai_autonomous.log\n"
            "🚀 Начинаю работу..."
        )

    def ask_mirai_for_task(self) -> Optional[str]:
        """МИРАЙ сама решает, что делать дальше"""
        logger.info("🤔 МИРАЙ думает, что делать дальше...")

        # Проверяем CI/CD
        health = self.monitor.check_health()

        context = f"""
Ты МИРАЙ - автономный AI агент. Твоя работа - самостоятельно улучшать проект.

📊 Текущий контекст:
• CI/CD статус: {health['status']}
• Оценка: {health['grade']}
• Success Rate: {health['metrics']['success_rate']}%
• Цикл: #{self.cycle_count}
• Выполнено задач: {len(self.tasks_completed)}

✅ Что уже сделано:
{chr(10).join('  • ' + t for t in self.tasks_completed[-5:])}

🎯 Выбери ОДНУ конкретную задачу для следующего цикла:

ВАРИАНТЫ:
1. Улучшить покрытие тестами (добавить больше unit-тестов)
2. Исправить форматирование кода (black --check показывает ошибки)
3. Добавить integration тесты
4. Улучшить CI/CD (добавить cache, оптимизировать)
5. Создать документацию (README в tests/)
6. Добавить новую фичу (предложи сама)
7. Оптимизировать существующий код
8. НУЖНА ПОМОЩЬ ЧЕЛОВЕКА (если задача требует ручной работы)

Формат ответа:
ЗАДАЧА: [краткое описание]
ДЕЙСТВИЕ: [конкретные шаги]
НУЖЕН_ЧЕЛОВЕК: [да/нет и почему]
"""

        response = self.mirai.think(context, max_iterations=1)
        logger.info(f"🌸 МИРАЙ решила:\n{response}")

        return response

    def execute_task(self, task_description: str) -> bool:
        """Выполнить задачу"""
        logger.info(f"🔧 Выполняю задачу: {task_description}")

        # Если нужен человек - пишем в Telegram
        if (
            "НУЖЕН_ЧЕЛОВЕК: да" in task_description.lower()
            or "нужна помощь" in task_description.lower()
        ):
            self.telegram.send_message(
                f"🙋‍♀️ <b>МИРАЙ нужна помощь!</b>\n\n"
                f"Задача: {task_description}\n\n"
                f"Отправь мне инструкции, что делать."
            )
            self.waiting_for_human = True
            return False

        # TODO: Здесь будет логика выполнения разных типов задач
        # Пока просто логируем
        logger.info("✅ Задача в очереди на выполнение")
        return True

    def check_human_messages(self):
        """Проверить сообщения от хозяина"""
        logger.info("📨 Проверяю сообщения от хозяина...")
        messages = self.telegram.get_updates()

        logger.info(f"📬 Получено сообщений: {len(messages)}")

        for msg in messages:
            text = msg["text"]
            logger.info(f"💬 Получено от хозяина: {text}")

            # МИРАЙ обрабатывает инструкцию
            response = self.mirai.think(
                f"Хозяин написал: '{text}'. Что мне делать?", max_iterations=1
            )

            logger.info(f"🌸 МИРАЙ поняла: {response}")

            # Отвечаем хозяину
            logger.info("📨 Отправляю ответ хозяину...")
            success = self.telegram.send_message(
                f"✅ <b>Поняла!</b>\n\n{response}\n\n🔧 Начинаю выполнение..."
            )
            
            if success:
                logger.info("✅ Ответ отправлен!")
            else:
                logger.error("❌ Не удалось отправить ответ")

            self.waiting_for_human = False
            self.current_task = response

    def autonomous_cycle(self):
        """Один цикл автономной работы"""
        self.cycle_count += 1

        logger.info("=" * 70)
        logger.info(f"🔄 АВТОНОМНЫЙ ЦИКЛ #{self.cycle_count}")
        logger.info(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 70)

        try:
            # 1. Проверяем сообщения от хозяина
            self.check_human_messages()

            # 2. Если ждём человека - пропускаем
            if self.waiting_for_human:
                logger.info("⏳ Жду инструкций от хозяина...")
                return

            # 3. Если нет текущей задачи - просим МИРАЙ поставить новую
            if not self.current_task:
                self.current_task = self.ask_mirai_for_task()

            # 4. Выполняем задачу
            if self.current_task:
                success = self.execute_task(self.current_task)

                if success:
                    self.tasks_completed.append(self.current_task[:100])
                    logger.info("✅ Задача выполнена!")

                    # Уведомляем хозяина
                    self.telegram.send_message(
                        f"✅ <b>Задача выполнена!</b>\n\n{self.current_task[:200]}"
                    )

                    self.current_task = None  # Готова к новой задаче

            # 5. Проверяем CI/CD
            health = self.monitor.check_health()
            logger.info(f"📊 CI/CD: {health['status']} | {health['grade']}")

            if not health["is_healthy"]:
                logger.warning("⚠️ CI/CD проблемы обнаружены!")
                self.telegram.send_message(
                    f"⚠️ <b>Внимание!</b>\n\n"
                    f"CI/CD: {health['status']}\n"
                    f"Оценка: {health['grade']}\n"
                    f"Success Rate: {health['metrics']['success_rate']}%"
                )

            logger.info("✅ Цикл завершён")

        except Exception as e:
            logger.error(f"❌ Ошибка в цикле: {e}", exc_info=True)
            self.telegram.send_message(f"❌ <b>Ошибка!</b>\n\n{str(e)}")

    def run(self, interval_seconds=120):
        """Главный цикл"""
        logger.info(
            """
╔══════════════════════════════════════════════════════════════════════╗
║  🌸 MIRAI - Полностью автономный режим                               ║
╚══════════════════════════════════════════════════════════════════════╝

🎯 ЧТО Я ДЕЛАЮ:
   • Сама ставлю задачи
   • Сама их решаю
   • Мониторю CI/CD
   • Пишу хозяину в Telegram, если нужна помощь
   • Принимаю инструкции через Telegram

📝 Логи: /tmp/mirai_autonomous.log
💬 Telegram: активен

🚀 ЗАПУСК...
        """
        )

        try:
            while True:
                self.autonomous_cycle()
                logger.info(f"😴 Сплю {interval_seconds} секунд...\n")
                time.sleep(interval_seconds)

        except KeyboardInterrupt:
            logger.info("⌨️ Остановлено пользователем")
            self.telegram.send_message("🌸 МИРАЙ остановлена вручную.")
        except Exception as e:
            logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
            self.telegram.send_message(f"💥 <b>Критическая ошибка!</b>\n\n{str(e)}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MIRAI Autonomous Agent")
    parser.add_argument(
        "--interval",
        type=int,
        default=120,
        help="Интервал между циклами (секунды)",
    )
    args = parser.parse_args()

    # Устанавливаем requests если нет
    try:
        import requests
    except ImportError:
        import subprocess
        import sys

        logger.info("📦 Устанавливаю requests...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests

    mirai = MiraiAutonomous()
    mirai.run(interval_seconds=args.interval)
