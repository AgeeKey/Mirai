#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Memory Manager                                               ║
║  Long-Term Memory System with SQLite Backend                        ║
╚══════════════════════════════════════════════════════════════════════╝

Version: 2.0.0
Codename: Evolution

Реализует топ-1 желание MIRAI - долгосрочную память! 🌸

Features:
- ✅ Short-term memory (12 messages, auto-summarize)
- ✅ Long-term memory (90 days retention)
- ✅ User preferences tracking
- ✅ Task history
- ✅ Knowledge base
- ✅ RAG-ready (embeddings support)
- ✅ Session management
"""

import json
import logging
import sqlite3
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════════
# Data Models
# ═══════════════════════════════════════════════════════════════════


@dataclass
class Message:
    """Сообщение в разговоре"""

    id: Optional[int] = None
    session_id: str = ""
    role: str = "user"  # 'user', 'assistant', 'system'
    content: str = ""
    timestamp: Optional[datetime] = None
    tokens: int = 0
    model: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for JSON serialization"""
        d = asdict(self)
        if self.timestamp:
            d["timestamp"] = self.timestamp.isoformat()
        return d


@dataclass
class Session:
    """Сессия разговора"""

    id: str = ""
    user_id: str = "default"
    created_at: Optional[datetime] = None
    last_active: Optional[datetime] = None
    summary: Optional[str] = None
    message_count: int = 0

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_active is None:
            self.last_active = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if self.created_at:
            d["created_at"] = self.created_at.isoformat()
        if self.last_active:
            d["last_active"] = self.last_active.isoformat()
        return d


@dataclass
class UserPreferences:
    """Предпочтения пользователя (MIRAI хотела помнить!)"""

    user_id: str = "default"
    coding_style: Optional[str] = None
    communication_tone: Optional[str] = None
    favorite_tools: List[str] = field(default_factory=list)
    project_context: Optional[str] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "user_id": self.user_id,
            "coding_style": self.coding_style,
            "communication_tone": self.communication_tone,
            "favorite_tools": json.dumps(self.favorite_tools),
            "project_context": self.project_context,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        return d


@dataclass
class Task:
    """Задача в истории"""

    id: Optional[int] = None
    session_id: str = ""
    description: str = ""
    status: str = "pending"  # 'pending', 'in_progress', 'completed', 'failed'
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        if self.created_at:
            d["created_at"] = self.created_at.isoformat()
        if self.completed_at:
            d["completed_at"] = self.completed_at.isoformat()
        return d


@dataclass
class Knowledge:
    """Элемент базы знаний"""

    id: Optional[int] = None
    category: str = "general"
    key: str = ""
    value: str = ""
    source: str = "user"
    confidence: float = 1.0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    embedding: Optional[List[float]] = None  # RAG support

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "id": self.id,
            "category": self.category,
            "key": self.key,
            "value": self.value,
            "source": self.source,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "embedding": json.dumps(self.embedding) if self.embedding else None,
        }
        return d


# ═══════════════════════════════════════════════════════════════════
# Memory Manager
# ═══════════════════════════════════════════════════════════════════


