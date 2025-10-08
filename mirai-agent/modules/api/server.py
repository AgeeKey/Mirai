"""
Минимальный API-сервер на FastAPI.

Расширен для безопасной LLM-проверки, задач/памяти и простого UI.
"""

import os
import time
import uuid
from dataclasses import asdict
from typing import Any, Dict, Optional
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import uvicorn
from fastapi import Body, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from pydantic import BaseModel, Field

from modules.agent.autonomous import Task
from modules.api.web.ui import ui_router


# Standardized API response format
def api_response(data: Any = None, error: str = None, status: str = "success") -> dict:
    """Create standardized API response"""
    from datetime import timezone
    response = {
        "status": status if not error else "error",
        "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
    }
    if data is not None:
        response["data"] = data
    if error:
        response["error"] = error
    return response


# Simple rate limiter
class RateLimiter:
    """Simple in-memory rate limiter"""
    def __init__(self):
        self.requests = defaultdict(list)
    
    def is_allowed(self, key: str, max_requests: int = 60, window: int = 60) -> bool:
        """Check if request is allowed (max_requests per window seconds)"""
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(seconds=window)
        
        # Clean old requests
        self.requests[key] = [ts for ts in self.requests[key] if ts > cutoff]
        
        # Check limit
        if len(self.requests[key]) >= max_requests:
            return False
        
        self.requests[key].append(now)
        return True


