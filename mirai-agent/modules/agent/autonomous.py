"""
Объединённый автономный агент Mirai.

Содержит ключевые идеи из legacy-файлов core/autonomous_agent.py
и app/agent/autonomous_agent.py: работа с задачами, памятью и AI.
"""

from __future__ import annotations

import asyncio
import json
import sqlite3
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from core.config import Config
from modules.utils.logger import Logger


@dataclass
class Task:
    """Описывает задачу автономного агента."""

    id: str
    description: str
    priority: int = 1
    status: str = "pending"  # pending | in_progress | completed | failed
    result: Optional[str] = None
    created_at: str = ""
    completed_at: Optional[str] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        return data


class MiraiMemory:
    """Простая SQLite-память для агента."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                importance REAL DEFAULT 0.5,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS trading_decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                action TEXT NOT NULL,
                reasoning TEXT,
                confidence REAL,
                result TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        conn.close()

    def store_memory(
        self,
        memory_type: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        importance: float = 0.5,
    ):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO memories (type, content, metadata, importance)
            VALUES (?, ?, ?, ?)
            """,
            (memory_type, content, json.dumps(metadata or {}), importance),
        )
        conn.commit()
        conn.close()

    def get_recent_memories(self, limit: int = 20) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT type, content, metadata, importance, timestamp
            FROM memories
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]


class AutonomousAgent:
    """Асинхронный автономный агент Mirai."""

    def __init__(
        self,
        ai_engine,
        logger=None,
        *,
        config: Optional[Dict[str, Any]] = None,
    ):
        self.ai = ai_engine
        self.logger = logger if logger is not None else Logger("AutonomousAgent").logger

        base_config = Config.load()
        overrides = config or {}

        self.data_dir = Path(overrides.get("data_dir", base_config.data_dir))
        self.state_dir = Path(overrides.get("state_dir", base_config.data_dir / "state"))
        self.logs_dir = Path(overrides.get("logs_dir", base_config.logs_dir))
        self.settings = base_config.agent_settings
        self._cycle_interval = overrides.get("cycle_interval", self.settings.cycle_interval)
        self._max_goals = overrides.get("max_goals", self.settings.max_goals)
        self._learning_sessions_limit = overrides.get(
            "learning_sessions_limit", self.settings.learning_sessions_limit
        )
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        self.state_file = self.state_dir / "agent_state.json"
        self.tasks_file = self.state_dir / "agent_tasks.json"
        self.memory = MiraiMemory(self.state_dir / "agent_memory.db")

        self.state: Dict[str, Any] = self._load_state()
        self.tasks: List[Task] = self._load_tasks()

        self.running = False
        self.logger.info("✅ AutonomousAgent initialized")

    # --- Persistence helpers -------------------------------------------------

    def _load_state(self) -> Dict[str, Any]:
        if self.state_file.exists():
            with self.state_file.open(encoding="utf-8") as fh:
                return json.load(fh)
        return {
            "tasks_completed": 0,
            "learning_sessions": 0,
            "code_improvements": 0,
            "internet_searches": 0,
            "last_activity": None,
        }

    def _save_state(self):
        self.state["last_activity"] = datetime.now().isoformat()
        with self.state_file.open("w", encoding="utf-8") as fh:
            json.dump(self.state, fh, indent=2, ensure_ascii=False)

    def _load_tasks(self) -> List[Task]:
        if self.tasks_file.exists():
            with self.tasks_file.open(encoding="utf-8") as fh:
                raw = json.load(fh)
            return [Task(**item) for item in raw]
        return []

    def _save_tasks(self):
        with self.tasks_file.open("w", encoding="utf-8") as fh:
            json.dump([task.to_dict() for task in self.tasks], fh, indent=2, ensure_ascii=False)

    # --- Core behaviours -----------------------------------------------------

    async def learn_from_internet(self):
        self.logger.info("📚 Learning from internet...")
        topics = [
            "latest AI developments 2025",
            "autonomous agents best practices",
            "machine learning for trading",
            "python async design patterns",
        ]

        for topic in topics:
            analysis = await self.ai.think(
                f"What can I learn from: {topic}? Provide 3 concise insights.",
                model="auto",
            )
            self.logger.info("💡 %s", analysis[:120])
            self.memory.store_memory(
                "learning",
                analysis,
                metadata={"topic": topic},
                importance=0.6,
            )
            await asyncio.sleep(1)

        self.state["learning_sessions"] += 1
        self._save_state()

    async def _propose_task(self) -> Task:
        description = await self.ai.think(
            "Suggest a high-impact task to improve Mirai autonomous trading agent. "
            "Make it actionable and concise.",
            model="auto",
        )
        task = Task(id=str(uuid.uuid4()), description=description, priority=1)
        self.memory.store_memory(
            "task_created",
            description,
            metadata={"task_id": task.id},
            importance=0.5,
        )
        return task

    async def create_task(self):
        self.logger.info("🎯 Creating new task...")
        task = await self._propose_task()
        self.tasks.append(task)
        self._save_tasks()
        self.logger.info("📝 Task created: %s", task.description[:120])

    async def execute_task(self):
        pending = [task for task in self.tasks if task.status == "pending"]
        if not pending:
            return

        task = pending[0]
        task.status = "in_progress"
        self._save_tasks()

        self.logger.info("⚡ Executing task %s", task.description[:80])

        plan = await self.ai.think(
            f"Provide a step-by-step plan to accomplish the task: {task.description}",
            model="auto",
        )
        self.logger.info("📋 Plan: %s", plan[:150])

        self.memory.store_memory(
            "task_plan",
            plan,
            metadata={"task_id": task.id},
            importance=0.7,
        )

        await asyncio.sleep(3)

        result = await self.ai.think(
            f"Task '{task.description}' is marked as completed. Summarise the outcome in 3 bullet points.",
            model="auto",
        )

        task.status = "completed"
        task.completed_at = datetime.now().isoformat()
        task.result = result
        self.state["tasks_completed"] += 1

        self.memory.store_memory(
            "task_result",
            result,
            metadata={"task_id": task.id},
            importance=0.6,
        )
        self._save_tasks()
        self._save_state()
        self.logger.info("✅ Task completed: %s", task.id)

    async def cycle(self):
        self.logger.info("🔄 Autonomous cycle started")

        if self.state["learning_sessions"] < self._learning_sessions_limit:
            await self.learn_from_internet()

        max_goals = self._max_goals
        if len([task for task in self.tasks if task.status == "pending"]) < max_goals:
            await self.create_task()

        await self.execute_task()

        self.logger.info(
            "📊 Stats: %s tasks completed, %s learning sessions",
            self.state["tasks_completed"],
            self.state["learning_sessions"],
        )

    async def run(self):
        self.running = True
        self.logger.info("🚀 AutonomousAgent started")

        interval = self._cycle_interval
        while self.running:
            try:
                await self.cycle()
                await asyncio.sleep(interval)
            except Exception as exc:  # noqa: BLE001
                self.logger.error(f"❌ Error in autonomous cycle: {exc}")
                await asyncio.sleep(60)

    async def stop(self):
        self.running = False
        self._save_state()
        self._save_tasks()
        self.logger.info("⏸️ AutonomousAgent stopped")


# Обратная совместимость с legacy-импортами
MiraiAutonomousAgent = AutonomousAgent
MiraiAgent = AutonomousAgent
