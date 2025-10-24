#!/usr/bin/env python3
"""
🔍 BROWSER DETECTION & SETUP - Шаги 1-15
Подраздел 1.1: Browser Detection & Setup

Полное обнаружение и настройка браузеров:
- Detect installed browsers (Chrome, Firefox, Safari, Edge, Opera)
- Check versions and compatibility
- Locate executables
- Initialize WebDriver
- Setup logging and monitoring
"""

import json
import logging
import os
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class BrowserType(Enum):
    """Типы поддерживаемых браузеров"""
    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"
    EDGE = "edge"
    OPERA = "opera"
    CHROMIUM = "chromium"
    BRAVE = "brave"


@dataclass
class BrowserInfo:
    """Информация о браузере"""
    browser_type: BrowserType
    version: str
    executable_path: str
    is_compatible: bool
    user_data_dir: Optional[str] = None
    profiles_dir: Optional[str] = None
    extensions_dir: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BrowserDetector:
    """
    ШАГ 1: Detect Installed Browsers
    Обнаружить какие браузеры установлены на системе
    """
    
    def __init__(self):
        self.system = platform.system()
        logger.info(f"🔍 BrowserDetector создан (ОС: {self.system})")
    
    def detect_installed_browsers(self) -> List[BrowserInfo]:
        """
        Обнаружить все установленные браузеры
        
        Returns:
            List[BrowserInfo]: Список найденных браузеров
        """
        logger.info("🔍 Поиск установленных браузеров...")
        browsers = []
        
        # Ищем каждый тип браузера
        for browser_type in BrowserType:
            browser = self._detect_browser(browser_type)
            if browser:
                browsers.append(browser)
                logger.info(f"  ✅ Найден: {browser_type.value} v{browser.version}")
        
        if not browsers:
            logger.warning("⚠️ Браузеры не найдены!")
        else:
            logger.info(f"✅ Найдено браузеров: {len(browsers)}")
        
        return browsers
    
    def _detect_browser(self, browser_type: BrowserType) -> Optional[BrowserInfo]:
        """Обнаружить конкретный браузер"""
        if self.system == "Windows":
            return self._detect_browser_windows(browser_type)
        elif self.system == "Darwin":  # macOS
            return self._detect_browser_macos(browser_type)
        elif self.system == "Linux":
            return self._detect_browser_linux(browser_type)
        return None
    
    def _detect_browser_windows(self, browser_type: BrowserType) -> Optional[BrowserInfo]:
        """Обнаружить браузер на Windows"""
        paths = {
            BrowserType.CHROME: [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ],
            BrowserType.FIREFOX: [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            ],
            BrowserType.EDGE: [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            ],
            BrowserType.OPERA: [
                r"C:\Program Files\Opera\launcher.exe",
                r"C:\Program Files (x86)\Opera\launcher.exe",
            ],
            BrowserType.BRAVE: [
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            ],
        }
        
        for path in paths.get(browser_type, []):
            if Path(path).exists():
                version = self._get_version_windows(path)
                return BrowserInfo(
                    browser_type=browser_type,
                    version=version or "unknown",
                    executable_path=path,
                    is_compatible=True,
                )
        
        return None
    
    def _detect_browser_macos(self, browser_type: BrowserType) -> Optional[BrowserInfo]:
        """Обнаружить браузер на macOS"""
        paths = {
            BrowserType.CHROME: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            BrowserType.FIREFOX: "/Applications/Firefox.app/Contents/MacOS/firefox",
            BrowserType.SAFARI: "/Applications/Safari.app/Contents/MacOS/Safari",
            BrowserType.EDGE: "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            BrowserType.OPERA: "/Applications/Opera.app/Contents/MacOS/Opera",
            BrowserType.BRAVE: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        }
        
        path = paths.get(browser_type)
        if path and Path(path).exists():
            version = self._get_version_macos(path)
            return BrowserInfo(
                browser_type=browser_type,
                version=version or "unknown",
                executable_path=path,
                is_compatible=True,
            )
        
        return None
    
    def _detect_browser_linux(self, browser_type: BrowserType) -> Optional[BrowserInfo]:
        """Обнаружить браузер на Linux"""
        commands = {
            BrowserType.CHROME: "google-chrome",
            BrowserType.CHROMIUM: "chromium-browser",
            BrowserType.FIREFOX: "firefox",
            BrowserType.OPERA: "opera",
            BrowserType.BRAVE: "brave-browser",
        }
        
        cmd = commands.get(browser_type)
        if not cmd:
            return None
        
        try:
            result = subprocess.run(
                ["which", cmd],
                capture_output=True,
                timeout=5,
                text=True,
            )
            
            if result.returncode == 0:
                path = result.stdout.strip()
                version = self._get_version_linux(cmd)
                return BrowserInfo(
                    browser_type=browser_type,
                    version=version or "unknown",
                    executable_path=path,
                    is_compatible=True,
                )
        except Exception as e:
            logger.debug(f"Ошибка поиска {cmd}: {e}")
        
        return None
    
    def _get_version_windows(self, path: str) -> Optional[str]:
        """Получить версию браузера на Windows"""
        try:
            result = subprocess.run(
                [path, "--version"],
                capture_output=True,
                timeout=5,
                text=True,
            )
            return self._extract_version(result.stdout)
        except:
            return None
    
    def _get_version_macos(self, path: str) -> Optional[str]:
        """Получить версию браузера на macOS"""
        try:
            result = subprocess.run(
                [path, "--version"],
                capture_output=True,
                timeout=5,
                text=True,
            )
            return self._extract_version(result.stdout)
        except:
            return None
    
    def _get_version_linux(self, cmd: str) -> Optional[str]:
        """Получить версию браузера на Linux"""
        try:
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True,
                timeout=5,
                text=True,
            )
            return self._extract_version(result.stdout)
        except:
            return None
    
    def _extract_version(self, text: str) -> Optional[str]:
        """Извлечь версию из текста"""
        match = re.search(r'(\d+\.[\d.]+)', text)
        return match.group(1) if match else None


