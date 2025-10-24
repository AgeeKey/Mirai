#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Phase 6: App Detector - Обнаружение приложений                ║
║  Application Discovery & Loading (Шаги 1-20)                         ║
╚══════════════════════════════════════════════════════════════════════╝

Шаги 1-20: Application Discovery & Loading
- Шаг 1: Detect Installed Applications
- Шаг 2: Identify Application Paths
- Шаг 3: Create Application Registry
- ... и так далее до Шага 20

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

import logging
import platform
import os
import psutil
import subprocess
from typing import Dict, List, Optional, Set
from pathlib import Path
from dataclasses import dataclass, field

from .application_manager import ApplicationInfo, get_application_manager

logger = logging.getLogger(__name__)


# Известные приложения и их возможные пути
KNOWN_APPLICATIONS = {
    "notepad": {
        "windows": ["C:\\Windows\\System32\\notepad.exe", "notepad.exe"],
        "category": "text_editor"
    },
    "vscode": {
        "windows": [
            "C:\\Program Files\\Microsoft VS Code\\Code.exe",
            "C:\\Program Files (x86)\\Microsoft VS Code\\Code.exe"
        ],
        "linux": ["/usr/bin/code", "/usr/local/bin/code"],
        "mac": ["/Applications/Visual Studio Code.app/Contents/MacOS/Electron"],
        "category": "code_editor"
    },
    "capcut": {
        "windows": [
            "C:\\Program Files\\CapCut\\CapCut.exe",
            os.path.expanduser("~\\AppData\\Local\\CapCut\\CapCut.exe")
        ],
        "category": "video_editor"
    },
    "explorer": {
        "windows": ["C:\\Windows\\explorer.exe"],
        "category": "file_manager"
    },
    "calculator": {
        "windows": ["calc.exe"],
        "category": "utility"
    },
    "cmd": {
        "windows": ["cmd.exe"],
        "category": "terminal"
    }
}


class InstalledAppsDetector:
    """
    Шаг 1: Detect Installed Applications
    
    Обнаружить какие приложения установлены на системе
    """
    
    def __init__(self):
        self.system = platform.system().lower()
        self.detected_apps: List[ApplicationInfo] = []
    
    def detect_all(self) -> List[ApplicationInfo]:
        """
        Обнаружить все установленные приложения
        
        Returns:
            Список ApplicationInfo для найденных приложений
        """
        logger.info("🔍 Шаг 1: Обнаружение установленных приложений...")
        
        self.detected_apps = []
        
        # Проверяем каждое известное приложение
        for app_name, app_config in KNOWN_APPLICATIONS.items():
            if self._detect_application(app_name, app_config):
                logger.info(f"✅ Найдено приложение: {app_name}")
        
        logger.info(f"📊 Обнаружено приложений: {len(self.detected_apps)}")
        return self.detected_apps
    
    def _detect_application(self, app_name: str, app_config: Dict) -> bool:
        """Обнаружить конкретное приложение"""
        # Получаем пути для текущей ОС
        os_key = "windows" if "windows" in self.system else self.system
        paths = app_config.get(os_key, [])
        
        if not paths:
            return False
        
        # Проверяем каждый возможный путь
        path_locator = AppPathLocator()
        found_path = path_locator.find_path(app_name, paths)
        
        if found_path:
            app_info = ApplicationInfo(
                name=app_name,
                path=found_path,
                category=app_config.get("category", "unknown")
            )
            self.detected_apps.append(app_info)
            
            # Регистрируем в Application Manager
            manager = get_application_manager()
            manager.register_application(app_info)
            
            return True
        
        return False


