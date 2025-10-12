#!/usr/bin/env python3
"""
MIRAI - Режим самоулучшения
Агент сам решает свои проблемы и улучшает себя
"""

import os
import asyncio
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from core.autonomous_agent import AutonomousAgent

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/mirai_self_improvement.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('MIRAI-SELF-IMPROVEMENT')


async def self_improvement_loop():
    """Цикл самоулучшения - агент сам решает свои проблемы"""
    
    logger.info("=" * 80)
    logger.info("🔧 MIRAI - РЕЖИМ САМОУЛУЧШЕНИЯ ЗАПУЩЕН")
    logger.info("=" * 80)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("❌ OPENAI_API_KEY не найден!")
        return
    
    logger.info(f"✅ OpenAI Key: {api_key[:20]}...")
    
    agent = AutonomousAgent()
    logger.info(f"✅ Агент инициализирован для самоулучшения")
    logger.info("=" * 80)
    
    # Задачи самоулучшения на основе выявленных проблем
    improvement_tasks = [
        # Приоритет 1: ВАЛИДАЦИЯ
        {
            "name": "Создать систему валидации кода",
            "task": """Ты MIRAI - улучшаешь себя.

ПРОБЛЕМА: Была ошибка синтаксиса при выполнении кода.

ЗАДАЧА:
1. Создай модуль validation.py в core/
2. Добавь функцию validate_python_code(code) 
3. Используй ast.parse() для проверки синтаксиса
4. Верни True/False и сообщение об ошибке
5. Протестируй на примерах

Создай РЕАЛЬНЫЙ рабочий код!"""
        },
        
        # Приоритет 2: ЛОГИРОВАНИЕ
        {
            "name": "Улучшить систему логирования",
            "task": """Ты MIRAI - улучшаешь логирование.

ПРОБЛЕМА: Логи не структурированы, нет ротации.

ЗАДАЧА:
1. Создай модуль core/advanced_logger.py
2. Реализуй структурированное логирование (JSON)
3. Добавь ротацию логов (по размеру/времени)
4. Разные уровни: DEBUG, INFO, WARNING, ERROR
5. Маскировку API ключей в логах
6. Сохрани код и протестируй

Создай производственный код!"""
        },
        
        # Приоритет 3: МОНИТОРИНГ
        {
            "name": "Создать систему мониторинга",
            "task": """Ты MIRAI - добавляешь мониторинг.

ПРОБЛЕМА: Нет отслеживания метрик в реальном времени.

ЗАДАЧА:
1. Создай utils/monitoring.py
2. Добавь сбор метрик:
   - Количество выполненных задач
   - Время выполнения
   - Количество ошибок
   - Использование ресурсов (CPU, RAM)
3. Сохраняй метрики в JSON файл
4. Создай функцию get_health_status()
5. Протестируй код

Реализуй полноценный мониторинг!"""
        },
        
        # Приоритет 4: ДОКУМЕНТАЦИЯ
        {
            "name": "Генерация документации",
            "task": """Ты MIRAI - создаешь документацию.

ПРОБЛЕМА: Недостаточно документации модулей.

ЗАДАЧА:
1. Прочитай файл core/autonomous_agent.py
2. Создай подробный README.md для него
3. Опиши каждую функцию
4. Добавь примеры использования
5. Создай файл docs/AUTONOMOUS_AGENT.md

Сделай качественную документацию!"""
        },
        
        # Приоритет 5: ТЕСТИРОВАНИЕ
        {
            "name": "Создать автотесты",
            "task": """Ты MIRAI - пишешь тесты.

ПРОБЛЕМА: Нет автоматических тестов.

ЗАДАЧА:
1. Создай tests/test_autonomous_agent.py
2. Напиши тесты для основных функций:
   - test_execute_python()
   - test_read_file()
   - test_write_file()
   - test_create_task()
3. Используй pytest
4. Добавь моки для OpenAI API
5. Сохрани тесты

Создай рабочие unit тесты!"""
        },
        
        # Приоритет 6: БЕЗОПАСНОСТЬ
        {
            "name": "Улучшить безопасность",
            "task": """Ты MIRAI - укрепляешь безопасность.

ПРОБЛЕМА: API ключи могут попасть в логи.

ЗАДАЧА:
1. Создай utils/security.py
2. Реализуй функции:
   - mask_api_key(key) - маскировка ключей
   - encrypt_config(data) - шифрование конфигов
   - validate_file_path(path) - проверка безопасности путей
3. Добавь защиту от directory traversal
4. Протестируй функции

Сделай систему безопасной!"""
        },
        
        # Приоритет 7: ОПТИМИЗАЦИЯ
        {
            "name": "Добавить асинхронность",
            "task": """Ты MIRAI - оптимизируешь производительность.

ПРОБЛЕМА: Блокирующие запросы к API.

ЗАДАЧА:
1. Создай core/async_agent.py
2. Переделай функции на async/await:
   - async def execute_python_async()
   - async def search_web_async()
   - async def batch_execute() - параллельное выполнение
3. Используй aiohttp для HTTP запросов
4. Протестируй скорость

Ускорь работу агента!"""
        },
        
        # Приоритет 8: CI/CD
        {
            "name": "Настроить CI/CD",
            "task": """Ты MIRAI - настраиваешь автоматизацию.

ПРОБЛЕМА: Нет CI/CD пайплайна.

ЗАДАЧА:
1. Создай .github/workflows/test.yml
2. Настрой GitHub Actions для:
   - Запуска тестов на каждый push
   - Проверки стиля кода (ruff)
   - Проверки типов (mypy)
3. Добавь badge в README
4. Создай workflow для деплоя

Автоматизируй процессы!"""
        }
    ]
    
    iteration = 1
    completed_improvements = []
    
    try:
        while iteration <= len(improvement_tasks):
            task_info = improvement_tasks[iteration - 1]
            
            logger.info("\n" + "=" * 80)
            logger.info(f"🔧 УЛУЧШЕНИЕ #{iteration}: {task_info['name']}")
            logger.info("=" * 80)
            logger.info(f"\n📋 Задача:\n{task_info['task'][:200]}...\n")
            
            try:
                # Агент выполняет задачу самоулучшения
                result = agent.think(task_info['task'], max_iterations=15)
                
                logger.info(f"\n✅ Результат улучшения #{iteration}:")
                logger.info(f"{result}\n")
                
                completed_improvements.append({
                    'iteration': iteration,
                    'name': task_info['name'],
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"❌ Ошибка в улучшении #{iteration}: {e}")
                completed_improvements.append({
                    'iteration': iteration,
                    'name': task_info['name'],
                    'status': 'failed',
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
            
            logger.info("=" * 80)
            
            # Пауза между улучшениями
            if iteration < len(improvement_tasks):
                logger.info(f"⏸️  Пауза 30 секунд до следующего улучшения...")
                await asyncio.sleep(30)
            
            iteration += 1
        
        # Итоговый отчет
        logger.info("\n" + "=" * 80)
        logger.info("🎉 ВСЕ УЛУЧШЕНИЯ ЗАВЕРШЕНЫ!")
        logger.info("=" * 80)
        logger.info(f"\nВсего улучшений: {len(improvement_tasks)}")
        logger.info(f"Успешных: {sum(1 for x in completed_improvements if x['status'] == 'completed')}")
        logger.info(f"Ошибок: {sum(1 for x in completed_improvements if x['status'] == 'failed')}")
        
        # Создаем отчет
        report = "# Отчет о самоулучшении MIRAI\n\n"
        report += f"Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        report += "## Выполненные улучшения:\n\n"
        
        for imp in completed_improvements:
            status_icon = "✅" if imp['status'] == 'completed' else "❌"
            report += f"{status_icon} {imp['iteration']}. {imp['name']} - {imp['status']}\n"
        
        # Сохраняем отчет
        with open('/root/mirai/mirai-agent/self_improvement_report.md', 'w') as f:
            f.write(report)
        
        logger.info(f"\n📄 Отчет сохранен: self_improvement_report.md")
        logger.info("=" * 80)
        
    except KeyboardInterrupt:
        logger.info("\n\n🛑 Самоулучшение остановлено вручную")
    except Exception as e:
        logger.error(f"\n\n💥 Критическая ошибка: {e}")
        raise


def main():
    """Точка входа"""
    try:
        asyncio.run(self_improvement_loop())
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
        raise


if __name__ == "__main__":
    main()
