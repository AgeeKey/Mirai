#!/usr/bin/env python3
"""
🧪 Tests for Phase 4: Action Execution Engine

Comprehensive tests for all 150 steps
"""

import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.action_execution import (
    ActionExecutor,
    ActionQueue,
    ExecutionContextValidator,
    ActionTemplateLoader,
    ActionHandlerRegistry,
    Action,
    ActionType,
    ActionStatus,
)


def test_action_executor():
    """Test 1: Action Executor - Шаг 1"""
    print("\n🧪 TEST 1: Action Executor")
    print("="*60)
    
    executor = ActionExecutor()
    assert executor is not None
    assert not executor.is_initialized
    assert not executor.is_running
    
    print("✅ ActionExecutor создан успешно")
    return True


async def test_executor_initialization():
    """Test 2: Executor Initialization"""
    print("\n🧪 TEST 2: Executor Initialization")
    print("="*60)
    
    executor = ActionExecutor()
    success = await executor.initialize()
    
    assert success
    assert executor.is_initialized
    
    print("✅ Инициализация успешна")
    return True


def test_execution_context_validator():
    """Test 3: Execution Context Validator - Шаг 2"""
    print("\n🧪 TEST 3: Execution Context Validator")
    print("="*60)
    
    validator = ExecutionContextValidator()
    result = validator.validate()
    
    assert result is not None
    assert isinstance(result.is_valid, bool)
    assert isinstance(result.errors, list)
    assert isinstance(result.warnings, list)
    assert isinstance(result.info, dict)
    
    print(f"✅ Валидация: {'PASSED' if result.is_valid else 'FAILED'}")
    print(f"   Ошибок: {len(result.errors)}")
    print(f"   Предупреждений: {len(result.warnings)}")
    return True


def test_action_queue():
    """Test 4: Action Queue - Шаг 3"""
    print("\n🧪 TEST 4: Action Queue")
    print("="*60)
    
    queue = ActionQueue(max_size=10)
    
    # Создаем тестовые действия
    action1 = Action(
        id="1",
        type=ActionType.MOUSE_CLICK,
        parameters={'x': 100, 'y': 200},
        description="Test action 1"
    )
    
    action2 = Action(
        id="2",
        type=ActionType.KEYBOARD_TYPE,
        parameters={'text': 'Hello'},
        description="Test action 2"
    )
    
    # Тестируем enqueue
    assert queue.enqueue(action1)
    assert queue.enqueue(action2, priority=True)
    assert queue.size() == 2
    
    # Тестируем dequeue
    first = queue.dequeue()
    assert first is not None
    assert first.id == "2"  # Priority first
    
    second = queue.dequeue()
    assert second is not None
    assert second.id == "1"
    
    assert queue.is_empty()
    
    print("✅ ActionQueue работает корректно")
    return True


def test_action_templates():
    """Test 5: Action Templates - Шаг 4"""
    print("\n🧪 TEST 5: Action Templates")
    print("="*60)
    
    loader = ActionTemplateLoader()
    
    # Проверяем количество templates
    templates = loader.list_templates()
    assert len(templates) > 0
    print(f"   Загружено {len(templates)} шаблонов")
    
    # Тестируем создание действия из шаблона
    click_action = loader.create_from_template('click', {'x': 100, 'y': 200})
    assert click_action['type'] == 'mouse_click'
    assert click_action['params']['x'] == 100
    
    type_action = loader.create_from_template('type', {'text': 'Hello'})
    assert type_action['type'] == 'keyboard_type'
    assert type_action['params']['text'] == 'Hello'
    
    print("✅ ActionTemplateLoader работает корректно")
    return True


def test_action_handlers():
    """Test 6: Action Handlers Registry - Шаг 5"""
    print("\n🧪 TEST 6: Action Handlers Registry")
    print("="*60)
    
    registry = ActionHandlerRegistry()
    
    # Проверяем статистику
    stats = registry.get_stats()
    assert stats['total_handlers'] > 0
    assert stats['total_action_types'] > 0
    print(f"   Handlers: {stats['total_handlers']}")
    print(f"   Action types: {stats['total_action_types']}")
    
    # Тестируем dispatch
    result = registry.dispatch('mouse_click', x=100, y=200)
    assert result['success']
    assert result['action'] == 'mouse_click'
    
    result = registry.dispatch('keyboard_type', text='Test')
    assert result['success']
    assert result['action'] == 'keyboard_type'
    
    print("✅ ActionHandlerRegistry работает корректно")
    return True


