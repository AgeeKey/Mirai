#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Phase 6: VSCode Controller - Управление VSCode                ║
║  VSCode Code Editing (Шаги 76-105)                                   ║
╚══════════════════════════════════════════════════════════════════════╝

Шаги 76-105: VSCode Code Editing
Подраздел 3.1: VSCode File Operations (Шаги 76-90)
Подраздел 3.2: VSCode Code Editing (Шаги 91-105)

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

import logging
import time
import pyautogui
from typing import Optional, Dict, Any, List
from pathlib import Path

from .app_launcher import launch_application, close_application
from .application_manager import get_application_manager

logger = logging.getLogger(__name__)

# Настройки pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


class VSCodeController:
    """
    Контроллер для управления VSCode
    Реализует Шаги 76-105
    """
    
    def __init__(self):
        self.app_name = "vscode"
        self.is_launched = False
        self.current_file: Optional[Path] = None
        
        # Регистрируем handler
        manager = get_application_manager()
        manager.register_handler("vscode", self)
    
    # ========== Подраздел 3.1: VSCode File Operations (Шаги 76-90) ==========
    
    def launch_vscode(self, wait_ready: bool = True) -> bool:
        """
        Шаг 77: Launch VSCode
        
        Args:
            wait_ready: Ждать готовности
            
        Returns:
            bool: Успешно ли запущен
        """
        logger.info("🚀 Шаг 77: Запуск VSCode...")
        
        result = launch_application(self.app_name, wait_ready)
        
        if result.success:
            self.is_launched = True
            logger.info("✅ VSCode запущен")
            return True
        else:
            logger.error(f"❌ Ошибка запуска VSCode: {result.error}")
            return False
    
    def open_file(self, file_path: str) -> bool:
        """
        Шаг 81: Open File in VSCode
        
        Args:
            file_path: Путь к файлу
            
        Returns:
            bool: Успешно ли открыт
        """
        logger.info(f"📂 Шаг 81: Открытие файла {file_path}...")
        
        if not self.is_launched:
            logger.warning("VSCode не запущен, запускаю...")
            self.launch_vscode()
            time.sleep(2)  # Даем время на загрузку
        
        try:
            # Ctrl+O для открытия файла
            pyautogui.hotkey('ctrl', 'o')
            time.sleep(0.5)
            
            # Вводим путь к файлу
            pyautogui.typewrite(file_path, interval=0.05)
            time.sleep(0.3)
            
            # Enter для открытия
            pyautogui.press('enter')
            time.sleep(0.5)
            
            self.current_file = Path(file_path)
            logger.info(f"✅ Файл открыт: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка открытия файла: {e}")
            return False
    
    def create_new_file(self) -> bool:
        """
        Шаг 84: Create New File
        
        Returns:
            bool: Успешно ли создан
        """
        logger.info("📄 Шаг 84: Создание нового файла...")
        
        try:
            # Ctrl+N для нового файла
            pyautogui.hotkey('ctrl', 'n')
            time.sleep(0.3)
            
            self.current_file = None
            logger.info("✅ Новый файл создан")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания файла: {e}")
            return False
    
    def save_file(self, file_path: Optional[str] = None) -> bool:
        """
        Шаг 85: Save File
        
        Args:
            file_path: Путь для сохранения (если новый файл)
            
        Returns:
            bool: Успешно ли сохранен
        """
        logger.info("💾 Шаг 85: Сохранение файла...")
        
        try:
            # Ctrl+S для сохранения
            pyautogui.hotkey('ctrl', 's')
            time.sleep(0.3)
            
            # Если указан путь (новый файл)
            if file_path:
                time.sleep(0.5)
                pyautogui.typewrite(file_path, interval=0.05)
                time.sleep(0.3)
                pyautogui.press('enter')
                self.current_file = Path(file_path)
            
            logger.info("✅ Файл сохранен")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения файла: {e}")
            return False
    
    def save_all_files(self) -> bool:
        """
        Шаг 86: Save All Files
        
        Returns:
            bool: Успешно ли сохранены все
        """
        logger.info("💾 Шаг 86: Сохранение всех файлов...")
        
        try:
            # Ctrl+Shift+S для сохранения всех (в некоторых версиях)
            # или Ctrl+K S
            pyautogui.hotkey('ctrl', 'k')
            time.sleep(0.1)
            pyautogui.press('s')
            time.sleep(0.3)
            
            logger.info("✅ Все файлы сохранены")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения файлов: {e}")
            return False
    
    def close_file(self) -> bool:
        """
        Шаг 87: Close File
        
        Returns:
            bool: Успешно ли закрыт
        """
        logger.info("❌ Шаг 87: Закрытие файла...")
        
        try:
            # Ctrl+W для закрытия файла
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.3)
            
            self.current_file = None
            logger.info("✅ Файл закрыт")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка закрытия файла: {e}")
            return False
    
    # ========== Подраздел 3.2: VSCode Code Editing (Шаги 91-105) ==========
    
    def type_code(self, code: str) -> bool:
        """
        Шаг 92: Type Code
        
        Args:
            code: Код для ввода
            
        Returns:
            bool: Успешно ли введен
        """
        logger.info("⌨️ Шаг 92: Ввод кода...")
        
        try:
            # Вводим код построчно для лучшей читаемости
            lines = code.split('\n')
            for line in lines:
                pyautogui.typewrite(line, interval=0.02)
                pyautogui.press('enter')
                time.sleep(0.1)
            
            logger.info("✅ Код введен")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка ввода кода: {e}")
            return False
    
    def search_in_file(self, search_text: str) -> bool:
        """
        Шаг 96: Search in File
        
        Args:
            search_text: Текст для поиска
            
        Returns:
            bool: Успешно ли выполнен поиск
        """
        logger.info(f"🔍 Шаг 96: Поиск '{search_text}' в файле...")
        
        try:
            # Ctrl+F для поиска
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.3)
            
            # Вводим текст поиска
            pyautogui.typewrite(search_text, interval=0.05)
            time.sleep(0.3)
            
            # Enter для перехода к результату
            pyautogui.press('enter')
            
            logger.info("✅ Поиск выполнен")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка поиска: {e}")
            return False
    
    def replace_in_file(self, find_text: str, replace_text: str) -> bool:
        """
        Шаг 97: Replace in File
        
        Args:
            find_text: Текст для поиска
            replace_text: Текст для замены
            
        Returns:
            bool: Успешно ли выполнена замена
        """
        logger.info(f"🔄 Шаг 97: Замена '{find_text}' на '{replace_text}'...")
        
        try:
            # Ctrl+H для замены
            pyautogui.hotkey('ctrl', 'h')
            time.sleep(0.3)
            
            # Вводим текст для поиска
            pyautogui.typewrite(find_text, interval=0.05)
            time.sleep(0.2)
            
            # Tab для перехода к полю замены
            pyautogui.press('tab')
            time.sleep(0.2)
            
            # Вводим текст замены
            pyautogui.typewrite(replace_text, interval=0.05)
            time.sleep(0.2)
            
            # Enter для замены (или Ctrl+Shift+1 для замены всех)
            pyautogui.hotkey('ctrl', 'shift', '1')
            
            logger.info("✅ Замена выполнена")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка замены: {e}")
            return False
    
    def format_code(self) -> bool:
        """
        Шаг 101: Format Code
        
        Returns:
            bool: Успешно ли отформатирован
        """
        logger.info("✨ Шаг 101: Форматирование кода...")
        
        try:
            # Shift+Alt+F для форматирования
            pyautogui.hotkey('shift', 'alt', 'f')
            time.sleep(0.5)
            
            logger.info("✅ Код отформатирован")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка форматирования: {e}")
            return False
    
    def run_code(self) -> bool:
        """
        Шаг 102: Run Code
        
        Returns:
            bool: Успешно ли запущен
        """
        logger.info("▶️ Шаг 102: Запуск кода...")
        
        try:
            # F5 для запуска
            pyautogui.press('f5')
            time.sleep(0.5)
            
            logger.info("✅ Код запущен")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка запуска кода: {e}")
            return False
    
    def open_terminal(self) -> bool:
        """
        Шаг 104: Open Terminal
        
        Returns:
            bool: Успешно ли открыт
        """
        logger.info("💻 Шаг 104: Открытие терминала...")
        
        try:
            # Ctrl+` для терминала
            pyautogui.hotkey('ctrl', '`')
            time.sleep(0.5)
            
            logger.info("✅ Терминал открыт")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка открытия терминала: {e}")
            return False
    
    def close_vscode(self) -> bool:
        """
        Закрыть VSCode
        
        Returns:
            bool: Успешно ли закрыт
        """
        logger.info("🛑 Закрытие VSCode...")
        
        result = close_application(self.app_name)
        
        if result:
            self.is_launched = False
            self.current_file = None
            logger.info("✅ VSCode закрыт")
        
        return result


# Convenience функции
def get_vscode_controller() -> VSCodeController:
    """Получить VSCode контроллер"""
    return VSCodeController()
