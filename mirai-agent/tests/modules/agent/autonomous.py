"""Mock for autonomous agent."""

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class Task:
    """Структура задачи для автономного агента."""

    id: str
    description: str
    status: str = "pending"
    priority: int = 2  # 1: low, 2: medium, 3: high
    result: Optional[str] = None
    created_at: Optional[int] = None


class AutonomousAgent:
    """Mock автономного агента для тестирования."""

    def __init__(self):
        """Инициализация."""
        self.tasks = []
        self.state_file = Path("dummy_path/state.json")
        
    def _save_tasks(self):
        """Сохранение задач в JSON."""
        # В реальном коде это метод сохраняет задачи в файл
        pass