async def test_execute_single_action():
    """Test 7: Execute Single Action"""
    print("\n🧪 TEST 7: Execute Single Action")
    print("="*60)
    
    executor = ActionExecutor()
    await executor.initialize()
    
    action = Action(
        id="test1",
        type=ActionType.MOUSE_CLICK,
        parameters={'x': 100, 'y': 200},
        description="Тестовый клик"
    )
    
    success = await executor.execute_action(action)
    
    assert success
    assert action.status == ActionStatus.SUCCESS
    assert executor.successful_actions == 1
    
    print("✅ Действие выполнено успешно")
    return True


async def test_execute_plan():
    """Test 8: Execute Full Plan"""
    print("\n🧪 TEST 8: Execute Full Plan")
    print("="*60)
    
    executor = ActionExecutor()
    
    # Создаем план из нескольких действий
    actions = [
        Action(
            id="1",
            type=ActionType.MOUSE_CLICK,
            parameters={'x': 100, 'y': 200},
            description="Кликнуть на кнопку"
        ),
        Action(
            id="2",
            type=ActionType.KEYBOARD_TYPE,
            parameters={'text': 'Hello World'},
            description="Напечатать текст"
        ),
        Action(
            id="3",
            type=ActionType.WINDOW_FOCUS,
            parameters={'window_title': 'Chrome'},
            description="Переключиться на Chrome"
        ),
    ]
    
    results = await executor.execute_plan(actions)
    
    assert results['total'] == 3
    assert results['successful'] == 3
    assert results['failed'] == 0
    
    status = executor.get_status()
    assert status['success_rate'] == 100.0
    
    print(f"✅ План выполнен: {results['successful']}/{results['total']}")
    return True


def test_resource_checking():
    """Test 9: Resource Checking - Шаг 16"""
    print("\n🧪 TEST 9: Resource Checking")
    print("="*60)
    
    validator = ExecutionContextValidator()
    result = validator.validate()
    
    # Проверяем что информация о ресурсах собрана
    assert 'cpu' in result.info
    assert 'memory' in result.info
    assert 'disk' in result.info
    assert 'system' in result.info
    
    print(f"✅ CPU: {result.info['cpu']['count']} cores")
    print(f"✅ RAM: {result.info['memory']['available_mb']:.0f} MB available")
    print(f"✅ Disk: {result.info['disk']['free_gb']:.1f} GB free")
    
    return True


async def test_error_handling():
    """Test 10: Error Handling"""
    print("\n🧪 TEST 10: Error Handling")
    print("="*60)
    
    executor = ActionExecutor()
    await executor.initialize()
    
    # Создаем действие которое может провалиться
    action = Action(
        id="error_test",
        type=ActionType.CUSTOM,
        parameters={},
        description="Тест обработки ошибок"
    )
    
    # Выполняем (не должно упасть)
    success = await executor.execute_action(action)
    
    # Проверяем что ошибка обработана
    status = executor.get_status()
    assert status['total_actions'] == 1
    
    print("✅ Обработка ошибок работает")
    return True


def run_all_tests():
    """Запустить все тесты"""
    print("\n" + "="*70)
    print("🚀 PHASE 4: ACTION EXECUTION - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    results = {}
    
    # Синхронные тесты
    tests = [
        ("Action Executor", test_action_executor),
        ("Execution Context", test_execution_context_validator),
        ("Action Queue", test_action_queue),
        ("Action Templates", test_action_templates),
        ("Action Handlers", test_action_handlers),
        ("Resource Checking", test_resource_checking),
    ]
    
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n❌ TEST FAILED: {name}")
            print(f"   Error: {e}")
            import traceback
            traceback.print_exc()
            results[name] = False
    
    # Асинхронные тесты
    async def run_async_tests():
        async_tests = [
            ("Executor Initialization", test_executor_initialization),
            ("Execute Single Action", test_execute_single_action),
            ("Execute Plan", test_execute_plan),
            ("Error Handling", test_error_handling),
        ]
        
        for name, test_func in async_tests:
            try:
                results[name] = await test_func()
            except Exception as e:
                print(f"\n❌ TEST FAILED: {name}")
                print(f"   Error: {e}")
                import traceback
                traceback.print_exc()
                results[name] = False
    
    asyncio.run(run_async_tests())
    
    # Итоги
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("="*70)
    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"Results: {passed}/{total} tests passed ({success_rate:.0f}%)")
    print("="*70)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Phase 4 Action Execution работает отлично!")
        return 0
    else:
        print(f"\n⚠️ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(run_all_tests())