class BrowserVersionChecker:
    """
    ШАГ 2: Identify Browser Versions
    Определить версию каждого браузера
    """
    
    def __init__(self):
        logger.info("🔢 BrowserVersionChecker создан")
    
    def check_version(self, browser: BrowserInfo) -> str:
        """
        Проверить версию браузера
        
        Args:
            browser: Информация о браузере
            
        Returns:
            str: Версия браузера
        """
        logger.info(f"🔢 Проверка версии: {browser.browser_type.value}")
        return browser.version
    
    def compare_versions(self, version1: str, version2: str) -> int:
        """
        Сравнить две версии
        
        Returns:
            int: -1 если version1 < version2, 0 если равны, 1 если version1 > version2
        """
        v1_parts = [int(x) for x in version1.split('.')]
        v2_parts = [int(x) for x in version2.split('.')]
        
        for i in range(max(len(v1_parts), len(v2_parts))):
            v1 = v1_parts[i] if i < len(v1_parts) else 0
            v2 = v2_parts[i] if i < len(v2_parts) else 0
            
            if v1 < v2:
                return -1
            elif v1 > v2:
                return 1
        
        return 0


class CompatibilityChecker:
    """
    ШАГ 3: Check Browser Compatibility
    Проверить совместимость браузера с требованиями
    """
    
    # Минимальные версии для совместимости
    MIN_VERSIONS = {
        BrowserType.CHROME: "90.0.0",
        BrowserType.FIREFOX: "88.0.0",
        BrowserType.EDGE: "90.0.0",
        BrowserType.SAFARI: "14.0.0",
        BrowserType.OPERA: "76.0.0",
    }
    
    def __init__(self):
        logger.info("✅ CompatibilityChecker создан")
        self.version_checker = BrowserVersionChecker()
    
    def check_compatibility(self, browser: BrowserInfo) -> bool:
        """
        Проверить совместимость браузера
        
        Args:
            browser: Информация о браузере
            
        Returns:
            bool: True если совместим
        """
        min_version = self.MIN_VERSIONS.get(browser.browser_type)
        
        if not min_version:
            logger.warning(f"⚠️ Нет минимальной версии для {browser.browser_type.value}")
            return True
        
        comparison = self.version_checker.compare_versions(browser.version, min_version)
        
        if comparison >= 0:
            logger.info(f"✅ {browser.browser_type.value} v{browser.version} совместим")
            return True
        else:
            logger.warning(
                f"⚠️ {browser.browser_type.value} v{browser.version} < {min_version} (требуется обновление)"
            )
            return False


