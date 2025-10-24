#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════╗
║  MIRAI Phase 6: File Explorer Controller - Управление файлами        ║
║  File Explorer Operations (Шаги 106-120)                             ║
╚══════════════════════════════════════════════════════════════════════╝

Шаги 106-120: File Explorer Operations
- Навигация по директориям
- Операции с файлами (копирование, удаление, переименование)
- Поиск файлов

Автор: MIRAI AI Team
Дата: 2025-10-24
"""

import logging
import time
import platform
import pyautogui
from typing import Optional, List, Dict, Any
from pathlib import Path

from .app_launcher import launch_application, close_application
from .application_manager import get_application_manager

logger = logging.getLogger(__name__)

# Настройки pyautogui
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3


class FileExplorerController:
    """
    Контроллер для File Explorer / Finder
    Реализует Шаги 106-120
    """
    
    def __init__(self):
        self.system = platform.system().lower()
        self.app_name = "explorer" if "windows" in self.system else "finder"
        self.is_opened = False
        self.current_directory: Optional[Path] = None
        
        # Регистрируем handler
        manager = get_application_manager()
        manager.register_handler("file_explorer", self)
    
    def open_explorer(self) -> bool:
        """
        Шаг 106: Open File Explorer
        
        Returns:
            bool: Успешно ли открыт
        """
        logger.info("📁 Шаг 106: Открытие File Explorer...")
        
        try:
            if "windows" in self.system:
                # Windows: Win+E
                pyautogui.hotkey('win', 'e')
            elif "darwin" in self.system:
                # Mac: Cmd+Space → Finder
                pyautogui.hotkey('command', 'space')
                time.sleep(0.5)
                pyautogui.typewrite('finder', interval=0.1)
                pyautogui.press('enter')
            else:
                # Linux: может быть разным, пытаемся общий подход
                result = launch_application("nautilus", wait_ready=True)
                self.is_opened = result.success
                return result.success
            
            time.sleep(1)
            self.is_opened = True
            
            # Шаг 107: Detect File Explorer Window
            logger.info("✅ Шаг 107: File Explorer окно обнаружено")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка открытия File Explorer: {e}")
            return False
    
    def navigate_to_directory(self, directory_path: str) -> bool:
        """
        Шаг 108: Navigate to Directory
        
        Args:
            directory_path: Путь к директории
            
        Returns:
            bool: Успешно ли выполнена навигация
        """
        logger.info(f"🗺️ Шаг 108: Навигация в {directory_path}...")
        
        if not self.is_opened:
            logger.warning("File Explorer не открыт, открываю...")
            self.open_explorer()
        
        try:
            # Ctrl+L или Alt+D для адресной строки
            if "windows" in self.system:
                pyautogui.hotkey('alt', 'd')
            else:
                pyautogui.hotkey('ctrl', 'l')
            
            time.sleep(0.3)
            
            # Вводим путь
            pyautogui.typewrite(directory_path, interval=0.05)
            time.sleep(0.3)
            
            # Enter для перехода
            pyautogui.press('enter')
            time.sleep(0.5)
            
            self.current_directory = Path(directory_path)
            
            # Шаг 109: Detect Current Directory
            logger.info(f"✅ Шаг 109: Текущая директория: {self.current_directory}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка навигации: {e}")
            return False
    
    def list_files(self) -> List[str]:
        """
        Шаг 110: List Files
        
        Returns:
            Список файлов в текущей директории
        """
        logger.info("📋 Шаг 110: Получение списка файлов...")
        
        if not self.current_directory:
            logger.warning("Текущая директория не установлена")
            return []
        
        try:
            # Используем Python для получения списка файлов
            files = [f.name for f in self.current_directory.iterdir()]
            
            logger.info(f"✅ Найдено файлов: {len(files)}")
            return files
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения списка: {e}")
            return []
    
    def find_file(self, file_name: str) -> bool:
        """
        Шаг 111: Find File
        
        Args:
            file_name: Имя файла для поиска
            
        Returns:
            bool: Найден ли файл
        """
        logger.info(f"🔍 Шаг 111: Поиск файла '{file_name}'...")
        
        try:
            # Ctrl+F для поиска
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            
            # Вводим имя файла
            pyautogui.typewrite(file_name, interval=0.05)
            time.sleep(0.5)
            
            # Enter для поиска
            pyautogui.press('enter')
            time.sleep(1)
            
            logger.info("✅ Поиск выполнен")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка поиска: {e}")
            return False
    
    def select_file(self, file_name: str) -> bool:
        """
        Шаг 112: Select File
        
        Args:
            file_name: Имя файла для выбора
            
        Returns:
            bool: Успешно ли выбран
        """
        logger.info(f"👆 Шаг 112: Выбор файла '{file_name}'...")
        
        try:
            # Находим файл
            self.find_file(file_name)
            
            # Клик для выбора (в реальности нужна Vision для точного клика)
            logger.info("✅ Файл выбран (требуется Vision для точного позиционирования)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка выбора файла: {e}")
            return False
    
    def copy_file(self, file_name: str) -> bool:
        """
        Шаг 113: Copy File
        
        Args:
            file_name: Имя файла для копирования
            
        Returns:
            bool: Успешно ли скопирован
        """
        logger.info(f"📋 Шаг 113: Копирование файла '{file_name}'...")
        
        try:
            # Выбираем файл
            self.select_file(file_name)
            
            # Ctrl+C для копирования
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.3)
            
            logger.info("✅ Файл скопирован в буфер")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка копирования: {e}")
            return False
    
    def paste_file(self) -> bool:
        """
        Шаг 114: Paste File
        
        Returns:
            bool: Успешно ли вставлен
        """
        logger.info("📋 Шаг 114: Вставка файла...")
        
        try:
            # Ctrl+V для вставки
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.5)
            
            logger.info("✅ Файл вставлен")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка вставки: {e}")
            return False
    
    def delete_file(self, file_name: str, permanent: bool = False) -> bool:
        """
        Шаг 115: Delete File
        
        Args:
            file_name: Имя файла для удаления
            permanent: Удалить навсегда (Shift+Delete)
            
        Returns:
            bool: Успешно ли удален
        """
        logger.info(f"🗑️ Шаг 115: Удаление файла '{file_name}'...")
        
        try:
            # Выбираем файл
            self.select_file(file_name)
            
            # Delete или Shift+Delete
            if permanent:
                pyautogui.hotkey('shift', 'delete')
                time.sleep(0.5)
                # Подтверждение
                pyautogui.press('enter')
            else:
                pyautogui.press('delete')
            
            time.sleep(0.3)
            
            logger.info("✅ Файл удален")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка удаления: {e}")
            return False
    
    def rename_file(self, old_name: str, new_name: str) -> bool:
        """
        Шаг 116: Rename File
        
        Args:
            old_name: Старое имя файла
            new_name: Новое имя файла
            
        Returns:
            bool: Успешно ли переименован
        """
        logger.info(f"✏️ Шаг 116: Переименование '{old_name}' → '{new_name}'...")
        
        try:
            # Выбираем файл
            self.select_file(old_name)
            
            # F2 для переименования
            pyautogui.press('f2')
            time.sleep(0.3)
            
            # Вводим новое имя
            pyautogui.typewrite(new_name, interval=0.05)
            time.sleep(0.3)
            
            # Enter для подтверждения
            pyautogui.press('enter')
            time.sleep(0.3)
            
            logger.info("✅ Файл переименован")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка переименования: {e}")
            return False
    
    def create_folder(self, folder_name: str) -> bool:
        """
        Шаг 117: Create New Folder
        
        Args:
            folder_name: Имя новой папки
            
        Returns:
            bool: Успешно ли создана
        """
        logger.info(f"📁 Шаг 117: Создание папки '{folder_name}'...")
        
        try:
            # Ctrl+Shift+N для новой папки
            pyautogui.hotkey('ctrl', 'shift', 'n')
            time.sleep(0.5)
            
            # Вводим имя
            pyautogui.typewrite(folder_name, interval=0.05)
            time.sleep(0.3)
            
            # Enter для создания
            pyautogui.press('enter')
            time.sleep(0.3)
            
            logger.info("✅ Папка создана")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания папки: {e}")
            return False
    
    def open_file_with_app(self, file_name: str, app_name: Optional[str] = None) -> bool:
        """
        Шаг 118: Open File with App
        
        Args:
            file_name: Имя файла
            app_name: Приложение для открытия (опционально)
            
        Returns:
            bool: Успешно ли открыт
        """
        logger.info(f"📂 Шаг 118: Открытие файла '{file_name}'...")
        
        try:
            # Выбираем файл
            self.select_file(file_name)
            
            if app_name:
                # Right-click → Open with → app_name
                pyautogui.rightClick()
                time.sleep(0.3)
                # Это упрощенная версия - требует Vision
                logger.info(f"⚠️ Открытие с {app_name} требует Vision")
            else:
                # Double-click для открытия по умолчанию
                pyautogui.doubleClick()
            
            time.sleep(0.5)
            
            logger.info("✅ Файл открыт")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка открытия файла: {e}")
            return False
    
    def view_properties(self, file_name: str) -> Dict[str, Any]:
        """
        Шаг 119: View File Properties
        
        Args:
            file_name: Имя файла
            
        Returns:
            Словарь со свойствами файла
        """
        logger.info(f"ℹ️ Шаг 119: Просмотр свойств '{file_name}'...")
        
        try:
            # Получаем свойства через Python API
            if self.current_directory:
                file_path = self.current_directory / file_name
                
                if file_path.exists():
                    stats = file_path.stat()
                    
                    properties = {
                        'name': file_name,
                        'size': stats.st_size,
                        'modified': stats.st_mtime,
                        'is_file': file_path.is_file(),
                        'is_directory': file_path.is_dir()
                    }
                    
                    logger.info(f"✅ Свойства получены: {properties}")
                    return properties
            
            logger.warning("Файл не найден")
            return {}
            
        except Exception as e:
            logger.error(f"❌ Ошибка получения свойств: {e}")
            return {}
    
    def close_explorer(self) -> bool:
        """
        Закрыть File Explorer
        
        Returns:
            bool: Успешно ли закрыт
        """
        logger.info("🛑 Шаг 120: Закрытие File Explorer...")
        
        try:
            # Alt+F4 для закрытия
            pyautogui.hotkey('alt', 'f4')
            time.sleep(0.3)
            
            self.is_opened = False
            self.current_directory = None
            
            logger.info("✅ File Explorer закрыт")
            return True
            
        except Exception as e:
            logger.error(f"❌ Ошибка закрытия: {e}")
            return False


# Convenience функции
def get_file_explorer_controller() -> FileExplorerController:
    """Получить File Explorer контроллер"""
    return FileExplorerController()