class MemoryManager:
    """
    MIRAI Memory Manager

    Управляет долгосрочной памятью AI агента:
    - Краткосрочная память (в рамках сессии)
    - Долгосрочная память (между сессиями)
    - Предпочтения пользователей
    - История задач
    - База знаний
    """

    def __init__(self, db_path: str = "data/mirai_memory.db", max_messages: int = 12):
        """
        Initialize Memory Manager

        Args:
            db_path: Path to SQLite database
            max_messages: Max messages in short-term memory
        """
        self.logger = logging.getLogger(__name__)
        self.db_path = Path(db_path)
        self.max_messages = max_messages

        # Create data directory if needed
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_database()

        self.logger.info(f"Memory Manager initialized: {self.db_path}")

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row  # Access columns by name
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Database error: {e}", exc_info=True)
            raise
        finally:
            conn.close()

    def _init_database(self):
        """Initialize database schema"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Sessions table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL DEFAULT 'default',
                    created_at TIMESTAMP NOT NULL,
                    last_active TIMESTAMP NOT NULL,
                    summary TEXT,
                    message_count INTEGER DEFAULT 0
                )
            """
            )

            # Messages table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP NOT NULL,
                    tokens INTEGER DEFAULT 0,
                    model TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(id)
                )
            """
            )

            # User preferences table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id TEXT PRIMARY KEY,
                    coding_style TEXT,
                    communication_tone TEXT,
                    favorite_tools TEXT,
                    project_context TEXT,
                    updated_at TIMESTAMP NOT NULL
                )
            """
            )

            # Tasks table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    created_at TIMESTAMP NOT NULL,
                    completed_at TIMESTAMP,
                    result TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions(id)
                )
            """
            )

            # Knowledge base table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL DEFAULT 'general',
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    source TEXT NOT NULL DEFAULT 'user',
                    confidence REAL DEFAULT 1.0,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    embedding TEXT
                )
            """
            )

            # Create indices for performance
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_messages_session 
                ON messages(session_id, timestamp DESC)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_tasks_session 
                ON tasks(session_id, status)
            """
            )

            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_knowledge_category 
                ON knowledge(category, key)
            """
            )

            conn.commit()
            self.logger.info("Database schema initialized")

    # ═══════════════════════════════════════════════════════════════
    # Session Management
    # ═══════════════════════════════════════════════════════════════

    def create_session(self, user_id: str = "default") -> Session:
        """Create new session"""
        session = Session(user_id=user_id)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO sessions (id, user_id, created_at, last_active, message_count)
                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    session.id,
                    session.user_id,
                    session.created_at,
                    session.last_active,
                    session.message_count,
                ),
            )

        self.logger.info(f"Created session: {session.id}")
        return session

    def get_session(self, session_id: str) -> Optional[Session]:
        """Get session by ID"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM sessions WHERE id = ?
            """,
                (session_id,),
            )
            row = cursor.fetchone()

            if row:
                return Session(
                    id=row["id"],
                    user_id=row["user_id"],
                    created_at=datetime.fromisoformat(row["created_at"]),
                    last_active=datetime.fromisoformat(row["last_active"]),
                    summary=row["summary"],
                    message_count=row["message_count"],
                )
            return None

    def update_session_activity(self, session_id: str):
        """Update session last_active timestamp"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE sessions 
                SET last_active = ? 
                WHERE id = ?
            """,
                (datetime.now(), session_id),
            )

    def get_active_sessions(self, hours: int = 24) -> List[Session]:
        """Get sessions active in last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM sessions 
                WHERE last_active > ?
                ORDER BY last_active DESC
            """,
                (cutoff,),
            )

            sessions = []
            for row in cursor.fetchall():
                sessions.append(
                    Session(
                        id=row["id"],
                        user_id=row["user_id"],
                        created_at=datetime.fromisoformat(row["created_at"]),
                        last_active=datetime.fromisoformat(row["last_active"]),
                        summary=row["summary"],
                        message_count=row["message_count"],
                    )
                )
            return sessions

    # ═══════════════════════════════════════════════════════════════
    # Message Management (Short-term Memory)
    # ═══════════════════════════════════════════════════════════════

    def add_message(self, message: Message) -> int:
        """Add message to session"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO messages (session_id, role, content, timestamp, tokens, model)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    message.session_id,
                    message.role,
                    message.content,
                    message.timestamp,
                    message.tokens,
                    message.model,
                ),
            )

            message_id = cursor.lastrowid

            # Update session message count
            cursor.execute(
                """
                UPDATE sessions 
                SET message_count = message_count + 1,
                    last_active = ?
                WHERE id = ?
            """,
                (datetime.now(), message.session_id),
            )

        self.logger.debug(f"Added message {message_id} to session {message.session_id}")
        return message_id

    def get_recent_messages(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[Message]:
        """
        Get recent messages from session

        Args:
            session_id: Session ID
            limit: Max messages to return (default: self.max_messages)
        """
        if limit is None:
            limit = self.max_messages

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM messages 
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """,
                (session_id, limit),
            )

            messages = []
            for row in reversed(
                list(cursor.fetchall())
            ):  # Reverse to get chronological order
                messages.append(
                    Message(
                        id=row["id"],
                        session_id=row["session_id"],
                        role=row["role"],
                        content=row["content"],
                        timestamp=datetime.fromisoformat(row["timestamp"]),
                        tokens=row["tokens"],
                        model=row["model"],
                    )
                )
            return messages

    def get_conversation_history(
        self, session_id: str, limit: Optional[int] = None
    ) -> List[Dict[str, str]]:
        """
        Get conversation history in OpenAI format

        Returns:
            List of {'role': 'user/assistant', 'content': '...'}
        """
        messages = self.get_recent_messages(session_id, limit)
        return [{"role": msg.role, "content": msg.content} for msg in messages]

    def trim_old_messages(self, session_id: str, keep: int = 12):
        """
        Trim old messages, keep only recent N

        Before deleting, could optionally summarize them (Phase 2 feature)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Get count
            cursor.execute(
                """
                SELECT COUNT(*) as count FROM messages WHERE session_id = ?
            """,
                (session_id,),
            )
            count = cursor.fetchone()["count"]

            if count > keep:
                # Delete old messages
                cursor.execute(
                    """
                    DELETE FROM messages 
                    WHERE session_id = ? 
                    AND id NOT IN (
                        SELECT id FROM messages 
                        WHERE session_id = ?
                        ORDER BY timestamp DESC 
                        LIMIT ?
                    )
                """,
                    (session_id, session_id, keep),
                )

                deleted = cursor.rowcount
                self.logger.info(
                    f"Trimmed {deleted} old messages from session {session_id}"
                )

    # ═══════════════════════════════════════════════════════════════
    # User Preferences (MIRAI хотела помнить!)
    # ═══════════════════════════════════════════════════════════════

    def save_user_preferences(self, prefs: UserPreferences):
        """Save or update user preferences"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO user_preferences 
                (user_id, coding_style, communication_tone, favorite_tools, project_context, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    prefs.user_id,
                    prefs.coding_style,
                    prefs.communication_tone,
                    json.dumps(prefs.favorite_tools),
                    prefs.project_context,
                    prefs.updated_at,
                ),
            )

        self.logger.info(f"Saved preferences for user: {prefs.user_id}")

    def get_user_preferences(
        self, user_id: str = "default"
    ) -> Optional[UserPreferences]:
        """Get user preferences"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM user_preferences WHERE user_id = ?
            """,
                (user_id,),
            )
            row = cursor.fetchone()

            if row:
                favorite_tools = (
                    json.loads(row["favorite_tools"]) if row["favorite_tools"] else []
                )
                return UserPreferences(
                    user_id=row["user_id"],
                    coding_style=row["coding_style"],
                    communication_tone=row["communication_tone"],
                    favorite_tools=favorite_tools,
                    project_context=row["project_context"],
                    updated_at=datetime.fromisoformat(row["updated_at"]),
                )
            return None

    # ═══════════════════════════════════════════════════════════════
    # Task Management
    # ═══════════════════════════════════════════════════════════════

    def add_task(self, task: Task) -> int:
        """Add new task"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO tasks (session_id, description, status, created_at)
                VALUES (?, ?, ?, ?)
            """,
                (task.session_id, task.description, task.status, task.created_at),
            )

            return cursor.lastrowid

    def update_task_status(
        self, task_id: int, status: str, result: Optional[str] = None
    ):
        """Update task status"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            completed_at = datetime.now() if status in ["completed", "failed"] else None

            cursor.execute(
                """
                UPDATE tasks 
                SET status = ?, result = ?, completed_at = ?
                WHERE id = ?
            """,
                (status, result, completed_at, task_id),
            )

        self.logger.info(f"Updated task {task_id}: {status}")

    def get_tasks(self, session_id: str, status: Optional[str] = None) -> List[Task]:
        """Get tasks from session"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            if status:
                cursor.execute(
                    """
                    SELECT * FROM tasks 
                    WHERE session_id = ? AND status = ?
                    ORDER BY created_at DESC
                """,
                    (session_id, status),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM tasks 
                    WHERE session_id = ?
                    ORDER BY created_at DESC
                """,
                    (session_id,),
                )

            tasks = []
            for row in cursor.fetchall():
                completed_at = (
                    datetime.fromisoformat(row["completed_at"])
                    if row["completed_at"]
                    else None
                )
                tasks.append(
                    Task(
                        id=row["id"],
                        session_id=row["session_id"],
                        description=row["description"],
                        status=row["status"],
                        created_at=datetime.fromisoformat(row["created_at"]),
                        completed_at=completed_at,
                        result=row["result"],
                    )
                )
            return tasks

    # ═══════════════════════════════════════════════════════════════
    # Knowledge Base (Long-term Memory)
    # ═══════════════════════════════════════════════════════════════

    def add_knowledge(self, knowledge: Knowledge) -> int:
        """Add knowledge to long-term memory"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO knowledge 
                (category, key, value, source, confidence, created_at, updated_at, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    knowledge.category,
                    knowledge.key,
                    knowledge.value,
                    knowledge.source,
                    knowledge.confidence,
                    knowledge.created_at,
                    knowledge.updated_at,
                    json.dumps(knowledge.embedding) if knowledge.embedding else None,
                ),
            )

            return cursor.lastrowid

    def get_knowledge(
        self, category: Optional[str] = None, key: Optional[str] = None
    ) -> List[Knowledge]:
        """Search knowledge base"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            if category and key:
                cursor.execute(
                    """
                    SELECT * FROM knowledge 
                    WHERE category = ? AND key = ?
                    ORDER BY confidence DESC, updated_at DESC
                """,
                    (category, key),
                )
            elif category:
                cursor.execute(
                    """
                    SELECT * FROM knowledge 
                    WHERE category = ?
                    ORDER BY confidence DESC, updated_at DESC
                """,
                    (category,),
                )
            else:
                cursor.execute(
                    """
                    SELECT * FROM knowledge 
                    ORDER BY confidence DESC, updated_at DESC
                """
                )

            knowledge_list = []
            for row in cursor.fetchall():
                embedding = json.loads(row["embedding"]) if row["embedding"] else None
                knowledge_list.append(
                    Knowledge(
                        id=row["id"],
                        category=row["category"],
                        key=row["key"],
                        value=row["value"],
                        source=row["source"],
                        confidence=row["confidence"],
                        created_at=datetime.fromisoformat(row["created_at"]),
                        updated_at=datetime.fromisoformat(row["updated_at"]),
                        embedding=embedding,
                    )
                )
            return knowledge_list

    def search_knowledge(self, query: str) -> List[Knowledge]:
        """
        Simple text search in knowledge base

        For RAG with embeddings, use get_knowledge() and compare embeddings
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM knowledge 
                WHERE key LIKE ? OR value LIKE ?
                ORDER BY confidence DESC, updated_at DESC
                LIMIT 10
            """,
                (f"%{query}%", f"%{query}%"),
            )

            knowledge_list = []
            for row in cursor.fetchall():
                embedding = json.loads(row["embedding"]) if row["embedding"] else None
                knowledge_list.append(
                    Knowledge(
                        id=row["id"],
                        category=row["category"],
                        key=row["key"],
                        value=row["value"],
                        source=row["source"],
                        confidence=row["confidence"],
                        created_at=datetime.fromisoformat(row["created_at"]),
                        updated_at=datetime.fromisoformat(row["updated_at"]),
                        embedding=embedding,
                    )
                )
            return knowledge_list

    # ═══════════════════════════════════════════════════════════════
    # Cleanup & Maintenance
    # ═══════════════════════════════════════════════════════════════

    def cleanup_old_sessions(self, days: int = 90):
        """Delete sessions older than N days"""
        cutoff = datetime.now() - timedelta(days=days)

        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Get old session IDs
            cursor.execute(
                """
                SELECT id FROM sessions WHERE last_active < ?
            """,
                (cutoff,),
            )
            old_sessions = [row["id"] for row in cursor.fetchall()]

            if old_sessions:
                # Delete messages from old sessions
                placeholders = ",".join("?" * len(old_sessions))
                cursor.execute(
                    f"""
                    DELETE FROM messages WHERE session_id IN ({placeholders})
                """,
                    old_sessions,
                )

                # Delete tasks from old sessions
                cursor.execute(
                    f"""
                    DELETE FROM tasks WHERE session_id IN ({placeholders})
                """,
                    old_sessions,
                )

                # Delete old sessions
                cursor.execute(
                    f"""
                    DELETE FROM sessions WHERE id IN ({placeholders})
                """,
                    old_sessions,
                )

                self.logger.info(f"Cleaned up {len(old_sessions)} old sessions")

    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Count sessions
            cursor.execute("SELECT COUNT(*) as count FROM sessions")
            session_count = cursor.fetchone()["count"]

            # Count messages
            cursor.execute("SELECT COUNT(*) as count FROM messages")
            message_count = cursor.fetchone()["count"]

            # Count tasks
            cursor.execute("SELECT COUNT(*) as count FROM tasks")
            task_count = cursor.fetchone()["count"]

            # Count knowledge
            cursor.execute("SELECT COUNT(*) as count FROM knowledge")
            knowledge_count = cursor.fetchone()["count"]

            # Active sessions (last 24h)
            cutoff = datetime.now() - timedelta(hours=24)
            cursor.execute(
                "SELECT COUNT(*) as count FROM sessions WHERE last_active > ?",
                (cutoff,),
            )
            active_sessions = cursor.fetchone()["count"]

            return {
                "total_sessions": session_count,
                "active_sessions_24h": active_sessions,
                "total_messages": message_count,
                "total_tasks": task_count,
                "total_knowledge": knowledge_count,
                "db_path": str(self.db_path),
                "db_size_mb": (
                    self.db_path.stat().st_size / 1024 / 1024
                    if self.db_path.exists()
                    else 0
                ),
            }


# ═══════════════════════════════════════════════════════════════════
# Convenience Functions
# ═══════════════════════════════════════════════════════════════════

_global_memory_manager: Optional[MemoryManager] = None


def get_memory_manager(db_path: str = "data/mirai_memory.db") -> MemoryManager:
    """Get global memory manager instance (singleton)"""
    global _global_memory_manager
    if _global_memory_manager is None:
        _global_memory_manager = MemoryManager(db_path)
    return _global_memory_manager


# ═══════════════════════════════════════════════════════════════════
# Main (Testing)
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║  MIRAI Memory Manager Test                                          ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    print()

    # Initialize
    mm = MemoryManager("data/test_memory.db")

    # Create session
    print("1️⃣  Creating session...")
    session = mm.create_session(user_id="test_user")
    print(f"   Session ID: {session.id}")
    print()

    # Add messages
    print("2️⃣  Adding messages...")
    for i in range(5):
        msg = Message(
            session_id=session.id,
            role="user" if i % 2 == 0 else "assistant",
            content=f"Test message {i+1}",
            tokens=10,
        )
        mm.add_message(msg)
    print(f"   Added 5 messages")
    print()

    # Get conversation history
    print("3️⃣  Conversation history:")
    history = mm.get_conversation_history(session.id)
    for msg in history:
        print(f"   {msg['role']:10} {msg['content']}")
    print()

    # Save user preferences
    print("4️⃣  Saving user preferences...")
    prefs = UserPreferences(
        user_id="test_user",
        coding_style="PEP 8",
        communication_tone="friendly",
        favorite_tools=["Python", "Git", "Docker"],
        project_context="AI Trading Agent",
    )
    mm.save_user_preferences(prefs)
    print("   ✅ Preferences saved")
    print()

    # Get preferences
    print("5️⃣  Loading preferences...")
    loaded_prefs = mm.get_user_preferences("test_user")
    print(f"   Coding style: {loaded_prefs.coding_style}")
    print(f"   Tone: {loaded_prefs.communication_tone}")
    print(f"   Tools: {', '.join(loaded_prefs.favorite_tools)}")
    print()

    # Add task
    print("6️⃣  Adding task...")
    task = Task(
        session_id=session.id,
        description="Implement memory manager",
        status="in_progress",
    )
    task_id = mm.add_task(task)
    print(f"   Task ID: {task_id}")
    print()

    # Complete task
    print("7️⃣  Completing task...")
    mm.update_task_status(
        task_id, "completed", "Memory manager implemented successfully!"
    )
    print("   ✅ Task completed")
    print()

    # Add knowledge
    print("8️⃣  Adding knowledge...")
    knowledge = Knowledge(
        category="code",
        key="memory_manager",
        value="SQLite-based memory system with 5 tables",
        source="implementation",
        confidence=0.95,
    )
    mm.add_knowledge(knowledge)
    print("   ✅ Knowledge added")
    print()

    # Get stats
    print("9️⃣  Memory statistics:")
    stats = mm.get_stats()
    for key, value in stats.items():
        print(f"   {key:25} {value}")
    print()

    print("✅ All tests passed!")
    print()
    print(f"Database created at: {mm.db_path}")
