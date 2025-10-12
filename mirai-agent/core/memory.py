"""
MIRAI Memory System - Долгосрочная память для автономного агента

Функции:
- Сохранение истории выполненных задач
- Логирование всех действий
- Хранение результатов работы
- Отслеживание прогресса
- Статистика и аналитика
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging


class MiraiMemory:
    """Система долгосрочной памяти для MIRAI"""

    def __init__(self, db_path: str = "data/mirai_memory.db"):
        """
        Инициализация системы памяти

        Args:
            db_path: Путь к файлу базы данных SQLite
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Возвращать словари вместо кортежей

        self._create_tables()

        logging.info(f"✅ Память инициализирована: {self.db_path}")

    def _create_tables(self):
        """Создать таблицы БД если их нет"""
        cursor = self.conn.cursor()

        # Таблица задач
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_at TIMESTAMP,
                completed_at TIMESTAMP,
                result TEXT,
                error TEXT
            )
        """
        )

        # Таблица логов действий
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                action_type TEXT NOT NULL,
                action_data TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN DEFAULT 1,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        """
        )

        # Таблица результатов
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                result_type TEXT,
                content TEXT,
                file_path TEXT,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (task_id) REFERENCES tasks (id)
            )
        """
        )

        # Таблица метрик и статистики
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL,
                metric_unit TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        """
        )

        # Таблица обучения (что узнал агент)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS learnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                confidence REAL DEFAULT 0.5,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP
            )
        """
        )

        self.conn.commit()
        logging.info("✅ Таблицы БД созданы/проверены")

    # === УПРАВЛЕНИЕ ЗАДАЧАМИ ===

    def create_task(
        self, task_name: str, description: str = "", priority: str = "medium"
    ) -> int:
        """Создать новую задачу"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO tasks (task_name, description, priority)
            VALUES (?, ?, ?)
        """,
            (task_name, description, priority),
        )
        self.conn.commit()
        task_id = cursor.lastrowid

        logging.info(f"📝 Задача создана: {task_name} (ID: {task_id})")
        return task_id

    def start_task(self, task_id: int):
        """Начать выполнение задачи"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE tasks 
            SET status = 'in_progress', started_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """,
            (task_id,),
        )
        self.conn.commit()
        logging.info(f"▶️ Задача начата: {task_id}")

    def complete_task(self, task_id: int, result: str = "", error: str = ""):
        """Завершить задачу"""
        status = "completed" if not error else "failed"
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE tasks 
            SET status = ?, completed_at = CURRENT_TIMESTAMP, 
                result = ?, error = ?
            WHERE id = ?
        """,
            (status, result, error, task_id),
        )
        self.conn.commit()

        emoji = "✅" if not error else "❌"
        logging.info(f"{emoji} Задача завершена: {task_id} ({status})")

    def get_task(self, task_id: int) -> Optional[Dict]:
        """Получить задачу по ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_recent_tasks(self, limit: int = 10) -> List[Dict]:
        """Получить последние задачи"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT * FROM tasks 
            ORDER BY created_at DESC 
            LIMIT ?
        """,
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]

    # === ЛОГИРОВАНИЕ ДЕЙСТВИЙ ===

    def log_action(
        self,
        action_type: str,
        action_data: Any = None,
        task_id: int = None,
        success: bool = True,
    ):
        """Залогировать действие"""
        cursor = self.conn.cursor()
        data_json = json.dumps(action_data) if action_data else None

        cursor.execute(
            """
            INSERT INTO action_logs (task_id, action_type, action_data, success)
            VALUES (?, ?, ?, ?)
        """,
            (task_id, action_type, data_json, success),
        )
        self.conn.commit()

    def get_action_history(self, task_id: int = None, limit: int = 100) -> List[Dict]:
        """Получить историю действий"""
        cursor = self.conn.cursor()

        if task_id:
            cursor.execute(
                """
                SELECT * FROM action_logs 
                WHERE task_id = ?
                ORDER BY timestamp DESC 
                LIMIT ?
            """,
                (task_id, limit),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM action_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            """,
                (limit,),
            )

        return [dict(row) for row in cursor.fetchall()]

    # === СОХРАНЕНИЕ РЕЗУЛЬТАТОВ ===

    def save_result(
        self,
        task_id: int,
        result_type: str,
        content: str = "",
        file_path: str = "",
        metadata: Dict = None,
    ) -> int:
        """Сохранить результат работы"""
        cursor = self.conn.cursor()
        metadata_json = json.dumps(metadata) if metadata else None

        cursor.execute(
            """
            INSERT INTO results (task_id, result_type, content, file_path, metadata)
            VALUES (?, ?, ?, ?, ?)
        """,
            (task_id, result_type, content, file_path, metadata_json),
        )
        self.conn.commit()

        result_id = cursor.lastrowid
        logging.info(f"💾 Результат сохранен: {result_type} (ID: {result_id})")
        return result_id

    def get_results(self, task_id: int = None) -> List[Dict]:
        """Получить результаты"""
        cursor = self.conn.cursor()

        if task_id:
            cursor.execute(
                """
                SELECT * FROM results WHERE task_id = ?
                ORDER BY created_at DESC
            """,
                (task_id,),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM results 
                ORDER BY created_at DESC 
                LIMIT 50
            """
            )

        return [dict(row) for row in cursor.fetchall()]

    # === МЕТРИКИ И СТАТИСТИКА ===

    def save_metric(
        self, metric_name: str, value: float, unit: str = "", metadata: Dict = None
    ):
        """Сохранить метрику"""
        cursor = self.conn.cursor()
        metadata_json = json.dumps(metadata) if metadata else None

        cursor.execute(
            """
            INSERT INTO metrics (metric_name, metric_value, metric_unit, metadata)
            VALUES (?, ?, ?, ?)
        """,
            (metric_name, value, unit, metadata_json),
        )
        self.conn.commit()

    def get_metrics(self, metric_name: str = None, limit: int = 100) -> List[Dict]:
        """Получить метрики"""
        cursor = self.conn.cursor()

        if metric_name:
            cursor.execute(
                """
                SELECT * FROM metrics 
                WHERE metric_name = ?
                ORDER BY timestamp DESC 
                LIMIT ?
            """,
                (metric_name, limit),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM metrics 
                ORDER BY timestamp DESC 
                LIMIT ?
            """,
                (limit,),
            )

        return [dict(row) for row in cursor.fetchall()]

    def get_statistics(self) -> Dict:
        """Получить общую статистику"""
        cursor = self.conn.cursor()

        stats = {}

        # Количество задач по статусам
        cursor.execute(
            """
            SELECT status, COUNT(*) as count 
            FROM tasks 
            GROUP BY status
        """
        )
        stats["tasks_by_status"] = {
            row["status"]: row["count"] for row in cursor.fetchall()
        }

        # Общее количество действий
        cursor.execute("SELECT COUNT(*) as count FROM action_logs")
        stats["total_actions"] = cursor.fetchone()["count"]

        # Количество результатов
        cursor.execute("SELECT COUNT(*) as count FROM results")
        stats["total_results"] = cursor.fetchone()["count"]

        # Успешность выполнения
        cursor.execute(
            """
            SELECT 
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful,
                COUNT(*) as total
            FROM action_logs
        """
        )
        row = cursor.fetchone()
        if row["total"] > 0:
            stats["success_rate"] = row["successful"] / row["total"] * 100
        else:
            stats["success_rate"] = 0

        return stats

    # === ОБУЧЕНИЕ (ЗНАНИЯ) ===

    def save_learning(
        self, topic: str, content: str, source: str = "", confidence: float = 0.5
    ) -> int:
        """Сохранить полученное знание"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO learnings (topic, content, source, confidence)
            VALUES (?, ?, ?, ?)
        """,
            (topic, content, source, confidence),
        )
        self.conn.commit()

        learning_id = cursor.lastrowid
        logging.info(f"🧠 Знание сохранено: {topic} (ID: {learning_id})")
        return learning_id

    def get_learnings(self, topic: str = None, limit: int = 50) -> List[Dict]:
        """Получить сохраненные знания"""
        cursor = self.conn.cursor()

        if topic:
            cursor.execute(
                """
                SELECT * FROM learnings 
                WHERE topic LIKE ?
                ORDER BY confidence DESC, created_at DESC
                LIMIT ?
            """,
                (f"%{topic}%", limit),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM learnings 
                ORDER BY created_at DESC 
                LIMIT ?
            """,
                (limit,),
            )

        return [dict(row) for row in cursor.fetchall()]

    def update_learning_usage(self, learning_id: int):
        """Обновить время последнего использования знания"""
        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE learnings 
            SET last_used = CURRENT_TIMESTAMP 
            WHERE id = ?
        """,
            (learning_id,),
        )
        self.conn.commit()

    # === УТИЛИТЫ ===

    def clear_old_data(self, days: int = 30):
        """Очистить старые данные (старше X дней)"""
        cursor = self.conn.cursor()

        # Удалить старые логи
        cursor.execute(
            """
            DELETE FROM action_logs 
            WHERE timestamp < datetime('now', '-' || ? || ' days')
        """,
            (days,),
        )

        deleted_logs = cursor.rowcount
        self.conn.commit()

        logging.info(f"🗑️ Удалено {deleted_logs} старых логов")
        return deleted_logs

    def close(self):
        """Закрыть соединение с БД"""
        self.conn.close()
        logging.info("🔌 Соединение с БД закрыто")

    def __del__(self):
        """Деструктор - закрыть соединение"""
        if hasattr(self, "conn"):
            self.conn.close()