class APIServer:
    """Обёртка вокруг FastAPI приложения."""

    def __init__(self, agent, trader, logger):
        self.agent = agent
        self.trader = trader
        self.logger = logger
        self.rate_limiter = RateLimiter()

        self.app = FastAPI(title="Mirai Agent API", version="1.0.0")
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
        
        # Rate limiting middleware
        @self.app.middleware("http")
        async def rate_limit_middleware(request: Request, call_next):
            # Skip rate limiting for static files
            if request.url.path.endswith(('.css', '.js', '.html', '/')):
                return await call_next(request)
            
            # Apply rate limiting to API endpoints
            client_ip = request.client.host if request.client else "unknown"
            if not self.rate_limiter.is_allowed(client_ip, max_requests=60, window=60):
                return JSONResponse(
                    status_code=429,
                    content=api_response(error="Rate limit exceeded. Try again later.", status="error")
                )
            
            return await call_next(request)

    def _setup_routes(self):
        # Mount simple HTML UI at root - DISABLED (uses auth)
        # self.app.include_router(ui_router)
        
        # Веб-интерфейс Mirai Dashboard (публичный)
        @self.app.get("/", response_class=HTMLResponse)
        async def web_dashboard():
            """Главная страница с веб-интерфейсом"""
            try:
                with open("/root/mirai/mirai-agent/web/index.html", "r") as f:
                    return f.read()
            except FileNotFoundError:
                return "<h1>🤖 Mirai Agent Running</h1><p>Web interface not found</p>"
        
        @self.app.get("/styles.css")
        async def get_styles_css():
            """CSS файл"""
            return FileResponse("/root/mirai/mirai-agent/web/styles.css")

        @self.app.get("/script.js")
        async def get_script_js():
            """JavaScript файл"""
            return FileResponse("/root/mirai/mirai-agent/web/script.js")
        
        # Legacy endpoints for compatibility
        @self.app.get("/style.css")
        async def get_css():
            """CSS файл (legacy)"""
            return FileResponse("/root/mirai/mirai-agent/web/styles.css")

        @self.app.get("/app.js")
        async def get_js():
            """JavaScript файл (legacy)"""
            return FileResponse("/root/mirai/mirai-agent/web/script.js")
        
        @self.app.get("/api")
        async def api_root():
            return api_response(data={"service": "Mirai Agent API", "version": "1.0.0"})

        @self.app.get("/health")
        async def health():
            try:
                # Add AI engine stats if available
                ai_stats = {}
                if hasattr(self.agent, 'ai') and hasattr(self.agent.ai, 'get_usage_stats'):
                    ai_stats = self.agent.ai.get_usage_stats()
                
                data = {
                    "status": "healthy",
                    "agent_running": getattr(self.agent, "running", False),
                    "trader_running": getattr(self.trader, "running", False),
                    "ai_usage": ai_stats,
                }
                return api_response(data=data)
            except Exception as e:
                return api_response(error=str(e), status="error")

        @self.app.get("/agent/stats")
        async def agent_stats():
            try:
                total_tasks = len(self.agent.tasks)
                pending = len([t for t in self.agent.tasks if t.status == "pending"])
                data = {
                    "tasks_completed": self.agent.state["tasks_completed"],
                    "learning_sessions": self.agent.state["learning_sessions"],
                    "tasks_total": total_tasks,
                    "tasks_pending": pending,
                }
                return api_response(data=data)
            except Exception as e:
                return api_response(error=str(e), status="error")

        @self.app.get("/trader/stats")
        async def trader_stats():
            try:
                data = {
                    "balance": self.trader.balance,
                    "positions": len(self.trader.positions),
                }
                return api_response(data=data)
            except Exception as e:
                return api_response(error=str(e), status="error")

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

        # ---------------- LLM ask endpoint (JSON body) ----------------
        class AskRequest(BaseModel):
            provider: Optional[str] = Field(None, description="openai | grok | auto")
            prompt: str
            system: Optional[str] = None
            temperature: Optional[float] = 0.7
            max_tokens: Optional[int] = 400

        @self.app.post("/ai/ask")
        async def ai_ask(payload: AskRequest = Body(...)):
            """Simple AI proxy endpoint.

            Accepts: {"provider":"openai|grok|auto", "prompt":"...", "system":"..."}
            Returns: {"answer": str, "provider": str, "latency_ms": int}
            """
            start = time.time()
            provider = (payload.provider or "auto").lower()
            model = "auto"
            if provider in ("openai", "gpt", "gpt-4"):
                model = "gpt-4"
                provider = "openai"
            elif provider in ("grok", "xai"):
                model = "grok"
                provider = "grok"

            composed_prompt = payload.prompt
            if payload.system:
                composed_prompt = f"[SYSTEM] {payload.system}\n\n{payload.prompt}"

            try:
                answer = await self.agent.ai.think(
                    composed_prompt,
                    model=model,
                    temperature=payload.temperature or 0.7,
                    max_tokens=payload.max_tokens or 400,
                )
                latency_ms = int((time.time() - start) * 1000)
                return {
                    "provider": provider,
                    "model": model,
                    "answer": answer,
                    "latency_ms": latency_ms,
                }
            except Exception as exc:  # noqa: BLE001
                raise HTTPException(status_code=502, detail=f"AI error: {exc}")

        # ---------------- Agent tasks endpoints ----------------
        class TaskCreateRequest(BaseModel):
            title: str
            priority: Optional[str | int] = Field("medium", description="high|medium|low or int")
            meta: Optional[Dict[str, Any]] = None

        @self.app.post("/agent/tasks")
        async def create_task(payload: TaskCreateRequest):
            pr_map = {"high": 3, "medium": 2, "low": 1}
            if isinstance(payload.priority, str):
                priority_val = pr_map.get(payload.priority.lower(), 2)
            else:
                priority_val = int(payload.priority or 2)

            task = Task(id=str(uuid.uuid4()), description=payload.title, priority=priority_val)
            self.agent.tasks.append(task)
            self.agent.memory.store_memory(
                "task_created",
                payload.title,
                metadata={"task_id": task.id, **(payload.meta or {})},
                importance=0.5,
            )
            self.agent._save_tasks()
            return {"status": "created", "task_id": task.id}

        @self.app.get("/agent/tasks")
        async def list_tasks():
            return [asdict(t) for t in self.agent.tasks]

        # Legacy compatibility endpoint
        @self.app.post("/agent/task")
        async def create_task_legacy(description: str):
            task = Task(id=str(uuid.uuid4()), description=description)
            self.agent.tasks.append(task)
            self.agent._save_tasks()
            return {"status": "created", "task_id": task.id}

        # ---------------- Agent memory endpoints ----------------
        class MemoryCreateRequest(BaseModel):
            type: str = Field(..., description="note|learning|task_plan|task_result|...")
            text: str
            importance: Optional[float] = 0.5
            metadata: Optional[Dict[str, Any]] = None

        @self.app.post("/agent/memory")
        async def memory_add(payload: MemoryCreateRequest):
            try:
                self.agent.memory.store_memory(
                    payload.type,
                    payload.text,
                    metadata=payload.metadata or {},
                    importance=float(payload.importance or 0.5),
                )
                return {"status": "stored"}
            except Exception as exc:  # noqa: BLE001
                raise HTTPException(status_code=500, detail=f"Memory error: {exc}")

        @self.app.get("/agent/memory")
        async def memory_list(limit: int = 5):
            try:
                items = self.agent.memory.get_recent_memories(limit=limit)
                return items
            except Exception as exc:  # noqa: BLE001
                raise HTTPException(status_code=500, detail=f"Memory error: {exc}")

        # ---------------- Trader decide (dry-run) ----------------
        class TraderDecideRequest(BaseModel):
            symbol: str = "BTCUSDT"
            budget: float = 25
            leverage: int = 1
            dry_run: bool = True

        @self.app.post("/trader/decide")
        async def trader_decide(payload: TraderDecideRequest):
            try:
                prompt = (
                    f"You are a cautious crypto trading assistant. Given symbol {payload.symbol}, "
                    f"budget ${payload.budget}, leverage x{payload.leverage}, recommend one action (LONG, SHORT, HOLD) "
                    f"with 1-2 sentences of reasoning. Return only the action word first, then a dash and reasoning."
                )
                llm_out = await self.agent.ai.think(prompt, model="auto")
                action = "hold"
                reason = llm_out or "no response"
                head = (llm_out or "").strip().lower()
                if head.startswith("long"):
                    action = "long"
                elif head.startswith("short"):
                    action = "short"
                elif head.startswith("hold"):
                    action = "hold"

                resp = {
                    "action": action,
                    "confidence": 0.66,
                    "symbol": payload.symbol,
                    "budget": payload.budget,
                    "leverage": payload.leverage,
                    "dry_run": True,
                    "reason": reason[:500],
                    "ts": int(time.time()),
                }

                self.agent.memory.store_memory(
                    "trading_decision",
                    f"{payload.symbol}: {action}",
                    metadata={"payload": payload.dict(), "reason": reason[:500]},
                    importance=0.6,
                )
                return resp
            except Exception as exc:  # noqa: BLE001
                raise HTTPException(status_code=502, detail=f"Decision error: {exc}")

        # ---------------- Simple Web UI helpers ----------------
        @self.app.get("/status")
        async def ui_status():
            return {
                "mode": os.getenv("DEFAULT_TRADING_MODE", "dry_run").replace("_", "-"),
                "agentPaused": False,
                "dayPnL": 0.0,
                "maxDayPnL": 0.0,
                "tradesToday": 0,
                "consecutiveLosses": 0,
                "openPositions": [],
                "errorsCount": 0,
            }

        class ModeReq(BaseModel):
            mode: str

        @self.app.post("/mode")
        async def change_mode(_: ModeReq):
            return {"success": True}

        @self.app.post("/pause")
        async def pause():
            return {"success": True}

        @self.app.post("/resume")
        async def resume():
            return {"success": True}

        class KillReq(BaseModel):
            symbol: str

        @self.app.post("/kill")
        async def kill_switch(_: KillReq):
            return {"success": True}

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
