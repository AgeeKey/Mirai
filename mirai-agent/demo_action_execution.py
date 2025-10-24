#!/usr/bin/env python3
"""
🎮 ДЕМОНСТРАЦИЯ PHASE 4: ACTION EXECUTION ENGINE
Показывает все возможности системы выполнения действий
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.action_execution import (
    ActionExecutor,
    ActionQueue,
    ExecutionContextValidator,
    ActionTemplateLoader,
    ActionHandlerRegistry,
    Action,
    ActionType,
)


def print_header(title: str):
    """Красивый заголовок"""
    print("\n" + "=" * 70)
    print(f"🚀 {title}")
    print("=" * 70)


def print_section(title: str):
    """Секция"""
    print(f"\n📋 {title}")
    print("-" * 70)


async def demo_basic_executor():
    """Демо 1: Базовое использование ActionExecutor"""
    print_header("ДЕМО 1: Базовый ActionExecutor")
    
    # Создаем исполнителя
    executor = ActionExecutor()
    print("✓ ActionExecutor создан")
    
    # Инициализируем
    await executor.initialize()
    print("✓ Инициализация завершена")
    
    # Показываем статус
    status = executor.get_status()
    print(f"✓ Статус: initialized={status['initialized']}, running={status['running']}")
    
    return executor


async def demo_single_action(executor):
    """Демо 2: Выполнение одного действия"""
    print_header("ДЕМО 2: Выполнение одного действия")
    
    # Создаем действие
    action = Action(
        id="demo1",
        type=ActionType.MOUSE_CLICK,
        parameters={'x': 100, 'y': 200},
        description="Кликнуть на кнопку Login"
    )
    print(f"✓ Действие создано: {action.description}")
    
    # Выполняем
    success = await executor.execute_action(action)
    print(f"✓ Выполнено: {action.status.value}")
    
    return success


async def demo_action_plan(executor):
    """Демо 3: Выполнение плана из нескольких действий"""
    print_header("ДЕМО 3: Выполнение плана действий")
    
    # Создаем план
    plan = [
        Action(
            id="1",
            type=ActionType.APPLICATION_OPEN,
            parameters={'app_name': 'chrome'},
            description="Открыть Chrome"
        ),
        Action(
            id="2",
            type=ActionType.WINDOW_FOCUS,
            parameters={'window_title': 'Chrome'},
            description="Переключиться на Chrome"
        ),
        Action(
            id="3",
            type=ActionType.KEYBOARD_TYPE,
            parameters={'text': 'https://google.com'},
            description="Напечатать URL"
        ),
        Action(
            id="4",
            type=ActionType.KEYBOARD_TYPE,
            parameters={'text': 'Enter'},
            description="Нажать Enter"
        ),
    ]
    
    print(f"✓ План создан: {len(plan)} действий")
    for i, action in enumerate(plan, 1):
        print(f"  {i}. {action.description}")
    
    # Выполняем план
    print("\n⏳ Выполнение плана...")
    results = await executor.execute_plan(plan)
    
    print(f"\n✓ План выполнен!")
    print(f"  Всего: {results['total']}")
    print(f"  Успешно: {results['successful']}")
    print(f"  Ошибок: {results['failed']}")
    
    return results


def demo_action_queue():
    """Демо 4: Работа с очередью действий"""
    print_header("ДЕМО 4: Очередь действий (ActionQueue)")
    
    # Создаем очередь
    queue = ActionQueue(max_size=100)
    print("✓ Очередь создана (max_size=100)")
    
    # Добавляем действия
    actions = [
        Action(id="1", type=ActionType.MOUSE_CLICK, parameters={}, description="Action 1"),
        Action(id="2", type=ActionType.KEYBOARD_TYPE, parameters={}, description="Action 2 (priority)"),
        Action(id="3", type=ActionType.WINDOW_FOCUS, parameters={}, description="Action 3"),
    ]
    
    queue.enqueue(actions[0])
    queue.enqueue(actions[2])
    queue.enqueue(actions[1], priority=True)  # С приоритетом
    
    print(f"✓ Добавлено {len(actions)} действий (одно с приоритетом)")
    
    # Показываем статистику
    stats = queue.get_stats()
    print(f"  Размер очереди: {stats['current_size']}")
    print(f"  Приоритетных: {stats['priority_size']}")
    print(f"  Обычных: {stats['regular_size']}")
    
    # Извлекаем
    print("\n⏳ Извлечение из очереди:")
    while not queue.is_empty():
        action = queue.dequeue()
        if action:
            print(f"  → {action.description}")
    
    print("✓ Очередь опустошена")


def demo_templates():
    """Демо 5: Использование шаблонов"""
    print_header("ДЕМО 5: Шаблоны действий (ActionTemplateLoader)")
    
    # Загружаем шаблоны
    loader = ActionTemplateLoader()
    templates = loader.list_templates()
    
    print(f"✓ Загружено {len(templates)} шаблонов")
    
    # Показываем несколько шаблонов
    print("\nПримеры шаблонов:")
    for tmpl in templates[:10]:
        print(f"  • {tmpl['name']}: {tmpl['description']}")
    
    # Создаем действия из шаблонов
    print("\n⏳ Создание действий из шаблонов:")
    
    click = loader.create_from_template('click', {'x': 100, 'y': 200})
    print(f"  ✓ Click: {click}")
    
    type_text = loader.create_from_template('type', {'text': 'Hello World'})
    print(f"  ✓ Type: {type_text}")
    
    shortcut = loader.create_from_template('shortcut', {'keys': ['ctrl', 'c']})
    print(f"  ✓ Shortcut: {shortcut}")


def demo_handlers():
    """Демо 6: Реестр обработчиков"""
    print_header("ДЕМО 6: Реестр обработчиков (ActionHandlerRegistry)")
    
    # Создаем реестр
    registry = ActionHandlerRegistry()
    
    # Показываем статистику
    stats = registry.get_stats()
    print(f"✓ Зарегистрировано {stats['total_handlers']} обработчиков")
    print(f"✓ Поддерживается {stats['total_action_types']} типов действий")
    
    # Показываем handlers
    print("\nОбработчики:")
    for handler in stats['handlers'][:10]:
        print(f"  • {handler['name']}: {handler['types']}")
    
    # Тестируем dispatch
    print("\n⏳ Тестирование dispatch:")
    
    result1 = registry.dispatch('mouse_click', x=100, y=200)
    print(f"  ✓ mouse_click: {result1}")
    
    result2 = registry.dispatch('keyboard_type', text='Test')
    print(f"  ✓ keyboard_type: {result2}")


def demo_context_validation():
    """Демо 7: Валидация контекста"""
    print_header("ДЕМО 7: Валидация контекста выполнения")
    
    # Создаем валидатор
    validator = ExecutionContextValidator()
    
    # Проверяем контекст
    result = validator.validate()
    
    print(f"✓ Статус: {'ВАЛИДНО ✅' if result.is_valid else 'НЕВАЛИДНО ❌'}")
    
    # Показываем ошибки и предупреждения
    if result.errors:
        print(f"\n❌ Ошибки ({len(result.errors)}):")
        for error in result.errors:
            print(f"  • {error}")
    
    if result.warnings:
        print(f"\n⚠️ Предупреждения ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  • {warning}")
    
    # Показываем информацию о системе
    print("\n📊 Информация о системе:")
    info = result.info
    
    print(f"  🖥️ ОС: {info['system']['os']} {info['system']['os_version']}")
    print(f"  🔧 Архитектура: {info['system']['architecture']}")
    print(f"  🐍 Python: {info['system']['python_version']}")
    print(f"  💻 CPU: {info['cpu']['count']} ядер, доступно {info['cpu']['available_percent']:.1f}%")
    print(f"  💾 RAM: {info['memory']['available_mb']:.0f} MB доступно ({info['memory']['percent']:.1f}% используется)")
    print(f"  💿 Disk: {info['disk']['free_gb']:.1f} GB свободно ({info['disk']['percent']:.1f}% используется)")


async def demo_full_workflow():
    """Демо 8: Полный workflow"""
    print_header("ДЕМО 8: Полный workflow - Автоматизация задачи")
    
    print("\n📝 Задача: Открыть Chrome и найти что-то в Google")
    print("-" * 70)
    
    # 1. Проверяем контекст
    print("\n1️⃣ Проверка контекста выполнения...")
    validator = ExecutionContextValidator()
    result = validator.validate()
    
    if not result.is_valid:
        print("❌ Контекст невалиден, прерываем")
        return
    
    print(f"✓ Контекст валиден (CPU: {result.info['cpu']['count']}, RAM: {result.info['memory']['available_mb']:.0f}MB)")
    
    # 2. Создаем исполнителя
    print("\n2️⃣ Создание исполнителя...")
    executor = ActionExecutor()
    await executor.initialize()
    print("✓ Исполнитель готов")
    
    # 3. Создаем план из шаблонов
    print("\n3️⃣ Создание плана из шаблонов...")
    loader = ActionTemplateLoader()
    
    plan = [
        Action(
            id="1",
            type=ActionType.APPLICATION_OPEN,
            parameters={'app_name': 'chrome'},
            description="Открыть Chrome"
        ),
        Action(
            id="2",
            type=ActionType.WINDOW_FOCUS,
            parameters={'window_title': 'Chrome'},
            description="Переключиться на Chrome"
        ),
        Action(
            id="3",
            type=ActionType.MOUSE_CLICK,
            parameters={'x': 400, 'y': 300},
            description="Кликнуть в адресную строку"
        ),
        Action(
            id="4",
            type=ActionType.KEYBOARD_TYPE,
            parameters={'text': 'https://google.com'},
            description="Напечатать google.com"
        ),
        Action(
            id="5",
            type=ActionType.KEYBOARD_TYPE,
            parameters={'text': 'Enter'},
            description="Нажать Enter"
        ),
    ]
    
    print(f"✓ План создан: {len(plan)} действий")
    
    # 4. Выполняем план
    print("\n4️⃣ Выполнение плана...")
    results = await executor.execute_plan(plan)
    
    # 5. Показываем результаты
    print("\n5️⃣ Результаты:")
    print(f"  Всего действий: {results['total']}")
    print(f"  Успешно: {results['successful']} ✅")
    print(f"  Ошибок: {results['failed']} {'✅' if results['failed'] == 0 else '❌'}")
    
    # 6. Статус исполнителя
    status = executor.get_status()
    print(f"\n6️⃣ Финальный статус исполнителя:")
    print(f"  Success Rate: {status['success_rate']:.1f}%")
    print(f"  Всего выполнено: {status['total_actions']}")


async def main():
    """Главная функция"""
    print("\n" + "=" * 70)
    print("🎮 PHASE 4: ACTION EXECUTION ENGINE - ПОЛНАЯ ДЕМОНСТРАЦИЯ")
    print("=" * 70)
    print("\nЭто демонстрация всех возможностей Action Execution Engine!")
    print("Система выполнения действий как человек: клики, печать, навигация.")
    
    try:
        # Синхронные демо
        demo_action_queue()
        demo_templates()
        demo_handlers()
        demo_context_validation()
        
        # Асинхронные демо
        executor = await demo_basic_executor()
        await demo_single_action(executor)
        await demo_action_plan(executor)
        await demo_full_workflow()
        
        # Итог
        print("\n" + "=" * 70)
        print("🎉 ВСЕ ДЕМОНСТРАЦИИ ЗАВЕРШЕНЫ УСПЕШНО!")
        print("=" * 70)
        print("\n📊 Возможности Phase 4:")
        print("  ✅ ActionExecutor - исполнение действий")
        print("  ✅ ActionQueue - очередь с приоритетами")
        print("  ✅ ActionTemplateLoader - 19 готовых шаблонов")
        print("  ✅ ActionHandlerRegistry - 11 обработчиков")
        print("  ✅ ExecutionContextValidator - проверка ресурсов")
        print("  ✅ Error Handling & Recovery - обработка ошибок")
        print("  ✅ Verification & Monitoring - проверка и мониторинг")
        print("\n🚀 Фаза 4 готова к использованию!")
        
    except Exception as e:
        print(f"\n❌ Ошибка во время демонстрации: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
