#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Phase 6: System App Controller - Системные приложения         ║
║  System Applications (Шаги 121-135)                                  ║
╚══════════════════════════════════════════════════════════════════════╝

Шаги 121-135: System Applications
- Notepad, Calculator, Task Manager, Command Prompt и т.д.

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

import logging
import time
import platform
import subprocess
import pyautogui
from typing import Optional, Dict, Any
from pathlib import Path

from .app_launcher import launch_application, close_application
from .application_manager import get_application_manager

logger = logging.getLogger(__name__)

# Настройки pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


class NotepadController:
    """
    Контроллер для Notepad (Шаги 121-123)
    """
    
    def __init__(self):
        self.app_name = "notepad"
        self.is_launched = False
    
    def open_notepad(self) -> bool:
        """
        Шаг 121: Open Notepad
        
        Returns:
            bool: Успешно ли открыт
        """
        logger.info("📝 Шаг 121: Открытие Notepad...")
        
        result = launch_application(self.app_name, wait_ready=True)
        
        if result.success:
            self.is_launched = True
            logger.info("✅ Notepad открыт")
            return True
        else:
            logger.error(f"❌ Ошибка открытия Notepad: {result.error}")
            return False
    
    def edit_text(self, text: str) -> bool:
        """
        Шаг 122: Edit Text in Notepad
        
        Args:
            text: Текст для ввода
            
        Returns:
            bool: Успешно ли введен
        """
        logger.info("⌨️ Шаг 122: Ввод текста в Notepad...")
        
        if not self.is_launched:
            logger.warning("Notepad не открыт, открываю...")
            self.open_notepad()
            time.sleep(1)
        
        try:
            # Вводим текст
            pyautogui.typewrite(text, interval=0.05)
            time.sleep(0.3)
            
            logger.info("✅ Текст введен")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка ввода текста: {e}")
            return False
    
    def save_text(self, file_path: str) -> bool:
        """
        Шаг 123: Save in Notepad
        
        Args:
            file_path: Путь для сохранения
            
        Returns:
            bool: Успешно ли сохранен
        """
        logger.info(f"💾 Шаг 123: Сохранение в {file_path}...")
        
        try:
            # Ctrl+S для сохранения
            pyautogui.hotkey('ctrl', 's')
            time.sleep(0.5)
            
            # Вводим путь
            pyautogui.typewrite(file_path, interval=0.05)
            time.sleep(0.3)
            
            # Enter для сохранения
            pyautogui.press('enter')
            time.sleep(0.3)
            
            logger.info("✅ Файл сохранен")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения: {e}")
            return False
    
    def close(self) -> bool:
        """Закрыть Notepad"""
        return close_application(self.app_name)


class CalculatorController:
    """
    Контроллер для Calculator (Шаги 124-125)
    """
    
    def __init__(self):
        self.app_name = "calculator"
        self.is_launched = False
    
    def open_calculator(self) -> bool:
        """
        Шаг 124: Open Calculator
        
        Returns:
            bool: Успешно ли открыт
        """
        logger.info("🔢 Шаг 124: Открытие Calculator...")
        
        result = launch_application(self.app_name, wait_ready=True)
        
        if result.success:
            self.is_launched = True
            logger.info("✅ Calculator открыт")
            return True
        else:
            logger.error(f"❌ Ошибка открытия Calculator: {result.error}")
            return False
    
    def calculate(self, expression: str) -> bool:
        """
        Шаг 125: Use Calculator
        
        Args:
            expression: Математическое выражение (например, "2+2")
            
        Returns:
            bool: Успешно ли выполнено
        """
        logger.info(f"🔢 Шаг 125: Вычисление {expression}...")
        
        if not self.is_launched:
            logger.warning("Calculator не открыт, открываю...")
            self.open_calculator()
            time.sleep(1)
        
        try:
            # Вводим выражение
            for char in expression:
                pyautogui.press(char)
                time.sleep(0.1)
            
            # Enter для вычисления
            pyautogui.press('enter')
            time.sleep(0.3)
            
            logger.info("✅ Вычисление выполнено")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка вычисления: {e}")
            return False
    
    def close(self) -> bool:
        """Закрыть Calculator"""
        return close_application(self.app_name)


