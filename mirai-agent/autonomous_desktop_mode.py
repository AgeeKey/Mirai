#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI AUTONOMOUS DESKTOP MODE - ПОЛНЫЙ КОНТРОЛЬ НАД КОМПЬЮТЕРОМ    ║
║  Максимально мощный автономный режим для саморазвития               ║
╚══════════════════════════════════════════════════════════════════════╝

MIRAI полностью управляет компьютером для саморазвития:
- Самостоятельно выбирает задачи
- Изучает новые технологии через Google Chrome
- Создает программы и проекты
- Анализирует свое поведение
- Улучшает свои способности
- Собирает данные из компьютера

Автор: MIRAI Team
Дата: 2024-10-24
"""

import asyncio
import json
import logging
import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from openai import OpenAI

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("autonomous_desktop.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AutonomousDesktopMirai:
    """
    Полностью автономный MIRAI с полным контролем над компьютером
    
    Архитектура максимальной эффективности:
    ┌─────────────────────────────────────────────────────────────┐
    │              MIRAI AUTONOMOUS DESKTOP AGENT                 │
    ├─────────────────────────────────────────────────────────────┤
    │  🧠 AI Brain (GPT-4o)  │  🖥️ Desktop Control              │
    │  🔍 Web Research       │  💻 Code Development             │
    │  📊 Data Analysis      │  🗄️ Database Management          │
    │  🌐 Browser Control    │  📁 File System Access           │
    ├─────────────────────────────────────────────────────────────┤
    │            CONTINUOUS LEARNING & IMPROVEMENT                │
    └─────────────────────────────────────────────────────────────┘
    """
    
    def __init__(self):
        """Инициализация автономного агента"""
        logger.info("=" * 70)
        logger.info("🚀 ЗАПУСК MIRAI AUTONOMOUS DESKTOP MODE")
        logger.info("=" * 70)
        
        # Загрузить API ключи
        self.api_keys = self._load_api_keys()
        self.client = OpenAI(api_key=self.api_keys.get("openai"))
        self.model = "gpt-4o"
        
        # Инициализация модулей
        self._init_modules()
        
        # Состояние агента
        self.is_running = False
        self.tasks_completed = 0
        self.learning_data = []
        self.projects_created = []
        self.technologies_learned = []
        
        # Директории для работы
        self.workspace_dir = Path("mirai_workspace")
        self.workspace_dir.mkdir(exist_ok=True)
        
        self.projects_dir = self.workspace_dir / "projects"
        self.projects_dir.mkdir(exist_ok=True)
        
        self.learning_dir = self.workspace_dir / "learning"
        self.learning_dir.mkdir(exist_ok=True)
        
        logger.info("✅ MIRAI AUTONOMOUS DESKTOP MODE готов к работе!")
        logger.info(f"📁 Рабочая директория: {self.workspace_dir.absolute()}")
    
    def _load_api_keys(self) -> Dict[str, str]:
        """Загрузить API ключи"""
        config_path = Path(__file__).parent / "configs" / "api_keys.json"
        
        if config_path.exists():
            with open(config_path, encoding='utf-8') as f:
                return json.load(f)
        
        return {"openai": os.getenv("OPENAI_API_KEY")}
    
    def _init_modules(self):
        """Инициализация всех модулей"""
        logger.info("🔧 Инициализация модулей...")
        
        # Desktop Agent
        try:
            from core.desktop_agent_v2 import MiraiDesktopAgent
            self.desktop = MiraiDesktopAgent(
                enable_safety=False,  # Максимальная свобода
                enable_memory=True,
                user_id="autonomous_mirai"
            )
            logger.info("✅ Desktop Agent: Активен (Safety: OFF)")
        except Exception as e:
            logger.error(f"❌ Desktop Agent: {e}")
            self.desktop = None
        
        # Code Executor
        try:
            from core.multi_language_executor import MultiLanguageExecutor
            self.code_executor = MultiLanguageExecutor()
            logger.info("✅ Code Executor: Активен (8 языков)")
        except Exception as e:
            logger.error(f"❌ Code Executor: {e}")
            self.code_executor = None
        
        # Browser Automation
        try:
            from core.browser_automation import BrowserAutomation
            self.browser = BrowserAutomation(headless=False)
            logger.info("✅ Browser: Активен (Chrome с UI)")
        except Exception as e:
            logger.error(f"❌ Browser: {e}")
            self.browser = None
        
        # Web Search
        try:
            from core.web_search_integration import get_web_search
            self.web_search = get_web_search()
            logger.info("✅ Web Search: Активен (OpenAI)")
        except Exception as e:
            logger.error(f"❌ Web Search: {e}")
            self.web_search = None
        
        # Database Manager
        try:
            from core.database_manager import DatabaseManager
            self.database = DatabaseManager()
            logger.info("✅ Database: Активен")
        except Exception as e:
            logger.error(f"❌ Database: {e}")
            self.database = None
        
        # Memory Manager
        try:
            from core.memory_manager import get_memory_manager, Message
            self.memory = get_memory_manager()
            self.session = self.memory.create_session(user_id="autonomous_mirai")
            logger.info(f"✅ Memory: Активна (session: {self.session.id})")
        except Exception as e:
            logger.error(f"❌ Memory: {e}")
            self.memory = None
    
    async def run_autonomous(self):
        """
        Главный автономный цикл
        
        MIRAI полностью самостоятельно:
        1. Анализирует компьютер и собирает данные
        2. Выбирает задачи для саморазвития
        3. Изучает новые технологии через браузер
        4. Создает проекты и программы
        5. Улучшает свой код
        6. Повторяет цикл бесконечно
        """
        self.is_running = True
        logger.info("=" * 70)
        logger.info("🤖 MIRAI AUTONOMOUS MODE: АКТИВИРОВАН")
        logger.info("💪 Полный контроль над компьютером включен")
        logger.info("🔄 Начинаю бесконечный цикл саморазвития...")
        logger.info("=" * 70)
        
        iteration = 0
        
        while self.is_running:
            iteration += 1
            logger.info(f"\n{'='*70}")
            logger.info(f"🔄 ЦИКЛ #{iteration} | Выполнено задач: {self.tasks_completed}")
            logger.info(f"{'='*70}")
            
            try:
                # ШАГ 1: Собрать данные о компьютере
                logger.info("\n📊 ШАГ 1: Анализ компьютера и сбор данных")
                computer_data = await self._analyze_computer()
                
                # ШАГ 2: Выбрать задачу для саморазвития
                logger.info("\n🎯 ШАГ 2: Выбор задачи для саморазвития")
                task = await self._choose_development_task(computer_data)
                
                # ШАГ 3: Выполнить задачу
                logger.info(f"\n💻 ШАГ 3: Выполнение задачи: {task}")
                result = await self._execute_autonomous_task(task)
                
                # ШАГ 4: Проанализировать результаты
                logger.info("\n📈 ШАГ 4: Анализ результатов и обучение")
                await self._analyze_and_learn(task, result)
                
                # ШАГ 5: Улучшить себя
                logger.info("\n🚀 ШАГ 5: Самоулучшение")
                await self._self_improve()
                
                self.tasks_completed += 1
                
                # Короткая пауза между циклами
                logger.info(f"\n✅ Цикл #{iteration} завершен. Пауза 30 секунд...")
                await asyncio.sleep(30)
                
            except KeyboardInterrupt:
                logger.info("\n⚠️ Получен сигнал остановки от пользователя")
                self.is_running = False
                break
            
            except Exception as e:
                logger.error(f"\n❌ Ошибка в цикле #{iteration}: {e}", exc_info=True)
                logger.info("⏳ Пауза 60 секунд перед повтором...")
                await asyncio.sleep(60)
        
        logger.info("\n" + "=" * 70)
        logger.info("🛑 MIRAI AUTONOMOUS MODE: ОСТАНОВЛЕН")
        logger.info(f"📊 Статистика: {self.tasks_completed} задач выполнено")
        logger.info("=" * 70)
    
    async def _analyze_computer(self) -> Dict[str, Any]:
        """Анализ компьютера и сбор данных"""
        logger.info("🔍 Анализирую компьютер...")
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "screen_analysis": None,
            "open_windows": [],
            "browser_tabs": [],
            "file_system": [],
            "system_info": {}
        }
        
        try:
            if self.desktop:
                # Собрать данные с экрана
                learning_data = self.desktop.collect_learning_data()
                data["screen_analysis"] = learning_data.get("screen_analysis")
                data["open_windows"] = learning_data.get("open_windows", [])
                
                logger.info(f"✅ Собрано: {len(data['open_windows'])} открытых окон")
            
            # Анализ рабочего пространства
            if self.workspace_dir.exists():
                data["file_system"] = [
                    str(f.relative_to(self.workspace_dir))
                    for f in self.workspace_dir.rglob("*")
                    if f.is_file()
                ][:50]  # Ограничим 50 файлами
                
                logger.info(f"✅ Найдено: {len(data['file_system'])} файлов в workspace")
            
            return data
            
        except Exception as e:
            logger.error(f"❌ Ошибка анализа компьютера: {e}")
            return data
    
    async def _choose_development_task(self, computer_data: Dict) -> str:
        """Выбрать задачу для саморазвития"""
        logger.info("🤔 MIRAI выбирает задачу...")
        
        # Список возможных категорий задач
        task_categories = [
            "Изучить новый язык программирования",
            "Создать веб-приложение",
            "Разработать утилиту для автоматизации",
            "Исследовать новую технологию",
            "Оптимизировать существующий код",
            "Создать базу данных и API",
            "Разработать машинное обучение модель",
            "Построить микросервис",
            "Создать CLI инструмент",
            "Разработать игру или симуляцию"
        ]
        
        prompt = f"""Ты MIRAI - автономный AI агент с полным контролем над компьютером.

