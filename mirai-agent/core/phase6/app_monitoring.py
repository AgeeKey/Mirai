#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Phase 6: App Monitoring - Мониторинг приложений                ║
║  Monitoring & Metrics (Шаги 143, 145-146)                            ║
╚══════════════════════════════════════════════════════════════════════╝

Шаги 143, 145-146: Monitoring
- Мониторинг ресурсов приложений
- Логирование событий
- Сбор метрик производительности

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

import logging
import time
import psutil
import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

from .application_manager import get_application_manager

logger = logging.getLogger(__name__)


@dataclass
class ResourceMetrics:
    """Метрики использования ресурсов"""
    timestamp: datetime
    app_name: str
    pid: int
    cpu_percent: float
    memory_mb: float
    memory_percent: float
    num_threads: int
    num_handles: int = 0


@dataclass
class ApplicationEvent:
    """Событие приложения"""
    timestamp: datetime
    app_name: str
    event_type: str  # launched, closed, crash, error, action
    event_data: Dict[str, Any]
    success: bool = True


@dataclass
class PerformanceMetrics:
    """Метрики производительности операций"""
    operation: str
    app_name: str
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    success: bool
    error_message: Optional[str] = None


class ResourceMonitor:
    """
    Шаг 143: Application Resource Monitoring
    
    Мониторинг использования ресурсов приложениями
    """
    
    def __init__(self, sampling_interval: float = 1.0):
        self.sampling_interval = sampling_interval
        self.metrics_history: List[ResourceMetrics] = []
    
    def monitor_app(self, app_name: str) -> Optional[ResourceMetrics]:
        """
        Мониторить ресурсы приложения
        
        Args:
            app_name: Название приложения
            
        Returns:
            ResourceMetrics или None если приложение не запущено
        """
        logger.debug(f"📊 Шаг 143: Мониторинг ресурсов {app_name}...")
        
        manager = get_application_manager()
        app_info = manager.get_application(app_name)
        
        if not app_info or not app_info.is_running or not app_info.pid:
            logger.debug(f"Приложение {app_name} не запущено")
            return None
        
        try:
            process = psutil.Process(app_info.pid)
            
            # Собираем метрики
            with process.oneshot():
                cpu_percent = process.cpu_percent(interval=self.sampling_interval)
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / (1024 * 1024)  # В мегабайтах
                memory_percent = process.memory_percent()
                num_threads = process.num_threads()
                
                # Windows-specific
                try:
                    num_handles = process.num_handles()
                except AttributeError:
                    num_handles = 0
            
            metrics = ResourceMetrics(
                timestamp=datetime.now(),
                app_name=app_name,
                pid=app_info.pid,
                cpu_percent=cpu_percent,
                memory_mb=memory_mb,
                memory_percent=memory_percent,
                num_threads=num_threads,
                num_handles=num_handles
            )
            
            # Сохраняем в историю
            self.metrics_history.append(metrics)
            
            # Ограничиваем размер истории (последние 1000 записей)
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]
            
            logger.debug(f"✅ CPU: {cpu_percent}%, Memory: {memory_mb:.1f}MB ({memory_percent:.1f}%)")
            
            return metrics
            
        except psutil.NoSuchProcess:
            logger.warning(f"Процесс {app_name} не найден")
            return None
        except Exception as e:
            logger.error(f"❌ Ошибка мониторинга: {e}")
            return None
    
    def get_average_metrics(self, app_name: str, last_n: int = 10) -> Optional[Dict[str, float]]:
        """
        Получить средние метрики за последние N измерений
        
        Args:
            app_name: Название приложения
            last_n: Количество последних измерений
            
        Returns:
            Словарь со средними значениями
        """
        app_metrics = [m for m in self.metrics_history if m.app_name == app_name]
        
        if not app_metrics:
            return None
        
        recent = app_metrics[-last_n:]
        
        avg = {
            'avg_cpu_percent': sum(m.cpu_percent for m in recent) / len(recent),
            'avg_memory_mb': sum(m.memory_mb for m in recent) / len(recent),
            'avg_memory_percent': sum(m.memory_percent for m in recent) / len(recent),
            'avg_threads': sum(m.num_threads for m in recent) / len(recent),
            'samples': len(recent)
        }
        
        return avg


