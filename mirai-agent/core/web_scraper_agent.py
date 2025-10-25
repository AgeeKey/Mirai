#!/usr/bin/env python3
"""
🌐 WEB SCRAPER AGENT - Реальное извлечение данных из веб-страниц
================================================================

Агент для настоящего парсинга и анализа веб-контента:
- Поиск в Google с извлечением результатов
- Загрузка и парсинг HTML страниц
- Извлечение основного текста
- AI анализ контента
- Реальная автоматизация браузера

Автор: MIRAI Team
Дата: 2025-10-25
"""

import asyncio
import logging
import re
from typing import Any, Dict, List, Optional
from urllib.parse import quote_plus, urlparse

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class WebScraperAgent:
    """
    Агент для скрапинга и анализа веб-страниц.
    
    Возможности:
    - Поиск в Google
    - Парсинг HTML
    - Извлечение текста
    - Анализ через AI
    """
    
    def __init__(self, ai_manager=None):
        """
        Инициализация агента.
        
        Args:
            ai_manager: Менеджер AI моделей для анализа контента
        """
        self.ai = ai_manager
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        })
        logger.info("✅ WebScraperAgent инициализирован")
    
    async def search_and_analyze(
        self,
        query: str,
        num_results: int = 3,
        analyze: bool = True
    ) -> Dict[str, Any]:
        """
        Поиск в Google и анализ результатов.
        
        Args:
            query: Поисковый запрос
            num_results: Количество сайтов для анализа
            analyze: Проводить AI анализ контента
            
        Returns:
            Результаты поиска и анализа
        """
        logger.info(f"🔍 Поиск и анализ: {query}")
        
        # 1. Выполнить поиск в Google
        search_results = await self._google_search(query)
        
        if not search_results:
            return {
                'success': False,
                'query': query,
                'error': 'Не удалось получить результаты поиска'
            }
        
        # 2. Загрузить и парсить топ-N сайтов
        content_list = []
        for i, result in enumerate(search_results[:num_results]):
            logger.info(f"📄 Загрузка сайта {i+1}/{num_results}: {result.get('title', 'N/A')}")
            
            content = await self._scrape_page(result['url'])
            if content:
                content_list.append({
                    'url': result['url'],
                    'title': result['title'],
                    'snippet': result.get('snippet', ''),
                    'content': content
                })
        
        # 3. AI анализ контента
        analysis = None
        if analyze and self.ai and content_list:
            logger.info("🧠 AI анализ контента...")
            analysis = await self._analyze_content(query, content_list)
        
        return {
            'success': True,
            'query': query,
            'search_results': search_results,
            'scraped_content': content_list,
            'analysis': analysis,
            'summary': {
                'total_results': len(search_results),
                'scraped_pages': len(content_list),
                'analyzed': analysis is not None
            }
        }
    
    async def _google_search(self, query: str) -> List[Dict[str, str]]:
        """
        Поиск в Google и извлечение результатов.
        
        Args:
            query: Поисковый запрос
            
        Returns:
            Список результатов с URL, заголовками и сниппетами
        """
        try:
            # Формируем URL поиска
            encoded_query = quote_plus(query)
            search_url = f"https://www.google.com/search?q={encoded_query}&hl=ru"
            
            logger.info(f"🔍 Google поиск: {search_url}")
            
            # Выполняем запрос
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            # Парсим HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Извлекаем результаты
            results = []
            
            # Ищем блоки результатов (Google часто меняет структуру)
            for g in soup.select('div.g, div[data-sokoban-container]'):
                try:
                    # Заголовок
                    title_elem = g.select_one('h3')
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)
                    
                    # Ссылка
                    link_elem = g.select_one('a')
                    if not link_elem or not link_elem.get('href'):
                        continue
                    url = link_elem['href']
                    
                    # Убираем Google редиректы
                    if url.startswith('/url?q='):
                        url = url.split('/url?q=')[1].split('&')[0]
                    
                    # Проверяем валидность URL
                    if not url.startswith('http'):
                        continue
                    
                    # Сниппет (описание)
                    snippet_elem = g.select_one('div[data-sncf], div.VwiC3b, span.aCOpRe')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet
                    })
                    
                except Exception as e:
                    logger.debug(f"Ошибка парсинга результата: {e}")
                    continue
            
            logger.info(f"✅ Найдено результатов: {len(results)}")
            return results
            
        except Exception as e:
            logger.error(f"❌ Ошибка поиска в Google: {e}")
            return []
    
    async def _scrape_page(self, url: str, max_length: int = 10000) -> Optional[str]:
        """
        Загрузка и извлечение текста со страницы.
        
        Args:
            url: URL страницы
            max_length: Максимальная длина текста
            
        Returns:
            Извлечённый текст или None
        """
        try:
            logger.debug(f"📥 Загрузка: {url}")
            
            # Загружаем страницу
            response = self.session.get(url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            # Парсим HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Удаляем скрипты, стили, навигацию
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']):
                element.decompose()
            
            # Извлекаем основной текст
            # Пытаемся найти основной контент
            main_content = soup.select_one('article, main, div.content, div.post')
            if main_content:
                text = main_content.get_text(separator='\n', strip=True)
            else:
                text = soup.get_text(separator='\n', strip=True)
            
            # Очищаем текст
            lines = [line.strip() for line in text.splitlines()]
            # Убираем пустые строки и очень короткие (меню, кнопки и т.д.)
            lines = [line for line in lines if line and len(line) > 20]
            text = '\n'.join(lines)
            
            # Ограничиваем длину
            if len(text) > max_length:
                text = text[:max_length]
            
            logger.debug(f"✅ Извлечено {len(text)} символов из {url}")
            return text
            
        except Exception as e:
            logger.warning(f"⚠️ Не удалось загрузить {url}: {e}")
            return None
    
    async def _analyze_content(
        self,
        query: str,
        content_list: List[Dict[str, str]]
    ) -> Optional[str]:
        """
        Анализ контента через AI.
        
        Args:
            query: Исходный запрос пользователя
            content_list: Список загруженного контента
            
        Returns:
            AI анализ или None
        """
        if not self.ai:
            logger.warning("⚠️ AI менеджер недоступен")
            return None
        
        try:
            # Формируем промпт
            combined_content = "\n\n---\n\n".join([
                f"Источник: {item['title']}\nURL: {item['url']}\n\n{item['content'][:2000]}"
                for item in content_list
            ])
            
            prompt = f"""Запрос пользователя: {query}

Найденная информация с веб-сайтов:

{combined_content}

Задача: Проанализируй информацию и дай подробный, структурированный ответ на русском языке.
Используй подзаголовки, списки и выделения для лучшей читаемости.
Обязательно укажи источники информации."""
            
            # Вызываем AI (предполагается что есть метод chat_completion)
            if hasattr(self.ai, 'chat_completion'):
                response = await self.ai.chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    task_type="analysis"
                )
                return response
            else:
                logger.warning("⚠️ AI менеджер не поддерживает chat_completion")
                return None
                
        except Exception as e:
            logger.error(f"❌ Ошибка AI анализа: {e}")
            return None
    
    def extract_search_query(self, full_query: str) -> str:
        """
        Умное извлечение поискового запроса из полного текста команды.
        
        Args:
            full_query: Полный запрос пользователя
            
        Returns:
            Очищенный поисковый запрос
        """
        # Удаляем команды и лишние слова
        query = full_query.lower()
        
        # Паттерны команд для удаления
        command_patterns = [
            r'открой браузер\s+(?:и\s+)?',
            r'открой\s+браузер\s+',
            r'найди\s+(?:в\s+)?(?:интернете\s+)?(?:информацию\s+)?(?:про\s+|о\s+|об\s+)?',
            r'поищи\s+(?:в\s+)?(?:интернете\s+)?(?:информацию\s+)?(?:про\s+|о\s+|об\s+)?',
            r'поиск\s+(?:информации\s+)?(?:про\s+|о\s+|об\s+)?',
            r'загугли\s+',
            r'гугл\s+',
            r'и\s+расскажи\s+мне.*$',
            r'расскажи\s+мне.*$',
            r'и\s+объясни.*$',
            r'объясни.*$',
        ]
        
        for pattern in command_patterns:
            query = re.sub(pattern, '', query, flags=re.IGNORECASE)
        
        # Убираем лишние пробелы
        query = ' '.join(query.split())
        
        # Исправляем распространённые опечатки
        query = query.replace('прос', 'про')
        query = query.replace('иформатцию', 'информацию')
        query = query.replace('иформацию', 'информацию')
        
        return query.strip()
    
    def close(self):
        """Закрыть сессию"""
        self.session.close()
        logger.info("🔒 WebScraperAgent закрыт")