class TaskManagerController:
    """
    Контроллер для Task Manager (Шаги 127-129)
    """
    
    def open_task_manager(self) -> bool:
        """
        Шаг 127: Open Task Manager
        
        Returns:
            bool: Успешно ли открыт
        """
        logger.info("📊 Шаг 127: Открытие Task Manager...")
        
        try:
            if platform.system() == "Windows":
                # Ctrl+Shift+Esc для Task Manager
                pyautogui.hotkey('ctrl', 'shift', 'esc')
                time.sleep(1)
                logger.info("✅ Task Manager открыт")
                return True
            else:
                logger.warning("⚠️ Task Manager доступен только на Windows")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ошибка открытия Task Manager: {e}")
            return False
    
    def monitor_processes(self) -> Dict[str, Any]:
        """
        Шаг 128: Monitor Processes
        
        Returns:
            Словарь с информацией о процессах
        """
        logger.info("👀 Шаг 128: Мониторинг процессов...")
        
        try:
            import psutil
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Сортируем по использованию CPU
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            
            result = {
                'total_processes': len(processes),
                'top_cpu': processes[:5] if len(processes) >= 5 else processes
            }
            
            logger.info(f"✅ Найдено процессов: {len(processes)}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка мониторинга: {e}")
            return {'error': str(e)}


class CMDController:
    """
    Контроллер для Command Prompt (Шаги 130-132)
    """
    
    def __init__(self):
        self.app_name = "cmd"
        self.is_launched = False
        self.process = None
    
    def open_cmd(self) -> bool:
        """
        Шаг 130: Open Command Prompt
        
        Returns:
            bool: Успешно ли открыт
        """
        logger.info("💻 Шаг 130: Открытие Command Prompt...")
        
        result = launch_application(self.app_name, wait_ready=True)
        
        if result.success:
            self.is_launched = True
            logger.info("✅ Command Prompt открыт")
            return True
        else:
            logger.error(f"❌ Ошибка открытия CMD: {result.error}")
            return False
    
    def execute_command(self, command: str) -> Optional[str]:
        """
        Шаг 131: Execute Command
        
        Args:
            command: Команда для выполнения
            
        Returns:
            Вывод команды или None
        """
        logger.info(f"⚡ Шаг 131: Выполнение команды: {command}")
        
        try:
            # Выполняем команду через subprocess
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout
            
            logger.info("✅ Команда выполнена")
            return output
            
        except subprocess.TimeoutExpired:
            logger.error("❌ Таймаут выполнения команды")
            return None
        except Exception as e:
            logger.error(f"❌ Ошибка выполнения команды: {e}")
            return None
    
    def read_output(self, output: str) -> Dict[str, Any]:
        """
        Шаг 132: Read Command Output
        
        Args:
            output: Вывод команды
            
        Returns:
            Словарь с разобранным выводом
        """
        logger.info("📖 Шаг 132: Чтение вывода команды...")
        
        lines = output.split('\n') if output else []
        
        result = {
            'raw_output': output,
            'line_count': len(lines),
            'lines': lines,
            'has_error': 'error' in output.lower() if output else False
        }
        
        logger.info(f"✅ Прочитано строк: {len(lines)}")
        return result


class SystemAppController:
    """
    Главный контроллер системных приложений
    Координирует Notepad, Calculator, Task Manager, CMD
    """
    
    def __init__(self):
        self.notepad = NotepadController()
        self.calculator = CalculatorController()
        self.task_manager = TaskManagerController()
        self.cmd = CMDController()
        
        # Регистрируем handler
        manager = get_application_manager()
        manager.register_handler("system_apps", self)
        
        logger.info("🔧 SystemAppController инициализирован")
    
    def get_notepad(self) -> NotepadController:
        """Получить Notepad контроллер"""
        return self.notepad
    
    def get_calculator(self) -> CalculatorController:
        """Получить Calculator контроллер"""
        return self.calculator
    
    def get_task_manager(self) -> TaskManagerController:
        """Получить Task Manager контроллер"""
        return self.task_manager
    
    def get_cmd(self) -> CMDController:
        """Получить CMD контроллер"""
        return self.cmd


# Convenience функции
def get_system_app_controller() -> SystemAppController:
    """Получить System App контроллер"""
    return SystemAppController()
