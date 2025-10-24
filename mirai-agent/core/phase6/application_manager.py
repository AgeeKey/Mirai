#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Phase 6: Application Manager - Главный модуль управления      ║
║  Orchestrates all application control operations                     ║
╚══════════════════════════════════════════════════════════════════════╝

Шаг 10: Initialize Application Manager
- Create главный Application Manager
- Orchestrate all app operations

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

import logging
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ApplicationInfo:
    """Информация о приложении"""
    name: str
    path: Optional[Path] = None
    version: Optional[str] = None
    category: str = "unknown"
    is_running: bool = False
    pid: Optional[int] = None
    windows: List[str] = field(default_factory=list)


class ApplicationManager:
    """
    ГЛАВНЫЙ МЕНЕДЖЕР ПРИЛОЖЕНИЙ (Шаг 10)
    
    Orchestrates all application control operations:
    - Обнаружение приложений
    - Запуск и управление
    - Координация между приложениями
    - Мониторинг и обработка ошибок
    """
    
    def __init__(self):
        """Инициализация Application Manager"""
        logger.info("🚀 Инициализация Application Manager...")
        
        # Реестр приложений
        self.applications: Dict[str, ApplicationInfo] = {}
        
        # Активное приложение
        self.active_app: Optional[str] = None
        
        # Handlers для специализированных контроллеров
        self.handlers: Dict[str, Any] = {}
        
        # Статус инициализации
        self.initialized = False
        
        logger.info("✅ Application Manager инициализирован")
    
    def register_application(self, app_info: ApplicationInfo) -> bool:
        """
        Зарегистрировать приложение в системе
        
        Args:
            app_info: Информация о приложении
            
        Returns:
            bool: Успешно ли зарегистрировано
        """
        try:
            self.applications[app_info.name] = app_info
            logger.info(f"📝 Зарегистрировано приложение: {app_info.name}")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка регистрации приложения {app_info.name}: {e}")
            return False
    
    def get_application(self, name: str) -> Optional[ApplicationInfo]:
        """
        Получить информацию о приложении
        
        Args:
            name: Название приложения
            
        Returns:
            ApplicationInfo или None
        """
        return self.applications.get(name)
    
    def list_applications(self, category: Optional[str] = None) -> List[ApplicationInfo]:
        """
        Получить список приложений
        
        Args:
            category: Фильтр по категории (optional)
            
        Returns:
            Список ApplicationInfo
        """
        apps = list(self.applications.values())
        
        if category:
            apps = [app for app in apps if app.category == category]
        
        return apps
    
    def set_active_application(self, name: str) -> bool:
        """
        Установить активное приложение
        
        Args:
            name: Название приложения
            
        Returns:
            bool: Успешно ли установлено
        """
        if name in self.applications:
            self.active_app = name
            logger.info(f"🎯 Активное приложение: {name}")
            return True
        else:
            logger.warning(f"⚠️ Приложение {name} не найдено")
            return False
    
    def get_active_application(self) -> Optional[ApplicationInfo]:
        """Получить активное приложение"""
        if self.active_app:
            return self.applications.get(self.active_app)
        return None
    
    def register_handler(self, app_type: str, handler: Any) -> None:
        """
        Зарегистрировать handler для типа приложения
        
        Args:
            app_type: Тип приложения (capcut, vscode, explorer, etc.)
            handler: Handler объект
        """
        self.handlers[app_type] = handler
        logger.info(f"🔧 Зарегистрирован handler для: {app_type}")
    
    def get_handler(self, app_type: str) -> Optional[Any]:
        """Получить handler для типа приложения"""
        return self.handlers.get(app_type)
    
    def mark_initialized(self) -> None:
        """Отметить систему как инициализированную"""
        self.initialized = True
        logger.info("✅ Application Manager полностью инициализирован")
    
    def is_initialized(self) -> bool:
        """Проверить инициализацию системы"""
        return self.initialized
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Получить статистику по приложениям
        
        Returns:
            Словарь со статистикой
        """
        total_apps = len(self.applications)
        running_apps = sum(1 for app in self.applications.values() if app.is_running)
        
        categories = {}
        for app in self.applications.values():
            categories[app.category] = categories.get(app.category, 0) + 1
        
        return {
            "total_applications": total_apps,
            "running_applications": running_apps,
            "categories": categories,
            "active_application": self.active_app,
            "initialized": self.initialized,
            "handlers_registered": len(self.handlers)
        }


# Convenience функции для быстрого доступа
_manager_instance: Optional[ApplicationManager] = None


def get_application_manager() -> ApplicationManager:
    """Получить глобальный экземпляр Application Manager (singleton)"""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = ApplicationManager()
    return _manager_instance
