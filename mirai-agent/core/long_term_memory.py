#!/usr/bin/env python3
"""
🧠 Долгосрочная Память MIRAI
Хранение целей, достижений, решений и обучение на истории
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


class Goal:
    """Класс цели"""

    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        priority: int,
        status: str,
        created_at: str,
        deadline: Optional[str] = None,
    ):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = created_at
        self.deadline = deadline

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "deadline": self.deadline,
        }


class LongTermMemory:
    """
    Долгосрочная память MIRAI:
    - Цели (goals)
    - Достижения (achievements)
    - Неудачи (failures)
    - Решения (decisions)
    """

    def __init__(
        self, db_path: str = "/root/mirai/mirai-agent/data/long_term_memory.db"
    ):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Таблица целей
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority INTEGER DEFAULT 5,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deadline TIMESTAMP,
                completed_at TIMESTAMP
            )
        """
        )

        # Таблица достижений
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id INTEGER,
                description TEXT NOT NULL,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (goal_id) REFERENCES goals(id)
            )
        """
        )

        # Таблица неудач (для обучения)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS failures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal_id INTEGER,
                reason TEXT NOT NULL,
                lesson_learned TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (goal_id) REFERENCES goals(id)
            )
        """
        )

        # Таблица решений
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                context TEXT NOT NULL,
                decision TEXT NOT NULL,
                reasoning TEXT,
                outcome TEXT,
                outcome_rating INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                evaluated_at TIMESTAMP
            )
        """
        )

        # Таблица планов
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                plan_type TEXT,
                plan_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                valid_until TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def set_goal(
        self,
        title: str,
        description: str = "",
        priority: int = 5,
        deadline: Optional[str] = None,
    ) -> int:
        """
        Установить новую цель

        Args:
            title: Название цели
            description: Описание цели
            priority: Приоритет (1-10, где 10 - самый высокий)
            deadline: Дедлайн в формате YYYY-MM-DD HH:MM:SS

        Returns:
            ID созданной цели
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO goals (title, description, priority, deadline)
            VALUES (?, ?, ?, ?)
        """,
            (title, description, priority, deadline),
        )

        goal_id = cursor.lastrowid
        conn.commit()
        conn.close()

        print(f"✅ Цель установлена: '{title}' (ID: {goal_id}, Priority: {priority})")
        return goal_id

    def get_active_goals(self, limit: int = 10) -> List[Goal]:
        """Получить активные цели, отсортированные по приоритету"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, title, description, priority, status, created_at, deadline
            FROM goals
            WHERE status = 'active'
            ORDER BY priority DESC, created_at ASC
            LIMIT ?
        """,
            (limit,),
        )

        goals = [Goal(*row) for row in cursor.fetchall()]
        conn.close()

        return goals

    def get_all_goals(self, status: Optional[str] = None) -> List[Goal]:
        """Получить все цели (опционально фильтр по статусу)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        if status:
            cursor.execute(
                """
                SELECT id, title, description, priority, status, created_at, deadline
                FROM goals
                WHERE status = ?
                ORDER BY priority DESC, created_at DESC
            """,
                (status,),
            )
        else:
            cursor.execute(
                """
                SELECT id, title, description, priority, status, created_at, deadline
                FROM goals
                ORDER BY priority DESC, created_at DESC
            """
            )

        goals = [Goal(*row) for row in cursor.fetchall()]
        conn.close()

        return goals

    def complete_goal(self, goal_id: int, result: str = "") -> bool:
        """Отметить цель как выполненную"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE goals
            SET status = 'completed', completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """,
            (goal_id,),
        )

        # Записываем достижение
        if result:
            cursor.execute(
                """
                INSERT INTO achievements (goal_id, description, result)
                VALUES (?, ?, ?)
            """,
                (goal_id, f"Goal completed: {goal_id}", result),
            )

        conn.commit()
        affected = cursor.rowcount
        conn.close()

        if affected > 0:
            print(f"🎉 Цель #{goal_id} выполнена!")
            return True
        return False

    def fail_goal(self, goal_id: int, reason: str, lesson_learned: str = "") -> bool:
        """Отметить цель как проваленную"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE goals
            SET status = 'failed', completed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """,
            (goal_id,),
        )

        # Записываем неудачу и урок
        cursor.execute(
            """
            INSERT INTO failures (goal_id, reason, lesson_learned)
            VALUES (?, ?, ?)
        """,
            (goal_id, reason, lesson_learned),
        )

        conn.commit()
        affected = cursor.rowcount
        conn.close()

        if affected > 0:
            print(f"❌ Цель #{goal_id} провалена. Урок: {lesson_learned}")
            return True
        return False

    def record_achievement(
        self, description: str, result: str = "", goal_id: Optional[int] = None
    ):
        """Записать достижение (может быть не связано с целью)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO achievements (goal_id, description, result)
            VALUES (?, ?, ?)
        """,
            (goal_id, description, result),
        )

        conn.commit()
        conn.close()

        print(f"🏆 Достижение записано: {description}")

    def record_decision(self, context: str, decision: str, reasoning: str = "") -> int:
        """Записать принятое решение"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO decisions (context, decision, reasoning)
            VALUES (?, ?, ?)
        """,
            (context, decision, reasoning),
        )

        decision_id = cursor.lastrowid
        conn.commit()
        conn.close()

        print(f"📝 Решение записано (ID: {decision_id})")
        return decision_id

    def evaluate_decision(self, decision_id: int, outcome: str, rating: int):
        """
        Оценить результат решения

        Args:
            decision_id: ID решения
            outcome: Описание результата
            rating: Оценка (1-10)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE decisions
            SET outcome = ?, outcome_rating = ?, evaluated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """,
            (outcome, rating, decision_id),
        )

        conn.commit()
        conn.close()

        emoji = "✅" if rating >= 7 else "⚠️" if rating >= 4 else "❌"
        print(f"{emoji} Решение #{decision_id} оценено: {rating}/10 - {outcome}")

    def learn_from_history(self, days: int = 30) -> Dict:
        """
        Извлечь уроки из истории за последние N дней

        Returns:
            Dict с анализом: успехи, неудачи, паттерны
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        since = (datetime.now() - timedelta(days=days)).isoformat()

        # Успешные цели
        cursor.execute(
            """
            SELECT COUNT(*) FROM goals
            WHERE status = 'completed' AND completed_at >= ?
        """,
            (since,),
        )
        completed_goals = cursor.fetchone()[0]

        # Проваленные цели
        cursor.execute(
            """
            SELECT COUNT(*) FROM goals
            WHERE status = 'failed' AND completed_at >= ?
        """,
            (since,),
        )
        failed_goals = cursor.fetchone()[0]

        # Достижения
        cursor.execute(
            """
            SELECT COUNT(*) FROM achievements
            WHERE created_at >= ?
        """,
            (since,),
        )
        achievements_count = cursor.fetchone()[0]

        # Лучшие и худшие решения
        cursor.execute(
            """
            SELECT AVG(outcome_rating) FROM decisions
            WHERE evaluated_at >= ? AND outcome_rating IS NOT NULL
        """,
            (since,),
        )
        avg_decision_rating = cursor.fetchone()[0] or 0

        # Уроки из неудач
        cursor.execute(
            """
            SELECT lesson_learned FROM failures
            WHERE created_at >= ? AND lesson_learned IS NOT NULL
            ORDER BY created_at DESC
            LIMIT 5
        """,
            (since,),
        )
        lessons = [row[0] for row in cursor.fetchall()]

        conn.close()

    def get_recent_achievements(self, limit: int = 20) -> List[Dict]:
        """
        Получить недавние достижения для анализа

        Args:
            limit: Максимальное количество достижений

        Returns:
            List словарей с достижениями
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, goal_id, description, result, created_at
            FROM achievements
            ORDER BY created_at DESC
            LIMIT ?
        """,
            (limit,),
        )

        achievements = []
        for row in cursor.fetchall():
            achievements.append(
                {
                    "id": row[0],
                    "goal_id": row[1],
                    "description": row[2],
                    "result": row[3],
                    "created_at": row[4],
                    "impact": 5,  # Default impact для совместимости
                }
            )

        conn.close()
        return achievements

    def learn_from_history_impl(self, days: int = 30) -> Dict:
        """Внутренняя реализация learn_from_history"""
        since = (datetime.now() - timedelta(days=days)).isoformat()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Собираем статистику
        cursor.execute(
            "SELECT COUNT(*) FROM goals WHERE status = 'completed' AND updated_at >= ?",
            (since,),
        )
        completed_goals = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM goals WHERE status = 'failed' AND updated_at >= ?",
            (since,),
        )
        failed_goals = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM achievements WHERE created_at >= ?", (since,)
        )
        achievements_count = cursor.fetchone()[0]

        cursor.execute(
            "SELECT AVG(outcome_rating) FROM decisions WHERE evaluated_at >= ? AND outcome_rating IS NOT NULL",
            (since,),
        )
        avg_decision_rating = cursor.fetchone()[0] or 0

        cursor.execute(
            "SELECT lesson_learned FROM failures WHERE created_at >= ? AND lesson_learned IS NOT NULL ORDER BY created_at DESC LIMIT 5",
            (since,),
        )
        lessons = [row[0] for row in cursor.fetchall()]

        conn.close()

        analysis = {
            "period_days": days,
            "completed_goals": completed_goals,
            "failed_goals": failed_goals,
            "success_rate": (
                completed_goals / (completed_goals + failed_goals) * 100
                if (completed_goals + failed_goals) > 0
                else 0
            ),
            "achievements_count": achievements_count,
            "avg_decision_rating": round(avg_decision_rating, 1),
            "recent_lessons": lessons,
        }

        return analysis

    def get_summary(self) -> str:
        """Получить краткую сводку памяти"""
        active_goals = self.get_active_goals()
        history = self.learn_from_history(days=7)

        summary = f"""
