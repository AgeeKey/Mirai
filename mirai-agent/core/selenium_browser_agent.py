#!/usr/bin/env python3
"""
🤖 SELENIUM BROWSER AGENT - Настоящая автоматизация браузера
============================================================

Агент для РЕАЛЬНОГО управления браузером через Selenium:
- Полный контроль над браузером
- Взаимодействие с элементами
- Заполнение форм
- Выполнение JavaScript
- Скриншоты и запись действий

Автор: MIRAI Team  
Дата: 2025-10-25
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# Опциональный импорт Selenium (может быть не установлен)
try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False
    logger.warning("⚠️ Selenium не установлен. Для использования установите: pip install selenium")


class SeleniumBrowserAgent:
    """
    Агент для настоящей автоматизации браузера через Selenium.
    
    Возможности:
    - Запуск и управление браузером
    - Навигация по страницам
    - Поиск и взаимодействие с элементами
    - Заполнение форм
    - Выполнение JavaScript
    - Скриншоты
    """
    
    def __init__(self, headless: bool = False):
        """
        Инициализация агента.
        
        Args:
            headless: Запускать браузер в headless режиме
        """
        if not SELENIUM_AVAILABLE:
            raise ImportError(
                "Selenium не установлен. Установите: pip install selenium"
            )
        
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        logger.info("✅ SeleniumBrowserAgent создан")
    
    async def initialize(self):
        """Инициализация и запуск браузера"""
        if self.driver:
            logger.warning("⚠️ Браузер уже запущен")
            return
        
        logger.info("🚀 Запуск браузера...")
        
        # Настройки Chrome
        options = ChromeOptions()
        
        if self.headless:
            options.add_argument('--headless')
        
        # Общие настройки для стабильности
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        
        # Отключаем предупреждения и логи
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # User agent
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
        
        try:
            # Запускаем браузер
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 10)
            
            logger.info("✅ Браузер запущен успешно")
            
        except Exception as e:
            logger.error(f"❌ Не удалось запустить браузер: {e}")
            raise
    
    async def search_google(self, query: str) -> Dict[str, Any]:
        """
        Поиск в Google с РЕАЛЬНЫМ взаимодействием.
        
        Args:
            query: Поисковый запрос
            
        Returns:
            Результаты поиска
        """
        if not self.driver:
            await self.initialize()
        
        logger.info(f"🔍 Google поиск: {query}")
        
        try:
            # 1. Открываем Google
            self.driver.get('https://www.google.com')
            await asyncio.sleep(1)
            
            # 2. Находим поле поиска
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, 'q'))
            )
            
            # 3. Вводим запрос
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # 4. Ждём загрузки результатов
            self.wait.until(
                EC.presence_of_element_located((By.ID, 'search'))
            )
            await asyncio.sleep(1)
            
            # 5. Извлекаем результаты
            results = []
            search_results = self.driver.find_elements(By.CSS_SELECTOR, 'div.g')
            
            for result in search_results[:10]:
                try:
                    # Заголовок
                    title_elem = result.find_element(By.CSS_SELECTOR, 'h3')
                    title = title_elem.text
                    
                    # Ссылка
                    link_elem = result.find_element(By.CSS_SELECTOR, 'a')
                    url = link_elem.get_attribute('href')
                    
                    # Описание
                    try:
                        snippet_elem = result.find_element(
                            By.CSS_SELECTOR, 
                            'div[data-sncf], div.VwiC3b, span.aCOpRe'
                        )
                        snippet = snippet_elem.text
                    except:
                        snippet = ''
                    
                    if title and url:
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet
                        })
                        
                except Exception as e:
                    logger.debug(f"Ошибка извлечения результата: {e}")
                    continue
            
            logger.info(f"✅ Найдено {len(results)} результатов")
            
            return {
                'success': True,
                'query': query,
                'results': results,
                'count': len(results)
            }
            
        except Exception as e:
            logger.error(f"❌ Ошибка поиска: {e}")
            return {
                'success': False,
                'query': query,
                'error': str(e)
            }
    
    async def visit_and_read(self, url: str) -> Optional[str]:
        """
        Посетить сайт и прочитать контент.
        
        Args:
            url: URL сайта
            
        Returns:
            Текст страницы или None
        """
        if not self.driver:
            await self.initialize()
        
        logger.info(f"📄 Загрузка страницы: {url}")
        
        try:
            # Переходим на сайт
            self.driver.get(url)
            
            # Ждём загрузки
            await asyncio.sleep(2)
            
            # Извлекаем текст
            # Пытаемся найти основной контент
            try:
                main_content = self.driver.find_element(
                    By.CSS_SELECTOR, 
                    'article, main, div.content, div.post, body'
                )
                text = main_content.text
            except:
                text = self.driver.find_element(By.TAG_NAME, 'body').text
            
            logger.info(f"✅ Прочитано {len(text)} символов")
            return text
            
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки {url}: {e}")
            return None
    
    async def click_element(
        self, 
        selector: str, 
        by: By = By.CSS_SELECTOR
    ) -> bool:
        """
        Кликнуть по элементу.
        
        Args:
            selector: Селектор элемента
            by: Тип селектора (CSS, XPATH, и т.д.)
            
        Returns:
            True если успешно
        """
        if not self.driver:
            await self.initialize()
        
        try:
            element = self.wait.until(
                EC.element_to_be_clickable((by, selector))
            )
            element.click()
            logger.info(f"✅ Клик по элементу: {selector}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Не удалось кликнуть: {e}")
            return False
    
    async def fill_input(
        self,
        selector: str,
        text: str,
        by: By = By.CSS_SELECTOR
    ) -> bool:
        """
        Заполнить поле ввода.
        
        Args:
            selector: Селектор поля
            text: Текст для ввода
            by: Тип селектора
            
        Returns:
            True если успешно
        """
        if not self.driver:
            await self.initialize()
        
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, selector))
            )
            element.clear()
            element.send_keys(text)
            logger.info(f"✅ Заполнено поле: {selector}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Не удалось заполнить поле: {e}")
            return False
    
    async def execute_javascript(self, script: str) -> Any:
        """
        Выполнить JavaScript код.
        
        Args:
            script: JavaScript код
            
        Returns:
            Результат выполнения
        """
        if not self.driver:
            await self.initialize()
        
        try:
            result = self.driver.execute_script(script)
            logger.info(f"✅ JavaScript выполнен")
            return result
            
        except Exception as e:
            logger.error(f"❌ Ошибка выполнения JavaScript: {e}")
            return None
    
    async def take_screenshot(
        self,
        filename: Optional[str] = None
    ) -> Optional[str]:
        """
        Сделать скриншот страницы.
        
        Args:
            filename: Имя файла для сохранения
            
        Returns:
            Путь к сохранённому файлу или None
        """
        if not self.driver:
            await self.initialize()
        
        try:
            if not filename:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
            
            filepath = Path(filename)
            self.driver.save_screenshot(str(filepath))
            
            logger.info(f"✅ Скриншот сохранён: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания скриншота: {e}")
            return None
    
    async def get_current_url(self) -> Optional[str]:
        """Получить текущий URL"""
        if not self.driver:
            return None
        return self.driver.current_url
    
    async def get_page_title(self) -> Optional[str]:
        """Получить заголовок страницы"""
        if not self.driver:
            return None
        return self.driver.title
    
    async def close(self):
        """Закрыть браузер"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("🔒 Браузер закрыт")
            except:
                pass
            finally:
                self.driver = None
                self.wait = None


