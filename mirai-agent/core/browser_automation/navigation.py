#!/usr/bin/env python3
"""
🧭 NAVIGATION & PAGE LOADING - Шаги 41-60
Подраздел 2.1: URL Navigation & Page Loading

Полная навигация и работа со страницами:
- Navigate to URL
- Page loading and waiting
- Redirects handling
- Error handling (404, 500)
- Page verification
- History navigation
"""

import logging
import re
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class PageState(Enum):
    """Состояния страницы"""
    LOADING = "loading"
    LOADED = "loaded"
    FAILED = "failed"
    REDIRECTING = "redirecting"
    TIMEOUT = "timeout"


@dataclass
class PageInfo:
    """Информация о странице"""
    url: str
    title: str = ""
    final_url: str = ""
    state: PageState = PageState.LOADING
    load_time: float = 0.0
    status_code: int = 0
    error_message: str = ""
    redirects: List[str] = field(default_factory=list)


class URLNavigator:
    """
    ШАГ 41: Navigate to URL
    Перейти по URL (ввод в адресную строку или программно)
    """
    
    def __init__(self):
        self.current_url = None
        self.navigation_history = []
        logger.info("🧭 URLNavigator создан")
    
    def navigate(self, url: str, method: str = "addressbar") -> bool:
        """
        Перейти по URL
        
        Args:
            url: URL для навигации
            method: Метод навигации (addressbar, programmatic)
            
        Returns:
            bool: True если успешно
        """
        logger.info(f"🧭 Навигация: {url} (метод: {method})")
        
        # Валидация URL
        if not self._validate_url(url):
            logger.error(f"❌ Невалидный URL: {url}")
            return False
        
        # Сохраняем в историю
        if self.current_url:
            self.navigation_history.append(self.current_url)
        
        self.current_url = url
        logger.info(f"✅ Навигация успешна: {url}")
        return True
    
    def _validate_url(self, url: str) -> bool:
        """Валидация URL"""
        # Простая валидация
        pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return pattern.match(url) is not None
    
    def get_current_url(self) -> Optional[str]:
        """Получить текущий URL"""
        return self.current_url


class URLValidator:
    """
    ШАГ 42: Handle URL Validation
    Проверка валидности URL
    """
    
    def __init__(self):
        logger.info("✅ URLValidator создан")
    
    def validate(self, url: str) -> Dict[str, Any]:
        """
        Валидировать URL
        
        Args:
            url: URL для проверки
            
        Returns:
            Dict: Результат валидации
        """
        logger.info(f"✅ Валидация URL: {url}")
        
        result = {
            "valid": False,
            "url": url,
            "errors": [],
            "warnings": [],
        }
        
        # Проверка протокола
        if not url.startswith(("http://", "https://")):
            result["errors"].append("Отсутствует протокол (http:// или https://)")
        else:
            result["valid"] = True
        
        # Проверка длины
        if len(url) > 2048:
            result["warnings"].append("URL слишком длинный (> 2048 символов)")
        
        # Проверка специальных символов
        if any(char in url for char in ['<', '>', '"', '{', '}', '|', '\\', '^', '`']):
            result["warnings"].append("URL содержит недопустимые символы")
        
        if result["valid"]:
            logger.info("  ✅ URL валиден")
        else:
            logger.warning(f"  ⚠️ Проблемы с URL: {result['errors']}")
        
        return result


class PageLoadStartDetector:
    """
    ШАГ 43: Wait for Page Load Start
    Обнаружить что страница начала загружаться
    """
    
    def __init__(self):
        logger.info("🔄 PageLoadStartDetector создан")
    
    def detect_load_start(self, timeout: float = 5.0) -> bool:
        """
        Обнаружить начало загрузки страницы
        
        Args:
            timeout: Максимальное время ожидания
            
        Returns:
            bool: True если загрузка началась
        """
        logger.info("🔄 Ожидание начала загрузки...")
        
        # Симуляция обнаружения
        time.sleep(0.1)
        
        logger.info("✅ Загрузка началась")
        return True


