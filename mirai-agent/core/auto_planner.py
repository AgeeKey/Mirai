#!/usr/bin/env python3
"""
📋 Автоматическое Планирование MIRAI
Создание daily/weekly планов на основе целей, приоритетов и самоанализа
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class Task:
    """Задача в плане"""

    id: int
    title: str
    description: str
    priority: int
    estimated_hours: float
    deadline: Optional[str]
    goal_id: Optional[int]
    status: str  # planned, in_progress, completed, skipped


class AutoPlanner:
    """
    Автоматическое планирование для MIRAI:
    - Анализ активных целей
    - Оценка приоритетов
    - Создание daily/weekly планов
    - Адаптация к результатам
    """

    def __init__(
        self,
        memory_db: str = "/root/mirai/mirai-agent/data/long_term_memory.db",
    ):
        self.memory_db = Path(memory_db)

    def create_daily_plan(self) -> Dict:
        """
        Создать план на день

        Returns:
            Dict с планом дня
        """
        from core.long_term_memory import LongTermMemory
        from core.self_awareness import SelfAwareness

        ltm = LongTermMemory()
        awareness = SelfAwareness()

        # 1. Получаем активные цели
        active_goals = ltm.get_active_goals(limit=10)

        # 2. Анализируем текущую эффективность
        performance = awareness.analyze_performance(days=7)
        improvements = awareness.propose_improvements()

        # 3. Определяем фокус дня на основе анализа
        focus_area = self._determine_daily_focus(performance, improvements)

        # 4. Генерируем задачи на день
        tasks = self._generate_daily_tasks(active_goals, focus_area, improvements)

        # 5. Сохраняем план
        plan = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "created_at": datetime.now().isoformat(),
            "focus_area": focus_area,
            "performance_score": performance["overall_score"],
            "tasks": [
                {
                    "title": t["title"],
                    "priority": t["priority"],
                    "estimated_hours": t["estimated_hours"],
                    "goal_id": t.get("goal_id"),
                }
                for t in tasks
            ],
            "total_tasks": len(tasks),
            "estimated_hours": sum(t["estimated_hours"] for t in tasks),
        }

        self._save_plan(plan, "daily")

        return plan

    def create_weekly_plan(self) -> Dict:
        """
        Создать план на неделю

        Returns:
            Dict с планом недели
        """
        from core.long_term_memory import LongTermMemory
        from core.self_awareness import SelfAwareness

        ltm = LongTermMemory()
        awareness = SelfAwareness()

        # 1. Получаем все активные цели
        active_goals = ltm.get_active_goals(limit=20)

        # 2. Анализируем текущую эффективность
        performance = awareness.analyze_performance(days=30)
        improvements = awareness.propose_improvements()

        # 3. Определяем стратегию недели
        strategy = self._determine_weekly_strategy(active_goals, performance, improvements)

        # 4. Распределяем задачи по дням недели
        weekly_tasks = self._distribute_tasks_by_days(active_goals, strategy)

        # 5. Сохраняем план
        plan = {
            "week_start": datetime.now().strftime("%Y-%m-%d"),
            "week_end": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "created_at": datetime.now().isoformat(),
            "strategy": strategy,
            "performance_score": performance["overall_score"],
            "daily_plans": weekly_tasks,
            "total_goals": len(active_goals),
            "high_priority_goals": len([g for g in active_goals if g.priority >= 8]),
        }

        self._save_plan(plan, "weekly")

        return plan

    def _determine_daily_focus(self, performance: Dict, improvements: List[Dict]) -> str:
        """Определить фокус дня на основе анализа"""

        # Если есть критичные проблемы - фокус на них
        critical = [i for i in improvements if i["priority"] == "критичный"]
        if critical:
            return f"🔴 Критично: {critical[0]['area']}"

        # Если performance низкий - фокус на улучшение слабых сторон
        if performance["overall_score"] < 50:
            return "⚠️ Улучшение базовых показателей"

        # Если есть высокоприоритетные улучшения
        high_priority = [i for i in improvements if i["priority"] == "высокий"]
        if high_priority:
            return f"🟠 Приоритет: {high_priority[0]['area']}"

        # Если performance средний - фокус на прогресс по целям
        if performance["overall_score"] < 70:
            return "🎯 Выполнение активных целей"

        # Если всё хорошо - фокус на инновации
        return "🚀 Инновации и новые возможности"

    def _determine_weekly_strategy(
        self, goals: List, performance: Dict, improvements: List[Dict]
    ) -> str:
        """Определить стратегию недели"""

        # Если много активных целей - фокус на завершение
        if len(goals) > 10:
            return "🎯 Завершение накопившихся целей"

        # Если низкий success rate - фокус на качество
        if performance["goals"]["success_rate"] < 50:
            return "✅ Качество выполнения над количеством"

        # Если тренд ухудшения - фокус на стабилизацию
        if performance["trends"]["direction"] == "degrading":
            return "📉 Стабилизация и исправление проблем"

        # Если тренд улучшения - продолжаем курс
        if performance["trends"]["direction"] == "improving":
            return "📈 Ускорение прогресса"

        # По умолчанию - сбалансированный подход
        return "⚖️ Баланс между целями и улучшениями"

    def _generate_daily_tasks(
        self, goals: List, focus_area: str, improvements: List[Dict]
    ) -> List[Dict]:
        """Генерировать задачи на день"""
        tasks = []

        # 1. Критичные задачи из improvements (если есть)
        critical = [i for i in improvements if i["priority"] in ["критичный", "высокий"]]
        for imp in critical[:2]:  # Максимум 2 критичные задачи в день
            tasks.append(
                {
                    "title": f"Улучшение: {imp['area']}",
                    "description": imp["suggestion"],
                    "priority": 10 if imp["priority"] == "критичный" else 9,
                    "estimated_hours": 2.0,
                    "goal_id": None,
                }
            )

        # 2. Задачи по топ-3 целям
        for goal in goals[:3]:
            tasks.append(
                {
                    "title": f"Цель: {goal.title}",
                    "description": goal.description,
                    "priority": goal.priority,
                    "estimated_hours": 1.5,
                    "goal_id": goal.id,
                }
            )

        # 3. Регулярные задачи (мониторинг, обучение)
        tasks.append(
            {
                "title": "Мониторинг системы и CI/CD",
                "description": "Проверить логи, метрики, GitHub Actions",
                "priority": 7,
                "estimated_hours": 0.5,
                "goal_id": None,
            }
        )

        tasks.append(
            {
                "title": "NASA-Level обучение",
                "description": "Изучить новую технологию через NASA-Level",
                "priority": 6,
                "estimated_hours": 1.0,
                "goal_id": None,
            }
        )

        # Сортируем по приоритету
        tasks.sort(key=lambda t: t["priority"], reverse=True)

        return tasks[:6]  # Максимум 6 задач в день

    def _distribute_tasks_by_days(self, goals: List, strategy: str) -> Dict:
        """Распределить задачи по дням недели"""
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

        weekly_plan = {}

        # Стратегия распределения зависит от общей стратегии
        if "Завершение" in strategy:
            # Фокус на завершение старых целей
            for i, day in enumerate(days):
                goals_for_day = goals[i * 2 : (i + 1) * 2]  # 2 цели в день
                weekly_plan[day] = [
                    {
                        "title": f"Завершить: {g.title}",
                        "priority": g.priority,
                        "estimated_hours": 3.0,
                    }
                    for g in goals_for_day
                ]

        elif "Качество" in strategy:
            # Меньше задач, больше фокуса
            for i, day in enumerate(days):
                if i < len(goals):
                    weekly_plan[day] = [
                        {
                            "title": f"Качественное выполнение: {goals[i].title}",
                            "priority": goals[i].priority,
                            "estimated_hours": 4.0,
                        }
                    ]
                else:
                    weekly_plan[day] = []

        else:
            # Сбалансированный подход
            for i, day in enumerate(days):
                tasks_per_day = []

                # 1 высокоприоритетная цель
                if i < len(goals):
                    tasks_per_day.append(
                        {
                            "title": goals[i].title,
                            "priority": goals[i].priority,
                            "estimated_hours": 2.0,
                        }
                    )

                # + регулярные задачи
                tasks_per_day.append(
                    {"title": "Мониторинг и обучение", "priority": 6, "estimated_hours": 1.5}
                )

                weekly_plan[day] = tasks_per_day

        return weekly_plan

    def _save_plan(self, plan: Dict, plan_type: str):
        """Сохранить план в базу данных"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO plans (title, description, plan_type, plan_data, valid_until)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                f"{plan_type.capitalize()} Plan - {plan.get('date', plan.get('week_start'))}",
                f"Auto-generated {plan_type} plan",
                plan_type,
                json.dumps(plan, ensure_ascii=False),
                (
                    datetime.now() + timedelta(days=1 if plan_type == "daily" else 7)
                ).isoformat(),
            ),
        )

        conn.commit()
        conn.close()

    def get_current_plan(self, plan_type: str = "daily") -> Optional[Dict]:
        """Получить текущий активный план"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT plan_data FROM plans
            WHERE plan_type = ? AND valid_until >= datetime('now')
            ORDER BY created_at DESC
            LIMIT 1
        """,
            (plan_type,),
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            return json.loads(row[0])
        return None

    def review_plan_execution(self) -> Dict:
        """
        Проанализировать выполнение плана

        Returns:
            Dict с анализом выполнения
        """
        from core.long_term_memory import LongTermMemory

        ltm = LongTermMemory()
        current_plan = self.get_current_plan("daily")

        if not current_plan:
            return {"status": "no_plan", "message": "Нет активного плана на сегодня"}

        # Анализируем достижения за сегодня
        today_start = datetime.now().replace(hour=0, minute=0, second=0)

        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) FROM achievements
            WHERE created_at >= ?
        """,
            (today_start.isoformat(),),
        )
        achievements_today = cursor.fetchone()[0]

        # Проверяем прогресс по целям
        cursor.execute(
            """
            SELECT COUNT(*) FROM goals
            WHERE status = 'completed' AND completed_at >= ?
        """,
            (today_start.isoformat(),),
        )
        completed_goals_today = cursor.fetchone()[0]

        conn.close()

        total_tasks = current_plan.get("total_tasks", 0)
        estimated_hours = current_plan.get("estimated_hours", 0)

        # Оценка выполнения (простая эвристика)
        completion_rate = min(
            (achievements_today / max(total_tasks, 1)) * 100,
            100,
        )

        review = {
            "plan_date": current_plan.get("date"),
            "focus_area": current_plan.get("focus_area"),
            "planned_tasks": total_tasks,
            "estimated_hours": estimated_hours,
            "achievements_today": achievements_today,
            "completed_goals_today": completed_goals_today,
            "completion_rate": round(completion_rate, 1),
            "status": (
                "excellent"
                if completion_rate >= 80
                else "good" if completion_rate >= 60 else "needs_improvement"
            ),
        }

        return review

    def adapt_plan(self) -> Dict:
        """
        Адаптировать план на основе результатов

        Returns:
            Dict с адаптированным планом
        """
        review = self.review_plan_execution()

        if review.get("status") == "no_plan":
            return self.create_daily_plan()

        # Если выполнение отличное - создаём более амбициозный план завтра
        if review["status"] == "excellent":
            return {
                "adaptation": "increase_ambition",
                "message": "Отличное выполнение! Завтра увеличим количество задач.",
                "next_plan_tasks": review["planned_tasks"] + 1,
            }

        # Если выполнение плохое - уменьшаем нагрузку
        elif review["status"] == "needs_improvement":
            return {
                "adaptation": "reduce_load",
                "message": "План не выполнен. Завтра уменьшим нагрузку.",
                "next_plan_tasks": max(review["planned_tasks"] - 1, 3),
            }

        # Если выполнение нормальное - без изменений
        else:
            return {
                "adaptation": "maintain",
                "message": "Нормальное выполнение. Продолжаем в том же духе.",
                "next_plan_tasks": review["planned_tasks"],
            }

    def get_plan_summary(self) -> str:
        """Получить краткую сводку текущего плана"""
        daily_plan = self.get_current_plan("daily")
        weekly_plan = self.get_current_plan("weekly")

        summary = "📋 ПЛАНИРОВАНИЕ MIRAI\n\n"

        if daily_plan:
            summary += f"📅 План на сегодня ({daily_plan['date']}):\n"
            summary += f"  Фокус: {daily_plan['focus_area']}\n"
            summary += f"  Задач: {daily_plan['total_tasks']}\n"
            summary += f"  Часов: {daily_plan['estimated_hours']:.1f}\n"

            if daily_plan.get("tasks"):
                summary += "\n  Топ-3 задачи:\n"
                for i, task in enumerate(daily_plan["tasks"][:3], 1):
                    summary += f"    {i}. [{task['priority']}] {task['title']}\n"
        else:
            summary += "📅 Нет плана на сегодня\n"

        summary += "\n"

        if weekly_plan:
            summary += f"📆 План на неделю ({weekly_plan['week_start']} - {weekly_plan['week_end']}):\n"
            summary += f"  Стратегия: {weekly_plan['strategy']}\n"
            summary += f"  Целей: {weekly_plan['total_goals']}\n"
            summary += f"  Высокоприоритетных: {weekly_plan['high_priority_goals']}\n"
        else:
            summary += "📆 Нет плана на неделю\n"

        return summary.strip()


def main():
    """Демонстрация автопланирования"""
    print("📋 ТЕСТ АВТОМАТИЧЕСКОГО ПЛАНИРОВАНИЯ MIRAI\n")

    planner = AutoPlanner()

    # Создаём план на день
    print("=" * 70)
    print("📅 СОЗДАЮ ПЛАН НА ДЕНЬ...\n")
    daily_plan = planner.create_daily_plan()

    print(f"Дата: {daily_plan['date']}")
    print(f"Фокус: {daily_plan['focus_area']}")
    print(f"Performance Score: {daily_plan['performance_score']:.1f}/100")
    print(f"\nЗадачи на день ({daily_plan['total_tasks']}):\n")

    for i, task in enumerate(daily_plan["tasks"], 1):
        print(f"{i}. [{task['priority']}] {task['title']}")
        print(f"   Время: {task['estimated_hours']}ч")
        if task.get("goal_id"):
            print(f"   Цель ID: {task['goal_id']}")
        print()

    print(f"Всего часов: {daily_plan['estimated_hours']:.1f}ч")

    # Создаём план на неделю
    print("\n" + "=" * 70)
    print("📆 СОЗДАЮ ПЛАН НА НЕДЕЛЮ...\n")
    weekly_plan = planner.create_weekly_plan()

    print(f"Период: {weekly_plan['week_start']} - {weekly_plan['week_end']}")
    print(f"Стратегия: {weekly_plan['strategy']}")
    print(f"Целей: {weekly_plan['total_goals']}")
    print(f"Высокоприоритетных: {weekly_plan['high_priority_goals']}")

    # Сводка
    print("\n" + "=" * 70)
    print(planner.get_plan_summary())


if __name__ == "__main__":
    main()