# ============================================================================
# Функции для удобного использования
# ============================================================================

async def search_with_selenium(query: str, headless: bool = False) -> Dict[str, Any]:
    """
    Быстрый поиск через Selenium.
    
    Args:
        query: Поисковый запрос
        headless: Запускать браузер в headless режиме
        
    Returns:
        Результаты поиска
    """
    agent = SeleniumBrowserAgent(headless=headless)
    try:
        await agent.initialize()
        results = await agent.search_google(query)
        return results
    finally:
        await agent.close()


if __name__ == "__main__":
    # Тест агента
    async def test():
        if not SELENIUM_AVAILABLE:
            print("❌ Selenium не установлен")
            return
        
        print("🚀 Тест SeleniumBrowserAgent")
        print("=" * 70)
        
        agent = SeleniumBrowserAgent(headless=False)
        
        try:
            # Инициализация
            await agent.initialize()
            print("✅ Браузер запущен")
            
            # Поиск
            results = await agent.search_google("Python programming")
            
            print(f"\n🔍 Найдено результатов: {results['count']}")
            for i, result in enumerate(results['results'][:3], 1):
                print(f"\n{i}. {result['title']}")
                print(f"   {result['url']}")
            
            # Скриншот
            screenshot = await agent.take_screenshot("test_search.png")
            if screenshot:
                print(f"\n📸 Скриншот сохранён: {screenshot}")
            
            # Пауза для просмотра
            print("\nБраузер останется открытым 5 секунд...")
            await asyncio.sleep(5)
            
        finally:
            await agent.close()
            print("\n✅ Тест завершён")
    
    asyncio.run(test())