class AppPathLocator:
    """
    Шаг 2: Identify Application Paths
    
    Найти пути к исполняемым файлам приложений
    """
    
    def find_path(self, app_name: str, possible_paths: List[str]) -> Optional[Path]:
        """
        Найти путь к приложению
        
        Args:
            app_name: Название приложения
            possible_paths: Список возможных путей
            
        Returns:
            Path к приложению или None
        """
        logger.debug(f"🔍 Шаг 2: Поиск пути для {app_name}...")
        
        for path_str in possible_paths:
            # Расширяем переменные окружения
            expanded_path = os.path.expandvars(os.path.expanduser(path_str))
            path = Path(expanded_path)
            
            # Проверяем существование файла
            if path.exists() and path.is_file():
                logger.debug(f"✅ Найден путь: {path}")
                return path
            
            # Проверяем в PATH
            if not path.is_absolute():
                which_path = self._find_in_path(path_str)
                if which_path:
                    logger.debug(f"✅ Найден в PATH: {which_path}")
                    return which_path
        
        logger.debug(f"❌ Путь не найден для {app_name}")
        return None
    
    def _find_in_path(self, executable: str) -> Optional[Path]:
        """Поиск исполняемого файла в PATH"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["where", executable],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            else:
                result = subprocess.run(
                    ["which", executable],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            
            if result.returncode == 0 and result.stdout.strip():
                return Path(result.stdout.strip().split('\n')[0])
        except Exception as e:
            logger.debug(f"Ошибка поиска в PATH: {e}")
        
        return None


class ApplicationRegistry:
    """
    Шаг 3: Create Application Registry
    
    Реестр всех известных приложений с их метаданными
    """
    
    def __init__(self):
        self.registry: Dict[str, Dict] = {}
        self._load_default_registry()
    
    def _load_default_registry(self):
        """Загрузить стандартный реестр приложений"""
        logger.info("📝 Шаг 3: Создание реестра приложений...")
        
        # Копируем известные приложения в реестр
        for app_name, app_config in KNOWN_APPLICATIONS.items():
            self.registry[app_name] = {
                "name": app_name,
                "category": app_config.get("category", "unknown"),
                "shortcuts": self._get_default_shortcuts(app_name),
                "metadata": {}
            }
        
        logger.info(f"✅ Реестр создан: {len(self.registry)} приложений")
    
    def _get_default_shortcuts(self, app_name: str) -> Dict[str, str]:
        """Получить стандартные горячие клавиши для приложения"""
        # Шаг 13: Load Application Shortcuts
        shortcuts = {
            "vscode": {
                "save": "Ctrl+S",
                "new_file": "Ctrl+N",
                "open": "Ctrl+O",
                "search": "Ctrl+F"
            },
            "notepad": {
                "save": "Ctrl+S",
                "new": "Ctrl+N",
                "open": "Ctrl+O"
            }
        }
        return shortcuts.get(app_name, {})
    
    def get_app_info(self, app_name: str) -> Optional[Dict]:
        """Получить информацию о приложении из реестра"""
        return self.registry.get(app_name)


class RunningAppsDetector:
    """
    Шаг 5: Detect Running Applications
    
    Обнаружить какие приложения уже запущены
    """
    
    def detect_running(self) -> List[Dict]:
        """
        Обнаружить запущенные приложения
        
        Returns:
            Список словарей с информацией о процессах
        """
        logger.info("🔍 Шаг 5: Обнаружение запущенных приложений...")
        
        running_apps = []
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    pinfo = proc.info
                    if pinfo['name']:
                        running_apps.append({
                            'pid': pinfo['pid'],
                            'name': pinfo['name'],
                            'exe': pinfo.get('exe', '')
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.error(f"❌ Ошибка обнаружения процессов: {e}")
        
        logger.info(f"📊 Найдено процессов: {len(running_apps)}")
        return running_apps
    
    def is_app_running(self, app_name: str) -> bool:
        """
        Проверить запущено ли приложение
        
        Args:
            app_name: Название приложения
            
        Returns:
            bool: Запущено ли приложение
        """
        running = self.detect_running()
        
        # Ищем по имени процесса
        for proc in running:
            if app_name.lower() in proc['name'].lower():
                return True
        
        return False


class AppDetector:
    """
    Главный класс для обнаружения приложений
    Координирует работу всех детекторов (Шаги 1-20)
    """
    
    def __init__(self):
        self.installed_detector = InstalledAppsDetector()
        self.path_locator = AppPathLocator()
        self.registry = ApplicationRegistry()
        self.running_detector = RunningAppsDetector()
        
        self.discovery_complete = False
    
    def discover_all(self) -> Dict[str, Any]:
        """
        Полное обнаружение всех приложений (Шаги 1-20)
        
        Returns:
            Словарь с результатами обнаружения
        """
        logger.info("🚀 Запуск полного обнаружения приложений...")
        
        # Шаг 1: Detect Installed Applications
        installed_apps = self.installed_detector.detect_all()
        
        # Шаг 5: Detect Running Applications
        running_apps = self.running_detector.detect_running()
        
        # Обновляем статус запущенных приложений
        manager = get_application_manager()
        for app_info in installed_apps:
            if self.running_detector.is_app_running(app_info.name):
                app_info.is_running = True
                manager.register_application(app_info)
        
        # Шаг 15/20: Discovery Complete
        self.discovery_complete = True
        manager.mark_initialized()
        
        results = {
            "installed_count": len(installed_apps),
            "running_count": len(running_apps),
            "discovery_complete": self.discovery_complete,
            "installed_apps": [app.name for app in installed_apps]
        }
        
        logger.info("✅ Обнаружение приложений завершено!")
        logger.info(f"📊 Результаты: {results}")
        
        return results


# Удобная функция для быстрого обнаружения
def detect_applications() -> Dict[str, Any]:
    """Обнаружить все приложения (convenience function)"""
    detector = AppDetector()
    return detector.discover_all()