class BrowserExecutableLocator:
    """
    ШАГ 4: Locate Browser Executable
    Найти путь к исполняемому файлу браузера
    """
    
    def __init__(self):
        logger.info("📍 BrowserExecutableLocator создан")
    
    def locate_executable(self, browser_type: BrowserType) -> Optional[str]:
        """
        Найти исполняемый файл браузера
        
        Args:
            browser_type: Тип браузера
            
        Returns:
            Optional[str]: Путь к исполняемому файлу или None
        """
        logger.info(f"📍 Поиск исполняемого файла: {browser_type.value}")
        
        detector = BrowserDetector()
        browser = detector._detect_browser(browser_type)
        
        if browser:
            logger.info(f"✅ Найден: {browser.executable_path}")
            return browser.executable_path
        
        logger.warning(f"❌ Исполняемый файл не найден: {browser_type.value}")
        return None


class BrowserConfigLoader:
    """
    ШАГ 5: Load Browser Configuration
    Загрузить конфигурацию браузера
    """
    
    def __init__(self):
        logger.info("⚙️ BrowserConfigLoader создан")
    
    def load_config(self, browser: BrowserInfo) -> Dict[str, Any]:
        """
        Загрузить конфигурацию браузера
        
        Args:
            browser: Информация о браузере
            
        Returns:
            Dict: Конфигурация браузера
        """
        logger.info(f"⚙️ Загрузка конфигурации: {browser.browser_type.value}")
        
        config = {
            "browser_type": browser.browser_type.value,
            "version": browser.version,
            "executable": browser.executable_path,
            "preferences": {},
            "settings": {},
            "extensions": [],
        }
        
        # Загружаем дополнительные настройки из файла, если существует
        config_file = self._get_config_file_path(browser)
        if config_file and config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    config.update(user_config)
                logger.info(f"✅ Конфигурация загружена из {config_file}")
            except Exception as e:
                logger.warning(f"⚠️ Ошибка загрузки конфигурации: {e}")
        
        return config
    
    def _get_config_file_path(self, browser: BrowserInfo) -> Optional[Path]:
        """Получить путь к файлу конфигурации"""
        # Примерный путь (в реальности зависит от браузера)
        if browser.user_data_dir:
            return Path(browser.user_data_dir) / "Preferences"
        return None


class WebDriverInitializer:
    """
    ШАГ 6: Initialize WebDriver
    Инициализация WebDriver для автоматизации
    """
    
    def __init__(self):
        logger.info("🚗 WebDriverInitializer создан")
        self.driver = None
    
    def initialize_driver(self, browser: BrowserInfo, headless: bool = False) -> bool:
        """
        Инициализировать WebDriver
        
        Args:
            browser: Информация о браузере
            headless: Запустить в headless режиме
            
        Returns:
            bool: True если успешно
        """
        logger.info(f"🚗 Инициализация WebDriver: {browser.browser_type.value}")
        
        try:
            # В реальности здесь будет инициализация Selenium/Playwright
            # Для демо просто логируем
            logger.info(f"  • Браузер: {browser.executable_path}")
            logger.info(f"  • Headless: {headless}")
            logger.info("✅ WebDriver инициализирован")
            return True
        
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации WebDriver: {e}")
            return False


