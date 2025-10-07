"""Memory module mock for tests."""

import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class AgentMemory:
    """Класс для работы с памятью агента.
    
    Сохраняет воспоминания в SQLite и предоставляет методы для их поиска и извлечения.
    """

    def __init__(self, db_path: str = None):
        """Инициализация памяти агента."""
        self.db_path = db_path or "memory_test.db"
        self.embedding_cache = {}
        self._setup_db()

    def _setup_db(self):
        """Создание таблицы для хранения воспоминаний, если её нет."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            memory_type TEXT,
            content TEXT,
            metadata TEXT,
            importance REAL,
            created_at INTEGER
        )
        """)
        conn.commit()
        conn.close()

    def store_memory(
        self, memory_type: str, content: str, metadata: Dict[str, Any] = None, importance: float = 0.5
    ) -> int:
        """Сохраняет новую память в базу данных."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        metadata_json = json.dumps(metadata or {})
        cursor.execute(
            """
            INSERT INTO memories (memory_type, content, metadata, importance, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (memory_type, content, metadata_json, importance, int(time.time())),
        )
        
        last_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return last_id

    def get_recent_memories(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Получает самые свежие воспоминания."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT id, memory_type, content, metadata, importance, created_at
            FROM memories
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )
        
        rows = cursor.fetchall()
        memories = []
        for row in rows:
            memory = dict(row)
            memories.append(memory)
        
        conn.close()
        return memories
        
    def search_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Поиск воспоминаний по содержимому."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            """
            SELECT id, memory_type, content, metadata, importance, created_at
            FROM memories
            WHERE content LIKE ?
            ORDER BY importance DESC
            LIMIT ?
            """,
            (f"%{query}%", limit),
        )
        
        rows = cursor.fetchall()
        memories = []
        for row in rows:
            memory = dict(row)
            memories.append(memory)
        
        conn.close()
        return memories

    def delete_old_memories(self, days: int = 30) -> int:
        """Удаляет старые воспоминания, которым больше указанного количества дней."""
        current_time = int(time.time())
        cutoff_time = current_time - (days * 24 * 60 * 60)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            """
            DELETE FROM memories
            WHERE created_at < ?
            """,
            (cutoff_time,),
        )
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        return deleted_count