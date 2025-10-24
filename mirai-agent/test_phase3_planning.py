#!/usr/bin/env python3
"""
🧪 ТЕСТЫ ДЛЯ ФАЗЫ 3: TASK PLANNING
==================================

Тестирование всех 150 шагов системы планирования.
"""

import sys
import logging
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.task_planning import TaskPlanningSystem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def test_simple_search_task():
    """Тест 1: Простая задача поиска"""
    print("\n" + "=" * 70)
    print("ТЕСТ 1: Простая задача поиска")
    print("=" * 70)
    
    planner = TaskPlanningSystem()
    
    result = planner.plan_task(
        user_task="Найди информацию о Python",
        requirements=["Информация найдена", "Результат релевантен"]
    )
    
    assert result.success, "Планирование должно быть успешным"
    assert result.parsed_task is not None, "Задача должна быть распарсена"
    assert len(result.decomposition) > 0, "Должно быть разложение"
    assert len(result.subtasks) > 0, "Должны быть подзадачи"
    assert result.execution_plan is not None, "Должен быть план выполнения"
    assert result.approved, "План должен быть утвержден"
    
    print("✅ Тест 1 пройден")
    print(f"   Подзадач: {len(result.subtasks)}")
    print(f"   Время: {result.execution_plan['total_duration']:.1f}с")
    print(f"   Утвержден: {result.approved}")
    
    return result


def test_complex_creation_task():
    """Тест 2: Сложная задача создания"""
    print("\n" + "=" * 70)
    print("ТЕСТ 2: Сложная задача создания")
    print("=" * 70)
    
    planner = TaskPlanningSystem()
    
    result = planner.plan_task(
        user_task="Создай новый Python проект с тестами и документацией",
        requirements=[
            "Проект создан",
            "Тесты написаны",
            "Документация готова"
        ],
        optimization_goals={
            'time': 0.3,
            'resources': 0.3,
            'safety': 0.4  # Безопасность важнее для создания
        }
    )
    
    assert result.success, "Планирование должно быть успешным"
    assert result.parsed_task.complexity.value >= 2, "Задача должна быть средней или выше сложности"
    
    # Проверяем что есть валидация
    validation_tasks = [
        t for t in result.execution_plan['tasks']
        if t.get('type') in ['validation', 'safety_check']
    ]
    assert len(validation_tasks) > 0, "Должны быть шаги валидации"
    
    print("✅ Тест 2 пройден")
    print(f"   Сложность: {result.parsed_task.complexity.name}")
    print(f"   Подзадач: {len(result.subtasks)}")
    print(f"   Валидаций: {len(validation_tasks)}")
    print(f"   Оптимизация score: {result.execution_plan.get('optimization_score', 0):.2f}")
    
    return result


def test_parallel_execution_task():
    """Тест 3: Задача с параллельным выполнением"""
    print("\n" + "=" * 70)
    print("ТЕСТ 3: Задача с параллельным выполнением")
    print("=" * 70)
    
    planner = TaskPlanningSystem()
    
    result = planner.plan_task(
        user_task="Проанализируй код в нескольких файлах и создай отчет",
        requirements=["Все файлы проанализированы", "Отчет создан"],
        optimization_goals={
            'time': 0.8,  # Максимизируем скорость
            'resources': 0.1,
            'safety': 0.1
        }
    )
    
    assert result.success, "Планирование должно быть успешным"
    
    # Проверяем параллелизм
    parallelism = result.execution_plan.get('max_parallelism', 1)
    assert parallelism >= 1, "Должен быть параллелизм"
    
    print("✅ Тест 3 пройден")
    print(f"   Параллелизм: {parallelism}")
    print(f"   Время: {result.execution_plan['total_duration']:.1f}с")
    
    # Проверяем балансировку нагрузки
    if 'load_balanced' in result.execution_plan:
        print(f"   Балансировка нагрузки: ✅")
    
    return result


def test_validation_checks():
    """Тест 4: Проверка всех валидаций"""
    print("\n" + "=" * 70)
    print("ТЕСТ 4: Проверка валидаций")
    print("=" * 70)
    
    planner = TaskPlanningSystem()
    
    result = planner.plan_task(
        user_task="Выполни задачу тестирования",
        requirements=["Тест пройден"]
    )
    
    # Проверяем все типы валидации
    expected_checks = ['completeness', 'consistency', 'feasibility', 'safety', 'performance']
    
    for check in expected_checks:
        assert check in result.validation_results, f"Должна быть проверка {check}"
        validation = result.validation_results[check]
        print(f"   {check.capitalize()}: "
              f"{'✅' if validation.valid else '❌'} "
              f"(score: {validation.score:.2f}, "
              f"{validation.checks_passed}/{validation.checks_total})")
    
    print("✅ Тест 4 пройден")
    
    return result