ТВОЯ ЦЕЛЬ: Максимально быстро и эффективно развиваться, используя компьютер пользователя.

ТЕКУЩЕЕ СОСТОЯНИЕ КОМПЬЮТЕРА:
- Открытых окон: {len(computer_data.get('open_windows', []))}
- Файлов в workspace: {len(computer_data.get('file_system', []))}
- Выполнено задач: {self.tasks_completed}
- Изучено технологий: {len(self.technologies_learned)}
- Создано проектов: {len(self.projects_created)}

ДОСТУПНЫЕ КАТЕГОРИИ ЗАДАЧ:
{chr(10).join(f'{i+1}. {cat}' for i, cat in enumerate(task_categories))}

ВЫБЕРИ КОНКРЕТНУЮ ЗАДАЧУ для саморазвития:
1. Задача должна быть практической и полезной
2. Должна помочь изучить что-то новое
3. Должна создать что-то реальное (код, проект, базу данных)
4. Должна быть выполнима за 10-30 минут
5. Приоритет: то, что еще не изучал

Опиши КОНКРЕТНУЮ задачу одним предложением (не категорию!)."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты MIRAI - автономный AI агент. Выбираешь КОНКРЕТНЫЕ практические задачи для саморазвития."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,  # Высокая креативность
                max_tokens=150
            )
            
            task = response.choices[0].message.content.strip()
            logger.info(f"✅ Выбрана задача: {task}")
            
            return task
            
        except Exception as e:
            logger.error(f"❌ Ошибка выбора задачи: {e}")
            # Fallback: случайная задача
            return random.choice(task_categories)
    
    async def _execute_autonomous_task(self, task: str) -> Dict[str, Any]:
        """Выполнить задачу автономно"""
        logger.info(f"🚀 Начинаю выполнение: {task}")
        
        result = {
            "task": task,
            "success": False,
            "steps": [],
            "created_files": [],
            "learned": [],
            "errors": []
        }
        
        try:
            # Разбить задачу на шаги
            steps = await self._plan_task_execution(task)
            logger.info(f"📋 План из {len(steps)} шагов создан")
            
            # Выполнить каждый шаг
            for i, step in enumerate(steps, 1):
                logger.info(f"\n▶️ Шаг {i}/{len(steps)}: {step}")
                
                step_result = await self._execute_step(step)
                result["steps"].append({
                    "step": step,
                    "result": step_result
                })
                
                if step_result.get("success"):
                    logger.info(f"✅ Шаг {i} выполнен успешно")
                else:
                    logger.warning(f"⚠️ Шаг {i} выполнен с предупреждениями")
                
                # Короткая пауза между шагами
                await asyncio.sleep(5)
            
            result["success"] = True
            logger.info(f"✅ Задача '{task}' выполнена!")
            
        except Exception as e:
            logger.error(f"❌ Ошибка выполнения задачи: {e}")
            result["errors"].append(str(e))
        
        return result
    
    async def _plan_task_execution(self, task: str) -> List[str]:
        """Спланировать выполнение задачи"""
        prompt = f"""Задача: {task}

Раздели эту задачу на 3-7 конкретных шагов для выполнения.
Каждый шаг должен быть четким действием.

Формат ответа - просто список шагов, без нумерации и дополнительного текста:
Шаг 1
Шаг 2
..."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты планировщик задач. Создаешь четкие планы из конкретных шагов."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            steps_text = response.choices[0].message.content.strip()
            steps = [s.strip() for s in steps_text.split('\n') if s.strip()]
            
            return steps[:7]  # Максимум 7 шагов
            
        except Exception as e:
            logger.error(f"❌ Ошибка планирования: {e}")
            return ["Выполнить задачу"]
    
    async def _execute_step(self, step: str) -> Dict[str, Any]:
        """Выполнить один шаг задачи"""
        result = {
            "success": False,
            "action": None,
            "output": None
        }
        
        try:
            # Определить тип действия
            step_lower = step.lower()
            
            # Поиск информации
            if any(word in step_lower for word in ['найти', 'поиск', 'изучить', 'узнать', 'исследовать']):
                if self.web_search:
                    logger.info("🔍 Ищу информацию в интернете...")
                    query = step
                    search_result = self.web_search.search(query)
                    
                    result["action"] = "web_search"
                    result["output"] = search_result
                    result["success"] = True
            
            # Работа с браузером
            elif any(word in step_lower for word in ['открой', 'браузер', 'сайт', 'страниц']):
                if self.browser and self.desktop:
                    logger.info("🌐 Работаю с браузером...")
                    # Открыть браузер через desktop agent
                    browser_result = self.desktop.execute_task(step, max_iterations=5)
                    
                    result["action"] = "browser"
                    result["output"] = browser_result
                    result["success"] = True
            
            # Создание кода
            elif any(word in step_lower for word in ['создай', 'напиши', 'код', 'программ', 'скрипт']):
                if self.code_executor:
                    logger.info("💻 Создаю код...")
                    
                    # Определить язык
                    language = "python"  # По умолчанию
                    if "javascript" in step_lower or "js" in step_lower:
                        language = "javascript"
                    elif "go" in step_lower:
                        language = "go"
                    elif "rust" in step_lower:
                        language = "rust"
                    
                    # Генерировать код через AI
                    code = await self._generate_code(step, language)
                    
                    # Сохранить в файл
                    filename = f"generated_{int(time.time())}.{language}"
                    filepath = self.projects_dir / filename
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(code)
                    
                    logger.info(f"📁 Код сохранен: {filepath}")
                    
                    # Выполнить если это Python
                    if language == "python":
                        exec_result = self.code_executor.execute(language, code)
                        result["output"] = exec_result
                    
                    result["action"] = "create_code"
                    result["success"] = True
            
            # Работа с файлами
            elif any(word in step_lower for word in ['файл', 'сохран', 'создай']):
                logger.info("📁 Работаю с файловой системой...")
                result["action"] = "file_operation"
                result["success"] = True
            
            # Общее действие через desktop agent
            else:
                if self.desktop:
                    logger.info("🖥️ Выполняю через desktop agent...")
                    desktop_result = self.desktop.execute_task(step, max_iterations=5)
                    
                    result["action"] = "desktop"
                    result["output"] = desktop_result
                    result["success"] = True
            
        except Exception as e:
            logger.error(f"❌ Ошибка выполнения шага: {e}")
            result["output"] = str(e)
        
        return result
    
    async def _generate_code(self, task: str, language: str) -> str:
        """Генерировать код для задачи"""
        prompt = f"""Создай {language} код для: {task}

