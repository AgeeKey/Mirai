"""
Context Manager - Система памяти для умного AI агента
Помнит всё: что открыто, что делал, какие проблемы встречались
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
import json
from pathlib import Path


class ActionStatus(Enum):
    """Статус выполненного действия"""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    SKIPPED = "skipped"


@dataclass
class ActionRecord:
    """Запись о выполненном действии"""
    timestamp: datetime
    action_type: str  # "click", "type", "open_app", "analyze"
    description: str
    status: ActionStatus
    result: Optional[str] = None
    problems: List[str] = field(default_factory=list)
    screenshot_before: Optional[str] = None
    screenshot_after: Optional[str] = None


@dataclass
class ApplicationState:
    """Состояние конкретного приложения"""
    app_name: str
    window_title: str
    is_active: bool
    state_description: str  # Что сейчас видно в приложении
    detected_elements: List[Dict] = field(default_factory=list)
    last_interaction: Optional[datetime] = None


@dataclass
class BrowserState(ApplicationState):
    """Расширенное состояние для браузера"""
    current_url: Optional[str] = None
    profile_name: Optional[str] = None
    tabs_count: int = 0
    has_ads: bool = False
    has_popups: bool = False
    page_loaded: bool = True


class AgentContext:
    """
    ЦЕНТРАЛЬНАЯ СИСТЕМА ПАМЯТИ АГЕНТА.
    Помнит всё что происходило, понимает текущее состояние.
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.started_at = datetime.now()

        # История действий
        self.action_history: List[ActionRecord] = []

        # Текущие открытые приложения
        self.applications: Dict[str, ApplicationState] = {}

        # Специальный контекст для браузера
        self.browser: Optional[BrowserState] = None

        # Обнаруженные проблемы (для избежания повторения)
        self.known_problems: Dict[str, int] = {}  # {"проблема": количество_встреч}

        # Цели и планы
        self.current_goal: Optional[str] = None
        self.current_plan: List[str] = []
        self.completed_steps: List[str] = []

        # Метрики
        self.total_actions = 0
        self.successful_actions = 0
        self.failed_actions = 0

        # Путь для сохранения
        self.context_file = Path(f"data/context_{session_id}.json")
        self.context_file.parent.mkdir(exist_ok=True)

    def record_action(
        self,
        action_type: str,
        description: str,
        status: ActionStatus,
        result: Optional[str] = None,
        problems: Optional[List[str]] = None,
        screenshot_before: Optional[str] = None,
        screenshot_after: Optional[str] = None
    ):
        """Записать выполненное действие"""
        record = ActionRecord(
            timestamp=datetime.now(),
            action_type=action_type,
            description=description,
            status=status,
            result=result,
            problems=problems or [],
            screenshot_before=screenshot_before,
            screenshot_after=screenshot_after
        )

        self.action_history.append(record)
        self.total_actions += 1

        if status == ActionStatus.SUCCESS:
            self.successful_actions += 1
        elif status == ActionStatus.FAILED:
            self.failed_actions += 1

        # Обновляем известные проблемы
        for problem in (problems or []):
            self.known_problems[problem] = self.known_problems.get(problem, 0) + 1

    def update_application_state(
        self,
        app_name: str,
        window_title: str,
        is_active: bool,
        state_description: str,
        detected_elements: Optional[List[Dict]] = None
    ):
        """Обновить состояние приложения"""
        state = ApplicationState(
            app_name=app_name,
            window_title=window_title,
            is_active=is_active,
            state_description=state_description,
            detected_elements=detected_elements or [],
            last_interaction=datetime.now() if is_active else None
        )

        self.applications[app_name] = state

    def update_browser_state(
        self,
        current_url: Optional[str] = None,
        profile_name: Optional[str] = None,
        tabs_count: int = 0,
        has_ads: bool = False,
        has_popups: bool = False,
        page_loaded: bool = True,
        state_description: str = "",
        window_title: str = "Chrome"
    ):
        """Обновить состояние браузера"""
        self.browser = BrowserState(
            app_name="chrome",
            window_title=window_title,
            is_active=True,
            state_description=state_description,
            current_url=current_url,
            profile_name=profile_name,
            tabs_count=tabs_count,
            has_ads=has_ads,
            has_popups=has_popups,
            page_loaded=page_loaded,
            last_interaction=datetime.now()
        )

        # Также добавляем в общий список приложений
        self.applications["chrome"] = self.browser

    def set_goal(self, goal: str, plan: List[str]):
        """Установить текущую цель и план"""
        self.current_goal = goal
        self.current_plan = plan
        self.completed_steps = []

    def complete_step(self, step: str):
        """Отметить шаг как выполненный"""
        if step in self.current_plan:
            self.completed_steps.append(step)

    def get_recent_actions(self, count: int = 10) -> List[ActionRecord]:
        """Получить последние N действий"""
        return self.action_history[-count:]

    def get_problem_frequency(self, problem: str) -> int:
        """Сколько раз встречалась эта проблема"""
        return self.known_problems.get(problem, 0)

    def is_problem_known(self, problem: str, threshold: int = 3) -> bool:
        """Известна ли эта проблема? (встречалась >= threshold раз)"""
        return self.get_problem_frequency(problem) >= threshold

    def get_active_application(self) -> Optional[ApplicationState]:
        """Получить активное приложение"""
        for app in self.applications.values():
            if app.is_active:
                return app
        return None

    def get_context_summary(self) -> Dict:
        """Получить краткую сводку контекста для AI"""
        active_app = self.get_active_application()

        return {
            "session_id": self.session_id,
            "current_goal": self.current_goal,
            "progress": f"{len(self.completed_steps)}/{len(self.current_plan)} шагов",
            "active_application": {
                "name": active_app.app_name if active_app else None,
                "state": active_app.state_description if active_app else None
            } if active_app else None,
            "browser": {
                "url": self.browser.current_url if self.browser else None,
                "profile": self.browser.profile_name if self.browser else None,
                "has_problems": (self.browser.has_ads or self.browser.has_popups) if self.browser else False
            } if self.browser else None,
            "recent_actions": len(self.get_recent_actions(5)),
            "success_rate": f"{(self.successful_actions / self.total_actions * 100):.1f}%" if self.total_actions > 0 else "0%",
            "known_problems": list(self.known_problems.keys())[:5]
        }

    def save_to_file(self):
        """Сохранить контекст в файл"""
        data = {
            "session_id": self.session_id,
            "started_at": self.started_at.isoformat(),
            "current_goal": self.current_goal,
            "current_plan": self.current_plan,
            "completed_steps": self.completed_steps,
            "total_actions": self.total_actions,
            "successful_actions": self.successful_actions,
            "failed_actions": self.failed_actions,
            "known_problems": self.known_problems,
            "action_history": [
                {
                    "timestamp": record.timestamp.isoformat(),
                    "type": record.action_type,
                    "description": record.description,
                    "status": record.status.value,
                    "result": record.result,
                    "problems": record.problems
                }
                for record in self.action_history[-50:]  # Последние 50 действий
            ]
        }

        with open(self.context_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self) -> bool:
        """Загрузить контекст из файла"""
        if not self.context_file.exists():
            return False

        try:
            with open(self.context_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.current_goal = data.get("current_goal")
            self.current_plan = data.get("current_plan", [])
            self.completed_steps = data.get("completed_steps", [])
            self.known_problems = data.get("known_problems", {})

            return True

        except Exception as e:
            print(f"❌ Ошибка загрузки контекста: {e}")
            return False