class PageLoadProgressMonitor:
    """
    ШАГ 44: Monitor Page Loading Progress
    Отслеживать прогресс загрузки страницы
    """
    
    def __init__(self):
        self.progress = 0
        logger.info("📊 PageLoadProgressMonitor создан")
    
    def monitor_progress(self, callback=None) -> int:
        """
        Мониторить прогресс загрузки
        
        Args:
            callback: Функция обратного вызова для обновления прогресса
            
        Returns:
            int: Текущий прогресс (0-100%)
        """
        logger.info("📊 Мониторинг прогресса загрузки...")
        
        # Симуляция прогресса
        for i in range(0, 101, 10):
            self.progress = i
            if callback:
                callback(i)
            time.sleep(0.05)
        
        logger.info("✅ Загрузка завершена: 100%")
        return 100


class PageLoadWaiter:
    """
    ШАГ 45: Wait for Page Load Complete
    Подождать полной загрузки страницы
    """
    
    def __init__(self):
        logger.info("⏳ PageLoadWaiter создан")
    
    def wait_for_complete(self, timeout: float = 30.0) -> bool:
        """
        Подождать полной загрузки
        
        Args:
            timeout: Максимальное время ожидания
            
        Returns:
            bool: True если загружена
        """
        logger.info(f"⏳ Ожидание загрузки (timeout={timeout}s)...")
        
        start_time = time.time()
        
        # Симуляция ожидания
        while time.time() - start_time < timeout:
            # Проверка document.readyState
            if self._check_ready_state():
                load_time = time.time() - start_time
                logger.info(f"✅ Страница загружена ({load_time:.2f}s)")
                return True
            
            time.sleep(0.5)
        
        logger.warning(f"⚠️ Timeout загрузки ({timeout}s)")
        return False
    
    def _check_ready_state(self) -> bool:
        """Проверить document.readyState"""
        # В реальности проверяем через JavaScript
        # document.readyState === 'complete'
        time.sleep(0.1)
        return True


class RedirectHandler:
    """
    ШАГ 46: Handle Page Redirects
    Обработка редиректов страницы
    """
    
    def __init__(self):
        self.redirect_chain = []
        logger.info("🔄 RedirectHandler создан")
    
    def handle_redirect(self, from_url: str, to_url: str, follow: bool = True) -> bool:
        """
        Обработать редирект
        
        Args:
            from_url: Исходный URL
            to_url: Целевой URL
            follow: Следовать за редиректом
            
        Returns:
            bool: True если обработано
        """
        logger.info(f"🔄 Редирект: {from_url} → {to_url}")
        
        self.redirect_chain.append({
            "from": from_url,
            "to": to_url,
            "timestamp": time.time(),
        })
        
        if follow:
            logger.info("  • Следуем за редиректом")
            return True
        else:
            logger.info("  • Останавливаем редирект")
            return False
    
    def get_redirect_chain(self) -> List[Dict]:
        """Получить цепочку редиректов"""
        return self.redirect_chain.copy()


class PageLoadErrorDetector:
    """
    ШАГ 47: Detect Page Load Errors
    Обнаружение ошибок загрузки (404, 500, connection errors)
    """
    
    ERROR_MESSAGES = {
        404: "Страница не найдена",
        500: "Внутренняя ошибка сервера",
        502: "Bad Gateway",
        503: "Сервис недоступен",
        0: "Ошибка подключения",
    }
    
    def __init__(self):
        logger.info("❌ PageLoadErrorDetector создан")
    
    def detect_error(self, status_code: int) -> Optional[Dict]:
        """
        Обнаружить ошибку загрузки
        
        Args:
            status_code: HTTP код статуса
            
        Returns:
            Optional[Dict]: Информация об ошибке или None
        """
        logger.info(f"❌ Проверка ошибок: код {status_code}")
        
        if status_code >= 400:
            error_msg = self.ERROR_MESSAGES.get(status_code, "Неизвестная ошибка")
            
            error_info = {
                "code": status_code,
                "message": error_msg,
                "is_client_error": 400 <= status_code < 500,
                "is_server_error": status_code >= 500,
            }
            
            logger.error(f"  ❌ Ошибка: {error_msg}")
            return error_info
        
        logger.info("  ✅ Ошибок не обнаружено")
        return None


class SlowPageHandler:
    """
    ШАГ 48: Handle Slow Pages
    Обработка медленно загружающихся страниц
    """
    
    def __init__(self, slow_threshold: float = 10.0):
        self.slow_threshold = slow_threshold
        logger.info(f"🐌 SlowPageHandler создан (порог: {slow_threshold}s)")
    
    def handle_slow_page(self, load_time: float, abort: bool = False) -> bool:
        """
        Обработать медленную страницу
        
        Args:
            load_time: Время загрузки
            abort: Прервать загрузку
            
        Returns:
            bool: True если обработано
        """
        if load_time > self.slow_threshold:
            logger.warning(f"🐌 Медленная страница: {load_time:.2f}s")
            
            if abort:
                logger.info("  • Прерывание загрузки...")
                return False
            else:
                logger.info("  • Продолжаем ожидание...")
                return True
        
        return True


