"""
MIRAI Phase 6: Application Control System
==========================================

Модуль для управления приложениями на компьютере:
- CapCut (видео редактирование)
- VSCode (редактирование кода)
- File Explorer (управление файлами)
- System Apps (Notepad, Calculator, и т.д.)

Реализовано 150 шагов:
- Detection & Initialization (1-35)
- CapCut Video Editing (36-75)
- VSCode Code Editing (76-105)
- File Explorer & System Apps (106-135)
- Error Handling & Integration (136-150)

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

from .application_manager import ApplicationManager, get_application_manager
from .app_detector import AppDetector, detect_applications
from .app_launcher import AppLauncher, launch_application, close_application
from .vscode_controller import VSCodeController, get_vscode_controller
from .capcut_controller import CapCutController, get_capcut_controller
from .file_explorer_controller import FileExplorerController, get_file_explorer_controller
from .system_app_controller import SystemAppController, get_system_app_controller
from .app_error_handler import AppRecovery, detect_crash, recover_application
from .app_monitoring import AppMonitor, get_app_monitor
from .app_coordination import AppCoordinator, get_app_coordinator

__all__ = [
    # Core
    'ApplicationManager',
    'get_application_manager',
    
    # Detection & Launch
    'AppDetector',
    'detect_applications',
    'AppLauncher',
    'launch_application',
    'close_application',
    
    # Controllers
    'VSCodeController',
    'get_vscode_controller',
    'CapCutController',
    'get_capcut_controller',
    'FileExplorerController',
    'get_file_explorer_controller',
    'SystemAppController',
    'get_system_app_controller',
    
    # Error Handling
    'AppRecovery',
    'detect_crash',
    'recover_application',
    
    # Monitoring
    'AppMonitor',
    'get_app_monitor',
    
    # Coordination
    'AppCoordinator',
    'get_app_coordinator',
]

__version__ = '1.0.0'
