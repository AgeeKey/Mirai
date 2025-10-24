"""
🧠 MIRAI AUTONOMOUS DESKTOP MODE V2 - УМНЫЙ AI АГЕНТ

НОВАЯ АРХИТЕКТУРА С ЧЕЛОВЕЧЕСКИМ ИНТЕЛЛЕКТОМ:
==============================================

Каждое действие теперь проходит через:
1. 📸 Vision анализ → Понимание контекста
2. 🤔 AI Принятие решения → Что делать?
3. ⚡ Умное выполнение → Действие с контролем
4. ✅ Vision проверка → Получилось ли?

ОТЛИЧИЯ ОТ V1:
- ✅ Видит и понимает КОНТЕКСТ (профили Chrome, рекламы, попапы)
- ✅ Анализирует РЕЗУЛЬТАТ каждого действия
- ✅ Печатает в ПРАВИЛЬНЫЕ места (не в терминал)
- ✅ Понимает ИНТЕРФЕЙСЫ приложений
- ✅ ПАМЯТЬ контекста сессии
- ✅ ОБУЧАЕТСЯ на ошибках
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import os
import pyautogui  # Добавлен импорт

# Умные компоненты
from core.vision_tools import VisionTools
from core.context_manager import AgentContext, ActionStatus
from core.smart_desktop_agent import SmartDesktopAgent

# Для AI решений
from openai import OpenAI

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autonomous_desktop_v2.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class IntelligentMiraiAgent:
    """
    🧠 УМНЫЙ АВТОНОМНЫЙ АГЕНТ MIRAI V2

    Принципы работы:
    - Каждый шаг с Vision анализом
    - Понимание контекста
    - Проверка результатов
    - Обучение на опыте
    """

    def __init__(self):
        # Загружаем API ключ
        api_key = self._load_api_key()

        # Инициализируем компоненты
        self.vision = VisionTools(api_key)
        self.context = AgentContext(session_id=f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.desktop = SmartDesktopAgent(self.vision, self.context)

        # AI для принятия решений
        self.ai_client = OpenAI(api_key=api_key)
        
        # ЗАЩИТА ОТ ЗАВИСАНИЯ
        self.max_actions_per_cycle = 10  # Максимум действий за цикл
        self.actions_in_cycle = 0
        
        # БЕЗОПАСНЫЙ РЕЖИМ
        pyautogui.FAILSAFE = True  # Курсор в угол = остановка

        # Статистика
        self.tasks_completed = 0
        self.cycle_count = 0

        # Рабочая директория
        self.workspace = Path("mirai_workspace_v2")
        self.workspace.mkdir(exist_ok=True)

        logger.info("=" * 70)
        logger.info("🧠 MIRAI INTELLIGENT AGENT V2 INITIALIZED")
        logger.info("=" * 70)

    def _load_api_key(self) -> str:
        """Загрузить OpenAI API ключ"""
        # Сначала пробуем из конфига
        config_path = Path(__file__).parent / "configs" / "api_keys.json"
        
        if config_path.exists():
            with open(config_path, encoding='utf-8') as f:
                config = json.load(f)
                api_key = config.get("OPENAI_API_KEY") or config.get("openai") or config.get("OPENAI")
                if api_key:
                    logger.info("✅ API ключ загружен из configs/api_keys.json")
                    return api_key

        # Из переменных окружения
        api_key = os.getenv("OPENAI_API_KEY", "")
        if api_key:
            logger.info("✅ API ключ загружен из переменной окружения")
            return api_key
        
        raise ValueError("❌ OPENAI_API_KEY не найден! Добавьте в configs/api_keys.json или в переменную окружения")

    async def intelligent_cycle(self):
        """
        🔄 ОДИН УМНЫЙ ЦИКЛ РАБОТЫ:

        1. 📊 Анализ ситуации (Vision)
        2. 🎯 Выбор задачи (AI с пониманием контекста)
        3. 📋 Планирование (детальный план с проверками)
        4. 💻 Выполнение (Vision контроль на каждом шаге)
        5. 📈 Анализ результатов (что получилось, чему научились)
        """

        self.cycle_count += 1

        logger.info("=" * 70)
        logger.info(f"🔄 УМНЫЙ ЦИКЛ #{self.cycle_count} | Выполнено задач: {self.tasks_completed}")
        logger.info("=" * 70)

        try:
            # ШАГ 1: ПОЛНЫЙ АНАЛИЗ ТЕКУЩЕЙ СИТУАЦИИ
            logger.info("\n📊 ШАГ 1: Анализ текущей ситуации")
            situation = await self.desktop.analyze_current_situation()

            logger.info(f"👁️ Вижу: {situation.scene_description}")
            logger.info(f"🎯 Доступно действий: {situation.ui_state.get('possible_actions', [])}")

            if situation.ui_state.get("problems"):
                logger.warning(f"⚠️ Проблемы: {situation.ui_state['problems']}")

            # ШАГ 2: AI ВЫБИРАЕТ ЗАДАЧУ С УЧЁТОМ КОНТЕКСТА
            logger.info("\n🎯 ШАГ 2: AI выбирает задачу")
            task = await self._choose_intelligent_task(situation)

            if not task:
                logger.warning("⚠️ Не удалось выбрать задачу, пропускаю цикл")
                return

            logger.info(f"✅ Выбрана задача: {task}")

            # ШАГ 3: ДЕТАЛЬНОЕ ПЛАНИРОВАНИЕ
            logger.info("\n📋 ШАГ 3: Планирование выполнения")
            plan = await self._create_intelligent_plan(task, situation)

            logger.info(f"📋 План из {len(plan)} шагов:")
            for i, step in enumerate(plan, 1):
                logger.info(f"  {i}. {step}")

            # Сохраняем в контекст
            self.context.set_goal(task, plan)

            # ШАГ 4: УМНОЕ ВЫПОЛНЕНИЕ С VISION КОНТРОЛЕМ
            logger.info("\n💻 ШАГ 4: Умное выполнение задачи")
            success = await self._execute_intelligent_plan(task, plan)

            # ШАГ 5: АНАЛИЗ РЕЗУЛЬТАТОВ И ОБУЧЕНИЕ
            logger.info("\n📈 ШАГ 5: Анализ результатов")
            await self._analyze_and_learn(task, success)

            if success:
                self.tasks_completed += 1
                logger.info(f"✅ Задача выполнена успешно! Всего: {self.tasks_completed}")
            else:
                logger.warning("⚠️ Задача выполнена частично")

            # Сохраняем контекст
            self.context.save_to_file()

            # Сброс счётчика действий
            self.actions_in_cycle = 0
            
            logger.info(f"\n✅ Цикл #{self.cycle_count} завершён. Пауза 60 секунд (безопасно)...")
            await asyncio.sleep(60)  # Увеличена пауза для безопасности

        except KeyboardInterrupt:
            raise  # Пробрасываем Ctrl+C
        except Exception as e:
            logger.error(f"❌ Ошибка в цикле: {e}", exc_info=True)
            logger.warning("⏸️ Безопасная остановка на 60 секунд...")
            await asyncio.sleep(60)  # Длинная пауза при ошибке

    async def _choose_intelligent_task(self, situation) -> Optional[str]:
        """
        AI ВЫБИРАЕТ ЗАДАЧУ С ПОНИМАНИЕМ КОНТЕКСТА.

        Учитывает:
        - Что сейчас открыто
        - Какие проблемы есть
        - Что уже делали
        - Что доступно сейчас
        """

        context_summary = self.context.get_context_summary()

        prompt = f"""Ты - умный AI агент MIRAI, управляющий компьютером для саморазвития.

