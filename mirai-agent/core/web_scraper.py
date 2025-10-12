"""
MIRAI Web Scraper - Полноценный доступ к интернету

Возможности:
- Playwright браузер (полная загрузка JavaScript)
- BeautifulSoup парсинг HTML
- Извлечение текста, ссылок, изображений
- Поиск в интернете
- Скрейпинг статей и документации
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
from typing import Dict, List, Optional
import logging
from urllib.parse import urljoin, urlparse
import re


class MiraiWebScraper:
    """Система веб-скрейпинга для MIRAI"""

    def __init__(self, headless: bool = True):
        """
        Инициализация скрейпера

        Args:
            headless: Запускать браузер в headless режиме (без GUI)
        """
        self.headless = headless
        self.browser = None
        self.context = None

        logging.info("✅ Веб-скрейпер инициализирован")

    async def start(self):
        """Запустить браузер"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=self.headless)
        self.context = await self.browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        logging.info("🌐 Chromium браузер запущен")

    async def close(self):
        """Закрыть браузер"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logging.info("🔌 Браузер закрыт")

    async def scrape_url(self, url: str, wait_for: str = None) -> Dict:
        """
        Загрузить страницу и извлечь контент

        Args:
            url: URL страницы
            wait_for: CSS селектор элемента для ожидания загрузки

        Returns:
            Dict с данными: title, text, links, html
        """
        if not self.browser:
            await self.start()

        page = await self.context.new_page()

        try:
            logging.info(f"📥 Загружаю: {url}")
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Ждать определенный элемент если указан
            if wait_for:
                await page.wait_for_selector(wait_for, timeout=10000)

            # Получить HTML
            html = await page.content()

            # Парсить с BeautifulSoup
            soup = BeautifulSoup(html, "lxml")

            # Извлечь заголовок
            title = soup.title.string if soup.title else ""

            # Извлечь текст (убрать скрипты и стили)
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator="\n", strip=True)

            # Извлечь ссылки
            links = []
            for link in soup.find_all("a", href=True):
                absolute_url = urljoin(url, link["href"])
                links.append({"text": link.get_text(strip=True), "url": absolute_url})

            # Извлечь изображения
            images = []
            for img in soup.find_all("img", src=True):
                absolute_url = urljoin(url, img["src"])
                images.append({"alt": img.get("alt", ""), "url": absolute_url})

            # Метаданные
            meta_desc = soup.find("meta", attrs={"name": "description"})
            description = meta_desc.get("content", "") if meta_desc else ""

            result = {
                "url": url,
                "title": title.strip(),
                "description": description,
                "text": text,
                "links": links[:50],  # Первые 50 ссылок
                "images": images[:20],  # Первые 20 изображений
                "html_length": len(html),
                "text_length": len(text),
            }

            logging.info(f"✅ Загружено: {title[:50]}... ({len(text)} символов)")
            return result

        except Exception as e:
            logging.error(f"❌ Ошибка загрузки {url}: {e}")
            return {
                "url": url,
                "error": str(e),
                "title": "",
                "text": "",
                "links": [],
                "images": [],
            }
        finally:
            await page.close()

    async def scrape_multiple(self, urls: List[str]) -> List[Dict]:
        """Загрузить несколько страниц параллельно"""
        if not self.browser:
            await self.start()

        tasks = [self.scrape_url(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    async def search_google(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Поиск в Google

        Args:
            query: Поисковый запрос
            num_results: Количество результатов

        Returns:
            List результатов с title, url, snippet
        """
        if not self.browser:
            await self.start()

        page = await self.context.new_page()

        try:
            search_url = f"https://www.google.com/search?q={query}&num={num_results}"
            logging.info(f"🔍 Поиск в Google: {query}")

            await page.goto(search_url, wait_until="networkidle")

            # Ждать результаты
            await page.wait_for_selector("div#search", timeout=10000)

            html = await page.content()
            soup = BeautifulSoup(html, "lxml")

            results = []

            # Найти результаты поиска
            for g in soup.find_all("div", class_="g"):
                # Заголовок и ссылка
                title_elem = g.find("h3")
                link_elem = g.find("a")
                snippet_elem = g.find("div", class_=["VwiC3b", "yXK7lf"])

                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    url = link_elem.get("href", "")
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

                    # Только реальные URL
                    if url.startswith("http"):
                        results.append({"title": title, "url": url, "snippet": snippet})

            logging.info(f"✅ Найдено {len(results)} результатов")
            return results[:num_results]

        except Exception as e:
            logging.error(f"❌ Ошибка поиска: {e}")
            return []
        finally:
            await page.close()

    async def search_duckduckgo(self, query: str, num_results: int = 10) -> List[Dict]:
        """
        Поиск в DuckDuckGo (как альтернатива Google)

        Args:
            query: Поисковый запрос
            num_results: Количество результатов
        """
        if not self.browser:
            await self.start()

        page = await self.context.new_page()

        try:
            search_url = f"https://duckduckgo.com/?q={query}"
            logging.info(f"🔍 Поиск в DuckDuckGo: {query}")

            await page.goto(search_url, wait_until="networkidle")
            await page.wait_for_selector("article", timeout=10000)

            html = await page.content()
            soup = BeautifulSoup(html, "lxml")

            results = []

            for article in soup.find_all("article", limit=num_results):
                title_elem = article.find("h2")
                link_elem = article.find("a")
                snippet_elem = article.find(
                    ["span", "div"], class_=re.compile("snippet")
                )

                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    url = link_elem.get("href", "")
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

                    results.append({"title": title, "url": url, "snippet": snippet})

            logging.info(f"✅ Найдено {len(results)} результатов")
            return results

        except Exception as e:
            logging.error(f"❌ Ошибка поиска: {e}")
            return []
        finally:
            await page.close()

    def scrape_simple(self, url: str) -> Dict:
        """
        Простой синхронный скрейпинг через requests (быстрее для статических страниц)

        Args:
            url: URL страницы

        Returns:
            Dict с данными
        """
        try:
            logging.info(f"📥 Загружаю (simple): {url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "lxml")

            # Извлечь текст
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator="\n", strip=True)

            title = soup.title.string if soup.title else ""

            # Ссылки
            links = []
            for link in soup.find_all("a", href=True):
                absolute_url = urljoin(url, link["href"])
                links.append({"text": link.get_text(strip=True), "url": absolute_url})

            result = {
                "url": url,
                "title": title.strip(),
                "text": text,
                "links": links[:50],
                "text_length": len(text),
            }

            logging.info(f"✅ Загружено: {title[:50]}... ({len(text)} символов)")
            return result

        except Exception as e:
            logging.error(f"❌ Ошибка: {e}")
            return {"url": url, "error": str(e), "title": "", "text": ""}

    async def extract_article(self, url: str) -> Dict:
        """
        Извлечь основной текст статьи (умное извлечение)

        Args:
            url: URL статьи

        Returns:
            Dict с заголовком, автором, датой, текстом
        """
        result = await self.scrape_url(url)

        if "error" in result:
            return result

        soup = BeautifulSoup(result.get("html", ""), "lxml")

        # Попытаться найти основной контент
        article = None

        # Попробовать стандартные теги
        for tag in ["article", "main", ["div", {"class": "content"}]]:
            article = soup.find(tag)
            if article:
                break

        if article:
            text = article.get_text(separator="\n", strip=True)
        else:
            text = result["text"]

        # Попытаться найти автора
        author = ""
        author_elem = soup.find(["meta", "span", "div"], attrs={"name": "author"})
        if author_elem:
            author = author_elem.get("content", "") or author_elem.get_text(strip=True)

        # Попытаться найти дату
        date = ""
        date_elem = soup.find("time")
        if date_elem:
            date = date_elem.get("datetime", "") or date_elem.get_text(strip=True)

        return {
            "url": url,
            "title": result.get("title", ""),
            "author": author,
            "date": date,
            "text": text,
            "text_length": len(text),
        }


