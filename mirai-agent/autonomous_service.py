#!/usr/bin/env python3
"""
🤖 KAIZEN × 🌸 MIRAI - Autonomous Background Service
Работают автономно в фоне, результаты в логи + web dashboard
"""

import sys
import time
import json
import logging
from pathlib import Path
from datetime import datetime
import signal
import os

sys.path.insert(0, "/root/mirai/mirai-agent")

from core.autonomous_agent import AutonomousAgent
from core.cicd_monitor import CICDMonitor

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("/tmp/kaizen_mirai.log"), logging.StreamHandler()],
)

logger = logging.getLogger("KAIZEN_MIRAI")


class AutonomousService:
    """Автономный сервис KAIZEN + MIRAI"""

    def __init__(self):
        logger.info("🤖 Инициализация KAIZEN...")
        self.kaizen = AutonomousAgent()

        logger.info("🌸 Инициализация MIRAI...")
        self.mirai = AutonomousAgent()

        # Load GitHub config
        config_path = Path(__file__).parent / "configs" / "api_keys.json"
        with open(config_path) as f:
            config = json.load(f)

        logger.info("📊 Инициализация CI/CD Monitor...")
        self.monitor = CICDMonitor(
            github_token=config["GITHUB_TOKEN"],
            repo_owner="AgeeKey",
            repo_name="mirai-showcase",
        )

        self.running = True
        self.cycle_count = 0

        # Handle signals
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

    def shutdown(self, signum, frame):
        """Graceful shutdown"""
        logger.info("🛑 Получен сигнал остановки...")
        self.running = False

    def log_separator(self):
        """Красивый разделитель в логах"""
        logger.info("=" * 70)

    def consult_mirai(self, question: str) -> str:
        """KAIZEN консультируется с MIRAI"""
        logger.info("🤖 КАЙДЗЕН спрашивает МИРАЙ...")
        response = self.mirai.think(question, max_iterations=1)
        logger.info(f"🌸 МИРАЙ отвечает: {response[:100]}...")
        return response

    def autonomous_cycle(self):
        """Один цикл автономной работы"""
        self.cycle_count += 1

        self.log_separator()
        logger.info(f"🔄 АВТОНОМНЫЙ ЦИКЛ #{self.cycle_count}")
        logger.info(f"⏰ Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.log_separator()

        try:
            # 1. Проверяем здоровье CI/CD
            logger.info("📊 Проверяю здоровье CI/CD...")
            health = self.monitor.check_health()

            logger.info(f"🏥 Статус: {health['status']} | Оценка: {health['grade']}")
            logger.info(f"✅ Success Rate: {health['metrics']['success_rate']}%")

            # 2. Если есть проблемы - советуемся с MIRAI
            if not health["is_healthy"]:
                logger.warning("⚠️  CI/CD НЕ ЗДОРОВ! Консультируюсь с МИРАЙ...")

                question = f"""
                Ты МИРАЙ. CI/CD pipeline нездоров:
                - Статус: {health['status']}
                - Оценка: {health['grade']}
                - Success rate: {health['metrics']['success_rate']}%
                - Провалов: {health['metrics']['failed']}
                
                Что делать? Выбери ОДНО:
                1. Ждать - возможно само починится
                2. Анализировать логи упавших тестов
                3. Перезапустить workflow
                4. Уведомить хозяина
                
                Формат: "Выбираю [номер]. [Почему]"
                """

                mirai_decision = self.consult_mirai(question)
                logger.info(f"💡 Решение МИРАЙ: {mirai_decision}")

                # KAIZEN выполняет решение MIRAI
                if "1" in mirai_decision:
                    logger.info("⏳ КАЙДЗЕН: Ожидаю улучшения...")
                elif "2" in mirai_decision:
                    logger.info("🔍 КАЙДЗЕН: Анализирую логи...")
                    failures = self.monitor.get_failing_workflows()
                    for fail in failures[:3]:
                        logger.warning(f"   ❌ {fail['name']} #{fail['run_number']}")
                elif "3" in mirai_decision:
                    logger.info("🔄 КАЙДЗЕН: Нужно перезапустить workflow (TODO)")
                elif "4" in mirai_decision:
                    logger.info("📢 КАЙДЗЕН: Уведомляю хозяина (TODO)")
            else:
                logger.info("✨ Всё отлично! CI/CD здоров.")

            # 3. Каждые 5 циклов - спрашиваем MIRAI что улучшить
            if self.cycle_count % 5 == 0:
                logger.info("💭 Время для планирования улучшений...")

                question = """
                Ты МИРАЙ. Прошло 5 циклов мониторинга.
                
                Что улучшить дальше?
                1. Добавить новые метрики в dashboard
                2. Оптимизировать скорость тестов
                3. Создать новые примеры кода
                4. Интегрировать новый сервис
                
                Выбери ОДНО и скажи почему кратко.
                """

                improvement = self.consult_mirai(question)
                logger.info(f"🎯 План улучшений от МИРАЙ: {improvement}")

            # 4. Логируем метрики для истории
            self.save_metrics(health["metrics"])

            logger.info("✅ Цикл завершён успешно")

        except Exception as e:
            logger.error(f"❌ Ошибка в цикле: {e}", exc_info=True)

    def save_metrics(self, metrics):
        """Сохраняем метрики для истории"""
        metrics_file = Path("/tmp/kaizen_mirai_metrics.jsonl")

        record = {
            "timestamp": datetime.now().isoformat(),
            "cycle": self.cycle_count,
            **metrics,
        }

        with open(metrics_file, "a") as f:
            f.write(json.dumps(record) + "\n")

    def run(self, interval_seconds=300):
        """Главный цикл - работаем автономно в фоне"""
        logger.info(
            """
╔══════════════════════════════════════════════════════════════════════╗
║  🤖 KAIZEN × 🌸 MIRAI - Autonomous Service Started                  ║
╚══════════════════════════════════════════════════════════════════════╝

🌸 РЕШЕНИЕ МИРАЙ: Работаем автономно в фоне
   
   "Такой режим позволяет AI-агентам работать без постоянного
   взаимодействия с пользователями, что увеличивает эффективность
   выполнения задач и автоматизацию процессов."

🤖 КАЙДЗЕН: Реализую решение МИРАЙ!

📋 РЕЖИМ РАБОТЫ:
   • Автономные циклы каждые {interval} секунд
   • Мониторинг CI/CD GitHub Actions
   • Консультации между KAIZEN ↔ MIRAI
   • Логи в /tmp/kaizen_mirai.log
   • Метрики в /tmp/kaizen_mirai_metrics.jsonl
   • Dashboard на http://localhost:5000

🎯 ЧТО ДЕЛАЕМ:
   1. Проверяем здоровье CI/CD
   2. При проблемах - MIRAI принимает решения
   3. Каждые 5 циклов - планируем улучшения
   4. Сохраняем метрики для анализа

🚀 ЗАПУСК АВТОНОМНОГО РЕЖИМА...
        """.format(
                interval=interval_seconds
            )
        )

        while self.running:
            try:
                self.autonomous_cycle()

                if self.running:
                    logger.info(
                        f"😴 Сплю {interval_seconds} секунд до следующего цикла..."
                    )
                    time.sleep(interval_seconds)

            except KeyboardInterrupt:
                logger.info("⌨️  Прервано пользователем")
                break
            except Exception as e:
                logger.error(f"💥 Критическая ошибка: {e}", exc_info=True)
                time.sleep(60)  # Wait before retry

        logger.info(
            """
╔══════════════════════════════════════════════════════════════════════╗
║  👋 KAIZEN × MIRAI - Autonomous Service Stopped                     ║
╚══════════════════════════════════════════════════════════════════════╝

🤖 КАЙДЗЕН: Останавливаем автономный режим.
🌸 МИРАЙ: До встречи, ониичан!

📊 Статистика сессии:
   • Циклов выполнено: {cycles}
   • Логи: /tmp/kaizen_mirai.log
   • Метрики: /tmp/kaizen_mirai_metrics.jsonl

改善 (Kaizen) - Continuous Improvement
未来 (Mirai) - Future
        """.format(
                cycles=self.cycle_count
            )
        )


def main():
    """Entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="KAIZEN × MIRAI Autonomous Service")
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Интервал между циклами в секундах (default: 300)",
    )
    parser.add_argument(
        "--daemon", action="store_true", help="Запустить как daemon в фоне"
    )

    args = parser.parse_args()

    if args.daemon:
        # Fork process to background
        pid = os.fork()
        if pid > 0:
            print(f"🚀 Daemon запущен с PID: {pid}")
            print(f"📋 Логи: /tmp/kaizen_mirai.log")
            print(f"🛑 Остановка: kill {pid}")
            sys.exit(0)

    service = AutonomousService()
    service.run(interval_seconds=args.interval)


if __name__ == "__main__":
    main()