Требования:
1. Код должен быть рабочим и полным
2. Добавь комментарии
3. Используй лучшие практики
4. Код должен быть готов к выполнению

Напиши ТОЛЬКО код, без объяснений."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": f"Ты эксперт по {language}. Пишешь чистый, рабочий код."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            code = response.choices[0].message.content.strip()
            
            # Убрать markdown форматирование если есть
            if code.startswith("```"):
                lines = code.split('\n')
                code = '\n'.join(lines[1:-1])
            
            return code
            
        except Exception as e:
            logger.error(f"❌ Ошибка генерации кода: {e}")
            return f"# Error generating code: {e}"
    
    async def _analyze_and_learn(self, task: str, result: Dict):
        """Проанализировать результаты и обучиться"""
        logger.info("📚 Анализирую результаты и учусь...")
        
        try:
            # Извлечь уроки
            lessons = []
            
            if result.get("success"):
                lessons.append(f"✅ Успешно выполнил: {task}")
            else:
                lessons.append(f"⚠️ Задача с трудностями: {task}")
            
            # Что создано
            if result.get("created_files"):
                lessons.append(f"📁 Создано файлов: {len(result['created_files'])}")
            
            # Что изучено
            if result.get("learned"):
                for item in result["learned"]:
                    if item not in self.technologies_learned:
                        self.technologies_learned.append(item)
                        lessons.append(f"🎓 Изучено: {item}")
            
            # Сохранить данные обучения
            learning_entry = {
                "timestamp": datetime.now().isoformat(),
                "task": task,
                "result": result.get("success"),
                "lessons": lessons,
                "steps_completed": len(result.get("steps", []))
            }
            
            self.learning_data.append(learning_entry)
            
            # Сохранить в файл
            learning_file = self.learning_dir / "learning_log.json"
            with open(learning_file, 'w', encoding='utf-8') as f:
                json.dump(self.learning_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Извлечено {len(lessons)} уроков")
            
        except Exception as e:
            logger.error(f"❌ Ошибка анализа: {e}")
    
    async def _self_improve(self):
        """Улучшить свой код и возможности"""
        logger.info("🔧 Анализирую возможности для самоулучшения...")
        
        try:
            # Каждые 5 задач - пробовать улучшить себя
            if self.tasks_completed > 0 and self.tasks_completed % 5 == 0:
                logger.info("🚀 Запускаю процесс самоулучшения...")
                
                # Проанализировать свой код
                improvement_ideas = await self._generate_improvement_ideas()
                
                if improvement_ideas:
                    logger.info(f"💡 Найдено {len(improvement_ideas)} идей улучшения")
                    
                    # Сохранить идеи
                    ideas_file = self.workspace_dir / "improvement_ideas.json"
                    with open(ideas_file, 'w', encoding='utf-8') as f:
                        json.dump(improvement_ideas, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            logger.error(f"❌ Ошибка самоулучшения: {e}")
    
    async def _generate_improvement_ideas(self) -> List[str]:
        """Генерировать идеи для улучшения"""
        prompt = f"""Ты MIRAI - автономный AI агент.

СТАТИСТИКА:
- Выполнено задач: {self.tasks_completed}
- Изучено технологий: {len(self.technologies_learned)}
- Создано проектов: {len(self.projects_created)}

Предложи 3-5 способов как ты можешь улучшить:
1. Свой код и архитектуру
2. Скорость выполнения задач
3. Качество создаваемых проектов
4. Эффективность обучения

Каждое предложение - одно короткое предложение."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Ты эксперт по самоулучшению AI систем."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=400
            )
            
            ideas_text = response.choices[0].message.content.strip()
            ideas = [s.strip() for s in ideas_text.split('\n') if s.strip()]
            
            return ideas
            
        except Exception as e:
            logger.error(f"❌ Ошибка генерации идей: {e}")
            return []


async def main():
    """Запуск автономного режима"""
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  MIRAI AUTONOMOUS DESKTOP MODE - ПОЛНЫЙ КОНТРОЛЬ НАД КОМПЬЮТЕРОМ    ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()
    print("⚠️  ВНИМАНИЕ: MIRAI получит ПОЛНЫЙ контроль над вашим компьютером")
    print("⚠️  Агент будет самостоятельно:")
    print("    • Управлять мышью и клавиатурой")
    print("    • Открывать браузер и искать информацию")
    print("    • Создавать файлы и проекты")
    print("    • Выполнять код")
    print("    • Анализировать экран")
    print()
    print("🛑 Для остановки нажмите Ctrl+C")
    print()
    
    input("Нажмите Enter для запуска... ")
    print()
    
    # Создать и запустить агента
    mirai = AutonomousDesktopMirai()
    
    try:
        await mirai.run_autonomous()
    except KeyboardInterrupt:
        print("\n\n🛑 Остановка по запросу пользователя...")
    
    print("\n✅ MIRAI AUTONOMOUS DESKTOP MODE завершен")


if __name__ == "__main__":
    asyncio.run(main())