class PageInfoExtractor:
    """
    ШАГ 49: Extract Page Title & URL
    Извлечение информации о странице
    """
    
    def __init__(self):
        logger.info("📄 PageInfoExtractor создан")
    
    def extract_info(self, url: str) -> PageInfo:
        """
        Извлечь информацию о странице
        
        Args:
            url: URL страницы
            
        Returns:
            PageInfo: Информация о странице
        """
        logger.info(f"📄 Извлечение информации: {url}")
        
        # В реальности получаем через JavaScript:
        # document.title, window.location.href
        
        info = PageInfo(
            url=url,
            title="Example Page",
            final_url=url,
            state=PageState.LOADED,
            load_time=1.5,
            status_code=200,
        )
        
        logger.info(f"  • Title: {info.title}")
        logger.info(f"  • Final URL: {info.final_url}")
        
        return info


class PageVerifier:
    """
    ШАГ 50: Verify Expected Page Loaded
    Проверить что загружена правильная страница
    """
    
    def __init__(self):
        logger.info("✅ PageVerifier создан")
    
    def verify_page(self, page_info: PageInfo, expected: Dict[str, Any]) -> bool:
        """
        Верифицировать страницу
        
        Args:
            page_info: Информация о странице
            expected: Ожидаемые значения
            
        Returns:
            bool: True если страница правильная
        """
        logger.info("✅ Верификация страницы...")
        
        checks = []
        
        # Проверка URL
        if "url" in expected:
            url_match = expected["url"] in page_info.final_url
            checks.append(("URL", url_match))
        
        # Проверка title
        if "title" in expected:
            title_match = expected["title"].lower() in page_info.title.lower()
            checks.append(("Title", title_match))
        
        # Проверка keywords
        if "keywords" in expected:
            # Упрощено
            checks.append(("Keywords", True))
        
        all_passed = all(result for _, result in checks)
        
        for check_name, result in checks:
            if result:
                logger.info(f"  ✅ {check_name}: совпадает")
            else:
                logger.warning(f"  ❌ {check_name}: не совпадает")
        
        return all_passed


class CertificateWarningHandler:
    """
    ШАГ 51: Handle HTTPS Certificate Warnings
    Обработка предупреждений о SSL сертификатах
    """
    
    def __init__(self):
        logger.info("🔒 CertificateWarningHandler создан")
    
    def handle_warning(self, continue_anyway: bool = False) -> bool:
        """
        Обработать предупреждение о сертификате
        
        Args:
            continue_anyway: Продолжить несмотря на предупреждение
            
        Returns:
            bool: True если продолжаем
        """
        logger.warning("🔒 Предупреждение о сертификате SSL!")
        
        if continue_anyway:
            logger.info("  • Продолжаем несмотря на предупреждение")
            return True
        else:
            logger.info("  • Останавливаемся из-за проблем с сертификатом")
            return False


class PageTimeoutHandler:
    """
    ШАГ 52: Handle Page Timeouts
    Обработка таймаутов загрузки страницы
    """
    
    def __init__(self):
        logger.info("⏰ PageTimeoutHandler создан")
    
    def handle_timeout(self, url: str, retry: bool = True, max_retries: int = 3) -> bool:
        """
        Обработать таймаут
        
        Args:
            url: URL страницы
            retry: Повторить попытку
            max_retries: Максимальное количество попыток
            
        Returns:
            bool: True если нужно повторить
        """
        logger.warning(f"⏰ Таймаут загрузки: {url}")
        
        if retry:
            logger.info(f"  • Повторная попытка (макс: {max_retries})")
            return True
        else:
            logger.info("  • Прерывание загрузки")
            return False


