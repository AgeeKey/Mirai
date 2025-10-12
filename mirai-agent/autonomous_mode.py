#!/usr/bin/env python3
"""
MIRAI - Полностью автономный режим 24/7
Агент работает постоянно в фоне, улучшает себя, пишет код, ищет информацию
"""

import os
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from core.autonomous_agent import AutonomousAgent

# Настройка логирования в файл
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/tmp/mirai_autonomous.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("MIRAI")


async def autonomous_loop():
    """Бесконечный цикл автономной работы"""

    logger.info("=" * 80)
    logger.info("🤖 MIRAI - АВТОНОМНЫЙ РЕЖИМ 24/7 ЗАПУЩЕН")
    logger.info("=" * 80)

    # Проверка API ключа
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("❌ OPENAI_API_KEY не найден!")
        return

    logger.info(f"✅ OpenAI Key: {api_key[:20]}...")

    # Создание агента
    agent = AutonomousAgent()
    logger.info(f"✅ Агент инициализирован")
    logger.info(f"📊 Модель: {agent.model}")
    logger.info(f"🛠️  Инструментов: {len(agent.tools)}")
    logger.info("=" * 80)

    # Счетчик итераций
    iteration = 1

    # Список автономных задач для агента
    autonomous_tasks = [
        """Ты MIRAI - автономный AI агент, работающий 24/7.
        
Твоя текущая задача:
1. Проанализируй структуру проекта /root/mirai/mirai-agent
2. Найди что можно улучшить
3. Создай полезный код или утилиту
4. Сохрани результат в файл

Будь проактивным и полезным! Используй свои инструменты.""",
        """Ты автономный агент MIRAI.

Задача:
1. Найди в интернете информацию о лучших практиках AI агентов
2. Создай краткий отчет
3. Сохрани в файл research/ai_agents_best_practices.md

Используй search_web и write_file.""",
        """Ты MIRAI - самоулучшающийся агент.

Задача:
1. Напиши утилиту для мониторинга системы (CPU, RAM, диск)
2. Сохрани как utils/system_monitor.py
3. Протестируй выполнение

Используй write_file и execute_python.""",
        """Автономная задача для MIRAI:

1. Создай скрипт для автоматического бэкапа важных файлов
2. Сохрани как utils/auto_backup.py
3. Добавь логирование

Будь креативным!""",
        """MIRAI, ты работаешь автономно.

Задача:
1. Проанализируй логи работы агента
2. Найди паттерны и улучшения
3. Создай отчет performance_analysis.md

Используй read_file и write_file.""",
    ]

    try:
        while True:
            logger.info("\n" + "=" * 80)
            logger.info(
                f"🔄 ИТЕРАЦИЯ #{iteration} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            logger.info("=" * 80)

            # Выбираем задачу циклично
            task = autonomous_tasks[(iteration - 1) % len(autonomous_tasks)]

            logger.info(f"\n🎯 Задача для агента:")
            logger.info(f"{task[:200]}...\n")

            try:
                # Агент выполняет задачу
                result = agent.think(task, max_iterations=10)

                logger.info(f"\n✅ Результат итерации #{iteration}:")
                logger.info(f"{result}\n")

                # Проверяем созданные задачи
                if agent.tasks:
                    logger.info(f"📋 Задачи агента: {len(agent.tasks)}")
                    for task_item in agent.tasks[-3:]:  # Последние 3 задачи
                        logger.info(f"  • {task_item['name']}: {task_item['status']}")

            except Exception as e:
                logger.error(f"❌ Ошибка в итерации #{iteration}: {e}")

            logger.info("=" * 80)
            logger.info(f"⏸️  Пауза 60 секунд до следующей итерации...")
            logger.info("=" * 80)

            iteration += 1

            # Пауза между итерациями (60 секунд)
            await asyncio.sleep(60)

    except KeyboardInterrupt:
        logger.info("\n\n🛑 Автономный режим остановлен вручную")
    except Exception as e:
        logger.error(f"\n\n💥 Критическая ошибка: {e}")
        raise


def main():
    """Точка входа"""
    try:
        asyncio.run(autonomous_loop())
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
        raise


if __name__ == "__main__":
    main()
