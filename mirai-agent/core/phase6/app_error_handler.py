#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Phase 6: App Error Handler - Обработка ошибок приложений      ║
║  Error Handling & Recovery (Шаги 136-140)                            ║
╚══════════════════════════════════════════════════════════════════════╝

Шаги 136-140: Error Handling
- Обнаружение сбоев приложений
- Обработка зависаний
- Принудительное закрытие
- Восстановление после сбоев

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

import logging
import time
import psutil
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime

from .application_manager import get_application_manager

logger = logging.getLogger(__name__)


@dataclass
class CrashReport:
    """Отчет о сбое приложения"""
    app_name: str
    timestamp: datetime
    error_type: str
    error_message: str
    pid: Optional[int] = None
    recovery_attempted: bool = False
    recovery_successful: bool = False


class CrashDetector:
    """
    Шаг 136: Detect Application Crash
    
    Обнаружение сбоев приложений
    """
    
    def __init__(self):
        self.crash_reports: List[CrashReport] = []
    
    def detect_crash(self, app_name: str) -> Optional[CrashReport]:
        """
        Обнаружить сбой приложения
        
        Args:
            app_name: Название приложения
            
        Returns:
            CrashReport если обнаружен сбой, иначе None
        """
        logger.info(f"🔍 Шаг 136: Проверка сбоя для {app_name}...")
        
        manager = get_application_manager()
        app_info = manager.get_application(app_name)
        
        if not app_info:
            logger.warning(f"Приложение {app_name} не найдено в реестре")
            return None
        
        # Проверяем что приложение должно быть запущено
        if not app_info.is_running or not app_info.pid:
            logger.debug(f"Приложение {app_name} не запущено")
            return None
        
        try:
            # Проверяем существует ли процесс
            process = psutil.Process(app_info.pid)
            
            # Проверяем статус процесса
            status = process.status()
            
            # Проверяем на zombie процесс
            if status == psutil.STATUS_ZOMBIE:
                error_msg = f"Процесс {app_name} в состоянии zombie"
                logger.error(f"💀 {error_msg}")
                
                crash_report = CrashReport(
                    app_name=app_name,
                    timestamp=datetime.now(),
                    error_type="zombie_process",
                    error_message=error_msg,
                    pid=app_info.pid
                )
                
                self.crash_reports.append(crash_report)
                return crash_report
            
            logger.debug(f"✅ Приложение {app_name} работает нормально (статус: {status})")
            return None
            
        except psutil.NoSuchProcess:
            # Процесс завершился
            error_msg = f"Процесс {app_name} неожиданно завершился"
            logger.error(f"❌ {error_msg}")
            
            crash_report = CrashReport(
                app_name=app_name,
                timestamp=datetime.now(),
                error_type="process_terminated",
                error_message=error_msg,
                pid=app_info.pid
            )
            
            self.crash_reports.append(crash_report)
            
            # Обновляем статус в manager
            app_info.is_running = False
            app_info.pid = None
            manager.register_application(app_info)
            
            return crash_report
            
        except Exception as e:
            error_msg = f"Ошибка проверки процесса {app_name}: {e}"
            logger.error(f"❌ {error_msg}")
            
            crash_report = CrashReport(
                app_name=app_name,
                timestamp=datetime.now(),
                error_type="check_error",
                error_message=error_msg,
                pid=app_info.pid
            )
            
            self.crash_reports.append(crash_report)
            return crash_report


class CrashHandler:
    """
    Шаг 137: Handle Application Crash
    
    Обработка сбоев приложений
    """
    
    def __init__(self):
        self.detector = CrashDetector()
    
    def handle_crash(self, crash_report: CrashReport, auto_restart: bool = False) -> bool:
        """
        Обработать сбой приложения
        
        Args:
            crash_report: Отчет о сбое
            auto_restart: Автоматически перезапустить приложение
            
        Returns:
            bool: Успешно ли обработан сбой
        """
        logger.error(f"🚨 Шаг 137: Обработка сбоя {crash_report.app_name}")
        logger.error(f"   Тип: {crash_report.error_type}")
        logger.error(f"   Сообщение: {crash_report.error_message}")
        
        crash_report.recovery_attempted = True
        
        try:
            # Очищаем процесс если он zombie
            if crash_report.error_type == "zombie_process" and crash_report.pid:
                self._cleanup_zombie(crash_report.pid)
            
            # Перезапускаем если требуется
            if auto_restart:
                logger.info(f"🔄 Перезапуск {crash_report.app_name}...")
                
                from .app_launcher import launch_application
                result = launch_application(crash_report.app_name, wait_ready=True)
                
                crash_report.recovery_successful = result.success
                
                if result.success:
                    logger.info(f"✅ {crash_report.app_name} успешно перезапущен")
                else:
                    logger.error(f"❌ Не удалось перезапустить {crash_report.app_name}")
            
            return crash_report.recovery_successful
            
        except Exception as e:
            logger.error(f"❌ Ошибка обработки сбоя: {e}")
            crash_report.recovery_successful = False
            return False
    
    def _cleanup_zombie(self, pid: int) -> None:
        """Очистить zombie процесс"""
        try:
            process = psutil.Process(pid)
            process.kill()
            logger.info(f"✅ Zombie процесс {pid} очищен")
        except Exception as e:
            logger.error(f"❌ Ошибка очистки zombie: {e}")


