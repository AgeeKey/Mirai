"""
MIRAI Phase 6: Application Control System
==========================================

Модуль для управления приложениями на компьютере:
- CapCut (видео редактирование)
- VSCode (редактирование кода)
- File Explorer (управление файлами)
- System Apps (Notepad, Calculator, и т.д.)

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

from .application_manager import ApplicationManager
from .app_detector import AppDetector
from .app_launcher import AppLauncher

__all__ = [
    'ApplicationManager',
    'AppDetector',
    'AppLauncher',
]

__version__ = '1.0.0'
