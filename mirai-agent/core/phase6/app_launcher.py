#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Phase 6: App Launcher - Запуск приложений                     ║
║  Application Launching & Control (Шаги 21-35)                        ║
╚══════════════════════════════════════════════════════════════════════╝

Шаги 21-35: Application Launching & Control
- Шаг 21: Launch Application
- Шаг 22: Wait for Application Ready
- Шаг 23: Handle Application Startup Errors
- ... до Шага 35

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

import logging
import time
import subprocess
import platform
import psutil
from typing import Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass

from .application_manager import get_application_manager

logger = logging.getLogger(__name__)


@dataclass
class LaunchResult:
    """Результат запуска приложения"""
    success: bool
    pid: Optional[int] = None
    error: Optional[str] = None
    ready: bool = False
    window_detected: bool = False


class AppLauncher:
    """
    Шаг 21: Launch Application
    
    Запустить приложение и управлять его жизненным циклом
    """
    
    def __init__(self):
        self.system = platform.system().lower()
        self.readiness_waiter = AppReadinessWaiter()
        self.error_handler = StartupErrorHandler()
    
    def launch(self, app_name: str, wait_ready: bool = True) -> LaunchResult:
        """
        Запустить приложение
        
        Args:
            app_name: Название приложения
            wait_ready: Ждать готовности приложения
            
        Returns:
            LaunchResult с результатом запуска
        """
        logger.info(f"🚀 Шаг 21: Запуск приложения {app_name}...")
        
        # Получаем информацию о приложении
        manager = get_application_manager()
        app_info = manager.get_application(app_name)
        
        if not app_info:
            error = f"Приложение {app_name} не найдено в реестре"
            logger.error(f"❌ {error}")
            return LaunchResult(success=False, error=error)
        
        if not app_info.path:
            error = f"Путь к приложению {app_name} не найден"
            logger.error(f"❌ {error}")
            return LaunchResult(success=False, error=error)
        
        # Проверяем уже запущено ли
        if app_info.is_running:
            logger.info(f"ℹ️ Приложение {app_name} уже запущено")
            return LaunchResult(success=True, ready=True)
        
        try:
            # Запускаем процесс
            logger.info(f"▶️ Запуск: {app_info.path}")
            
            if "windows" in self.system:
                # Windows: используем subprocess с CREATE_NEW_CONSOLE
                process = subprocess.Popen(
                    [str(app_info.path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, 'CREATE_NEW_CONSOLE') else 0
                )
            else:
                # Linux/Mac
                process = subprocess.Popen(
                    [str(app_info.path)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    start_new_session=True
                )
            
            pid = process.pid
            logger.info(f"✅ Процесс запущен, PID: {pid}")
            
            # Обновляем информацию в manager
            app_info.is_running = True
            app_info.pid = pid
            manager.register_application(app_info)
            
            result = LaunchResult(success=True, pid=pid)
            
            # Шаг 22: Wait for Application Ready
            if wait_ready:
                is_ready = self.readiness_waiter.wait_until_ready(app_name, pid)
                result.ready = is_ready
                
                if is_ready:
                    logger.info(f"✅ Приложение {app_name} готово к работе")
                else:
                    logger.warning(f"⚠️ Приложение {app_name} запущено, но может быть не полностью готово")
            
            return result
            
        except FileNotFoundError as e:
            # Шаг 23: Handle Application Startup Errors
            error = f"Исполняемый файл не найден: {e}"
            logger.error(f"❌ {error}")
            return self.error_handler.handle_error(app_name, error)
            
        except PermissionError as e:
            error = f"Нет прав для запуска: {e}"
            logger.error(f"❌ {error}")
            return self.error_handler.handle_error(app_name, error)
            
        except Exception as e:
            error = f"Ошибка запуска: {e}"
            logger.error(f"❌ {error}")
            return self.error_handler.handle_error(app_name, error)
    
    def close(self, app_name: str, force: bool = False) -> bool:
        """
        Шаг 34: Close Application
        
        Закрыть приложение gracefully или принудительно
        
        Args:
            app_name: Название приложения
            force: Принудительное закрытие
            
        Returns:
            bool: Успешно ли закрыто
        """
        logger.info(f"🛑 Шаг 34: Закрытие приложения {app_name}...")
        
        manager = get_application_manager()
        app_info = manager.get_application(app_name)
        
        if not app_info or not app_info.is_running or not app_info.pid:
            logger.warning(f"⚠️ Приложение {app_name} не запущено")
            return False
        
        try:
            process = psutil.Process(app_info.pid)
            
            if force:
                logger.info("⚡ Принудительное закрытие...")
                process.kill()
            else:
                logger.info("🔄 Graceful закрытие...")
                process.terminate()
                
                # Ждем завершения (до 5 секунд)
                try:
                    process.wait(timeout=5)
                except psutil.TimeoutExpired:
                    logger.warning("⚠️ Таймаут graceful закрытия, принудительное завершение")
                    process.kill()
            
            # Обновляем статус
            app_info.is_running = False
            app_info.pid = None
            manager.register_application(app_info)
            
            logger.info(f"✅ Приложение {app_name} закрыто")
            return True
            
        except psutil.NoSuchProcess:
            logger.info(f"ℹ️ Процесс {app_name} уже завершен")
            app_info.is_running = False
            app_info.pid = None
            manager.register_application(app_info)
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка закрытия приложения: {e}")
            return False


class AppReadinessWaiter:
    """
    Шаг 22: Wait for Application Ready
    
    Подождать пока приложение полностью загрузится и будет готово к работе
    """
    
    def wait_until_ready(
        self,
        app_name: str,
        pid: int,
        timeout: int = 10,
        check_interval: float = 0.5
    ) -> bool:
        """
        Ждать готовности приложения
        
        Args:
            app_name: Название приложения
            pid: PID процесса
            timeout: Максимальное время ожидания (секунды)
            check_interval: Интервал проверки (секунды)
            
        Returns:
            bool: Готово ли приложение
        """
        logger.info(f"⏳ Шаг 22: Ожидание готовности {app_name}...")
        
        start_time = time.time()
        
        while (time.time() - start_time) < timeout:
            try:
                process = psutil.Process(pid)
                
                # Проверяем что процесс жив
                if not process.is_running():
                    logger.error("❌ Процесс завершился преждевременно")
                    return False
                
                # Проверяем статус процесса
                status = process.status()
                
                # Если процесс sleeping или running - считаем готовым
                # (большинство GUI приложений в этом состоянии когда готовы)
                if status in [psutil.STATUS_SLEEPING, psutil.STATUS_RUNNING]:
                    # Даем еще немного времени для инициализации UI
                    time.sleep(1)
                    logger.info(f"✅ Приложение {app_name} готово (статус: {status})")
                    return True
                
            except psutil.NoSuchProcess:
                logger.error("❌ Процесс не найден")
                return False
            except Exception as e:
                logger.debug(f"Ошибка проверки готовности: {e}")
            
            time.sleep(check_interval)
        
        logger.warning(f"⚠️ Таймаут ожидания готовности {app_name}")
        return False


class StartupErrorHandler:
    """
    Шаг 23: Handle Application Startup Errors
    
    Обработка ошибок при запуске приложения
    """
    
    def handle_error(self, app_name: str, error_message: str) -> LaunchResult:
        """
        Обработать ошибку запуска
        
        Args:
            app_name: Название приложения
            error_message: Сообщение об ошибке
            
        Returns:
            LaunchResult с информацией об ошибке
        """
        logger.error(f"🚨 Шаг 23: Обработка ошибки запуска {app_name}")
        logger.error(f"   Ошибка: {error_message}")
        
        # Анализируем тип ошибки
        error_type = self._categorize_error(error_message)
        
        # Предлагаем решение
        suggestion = self._get_suggestion(error_type)
        logger.info(f"💡 Рекомендация: {suggestion}")
        
        return LaunchResult(
            success=False,
            error=f"{error_message} | Рекомендация: {suggestion}"
        )
    
    def _categorize_error(self, error_message: str) -> str:
        """Категоризировать тип ошибки"""
        error_lower = error_message.lower()
        
        if "not found" in error_lower or "не найден" in error_lower:
            return "file_not_found"
        elif "permission" in error_lower or "доступ" in error_lower:
            return "permission_denied"
        elif "dll" in error_lower or "library" in error_lower:
            return "missing_dependency"
        else:
            return "unknown"
    
    def _get_suggestion(self, error_type: str) -> str:
        """Получить рекомендацию по исправлению ошибки"""
        suggestions = {
            "file_not_found": "Проверьте что приложение установлено и путь правильный",
            "permission_denied": "Запустите от имени администратора или проверьте права",
            "missing_dependency": "Установите недостающие библиотеки или обновите приложение",
            "unknown": "Проверьте логи приложения для деталей"
        }
        return suggestions.get(error_type, "Обратитесь к документации приложения")


class LaunchCompleteValidator:
    """
    Шаг 35: Application Launch/Control Complete
    
    Проверка что запуск и контроль приложения выполнен успешно
    """
    
    def validate(self, app_name: str, launch_result: LaunchResult) -> bool:
        """
        Валидировать успешность запуска
        
        Args:
            app_name: Название приложения
            launch_result: Результат запуска
            
        Returns:
            bool: Валидация пройдена
        """
        logger.info(f"✓ Шаг 35: Валидация запуска {app_name}...")
        
        if not launch_result.success:
            logger.error("❌ Запуск не успешен")
            return False
        
        if not launch_result.ready:
            logger.warning("⚠️ Приложение запущено, но готовность не подтверждена")
            return False
        
        logger.info("✅ Валидация пройдена: приложение успешно запущено и готово")
        return True


# Convenience функции
def launch_application(app_name: str, wait_ready: bool = True) -> LaunchResult:
    """Запустить приложение (convenience function)"""
    launcher = AppLauncher()
    return launcher.launch(app_name, wait_ready)


def close_application(app_name: str, force: bool = False) -> bool:
    """Закрыть приложение (convenience function)"""
    launcher = AppLauncher()
    return launcher.close(app_name, force)
