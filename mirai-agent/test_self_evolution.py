#!/usr/bin/env python3
"""
Тест системы саморазвития МИРАЙ
"""

import json
import sys
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent))

from core.autonomous_agent import AutonomousAgent
from core.self_evolution import SelfEvolutionSystem


def test_evolution_system():
    """Тестируем систему саморазвития"""

    print("=" * 70)
    print("🧬 ТЕСТ СИСТЕМЫ САМОРАЗВИТИЯ МИРАЙ")
    print("=" * 70)

    # Инициализация
    print("\n1️⃣ Инициализация агента...")
    agent = AutonomousAgent()

    print("2️⃣ Создание системы саморазвития...")
    evolution = SelfEvolutionSystem(agent)

    # Проверка начального состояния
    print("\n3️⃣ Проверка начального состояния...")
    status = evolution.get_status()
    print(f"   Технологий в базе: {status['knowledge']['technologies']}")
    print(f"   Навыков: {status['knowledge']['skills']}")
    print(f"   Активных проектов: {status['projects']['active']}")

    # Генерация целей
    print("\n4️⃣ Генерация целей саморазвития...")
    goals = evolution.goal_generator.generate_goals(count=5)
    print(f"   Сгенерировано целей: {len(goals)}")

    for i, goal in enumerate(goals[:3], 1):
        print(f"\n   Цель #{i}:")
        print(f"     • Тип: {goal['type']}")
        print(f"     • Описание: {goal['description']}")
        print(f"     • Приоритет: {goal['priority']:.2f}")
        if "technology" in goal:
            print(f"     • Технология: {goal['technology']}")
            print(f"     • Область: {goal['area']}")

    # Запуск одного цикла саморазвития
    print("\n5️⃣ Запуск цикла саморазвития...")
    print("   (это может занять 30-60 секунд...)")

    result = evolution.evolution_cycle()

    print("\n✅ РЕЗУЛЬТАТЫ ЦИКЛА:")
    print(f"   • Сгенерировано целей: {result['goals_generated']}")
    print(f"   • Завершено обучений: {result['learning_completed']}")
    print(f"   • Сделано улучшений: {result['improvements_made']}")
    print(f"   • Прогресс проектов: {len(result['projects_progress'])}")

    if result["projects_progress"]:
        print("\n   📊 Детали прогресса:")
        for progress in result["projects_progress"]:
            print(f"     • {progress.get('project', 'Unknown')[:50]}")
            print(f"       Действие: {progress.get('action', 'N/A')}")
            print(f"       Прогресс: {progress.get('progress', 0) * 100:.0f}%")

    # Финальное состояние
    print("\n6️⃣ Финальное состояние...")
    final_status = evolution.get_status()

    print(f"\n   📚 База знаний:")
    print(f"     • Технологий: {final_status['knowledge']['technologies']}")
    print(f"     • Навыков: {final_status['knowledge']['skills']}")
    print(f"     • Выполнено задач: {final_status['knowledge']['completed_tasks']}")

    print(f"\n   🎯 Проекты:")
    print(f"     • Активных: {final_status['projects']['active']}")
    print(f"     • Завершённых: {final_status['projects']['completed']}")

    print(f"\n   🔧 Самомодификаций: {final_status['modifications']}")

    # Показываем содержимое базы знаний
    print("\n7️⃣ Содержимое базы знаний:")
    kb_path = Path("data/state/knowledge_base.json")

    if kb_path.exists():
        with open(kb_path) as f:
            kb_data = json.load(f)

        print(f"\n   Изучено технологий: {len(kb_data.get('technologies', []))}")
        for tech in kb_data.get("technologies", [])[:5]:
            print(f"     • {tech['name']} (уровень: {tech['proficiency']:.2f})")

        if len(kb_data.get("technologies", [])) > 5:
            print(f"     ... и ещё {len(kb_data['technologies']) - 5}")

    print("\n" + "=" * 70)
    print("✅ ТЕСТ ЗАВЕРШЁН")
    print("=" * 70)

    print(f"\n📁 Созданные файлы:")
    print(f"   • База знаний: {kb_path}")
    print(f"   • Обучающие проекты: learning/")

    print("\n💡 Команды Telegram для управления:")
    print("   /status или /статус - статус системы")
    print("   /evolve или /развивайся - запустить цикл саморазвития")
    print("   /toggle_evolution - включить/выключить автосаморазвитие")


if __name__ == "__main__":
    try:
        test_evolution_system()
    except KeyboardInterrupt:
        print("\n\n⌨️ Тест прерван пользователем")
    except Exception as e:
        print(f"\n\n❌ Ошибка теста: {e}")
        import traceback

        traceback.print_exc()