ТЕКУЩАЯ СИТУАЦИЯ:
{situation.scene_description}

Доступные действия: {situation.ui_state.get('possible_actions', [])}
Проблемы: {situation.ui_state.get('problems', 'нет')}

КОНТЕКСТ СЕССИИ:
{json.dumps(context_summary, ensure_ascii=False, indent=2)}

ЗАДАЧА: Выбери ОДНУ конкретную задачу для выполнения СЕЙЧАС.

ТРЕБОВАНИЯ:
1. Задача должна быть РЕАЛИСТИЧНОЙ с учётом текущей ситуации
2. Если есть проблемы - сначала их решить
3. Не повторяй то что недавно делал
4. Задача должна быть выполнима за 5-10 минут

ПРИМЕРЫ ХОРОШИХ ЗАДАЧ:
- "Создать Python скрипт для анализа файлов в VS Code"
- "Найти в Google информацию о REST API и сохранить в файл"
- "Создать TODO list приложение на HTML/CSS/JS"

Ответь ОДНОЙ строкой - только описание задачи, без объяснений."""

        try:
            response = self.ai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.8
            )

            task = response.choices[0].message.content.strip()
            return task

        except Exception as e:
            logger.error(f"❌ Ошибка выбора задачи: {e}")
            return None

    async def _create_intelligent_plan(self, task: str, situation) -> List[str]:
        """
        СОЗДАТЬ ДЕТАЛЬНЫЙ ПЛАН С ПРОВЕРКАМИ.

        Каждый шаг = конкретное действие с ожидаемым результатом
        """

        prompt = f"""Создай ДЕТАЛЬНЫЙ план для выполнения задачи: {task}

ТЕКУЩАЯ СИТУАЦИЯ:
{situation.scene_description}