# ============================================================================
# Функции для удобного использования
# ============================================================================

async def search_web(query: str, ai_manager=None) -> Dict[str, Any]:
    """
    Быстрый поиск в интернете с анализом.
    
    Args:
        query: Поисковый запрос
        ai_manager: Менеджер AI для анализа
        
    Returns:
        Результаты поиска и анализа
    """
    scraper = WebScraperAgent(ai_manager)
    try:
        result = await scraper.search_and_analyze(query)
        return result
    finally:
        scraper.close()


if __name__ == "__main__":
    # Тест агента
    async def test():
        scraper = WebScraperAgent()
        result = await scraper.search_and_analyze("Python программирование", num_results=2, analyze=False)
        
        print("\n" + "="*70)
        print("🔍 РЕЗУЛЬТАТЫ ПОИСКА")
        print("="*70)
        print(f"Запрос: {result['query']}")
        print(f"Найдено результатов: {result['summary']['total_results']}")
        print(f"Загружено страниц: {result['summary']['scraped_pages']}")
        
        print("\n📋 Результаты поиска:")
        for i, res in enumerate(result['search_results'][:5], 1):
            print(f"\n{i}. {res['title']}")
            print(f"   {res['url']}")
            print(f"   {res['snippet'][:100]}...")
        
        if result['scraped_content']:
            print("\n📄 Загруженный контент:")
            for i, content in enumerate(result['scraped_content'], 1):
                print(f"\n{i}. {content['title']}")
                print(f"   Символов: {len(content['content'])}")
                print(f"   Превью: {content['content'][:200]}...")
        
        scraper.close()
    
    asyncio.run(test())