class EventLogger:
    """
    Шаг 145: Application Event Logging
    
    Логирование всех событий приложений
    """
    
    def __init__(self, log_file: Optional[Path] = None):
        self.events: List[ApplicationEvent] = []
        self.log_file = log_file or Path("/tmp/mirai_app_events.jsonl")
    
    def log_event(
        self,
        app_name: str,
        event_type: str,
        event_data: Dict[str, Any],
        success: bool = True
    ) -> None:
        """
        Залогировать событие приложения
        
        Args:
            app_name: Название приложения
            event_type: Тип события
            event_data: Данные события
            success: Успешно ли выполнено
        """
        event = ApplicationEvent(
            timestamp=datetime.now(),
            app_name=app_name,
            event_type=event_type,
            event_data=event_data,
            success=success
        )
        
        self.events.append(event)
        
        # Сохраняем в файл
        self._write_to_file(event)
        
        logger.info(f"📝 Шаг 145: Событие залогировано - {app_name}: {event_type} (success={success})")
    
    def _write_to_file(self, event: ApplicationEvent) -> None:
        """Записать событие в файл"""
        try:
            # Преобразуем в словарь
            event_dict = asdict(event)
            event_dict['timestamp'] = event.timestamp.isoformat()
            
            # Записываем в JSONL формате
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event_dict, ensure_ascii=False) + '\n')
                
        except Exception as e:
            logger.error(f"❌ Ошибка записи события в файл: {e}")
    
    def get_events(
        self,
        app_name: Optional[str] = None,
        event_type: Optional[str] = None,
        last_n: Optional[int] = None
    ) -> List[ApplicationEvent]:
        """
        Получить события
        
        Args:
            app_name: Фильтр по приложению
            event_type: Фильтр по типу события
            last_n: Количество последних событий
            
        Returns:
            Список событий
        """
        events = self.events
        
        if app_name:
            events = [e for e in events if e.app_name == app_name]
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        if last_n:
            events = events[-last_n:]
        
        return events


class MetricsCollector:
    """
    Шаг 146: Application Performance Metrics
    
    Сбор метрик производительности операций
    """
    
    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
    
    def start_operation(self, operation: str, app_name: str) -> datetime:
        """
        Начать замер операции
        
        Args:
            operation: Название операции
            app_name: Название приложения
            
        Returns:
            Время начала
        """
        start_time = datetime.now()
        logger.debug(f"⏱️ Начало операции: {operation} для {app_name}")
        return start_time
    
    def end_operation(
        self,
        operation: str,
        app_name: str,
        start_time: datetime,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> PerformanceMetrics:
        """
        Завершить замер операции
        
        Args:
            operation: Название операции
            app_name: Название приложения
            start_time: Время начала
            success: Успешно ли выполнено
            error_message: Сообщение об ошибке (если есть)
            
        Returns:
            PerformanceMetrics
        """
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        metrics = PerformanceMetrics(
            operation=operation,
            app_name=app_name,
            start_time=start_time,
            end_time=end_time,
            duration_seconds=duration,
            success=success,
            error_message=error_message
        )
        
        self.metrics.append(metrics)
        
        logger.info(
            f"📊 Шаг 146: Операция завершена - {operation} для {app_name}: "
            f"{duration:.2f}s (success={success})"
        )
        
        return metrics
    
    def get_operation_stats(self, operation: str, app_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Получить статистику по операции
        
        Args:
            operation: Название операции
            app_name: Фильтр по приложению (опционально)
            
        Returns:
            Словарь со статистикой
        """
        operation_metrics = [m for m in self.metrics if m.operation == operation]
        
        if app_name:
            operation_metrics = [m for m in operation_metrics if m.app_name == app_name]
        
        if not operation_metrics:
            return {'error': 'No metrics found'}
        
        durations = [m.duration_seconds for m in operation_metrics]
        successes = sum(1 for m in operation_metrics if m.success)
        
        stats = {
            'total_operations': len(operation_metrics),
            'successful_operations': successes,
            'failed_operations': len(operation_metrics) - successes,
            'success_rate': successes / len(operation_metrics) * 100,
            'avg_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations)
        }
        
        return stats


class AppMonitor:
    """
    Главный класс мониторинга приложений
    Объединяет все компоненты мониторинга
    """
    
    def __init__(self):
        self.resource_monitor = ResourceMonitor()
        self.event_logger = EventLogger()
        self.metrics_collector = MetricsCollector()
        
        logger.info("✅ Шаг 11: App Monitor инициализирован")
    
    def get_resource_monitor(self) -> ResourceMonitor:
        """Получить Resource Monitor"""
        return self.resource_monitor
    
    def get_event_logger(self) -> EventLogger:
        """Получить Event Logger"""
        return self.event_logger
    
    def get_metrics_collector(self) -> MetricsCollector:
        """Получить Metrics Collector"""
        return self.metrics_collector
    
    def get_full_report(self, app_name: str) -> Dict[str, Any]:
        """
        Получить полный отчет по приложению
        
        Args:
            app_name: Название приложения
            
        Returns:
            Словарь с полным отчетом
        """
        # Текущие ресурсы
        current_metrics = self.resource_monitor.monitor_app(app_name)
        
        # Средние ресурсы
        avg_metrics = self.resource_monitor.get_average_metrics(app_name, last_n=10)
        
        # События
        events = self.event_logger.get_events(app_name=app_name, last_n=5)
        
        report = {
            'app_name': app_name,
            'current_resources': asdict(current_metrics) if current_metrics else None,
            'average_resources': avg_metrics,
            'recent_events': [
                {
                    'type': e.event_type,
                    'timestamp': e.timestamp.isoformat(),
                    'success': e.success
                }
                for e in events
            ],
            'timestamp': datetime.now().isoformat()
        }
        
        return report


# Convenience функции
_monitor_instance: Optional[AppMonitor] = None


def get_app_monitor() -> AppMonitor:
    """Получить глобальный экземпляр App Monitor (singleton)"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = AppMonitor()
    return _monitor_instance
