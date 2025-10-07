"""
Минимальный API-сервер на FastAPI.
"""

import uuid

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.agent.autonomous import Task


class APIServer:
    """Обёртка вокруг FastAPI приложения."""

    def __init__(self, agent, trader, logger):
        self.agent = agent
        self.trader = trader
        self.logger = logger

        self.app = FastAPI(title="Mirai Agent API")
        self._setup_middleware()
        self._setup_routes()

        self.logger.info("✅ APIServer initialized")

    def _setup_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routes(self):
        @self.app.get("/")
        async def root():
            return {"status": "ok", "service": "Mirai Agent API"}

        @self.app.get("/health")
        async def health():
            return {
                "status": "healthy",
                "agent_running": getattr(self.agent, "running", False),
                "trader_running": getattr(self.trader, "running", False),
            }

        @self.app.get("/agent/stats")
        async def agent_stats():
            total_tasks = len(self.agent.tasks)
            pending = len([t for t in self.agent.tasks if t.status == "pending"])
            return {
                "tasks_completed": self.agent.state["tasks_completed"],
                "learning_sessions": self.agent.state["learning_sessions"],
                "tasks_total": total_tasks,
                "tasks_pending": pending,
            }

        @self.app.get("/trader/stats")
        async def trader_stats():
            return {
                "balance": self.trader.balance,
                "positions": len(self.trader.positions),
            }

        @self.app.get("/stats")
        async def combined_stats():
            """Aggregate stats similar to what documentation expects."""
            total_tasks = len(self.agent.tasks)
            pending = len([t for t in self.agent.tasks if t.status == "pending"])
            return {
                "status": "ok",
                "agent": {
                    "tasks_completed": self.agent.state["tasks_completed"],
                    "learning_sessions": self.agent.state["learning_sessions"],
                    "tasks_total": total_tasks,
                    "tasks_pending": pending,
                },
                "trading": {
                    "balance": self.trader.balance,
                    "positions": len(self.trader.positions),
                },
            }

        @self.app.get("/trading/status")
        async def trading_status():
            return {
                "mode": getattr(self.trader, "mode", "demo"),
                "balance": self.trader.balance,
                "positions": [str(p) for p in getattr(self.trader, "positions", [])],
                "positions_count": len(self.trader.positions),
            }

        @self.app.post("/ai/ask")
        async def ai_ask(question: str, model: str = "auto"):
            """Simple AI proxy endpoint (light wrapper)."""
            try:
                answer = await self.agent.ai.think(question, model=model)
                return {"question": question, "answer": answer, "model": model}
            except Exception as exc:  # noqa: BLE001
                return {"error": str(exc)}

        @self.app.post("/agent/task")
        async def create_task(description: str):
            task = Task(id=str(uuid.uuid4()), description=description)
            self.agent.tasks.append(task)
            self.agent._save_tasks()  # noqa: SLF001 - временная интеграция
            return {"status": "created", "task_id": task.id}

    async def run(self):
        self.logger.info("🚀 API Server starting on http://0.0.0.0:8000")

        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=8000,
            log_level="info",
        )
        server = uvicorn.Server(config)
        await server.serve()

    async def stop(self):
        self.logger.info("⏸️ API Server stopped")