ТРЕБОВАНИЯ К ПЛАНУ:
1. Каждый шаг должен быть КОНКРЕТНЫМ и ВЫПОЛНИМЫМ
2. Учитывай текущую ситуацию (что уже открыто)
3. Включи проверки после важных действий
4. Максимум 7 шагов
5. Используй реальные инструменты: браузер, редакторы, терминал

ФОРМАТ:
Ответь списком JSON:
["Шаг 1: конкретное действие", "Шаг 2: конкретное действие", ...]

Пример:
["Открыть VS Code", "Создать новый файл script.py", "Написать код для анализа файлов", "Сохранить файл", "Запустить и проверить"]

Ответь только JSON массивом, без объяснений."""

        try:
            response = self.ai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.5
            )

            result = response.choices[0].message.content.strip()

            # Парсим JSON
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                result = result.split("```")[1].split("```")[0].strip()

            plan = json.loads(result)
            return plan[:7]  # Максимум 7 шагов

        except Exception as e:
            logger.error(f"❌ Ошибка создания плана: {e}")
            return ["Выполнить задачу автоматически"]

    async def _execute_intelligent_plan(self, task: str, plan: List[str]) -> bool:
        """
        УМНОЕ ВЫПОЛНЕНИЕ ПЛАНА.

        Каждый шаг:
        1. Vision анализ → понимание контекста
        2. Выполнение → умное действие
        3. Vision проверка → получилось ли?
        """

        logger.info(f"🚀 Начинаю умное выполнение: {task}")

        for i, step in enumerate(plan, 1):
            logger.info(f"\n▶️ Шаг {i}/{len(plan)}: {step}")

            try:
                # Используем умный desktop agent
                result = await self.desktop.smart_execute_task(step)

                if result.get("success"):
                    logger.info(f"✅ Шаг {i} выполнен успешно")
                    self.context.complete_step(step)
                else:
                    logger.warning(f"⚠️ Шаг {i} выполнен частично")

                await asyncio.sleep(2)  # Пауза между шагами

            except Exception as e:
                logger.error(f"❌ Ошибка на шаге {i}: {e}")
                continue

        # Проверяем итоговый результат
        completed = len(self.context.completed_steps)
        total = len(plan)

        success = completed >= total * 0.7  # 70% успеха

        logger.info(f"\n📊 Итог: {completed}/{total} шагов выполнено")

        return success

    async def _analyze_and_learn(self, task: str, success: bool):
        """
        АНАЛИЗ РЕЗУЛЬТАТОВ И ОБУЧЕНИЕ.
        Что получилось, что нет, чему научились.
        """

        recent_actions = self.context.get_recent_actions(10)

        # Анализируем что было сделано
        logger.info("📚 Анализирую опыт...")

        lessons = []

        for action in recent_actions:
            if action.status == ActionStatus.FAILED:
                lesson = f"НЕ РАБОТАЕТ: {action.description} - {action.problems}"
                lessons.append(lesson)
            elif action.status == ActionStatus.SUCCESS:
                lesson = f"РАБОТАЕТ: {action.description}"
                lessons.append(lesson)

        if lessons:
            logger.info(f"📝 Извлечено {len(lessons)} уроков:")
            for lesson in lessons[:3]:
                logger.info(f"  - {lesson}")

        # Метрики
        logger.info(f"\n📊 Статистика сессии:")
        logger.info(f"  Всего действий: {self.context.total_actions}")
        logger.info(f"  Успешных: {self.context.successful_actions}")
        logger.info(f"  Успешность: {self.context.get_context_summary()['success_rate']}")

    async def run_forever(self):
        """🚀 ЗАПУСК БЕСКОНЕЧНОГО УМНОГО РЕЖИМА"""

        print("\n" + "=" * 70)
        print("🧠 MIRAI INTELLIGENT AUTONOMOUS MODE V2")
        print("=" * 70)
        print("\n🎯 НОВЫЕ ВОЗМОЖНОСТИ:")
        print("  ✅ Vision анализ каждого шага")
        print("  ✅ Понимание контекста (профили, реклама, попапы)")
        print("  ✅ Умная печать (не в терминал)")
        print("  ✅ Память сессии и обучение")
        print("  ✅ Проверка результатов")
        print("\n🚀 Запуск бесконечного цикла...\n")

        try:
            while True:
                await self.intelligent_cycle()

        except KeyboardInterrupt:
            logger.info("\n\n🛑 Остановка агента...")
            self.context.save_to_file()
            logger.info("💾 Контекст сохранён")
            logger.info(f"📊 Итого выполнено задач: {self.tasks_completed}")
            logger.info("👋 До встречи!")


def main():
    """Точка входа"""
    agent = IntelligentMiraiAgent()
    asyncio.run(agent.run_forever())


if __name__ == "__main__":
    main()