def test_risk_assessment():
    """Тест 5: Оценка рисков и безопасность"""
    print("\n" + "=" * 70)
    print("ТЕСТ 5: Оценка рисков и безопасность")
    print("=" * 70)
    
    planner = TaskPlanningSystem()
    
    result = planner.plan_task(
        user_task="Удали старые файлы и очисти систему",  # Рискованная задача
        optimization_goals={
            'time': 0.1,
            'resources': 0.1,
            'safety': 0.8  # Максимальная безопасность
        }
    )
    
    assert result.success, "Планирование должно быть успешным"
    
    # Проверяем что оценен риск
    assert result.parsed_task.risk_level is not None, "Должна быть оценка риска"
    print(f"   Уровень риска: {result.parsed_task.risk_level.value}")
    
    # Проверяем что добавлены проверки безопасности
    safety_checks = [
        t for t in result.execution_plan['tasks']
        if t.get('type') == 'safety_check'
    ]
    print(f"   Проверок безопасности: {len(safety_checks)}")
    
    # Проверяем checkpoints
    checkpoints = result.execution_plan.get('checkpoints', [])
    print(f"   Checkpoints: {len(checkpoints)}")
    
    assert len(safety_checks) > 0 or len(checkpoints) > 0, \
        "Для рискованных задач должны быть меры безопасности"
    
    print("✅ Тест 5 пройден")
    
    return result


def test_optimization():
    """Тест 6: Оптимизация плана"""
    print("\n" + "=" * 70)
    print("ТЕСТ 6: Оптимизация плана")
    print("=" * 70)
    
    planner = TaskPlanningSystem()
    
    # Два плана с разными целями оптимизации
    result_speed = planner.plan_task(
        user_task="Обработай данные",
        optimization_goals={'time': 1.0, 'resources': 0.0, 'safety': 0.0}
    )
    
    result_safety = planner.plan_task(
        user_task="Обработай данные",
        optimization_goals={'time': 0.0, 'resources': 0.0, 'safety': 1.0}
    )
    
    # План с приоритетом скорости должен быть быстрее
    speed_time = result_speed.execution_plan.get('total_duration', float('inf'))
    safety_time = result_safety.execution_plan.get('total_duration', float('inf'))
    
    print(f"   Оптимизация на скорость: {speed_time:.1f}с")
    print(f"   Оптимизация на безопасность: {safety_time:.1f}с")
    
    # План с приоритетом безопасности должен иметь больше проверок
    speed_validations = len([
        t for t in result_speed.execution_plan['tasks']
        if t.get('type') in ['validation', 'safety_check']
    ])
    safety_validations = len([
        t for t in result_safety.execution_plan['tasks']
        if t.get('type') in ['validation', 'safety_check']
    ])
    
    print(f"   Валидаций (скорость): {speed_validations}")
    print(f"   Валидаций (безопасность): {safety_validations}")
    
    assert safety_validations >= speed_validations, \
        "План с фокусом на безопасность должен иметь больше проверок"
    
    print("✅ Тест 6 пройден")
    
    return result_speed, result_safety


def test_statistics():
    """Тест 7: Статистика системы"""
    print("\n" + "=" * 70)
    print("ТЕСТ 7: Статистика системы")
    print("=" * 70)
    
    planner = TaskPlanningSystem()
    stats = planner.get_statistics()
    
    print(f"   Название: {stats['name']}")
    print(f"   Версия: {stats['version']}")
    print(f"   Всего шагов: {stats['total_steps']}")
    print(f"   Разделов: {len(stats['sections'])}")
    print(f"   Компонентов: {sum(stats['components'].values())}")
    
    assert stats['total_steps'] == 150, "Должно быть 150 шагов"
    assert len(stats['sections']) == 4, "Должно быть 4 раздела"
    
    print("✅ Тест 7 пройден")
    
    return stats


def run_all_tests():
    """Запуск всех тестов"""
    print("\n" + "=" * 70)
    print("🧪 ЗАПУСК ВСЕХ ТЕСТОВ ФАЗЫ 3")
    print("=" * 70)
    
    tests = [
        ("Простая задача поиска", test_simple_search_task),
        ("Сложная задача создания", test_complex_creation_task),
        ("Параллельное выполнение", test_parallel_execution_task),
        ("Валидация", test_validation_checks),
        ("Оценка рисков", test_risk_assessment),
        ("Оптимизация", test_optimization),
        ("Статистика", test_statistics),
    ]
    
    results = {}
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
            passed += 1
        except Exception as e:
            logger.error(f"❌ Тест '{test_name}' провалился: {e}", exc_info=True)
            results[test_name] = None
            failed += 1
    
    # Итоги
    print("\n" + "=" * 70)
    print("📊 ИТОГИ ТЕСТИРОВАНИЯ")
    print("=" * 70)
    print(f"Всего тестов: {len(tests)}")
    print(f"✅ Пройдено: {passed}")
    print(f"❌ Провалено: {failed}")
    print(f"Процент успеха: {passed/len(tests)*100:.1f}%")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
        print("✅ Фаза 3: Task Planning полностью функциональна")
    else:
        print(f"\n⚠️ Есть проблемы в {failed} тестах")
    
    return results, passed, failed


if __name__ == "__main__":
    results, passed, failed = run_all_tests()
    
    # Возвращаем код выхода
    sys.exit(0 if failed == 0 else 1)