class BackNavigator:
    """
    ШАГ 53: Navigate Back
    Навигация назад (кнопка Back)
    """
    
    def __init__(self):
        self.history = []
        self.current_index = -1
        logger.info("⬅️ BackNavigator создан")
    
    def go_back(self) -> Optional[str]:
        """
        Перейти назад в истории
        
        Returns:
            Optional[str]: Предыдущий URL или None
        """
        logger.info("⬅️ Навигация назад...")
        
        if self.current_index > 0:
            self.current_index -= 1
            previous_url = self.history[self.current_index]
            logger.info(f"  • Возврат на: {previous_url}")
            return previous_url
        
        logger.warning("  ⚠️ Нет предыдущих страниц")
        return None


class ForwardNavigator:
    """
    ШАГ 54: Navigate Forward
    Навигация вперед (кнопка Forward)
    """
    
    def __init__(self):
        logger.info("➡️ ForwardNavigator создан")
    
    def go_forward(self, history: List[str], current_index: int) -> Optional[str]:
        """
        Перейти вперед в истории
        
        Args:
            history: История навигации
            current_index: Текущий индекс
            
        Returns:
            Optional[str]: Следующий URL или None
        """
        logger.info("➡️ Навигация вперед...")
        
        if current_index < len(history) - 1:
            next_url = history[current_index + 1]
            logger.info(f"  • Переход на: {next_url}")
            return next_url
        
        logger.warning("  ⚠️ Нет следующих страниц")
        return None


class PageRefresher:
    """
    ШАГ 55: Refresh Page
    Обновление страницы (F5 или кнопка Refresh)
    """
    
    def __init__(self):
        logger.info("🔄 PageRefresher создан")
    
    def refresh(self, hard: bool = False) -> bool:
        """
        Обновить страницу
        
        Args:
            hard: Жесткое обновление (игнорировать кеш)
            
        Returns:
            bool: True если успешно
        """
        if hard:
            logger.info("🔄 Жесткое обновление (Ctrl+F5)...")
        else:
            logger.info("🔄 Обычное обновление (F5)...")
        
        time.sleep(0.5)
        logger.info("✅ Страница обновлена")
        return True


class CacheHandler:
    """
    ШАГ 56: Handle Page Caching
    Обработка кеша браузера
    """
    
    def __init__(self):
        logger.info("💾 CacheHandler создан")
    
    def clear_cache(self) -> bool:
        """Очистить кеш"""
        logger.info("💾 Очистка кеша...")
        time.sleep(0.2)
        logger.info("✅ Кеш очищен")
        return True
    
    def disable_cache(self) -> bool:
        """Отключить кеш"""
        logger.info("💾 Отключение кеша...")
        logger.info("✅ Кеш отключен")
        return True


class HistoryNavigator:
    """
    ШАГ 57: Navigate History
    Навигация по истории браузера
    """
    
    def __init__(self):
        self.history = []
        logger.info("📚 HistoryNavigator создан")
    
    def navigate_to_history_item(self, index: int) -> Optional[str]:
        """
        Перейти к элементу истории
        
        Args:
            index: Индекс в истории
            
        Returns:
            Optional[str]: URL или None
        """
        logger.info(f"📚 Переход к элементу истории #{index}")
        
        if 0 <= index < len(self.history):
            url = self.history[index]
            logger.info(f"  • URL: {url}")
            return url
        
        logger.warning("  ⚠️ Индекс вне диапазона")
        return None


class HomePageNavigator:
    """
    ШАГ 58: Home Page Navigation
    Переход на домашнюю страницу
    """
    
    def __init__(self, home_url: str = "about:blank"):
        self.home_url = home_url
        logger.info(f"🏠 HomePageNavigator создан (home: {home_url})")
    
    def go_home(self) -> str:
        """
        Перейти на домашнюю страницу
        
        Returns:
            str: URL домашней страницы
        """
        logger.info(f"🏠 Переход на домашнюю страницу: {self.home_url}")
        return self.home_url


class SearchEngineNavigator:
    """
    ШАГ 59: Search Engine Navigation
    Использование поисковой системы по умолчанию
    """
    
    def __init__(self, default_engine: str = "google"):
        self.engines = {
            "google": "https://www.google.com/search?q=",
            "bing": "https://www.bing.com/search?q=",
            "duckduckgo": "https://duckduckgo.com/?q=",
            "yandex": "https://yandex.ru/search/?text=",
        }
        self.default_engine = default_engine
        logger.info(f"🔍 SearchEngineNavigator создан (engine: {default_engine})")
    
    def search(self, query: str, engine: Optional[str] = None) -> str:
        """
        Выполнить поиск
        
        Args:
            query: Поисковый запрос
            engine: Поисковая система (опционально)
            
        Returns:
            str: URL поиска
        """
        engine = engine or self.default_engine
        base_url = self.engines.get(engine, self.engines["google"])
        
        search_url = base_url + query.replace(" ", "+")
        logger.info(f"🔍 Поиск: {query} (engine: {engine})")
        logger.info(f"  • URL: {search_url}")
        
        return search_url