📊 ДОЛГОСРОЧНАЯ ПАМЯТЬ MIRAI

🎯 Активные цели: {len(active_goals)}
"""

        if active_goals:
            summary += "\nТоп-3 приоритета:\n"
            for i, goal in enumerate(active_goals[:3], 1):
                summary += f"  {i}. [{goal.priority}] {goal.title}\n"

        summary += f"""
📈 За последние 7 дней:
  ✅ Выполнено целей: {history['completed_goals']}
  ❌ Провалено целей: {history['failed_goals']}
  📊 Success Rate: {history['success_rate']:.1f}%
  🏆 Достижений: {history['achievements_count']}
  🧠 Качество решений: {history['avg_decision_rating']}/10
"""

        if history["recent_lessons"]:
            summary += "\n💡 Последние уроки:\n"
            for lesson in history["recent_lessons"][:3]:
                summary += f"  • {lesson}\n"

        return summary.strip()


def main():
    """Демонстрация работы долгосрочной памяти"""
    print("🧠 ТЕСТ ДОЛГОСРОЧНОЙ ПАМЯТИ MIRAI\n")

    ltm = LongTermMemory()

    # Создаём примеры целей
    goal1 = ltm.set_goal(
        title="Достичь 90% покрытия тестами",
        description="Написать unit-тесты для всех core модулей",
        priority=8,
        deadline=(datetime.now() + timedelta(days=14)).isoformat(),
    )

    goal2 = ltm.set_goal(
        title="Оптимизировать производительность на 20%",
        description="Профилировать код и устранить узкие места",
        priority=6,
    )

    goal3 = ltm.set_goal(
        title="Автоматизировать деплоймент",
        description="Настроить CI/CD pipeline с автоматическим деплоем",
        priority=9,
    )

    # Записываем достижение
    ltm.record_achievement(
        description="Добавлена GitHub Integration с auto-fix кода",
        result="Создано 4 новых метода, интеграция работает",
    )

    # Записываем решение
    decision1 = ltm.record_decision(
        context="CI/CD показывает 75% success rate",
        decision="Добавить автоматическое исправление кода каждые 30 минут",
        reasoning="Проактивный подход лучше реактивного",
    )

    # Оцениваем решение
    ltm.evaluate_decision(
        decision1, outcome="Auto-fix успешно создаёт PR с исправлениями", rating=9
    )

    # Получаем активные цели
    print("\n" + "=" * 60)
    print("АКТИВНЫЕ ЦЕЛИ:")
    print("=" * 60)
    for goal in ltm.get_active_goals():
        print(f"\n[{goal.priority}] {goal.title}")
        print(f"    {goal.description}")
        if goal.deadline:
            print(f"    ⏰ Deadline: {goal.deadline}")

    # Показываем сводку
    print("\n" + "=" * 60)
    print(ltm.get_summary())
    print("=" * 60)

    # Анализ истории
    print("\n📚 АНАЛИЗ ИСТОРИИ:")
    history = ltm.learn_from_history(days=30)
    print(json.dumps(history, indent=2, ensure_ascii=False))

    def get_recent_achievements(self, limit: int = 20) -> List[Dict]:
        """
        Получить недавние достижения для анализа

        Args:
            limit: Максимальное количество достижений

        Returns:
            List словарей с достижениями
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, goal_id, description, result, created_at
            FROM achievements
            ORDER BY created_at DESC
            LIMIT ?
        """,
            (limit,),
        )

        achievements = []
        for row in cursor.fetchall():
            achievements.append(
                {
                    "id": row[0],
                    "goal_id": row[1],
                    "description": row[2],
                    "result": row[3],
                    "created_at": row[4],
                    "impact": 5,  # Default impact для совместимости
                }
            )

        conn.close()
        return achievements


if __name__ == "__main__":
    main()
