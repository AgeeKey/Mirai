#!/usr/bin/env python3
"""
🚀 ФАЗА 4: ACTION EXECUTION ENGINE
Полная реализация исполнительного движка для автоматизации действий

Этот модуль содержит все компоненты для выполнения действий как человек:
- Клики мышью
- Ввод с клавиатуры  
- Управление окнами
- Браузерная автоматизация
- Файловые операции
- Проверка результатов
- Восстановление после ошибок
"""

from .action_executor import ActionExecutor, Action, ActionType, ActionStatus
from .action_queue import ActionQueue
from .execution_context import ExecutionContextValidator
from .action_templates import ActionTemplateLoader
from .action_handlers import ActionHandlerRegistry
from .execution_monitor import ExecutionMonitor
from .error_handling import ErrorHandlingSystem
from .state_manager import ExecutionStateManager
from .checkpoint_manager import CheckpointManager
from .performance_tracker import PerformanceTracker
from .action_logger import ActionLogger
from .metrics_collector import MetricsCollector
from .rollback_system import RollbackSystem
from .safety_guards import SafetyGuards

# Mouse & Keyboard Actions
from .mouse_actions import (
    MouseClicker,
    MouseDragger,
    Scroller,
    MouseMovementHandler,
)
from .keyboard_actions import (
    KeyboardTyper,
    KeyboardShortcutExecutor,
    KeyPresser,
    PasteExecutor,
)

# Window & Application Actions
from .window_actions import (
    WindowFocuser,
    WindowMaximizer,
    WindowMinimizer,
    WindowResizer,
    WindowMover,
    WindowCloser,
)
from .application_actions import (
    ApplicationOpener,
    ApplicationWaiter,
    ApplicationCloser,
    WindowSwitcher,
)

# Verification & Error Recovery
from .verification import (
    ActionSuccessVerifier,
    StateChangeVerifier,
    ErrorDetector,
)
from .error_recovery import (
    ActionRetrier,
    CheckpointRollbacker,
    FallbackActionExecutor,
)

__all__ = [
    # Core
    'ActionExecutor',
    'Action',
    'ActionType',
    'ActionStatus',
    'ActionQueue',
    'ExecutionContextValidator',
    'ActionTemplateLoader',
    'ActionHandlerRegistry',
    'ExecutionMonitor',
    'ErrorHandlingSystem',
    'ExecutionStateManager',
    'CheckpointManager',
    'PerformanceTracker',
    'ActionLogger',
    'MetricsCollector',
    'RollbackSystem',
    'SafetyGuards',
    
    # Mouse & Keyboard
    'MouseClicker',
    'MouseDragger',
    'Scroller',
    'MouseMovementHandler',
    'KeyboardTyper',
    'KeyboardShortcutExecutor',
    'KeyPresser',
    'PasteExecutor',
    
    # Window & Application
    'WindowFocuser',
    'WindowMaximizer',
    'WindowMinimizer',
    'WindowResizer',
    'WindowMover',
    'WindowCloser',
    'ApplicationOpener',
    'ApplicationWaiter',
    'ApplicationCloser',
    'WindowSwitcher',
    
    # Verification & Recovery
    'ActionSuccessVerifier',
    'StateChangeVerifier',
    'ErrorDetector',
    'ActionRetrier',
    'CheckpointRollbacker',
    'FallbackActionExecutor',
]

__version__ = '1.0.0'
__author__ = 'MIRAI Team'