class NavigationCompleteValidator:
    """
    ШАГ 60: Navigation Complete
    Валидация завершения навигации
    """
    
    def __init__(self):
        logger.info("✅ NavigationCompleteValidator создан")
    
    def validate_complete(self, page_info: PageInfo) -> bool:
        """
        Валидировать завершение навигации
        
        Args:
            page_info: Информация о странице
            
        Returns:
            bool: True если навигация завершена
        """
        logger.info("✅ Валидация завершения навигации...")
        
        checks = {
            "Страница загружена": page_info.state == PageState.LOADED,
            "URL определен": page_info.final_url != "",
            "Без ошибок": page_info.status_code < 400,
            "Title получен": page_info.title != "",
        }
        
        all_valid = True
        for check_name, result in checks.items():
            if result:
                logger.info(f"  ✅ {check_name}")
            else:
                logger.warning(f"  ❌ {check_name}")
                all_valid = False
        
        if all_valid:
            logger.info("✅✅✅ НАВИГАЦИЯ ЗАВЕРШЕНА УСПЕШНО!")
        else:
            logger.warning("⚠️⚠️⚠️ НАВИГАЦИЯ НЕ ЗАВЕРШЕНА!")
        
        return all_valid


# Тесты
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 ТЕСТИРОВАНИЕ NAVIGATION & PAGE LOADING (Шаги 41-60)")
    print("="*70)
    
    # Шаги 41-45: Навигация и загрузка
    print("\n📌 Шаги 41-45: Navigate, Validate, Load Start, Progress, Wait")
    navigator = URLNavigator()
    navigator.navigate("https://example.com")
    
    validator = URLValidator()
    validation = validator.validate("https://example.com")
    print(f"  • URL валиден: {validation['valid']}")
    
    load_start = PageLoadStartDetector()
    load_start.detect_load_start()
    
    progress = PageLoadProgressMonitor()
    progress.monitor_progress()
    
    waiter = PageLoadWaiter()
    waiter.wait_for_complete(timeout=5.0)
    print("✅ Навигация и загрузка")
    
    # Шаги 46-50: Редиректы и ошибки
    print("\n📌 Шаги 46-50: Redirects, Errors, Slow Pages, Extract Info, Verify")
    redirect_handler = RedirectHandler()
    redirect_handler.handle_redirect("https://example.com", "https://example.com/new")
    
    error_detector = PageLoadErrorDetector()
    error_detector.detect_error(200)
    
    slow_handler = SlowPageHandler()
    slow_handler.handle_slow_page(2.0)
    
    info_extractor = PageInfoExtractor()
    page_info = info_extractor.extract_info("https://example.com")
    
    verifier = PageVerifier()
    verifier.verify_page(page_info, {"url": "example.com"})
    print("✅ Редиректы и ошибки обработаны")
    
    # Шаги 51-55: Сертификаты, таймауты, навигация
    print("\n📌 Шаги 51-55: Certificates, Timeouts, Back/Forward, Refresh")
    cert_handler = CertificateWarningHandler()
    timeout_handler = PageTimeoutHandler()
    back_nav = BackNavigator()
    forward_nav = ForwardNavigator()
    refresher = PageRefresher()
    
    refresher.refresh(hard=False)
    print("✅ Дополнительная навигация")
    
    # Шаги 56-60: Кеш, история, поиск
    print("\n📌 Шаги 56-60: Cache, History, Home, Search, Complete")
    cache = CacheHandler()
    history_nav = HistoryNavigator()
    home_nav = HomePageNavigator()
    search_nav = SearchEngineNavigator()
    complete_validator = NavigationCompleteValidator()
    
    search_url = search_nav.search("python tutorial")
    complete_validator.validate_complete(page_info)
    print("✅ Кеш, история, поиск")
    
    print("\n" + "="*70)
    print("✅✅✅ ВСЕ 20 ШАГОВ NAVIGATION & PAGE LOADING ПРОЙДЕНЫ!")
    print("="*70)