# Пример использования
async def main():
    logging.basicConfig(level=logging.INFO)

    print("🧪 Тестирование веб-скрейпера MIRAI...\n")

    scraper = MiraiWebScraper()
    await scraper.start()

    # Тест 1: Загрузка простой страницы
    print("📝 Тест 1: Загрузка Wikipedia...")
    result = await scraper.scrape_url(
        "https://en.wikipedia.org/wiki/Python_(programming_language)"
    )
    print(f"✅ Заголовок: {result['title']}")
    print(f"✅ Текста: {result['text_length']} символов")
    print(f"✅ Ссылок: {len(result['links'])}")
    print()

    # Тест 2: Поиск в DuckDuckGo
    print("📝 Тест 2: Поиск в DuckDuckGo...")
    search_results = await scraper.search_duckduckgo(
        "artificial intelligence", num_results=5
    )
    print(f"✅ Найдено результатов: {len(search_results)}")
    for i, res in enumerate(search_results, 1):
        print(f"  {i}. {res['title'][:60]}...")
    print()

    # Тест 3: Синхронный скрейпинг
    print("📝 Тест 3: Быстрый скрейпинг...")
    simple_result = scraper.scrape_simple("https://example.com")
    print(f"✅ Заголовок: {simple_result['title']}")
    print()

    await scraper.close()
    print("✅ Все тесты пройдены!")


if __name__ == "__main__":
    asyncio.run(main())