class HangDetector:
    """
    Шаг 138: Application Hang Detection
    
    Обнаружение зависаний приложений
    """
    
    def detect_hang(self, app_name: str, timeout: int = 5) -> bool:
        """
        Обнаружить зависание приложения
        
        Args:
            app_name: Название приложения
            timeout: Таймаут проверки (секунды)
            
        Returns:
            bool: Зависло ли приложение
        """
        logger.info(f"🔍 Шаг 138: Проверка зависания {app_name}...")
        
        manager = get_application_manager()
        app_info = manager.get_application(app_name)
        
        if not app_info or not app_info.pid:
            logger.warning(f"Приложение {app_name} не запущено")
            return False
        
        try:
            process = psutil.Process(app_info.pid)
            
            # Проверяем CPU usage
            cpu_percent = process.cpu_percent(interval=timeout)
            
            # Проверяем статус
            status = process.status()
            
            # Приложение зависло если:
            # 1. Статус stopped или disk-sleep
            # 2. CPU использование 0% длительное время (для GUI приложений подозрительно)
            is_hung = (
                status in [psutil.STATUS_STOPPED, psutil.STATUS_DISK_SLEEP] or
                (status == psutil.STATUS_SLEEPING and cpu_percent == 0)
            )
            
            if is_hung:
                logger.warning(f"⚠️ Приложение {app_name} возможно зависло (статус: {status}, CPU: {cpu_percent}%)")
            else:
                logger.debug(f"✅ Приложение {app_name} работает (статус: {status}, CPU: {cpu_percent}%)")
            
            return is_hung
            
        except psutil.NoSuchProcess:
            logger.error(f"❌ Процесс {app_name} не найден")
            return False
        except Exception as e:
            logger.error(f"❌ Ошибка проверки зависания: {e}")
            return False


class ForceCloser:
    """
    Шаг 139: Force Close Application
    
    Принудительное закрытие приложения
    """
    
    def force_close(self, app_name: str) -> bool:
        """
        Принудительно закрыть приложение
        
        Args:
            app_name: Название приложения
            
        Returns:
            bool: Успешно ли закрыто
        """
        logger.warning(f"⚡ Шаг 139: Принудительное закрытие {app_name}...")
        
        manager = get_application_manager()
        app_info = manager.get_application(app_name)
        
        if not app_info or not app_info.pid:
            logger.warning(f"Приложение {app_name} не запущено")
            return False
        
        try:
            process = psutil.Process(app_info.pid)
            
            # Сначала пытаемся terminate
            logger.info("Попытка terminate...")
            process.terminate()
            
            # Ждем завершения
            try:
                process.wait(timeout=3)
                logger.info("✅ Приложение завершено через terminate")
            except psutil.TimeoutExpired:
                # Если не помогло - kill
                logger.warning("Terminate не помог, использую kill...")
                process.kill()
                logger.info("✅ Приложение убито через kill")
            
            # Обновляем статус
            app_info.is_running = False
            app_info.pid = None
            manager.register_application(app_info)
            
            return True
            
        except psutil.NoSuchProcess:
            logger.info(f"Процесс {app_name} уже завершен")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка принудительного закрытия: {e}")
            return False


class AppRecovery:
    """
    Шаг 140: Application Recovery
    
    Восстановление после сбоев
    """
    
    def __init__(self):
        self.crash_handler = CrashHandler()
        self.hang_detector = HangDetector()
        self.force_closer = ForceCloser()
    
    def recover_application(self, app_name: str, restart: bool = True) -> bool:
        """
        Восстановить приложение после сбоя
        
        Args:
            app_name: Название приложения
            restart: Перезапустить приложение
            
        Returns:
            bool: Успешно ли восстановлено
        """
        logger.info(f"🔧 Шаг 140: Восстановление {app_name}...")
        
        # Проверяем на сбой
        crash_report = self.crash_handler.detector.detect_crash(app_name)
        
        if crash_report:
            # Обрабатываем сбой
            return self.crash_handler.handle_crash(crash_report, auto_restart=restart)
        
        # Проверяем на зависание
        if self.hang_detector.detect_hang(app_name):
            # Принудительно закрываем
            self.force_closer.force_close(app_name)
            
            # Перезапускаем если нужно
            if restart:
                from .app_launcher import launch_application
                result = launch_application(app_name, wait_ready=True)
                return result.success
            
            return True
        
        logger.info(f"✅ Приложение {app_name} работает нормально, восстановление не требуется")
        return True


# Convenience функции
def detect_crash(app_name: str) -> Optional[CrashReport]:
    """Обнаружить сбой приложения"""
    detector = CrashDetector()
    return detector.detect_crash(app_name)


def recover_application(app_name: str, restart: bool = True) -> bool:
    """Восстановить приложение"""
    recovery = AppRecovery()
    return recovery.recover_application(app_name, restart)