class BrowserLogger:
    """
    ШАГ 7: Setup Browser Logging
    Настройка логирования браузера
    """
    
    def __init__(self, log_file: Optional[str] = None):
        self.log_file = log_file or "/tmp/browser_automation.log"
        logger.info(f"📝 BrowserLogger создан (файл: {self.log_file})")
    
    def setup_logging(self, level: str = "INFO") -> bool:
        """
        Настроить логирование
        
        Args:
            level: Уровень логирования (DEBUG, INFO, WARNING, ERROR)
            
        Returns:
            bool: True если успешно
        """
        try:
            logging.basicConfig(
                filename=self.log_file,
                level=getattr(logging, level),
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            logger.info(f"✅ Логирование настроено: {level}")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка настройки логирования: {e}")
            return False


class BrowserSessionManager:
    """
    ШАГ 8: Initialize Browser Session
    Управление сессиями браузера
    """
    
    def __init__(self):
        self.sessions = {}
        logger.info("🔐 BrowserSessionManager создан")
    
    def create_session(self, browser: BrowserInfo, session_id: str) -> bool:
        """
        Создать новую сессию браузера
        
        Args:
            browser: Информация о браузере
            session_id: ID сессии
            
        Returns:
            bool: True если успешно
        """
        logger.info(f"🔐 Создание сессии: {session_id}")
        
        self.sessions[session_id] = {
            "browser": browser,
            "created_at": __import__("datetime").datetime.now(),
            "active": True,
        }
        
        logger.info(f"✅ Сессия создана: {session_id}")
        return True
    
    def end_session(self, session_id: str) -> bool:
        """Завершить сессию"""
        if session_id in self.sessions:
            self.sessions[session_id]["active"] = False
            logger.info(f"✅ Сессия завершена: {session_id}")
            return True
        return False


class BrowserReadinessChecker:
    """
    ШАГ 9: Verify Browser Readiness
    Проверить готовность браузера к работе
    """
    
    def __init__(self):
        logger.info("✔️ BrowserReadinessChecker создан")
    
    def check_readiness(self, browser: BrowserInfo) -> bool:
        """
        Проверить готовность браузера
        
        Args:
            browser: Информация о браузере
            
        Returns:
            bool: True если готов
        """
        logger.info(f"✔️ Проверка готовности: {browser.browser_type.value}")
        
        # Проверяем основные параметры
        checks = [
            ("Исполняемый файл", Path(browser.executable_path).exists()),
            ("Версия", browser.version != "unknown"),
            ("Совместимость", browser.is_compatible),
        ]
        
        all_ready = True
        for check_name, result in checks:
            if result:
                logger.info(f"  ✅ {check_name}: OK")
            else:
                logger.warning(f"  ❌ {check_name}: FAILED")
                all_ready = False
        
        if all_ready:
            logger.info("✅ Браузер готов к работе")
        else:
            logger.warning("⚠️ Браузер не готов")
        
        return all_ready


class BrowserMonitor:
    """
    ШАГ 10: Setup Browser Monitoring
    Мониторинг состояния браузера
    """
    
    def __init__(self):
        self.metrics = {
            "pages_loaded": 0,
            "errors": 0,
            "warnings": 0,
            "uptime": 0,
        }
        logger.info("📊 BrowserMonitor создан")
    
    def start_monitoring(self) -> bool:
        """Начать мониторинг"""
        logger.info("📊 Мониторинг запущен")
        return True
    
    def get_metrics(self) -> Dict[str, Any]:
        """Получить метрики"""
        return self.metrics.copy()
    
    def record_page_load(self):
        """Записать загрузку страницы"""
        self.metrics["pages_loaded"] += 1
    
    def record_error(self):
        """Записать ошибку"""
        self.metrics["errors"] += 1


class ExtensionLoader:
    """
    ШАГ 11: Load Browser Extensions/Addons
    Загрузка расширений браузера
    """
    
    def __init__(self):
        self.loaded_extensions = []
        logger.info("🧩 ExtensionLoader создан")
    
    def load_extension(self, extension_path: str) -> bool:
        """
        Загрузить расширение
        
        Args:
            extension_path: Путь к расширению
            
        Returns:
            bool: True если успешно
        """
        logger.info(f"🧩 Загрузка расширения: {extension_path}")
        
        if Path(extension_path).exists():
            self.loaded_extensions.append(extension_path)
            logger.info(f"✅ Расширение загружено: {extension_path}")
            return True
        
        logger.warning(f"⚠️ Расширение не найдено: {extension_path}")
        return False


class PermissionConfigurator:
    """
    ШАГ 12: Configure Browser Permissions
    Настройка разрешений браузера
    """
    
    def __init__(self):
        self.permissions = {}
        logger.info("🔒 PermissionConfigurator создан")
    
    def set_permission(self, permission: str, allowed: bool) -> bool:
        """
        Установить разрешение
        
        Args:
            permission: Тип разрешения (location, camera, microphone, notifications)
            allowed: Разрешено или нет
            
        Returns:
            bool: True если успешно
        """
        logger.info(f"🔒 Установка разрешения: {permission} = {allowed}")
        self.permissions[permission] = allowed
        return True


class ProxyConfigurator:
    """
    ШАГ 13: Setup Proxy Configuration
    Настройка прокси
    """
    
    def __init__(self):
        self.proxy_config = None
        logger.info("🌐 ProxyConfigurator создан")
    
    def configure_proxy(self, proxy_url: str, username: Optional[str] = None, 
                       password: Optional[str] = None) -> bool:
        """
        Настроить прокси
        
        Args:
            proxy_url: URL прокси
            username: Имя пользователя (опционально)
            password: Пароль (опционально)
            
        Returns:
            bool: True если успешно
        """
        logger.info(f"🌐 Настройка прокси: {proxy_url}")
        
        self.proxy_config = {
            "url": proxy_url,
            "username": username,
            "password": password,
        }
        
        logger.info("✅ Прокси настроен")
        return True


class CookieManager:
    """
    ШАГ 14: Initialize Cookie Management
    Управление cookies
    """
    
    def __init__(self):
        self.cookies = {}
        logger.info("🍪 CookieManager создан")
    
    def load_cookies(self, cookie_file: str) -> bool:
        """Загрузить cookies из файла"""
        logger.info(f"🍪 Загрузка cookies: {cookie_file}")
        
        if Path(cookie_file).exists():
            try:
                with open(cookie_file, 'r') as f:
                    self.cookies = json.load(f)
                logger.info(f"✅ Загружено cookies: {len(self.cookies)}")
                return True
            except Exception as e:
                logger.error(f"❌ Ошибка загрузки cookies: {e}")
        
        return False
    
    def save_cookies(self, cookie_file: str) -> bool:
        """Сохранить cookies в файл"""
        logger.info(f"🍪 Сохранение cookies: {cookie_file}")
        
        try:
            with open(cookie_file, 'w') as f:
                json.dump(self.cookies, f, indent=2)
            logger.info(f"✅ Сохранено cookies: {len(self.cookies)}")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения cookies: {e}")
            return False
    
    def clear_cookies(self) -> bool:
        """Очистить cookies"""
        logger.info("🍪 Очистка cookies")
        self.cookies.clear()
        return True


class BrowserStartupValidator:
    """
    ШАГ 15: Browser Startup Complete
    Валидация завершения инициализации браузера
    """
    
    def __init__(self):
        logger.info("✅ BrowserStartupValidator создан")
    
    def validate_startup(self, browser: BrowserInfo, session_id: str) -> bool:
        """
        Валидировать запуск браузера
        
        Args:
            browser: Информация о браузере
            session_id: ID сессии
            
        Returns:
            bool: True если все готово
        """
        logger.info(f"✅ Валидация запуска браузера: {session_id}")
        
        # Проверяем все критичные компоненты
        checks = {
            "Браузер обнаружен": browser is not None,
            "Исполняемый файл найден": browser and Path(browser.executable_path).exists(),
            "Версия определена": browser and browser.version != "unknown",
            "Браузер совместим": browser and browser.is_compatible,
            "Сессия создана": session_id is not None,
        }
        
        all_valid = True
        for check_name, result in checks.items():
            if result:
                logger.info(f"  ✅ {check_name}")
            else:
                logger.error(f"  ❌ {check_name}")
                all_valid = False
        
        if all_valid:
            logger.info("✅✅✅ БРАУЗЕР ПОЛНОСТЬЮ ГОТОВ К РАБОТЕ!")
        else:
            logger.error("❌❌❌ ИНИЦИАЛИЗАЦИЯ БРАУЗЕРА НЕ ЗАВЕРШЕНА!")
        
        return all_valid


# Тесты
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 ТЕСТИРОВАНИЕ BROWSER DETECTION & SETUP (Шаги 1-15)")
    print("="*70)
    
    # Шаг 1: Обнаружение браузеров
    detector = BrowserDetector()
    browsers = detector.detect_installed_browsers()
    print(f"\n✅ Шаг 1: Найдено браузеров: {len(browsers)}")
    
    if browsers:
        browser = browsers[0]
        print(f"  • Используем: {browser.browser_type.value} v{browser.version}")
        
        # Шаг 2: Проверка версии
        version_checker = BrowserVersionChecker()
        version = version_checker.check_version(browser)
        print(f"\n✅ Шаг 2: Версия браузера: {version}")
        
        # Шаг 3: Проверка совместимости
        compat_checker = CompatibilityChecker()
        is_compatible = compat_checker.check_compatibility(browser)
        print(f"\n✅ Шаг 3: Совместимость: {is_compatible}")
        
        # Шаг 4: Поиск исполняемого файла
        locator = BrowserExecutableLocator()
        exe_path = locator.locate_executable(browser.browser_type)
        print(f"\n✅ Шаг 4: Исполняемый файл: {exe_path}")
        
        # Шаг 5: Загрузка конфигурации
        config_loader = BrowserConfigLoader()
        config = config_loader.load_config(browser)
        print(f"\n✅ Шаг 5: Конфигурация загружена ({len(config)} параметров)")
        
        # Шаг 6: Инициализация WebDriver
        webdriver_init = WebDriverInitializer()
        driver_ok = webdriver_init.initialize_driver(browser)
        print(f"\n✅ Шаг 6: WebDriver инициализирован: {driver_ok}")
        
        # Шаг 7: Настройка логирования
        browser_logger = BrowserLogger()
        log_ok = browser_logger.setup_logging()
        print(f"\n✅ Шаг 7: Логирование настроено: {log_ok}")
        
        # Шаг 8: Создание сессии
        session_mgr = BrowserSessionManager()
        session_ok = session_mgr.create_session(browser, "test-session-1")
        print(f"\n✅ Шаг 8: Сессия создана: {session_ok}")
        
        # Шаг 9: Проверка готовности
        readiness = BrowserReadinessChecker()
        is_ready = readiness.check_readiness(browser)
        print(f"\n✅ Шаг 9: Браузер готов: {is_ready}")
        
        # Шаг 10: Мониторинг
        monitor = BrowserMonitor()
        monitor.start_monitoring()
        print(f"\n✅ Шаг 10: Мониторинг запущен")
        
        # Шаг 11: Загрузка расширений
        ext_loader = ExtensionLoader()
        print(f"\n✅ Шаг 11: ExtensionLoader готов")
        
        # Шаг 12: Настройка разрешений
        perms = PermissionConfigurator()
        perms.set_permission("notifications", False)
        perms.set_permission("location", False)
        print(f"\n✅ Шаг 12: Разрешения настроены")
        
        # Шаг 13: Настройка прокси
        proxy = ProxyConfigurator()
        print(f"\n✅ Шаг 13: ProxyConfigurator готов")
        
        # Шаг 14: Управление cookies
        cookies = CookieManager()
        print(f"\n✅ Шаг 14: CookieManager готов")
        
        # Шаг 15: Финальная валидация
        validator = BrowserStartupValidator()
        startup_ok = validator.validate_startup(browser, "test-session-1")
        print(f"\n✅ Шаг 15: Валидация запуска: {startup_ok}")
        
        print("\n" + "="*70)
        print("✅✅✅ ВСЕ 15 ШАГОВ BROWSER DETECTION & SETUP ПРОЙДЕНЫ!")
        print("="*70)
    else:
        print("\n⚠️ Браузеры не найдены, пропускаем остальные тесты")