# Пример использования
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("🧪 Тестирование системы памяти MIRAI...\n")

    # Создать память
    memory = MiraiMemory()

    # Создать задачу
    task_id = memory.create_task(
        "Тестирование памяти", "Проверка работы SQLite базы данных", priority="high"
    )

    # Начать задачу
    memory.start_task(task_id)

    # Залогировать действия
    memory.log_action("test_action", {"data": "test"}, task_id=task_id)
    memory.log_action("another_action", {"value": 123}, task_id=task_id)

    # Сохранить результат
    memory.save_result(
        task_id, "test_result", content="Тест прошел успешно!", metadata={"test": True}
    )

    # Завершить задачу
    memory.complete_task(task_id, result="Всё работает!")

    # Сохранить метрики
    memory.save_metric("test_metric", 42.5, "units")

    # Сохранить знание
    memory.save_learning(
        "SQLite",
        "SQLite - это легковесная встраиваемая БД",
        source="документация",
        confidence=0.9,
    )

    # Получить статистику
    stats = memory.get_statistics()

    print("\n📊 Статистика:")
    print(f"Задачи по статусам: {stats['tasks_by_status']}")
    print(f"Всего действий: {stats['total_actions']}")
    print(f"Всего результатов: {stats['total_results']}")
    print(f"Процент успеха: {stats['success_rate']:.1f}%")

    # Получить последние задачи
    recent_tasks = memory.get_recent_tasks(limit=5)
    print(f"\n📋 Последние задачи: {len(recent_tasks)}")
    for task in recent_tasks:
        print(f"  - {task['task_name']} ({task['status']})")

    print("\n✅ Тест системы памяти завершен!")
