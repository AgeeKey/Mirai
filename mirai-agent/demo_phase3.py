#!/usr/bin/env python3
"""
🎯 ДЕМОНСТРАЦИЯ ФАЗЫ 3: TASK PLANNING
=====================================

Простой пример использования системы планирования.
"""

import sys
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent))

from core.task_planning import TaskPlanningSystem

print("=" * 70)
print("🎯 ДЕМОНСТРАЦИЯ: ФАЗА 3 - TASK PLANNING")
print("=" * 70)
print()

# Создаем систему планирования
print("📋 Инициализация системы планирования...")
planner = TaskPlanningSystem()
print("✅ Система готова!")
print()

# Пример 1: Простая задача
print("=" * 70)
print("ПРИМЕР 1: Простая задача поиска")
print("=" * 70)

result = planner.plan_task(
    user_task="Найди информацию о Python"
)

if result.success:
    print("✅ Планирование успешно!")
    print(f"   📊 Статистика:")
    print(f"      - Тип: {result.parsed_task.task_type.value}")
    print(f"      - Сложность: {result.parsed_task.complexity.name}")
    print(f"      - Подзадач: {len(result.subtasks)}")
    print(f"      - Время: {result.execution_plan['total_duration']:.1f}с")
    print(f"      - Checkpoints: {len(result.execution_plan.get('checkpoints', []))}")
    print()
    print(f"   📝 Подзадачи:")
    for i, subtask in enumerate(result.subtasks[:5], 1):
        print(f"      {i}. {subtask.name}")
    print()
else:
    print("❌ Планирование провалилось")
    for error in result.errors:
        print(f"   - {error}")

print()

# Пример 2: Оптимизация
print("=" * 70)
print("ПРИМЕР 2: Оптимизация на безопасность")
print("=" * 70)

result2 = planner.plan_task(
    user_task="Удали старые файлы из системы",
    optimization_goals={
        'time': 0.2,
        'resources': 0.2,
        'safety': 0.6  # Приоритет на безопасность
    }
)

if result2.success:
    print("✅ Планирование успешно!")
    print(f"   📊 Оценка рисков: {result2.parsed_task.risk_level.value}")
    print(f"   🛡️ Проверок безопасности:")
    
    safety_checks = [
        t for t in result2.execution_plan.get('tasks', [])
        if t.get('type') == 'safety_check'
    ]
    print(f"      - Safety checks: {len(safety_checks)}")
    
    checkpoints = result2.execution_plan.get('checkpoints', [])
    print(f"      - Checkpoints: {len(checkpoints)}")
    
    print()
    print(f"   ✅ Валидация:")
    for check_name, check_result in result2.validation_results.items():
        status = "✅" if check_result.valid else "❌"
        print(f"      {status} {check_name.capitalize()}: {check_result.score:.2f}")
    print()
else:
    print("❌ Планирование провалилось")

# Пример 3: Статистика
print("=" * 70)
print("ПРИМЕР 3: Статистика системы")
print("=" * 70)

stats = planner.get_statistics()
print(f"📈 {stats['name']}")
print(f"   Версия: {stats['version']}")
print(f"   Всего шагов: {stats['total_steps']}")
print()
print(f"   📂 Разделы:")
for section, steps in stats['sections'].items():
    print(f"      - {section}: {steps}")
print()
print(f"   🔧 Компоненты:")
for category, count in stats['components'].items():
    print(f"      - {category}: {count}")
print()

print("=" * 70)
print("🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
print("=" * 70)
print()
print("💡 Для запуска полных тестов:")
print("   python test_phase3_planning.py")
print()
print("📚 Для документации:")
print("   cat PHASE3_TASK_PLANNING_README.md")
print()
