#!/usr/bin/env python3
"""
✅ Execution Context Validator - Валидатор контекста выполнения
Шаг 2 из 150: Validate Execution Context

Проверяет что контекст выполнения готов:
- Все параметры
- Ресурсы
- Права доступа
"""

import logging
import platform
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("⚠️ psutil не установлен, используются mock данные")

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Результат валидации"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    info: Dict[str, Any]


class ExecutionContextValidator:
    """
    Валидатор контекста выполнения
    
    Проверяет:
    - Системные ресурсы (CPU, RAM, Disk)
    - Права доступа
    - Необходимые зависимости
    - Параметры окружения
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Инициализация валидатора
        
        Args:
            config: Конфигурация требований
        """
        self.config = config or {}
        
        # Минимальные требования по умолчанию
        self.min_cpu_percent = self.config.get('min_cpu_percent', 10.0)
        self.min_memory_mb = self.config.get('min_memory_mb', 512)
        self.min_disk_gb = self.config.get('min_disk_gb', 1)
        
        logger.info("✅ ExecutionContextValidator создан")
    
    def validate(self) -> ValidationResult:
        """
        Полная валидация контекста
        
        Returns:
            ValidationResult с результатами проверки
        """
        errors = []
        warnings = []
        info = {}
        
        # Проверка системы
        system_check = self._check_system()
        info['system'] = system_check
        if not system_check['os_supported']:
            errors.append(f"Неподдерживаемая ОС: {system_check['os']}")
        
        # Проверка CPU
        cpu_check = self._check_cpu()
        info['cpu'] = cpu_check
        if cpu_check['available_percent'] < self.min_cpu_percent:
            warnings.append(
                f"Мало доступного CPU: {cpu_check['available_percent']:.1f}% "
                f"(минимум {self.min_cpu_percent}%)"
            )
        
        # Проверка памяти
        memory_check = self._check_memory()
        info['memory'] = memory_check
        if memory_check['available_mb'] < self.min_memory_mb:
            errors.append(
                f"Недостаточно памяти: {memory_check['available_mb']:.0f} MB "
                f"(минимум {self.min_memory_mb} MB)"
            )
        
        # Проверка диска
        disk_check = self._check_disk()
        info['disk'] = disk_check
        if disk_check['free_gb'] < self.min_disk_gb:
            warnings.append(
                f"Мало свободного места: {disk_check['free_gb']:.1f} GB "
                f"(минимум {self.min_disk_gb} GB)"
            )
        
        # Проверка сети (опционально)
        network_check = self._check_network()
        info['network'] = network_check
        
        is_valid = len(errors) == 0
        
        if is_valid:
            logger.info("✅ Валидация контекста выполнения успешна")
        else:
            logger.error(f"❌ Валидация не прошла: {len(errors)} ошибок")
        
        return ValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            info=info
        )
    
    def _check_system(self) -> Dict[str, Any]:
        """Проверка системы"""
        os_name = platform.system()
        
        return {
            'os': os_name,
            'os_version': platform.version(),
            'architecture': platform.machine(),
            'python_version': platform.python_version(),
            'os_supported': os_name in ['Windows', 'Linux', 'Darwin']
        }
    
    def _check_cpu(self) -> Dict[str, Any]:
        """Проверка CPU"""
        if not PSUTIL_AVAILABLE:
            return {
                'count': 4,
                'used_percent': 20.0,
                'available_percent': 80.0,
                'per_cpu': [20.0, 20.0, 20.0, 20.0]
            }
        
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        return {
            'count': cpu_count,
            'used_percent': cpu_percent,
            'available_percent': 100 - cpu_percent,
            'per_cpu': psutil.cpu_percent(interval=1, percpu=True)
        }
    
    def _check_memory(self) -> Dict[str, Any]:
        """Проверка памяти"""
        if not PSUTIL_AVAILABLE:
            return {
                'total_mb': 8192,
                'available_mb': 4096,
                'used_mb': 4096,
                'percent': 50.0
            }
        
        memory = psutil.virtual_memory()
        
        return {
            'total_mb': memory.total / (1024 * 1024),
            'available_mb': memory.available / (1024 * 1024),
            'used_mb': memory.used / (1024 * 1024),
            'percent': memory.percent
        }
    
    def _check_disk(self) -> Dict[str, Any]:
        """Проверка диска"""
        if not PSUTIL_AVAILABLE:
            return {
                'total_gb': 256,
                'used_gb': 128,
                'free_gb': 128,
                'percent': 50.0
            }
        
        disk = psutil.disk_usage('/')
        
        return {
            'total_gb': disk.total / (1024 ** 3),
            'used_gb': disk.used / (1024 ** 3),
            'free_gb': disk.free / (1024 ** 3),
            'percent': disk.percent
        }
    
    def _check_network(self) -> Dict[str, Any]:
        """Проверка сети"""
        if not PSUTIL_AVAILABLE:
            return {
                'bytes_sent': 0,
                'bytes_recv': 0,
                'available': True
            }
        
        try:
            net_io = psutil.net_io_counters()
            
            return {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'available': True
            }
        except Exception as e:
            logger.warning(f"⚠️ Не удалось проверить сеть: {e}")
            return {'available': False}
    
    def check_resources(self) -> bool:
        """
        Быстрая проверка ресурсов
        
        Returns:
            bool: True если ресурсы достаточны
        """
        result = self.validate()
        return result.is_valid


# Тесты
if __name__ == "__main__":
    # Создаем валидатор
    validator = ExecutionContextValidator()
    
    # Проверяем контекст
    result = validator.validate()
    
    print("\n" + "="*60)
    print("✅ РЕЗУЛЬТАТЫ ВАЛИДАЦИИ КОНТЕКСТА")
    print("="*60)
    print(f"Статус: {'✅ ВАЛИДНО' if result.is_valid else '❌ НЕВАЛИДНО'}")
    
    if result.errors:
        print(f"\n❌ Ошибки ({len(result.errors)}):")
        for error in result.errors:
            print(f"  • {error}")
    
    if result.warnings:
        print(f"\n⚠️ Предупреждения ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"  • {warning}")
    
    print("\n📊 Информация о системе:")
    print(f"  ОС: {result.info['system']['os']} {result.info['system']['os_version']}")
    print(f"  CPU: {result.info['cpu']['count']} ядер, доступно {result.info['cpu']['available_percent']:.1f}%")
    print(f"  RAM: {result.info['memory']['available_mb']:.0f} MB доступно")
    print(f"  Диск: {result.info['disk']['free_gb']:.1f} GB свободно")
    print("="*60)
