"""
Real-time Learning API
Управление асинхронными задачами обучения через API
"""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Optional, List
import logging

from core.nasa_level.orchestrator import NASALearningOrchestrator
from core.nasa_level.learning_pipeline import Priority

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Статусы задачи обучения"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class LearningTask:
    """Задача обучения"""
    task_id: str
    technology: str
    depth: str = "basic"
    priority: Priority = Priority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    progress: int = 0
    result: Optional[dict] = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Конвертация в словарь для JSON"""
        return {
            "task_id": self.task_id,
            "technology": self.technology,
            "depth": self.depth,
            "priority": self.priority.name,
            "status": self.status.value,
            "progress": self.progress,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class LearningTaskManager:
    """
    Менеджер задач обучения
    
    Управляет очередью задач, выполняет их асинхронно,
    предоставляет статус и результаты
    """

    def __init__(self, max_concurrent: int = 2):
        self.orchestrator = NASALearningOrchestrator()
        self.tasks: Dict[str, LearningTask] = {}
        self.queue: asyncio.Queue = asyncio.Queue()
        self.max_concurrent = max_concurrent
        self.workers: List[asyncio.Task] = []
        self.running = False
        self.callbacks: Dict[str, List] = {}  # task_id -> [callback functions]

        logger.info(f"🎯 LearningTaskManager initialized (max_concurrent={max_concurrent})")

    def add_task(
        self, 
        technology: str, 
        depth: str = "basic",
        priority: Priority = Priority.NORMAL
    ) -> str:
        """
        Добавить задачу в очередь
        
        Returns:
            task_id: Уникальный идентификатор задачи
        """
        task_id = str(uuid.uuid4())
        task = LearningTask(
            task_id=task_id,
            technology=technology,
            depth=depth,
            priority=priority,
        )
        
        self.tasks[task_id] = task
        
        # Добавляем в очередь с приоритетом
        priority_value = priority.value
        self.queue.put_nowait((priority_value, task_id))
        
        logger.info(f"📝 Task added: {task_id} - {technology} ({priority.name})")
        self._emit_event(task_id, "created", {
            "task_id": task_id,
            "technology": technology,
            "status": "pending"
        })
        
        return task_id

    def get_task(self, task_id: str) -> Optional[LearningTask]:
        """Получить задачу по ID"""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[LearningTask]:
        """Получить все задачи"""
        return list(self.tasks.values())

    def cancel_task(self, task_id: str) -> bool:
        """
        Отменить задачу
        
        Returns:
            True если задача была отменена, False если нет
        """
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            return False
        
        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.now()
        
        logger.info(f"❌ Task cancelled: {task_id}")
        self._emit_event(task_id, "cancelled", {"task_id": task_id})
        
        return True

    async def start(self):
        """Запустить воркеры для обработки очереди"""
        if self.running:
            logger.warning("⚠️  Task manager already running")
            return
        
        self.running = True
        logger.info(f"🚀 Starting {self.max_concurrent} workers...")
        
        for i in range(self.max_concurrent):
            worker = asyncio.create_task(self._worker(i))
            self.workers.append(worker)
        
        logger.info(f"✅ {len(self.workers)} workers started")

    async def stop(self):
        """Остановить воркеры"""
        if not self.running:
            return
        
        logger.info("🛑 Stopping workers...")
        self.running = False
        
        # Отменяем все воркеры
        for worker in self.workers:
            worker.cancel()
        
        # Ждём завершения
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()
        
        logger.info("✅ Workers stopped")

    async def _worker(self, worker_id: int):
        """
        Воркер для обработки задач из очереди
        
        Args:
            worker_id: ID воркера для логирования
        """
        logger.info(f"👷 Worker {worker_id} started")
        
        while self.running:
            try:
                # Ждём задачу из очереди (с таймаутом)
                try:
                    priority, task_id = await asyncio.wait_for(
                        self.queue.get(), 
                        timeout=1.0
                    )
                except asyncio.TimeoutError:
                    continue
                
                task = self.tasks.get(task_id)
                if not task:
                    logger.error(f"❌ Task {task_id} not found")
                    continue
                
                # Проверяем, не отменена ли задача
                if task.status == TaskStatus.CANCELLED:
                    logger.info(f"⏭️  Task {task_id} was cancelled, skipping")
                    continue
                
                # Выполняем задачу
                await self._execute_task(worker_id, task)
                
            except asyncio.CancelledError:
                logger.info(f"👷 Worker {worker_id} cancelled")
                break
            except Exception as e:
                logger.error(f"💥 Worker {worker_id} error: {e}", exc_info=True)

        logger.info(f"👷 Worker {worker_id} stopped")

    async def _execute_task(self, worker_id: int, task: LearningTask):
        """
        Выполнить задачу обучения
        
        Args:
            worker_id: ID воркера
            task: Задача для выполнения
        """
        logger.info(f"🎓 Worker {worker_id} executing: {task.task_id} - {task.technology}")
        
        # Обновляем статус
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        task.progress = 0
        
        self._emit_event(task.task_id, "started", {
            "task_id": task.task_id,
            "technology": task.technology,
            "worker_id": worker_id
        })
        
        try:
            # Выполняем обучение (синхронная функция, запускаем в executor)
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self.orchestrator.learn_technology,
                task.technology,
                task.depth,
                task.priority
            )
            
            # Симуляция прогресса (в реальности нужно интегрировать с learning engine)
            for progress in [25, 50, 75, 100]:
                task.progress = progress
                self._emit_event(task.task_id, "progress", {
                    "task_id": task.task_id,
                    "progress": progress,
                    "technology": task.technology
                })
                await asyncio.sleep(0.1)
            
            # Успешное завершение
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.progress = 100
            task.result = {
                "success": result.success,
                "proficiency": result.proficiency,
                "quality_grade": result.quality_grade,
                "execution_time": result.execution_time,
                "tests_passed": result.tests_passed,
                "tests_total": result.tests_total,
            }
            
            logger.info(f"✅ Task completed: {task.task_id} - {task.technology} "
                       f"(proficiency: {result.proficiency:.1f}%)")
            
            self._emit_event(task.task_id, "completed", {
                "task_id": task.task_id,
                "technology": task.technology,
                "result": task.result
            })
            
        except Exception as e:
            # Ошибка выполнения
            task.status = TaskStatus.FAILED
            task.completed_at = datetime.now()
            task.error = str(e)
            
            logger.error(f"❌ Task failed: {task.task_id} - {e}")
            
            self._emit_event(task.task_id, "error", {
                "task_id": task.task_id,
                "technology": task.technology,
                "error": str(e)
            })

    def register_callback(self, task_id: str, callback):
        """
        Зарегистрировать callback для событий задачи
        
        Args:
            task_id: ID задачи
            callback: Функция callback(event_type, data)
        """
        if task_id not in self.callbacks:
            self.callbacks[task_id] = []
        self.callbacks[task_id].append(callback)

    def _emit_event(self, task_id: str, event_type: str, data: dict):
        """
        Отправить событие для задачи
        
        Args:
            task_id: ID задачи
            event_type: Тип события
            data: Данные события
        """
        if task_id in self.callbacks:
            for callback in self.callbacks[task_id]:
                try:
                    callback(event_type, data)
                except Exception as e:
                    logger.error(f"💥 Callback error: {e}")

    def get_stats(self) -> dict:
        """Получить статистику задач"""
        total = len(self.tasks)
        pending = sum(1 for t in self.tasks.values() if t.status == TaskStatus.PENDING)
        running = sum(1 for t in self.tasks.values() if t.status == TaskStatus.RUNNING)
        completed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in self.tasks.values() if t.status == TaskStatus.FAILED)
        cancelled = sum(1 for t in self.tasks.values() if t.status == TaskStatus.CANCELLED)
        
        return {
            "total": total,
            "pending": pending,
            "running": running,
            "completed": completed,
            "failed": failed,
            "cancelled": cancelled,
            "queue_size": self.queue.qsize(),
            "workers": len(self.workers),
            "max_concurrent": self.max_concurrent,
        }


# Глобальный инстанс task manager
_task_manager: Optional[LearningTaskManager] = None


def get_task_manager() -> LearningTaskManager:
    """Получить глобальный task manager (singleton)"""
    global _task_manager
    if _task_manager is None:
        _task_manager = LearningTaskManager(max_concurrent=2)
    return _task_manager
