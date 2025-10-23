#!/usr/bin/env python3
"""
Web Search Integration для MIRAI
Использует OpenAI gpt-5-search-api для поиска в интернете
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)


class WebSearchAgent:
    """Агент для поиска информации в интернете через OpenAI"""

    def __init__(self):
        # Загружаем API ключ
        config_path = Path(__file__).parent.parent / "configs" / "api_keys.json"
        with open(config_path) as f:
            config = json.load(f)

        self.client = OpenAI(api_key=config["openai"])
        self.search_model = "gpt-5-search-api-2025-10-14"
        self.search_history = []

    def search(
        self,
        query: str,
        max_tokens: int = 1000,
    ) -> Dict:
        """
        Выполнить поиск в интернете

        Args:
            query: Запрос для поиска
            max_tokens: Максимум токенов в ответе

        Returns:
            Dict с результатами поиска
        """
        try:
            logger.info(f"🔍 Web Search: {query}")

            # Добавляем инструкцию для поиска
            search_prompt = f"""Search the internet for current, real-time information about:
{query}

Please provide:
1. Direct answer to the query
2. Sources and links if available
3. Timestamp of information
4. Any relevant context

Be concise but thorough."""

            response = self.client.chat.completions.create(
                model=self.search_model,
                messages=[{"role": "user", "content": search_prompt}],
                max_tokens=max_tokens,
            )

            result = {
                "query": query,
                "answer": response.choices[0].message.content,
                "model": self.search_model,
                "tokens_used": response.usage.total_tokens,
                "timestamp": datetime.now().isoformat(),
                "success": True,
            }

            # Сохраняем в историю
            self.search_history.append(result)

            logger.info(f"✅ Search completed: {response.usage.total_tokens} tokens")
            return result

        except Exception as e:
            logger.error(f"❌ Search error: {e}")
            return {
                "query": query,
                "answer": None,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "success": False,
            }

    def quick_search(self, query: str) -> str:
        """Быстрый поиск - возвращает только текст ответа"""
        result = self.search(query, max_tokens=500)
        return result.get("answer", f"Error: {result.get('error')}")

    def get_current_info(self, topic: str) -> str:
        """Получить актуальную информацию о топике"""
        query = f"What is the latest information about {topic} as of {datetime.now().strftime('%B %Y')}?"
        return self.quick_search(query)

    def verify_fact(self, statement: str) -> Dict:
        """Проверить факт в интернете"""
        query = f"Verify this statement with current sources: {statement}"
        result = self.search(query, max_tokens=800)
        return result

    def compare_sources(self, topic: str, num_perspectives: int = 3) -> str:
        """Сравнить информацию из разных источников"""
        query = f"Search multiple sources and compare {num_perspectives} different perspectives on: {topic}"
        return self.quick_search(query)

    def find_documentation(self, library: str, language: str = "Python") -> str:
        """Найти документацию для библиотеки"""
        query = f"Find official documentation and quick start guide for {library} {language} library"
        return self.quick_search(query)

    def search_error_solution(self, error_message: str, language: str = "Python") -> str:
        """Найти решение для ошибки"""
        query = f"""Search for solutions to this {language} error:
{error_message}

Find:
1. What causes this error
2. How to fix it
3. Code examples
4. Best practices to avoid it"""
        return self.quick_search(query)

    def research_topic(self, topic: str, depth: str = "medium") -> Dict:
        """
        Глубокое исследование темы

        Args:
            topic: Тема для исследования
            depth: Глубина (quick, medium, deep)
        """
        token_map = {"quick": 500, "medium": 1500, "deep": 3000}
        max_tokens = token_map.get(depth, 1500)

        query = f"""Conduct a comprehensive research on: {topic}

Please include:
1. Overview and key concepts
2. Current state and recent developments
3. Main use cases and applications
4. Best practices and recommendations
5. Resources for learning more

Depth level: {depth}"""

        return self.search(query, max_tokens=max_tokens)

    def get_trending(self, category: str = "technology") -> str:
        """Получить трендовые темы"""
        query = f"What are the current trending topics and news in {category} as of today?"
        return self.quick_search(query)

    def get_history(self, limit: int = 10) -> List[Dict]:
        """Получить историю поисков"""
        return self.search_history[-limit:]

    def clear_history(self):
        """Очистить историю"""
        self.search_history = []
        logger.info("🧹 Search history cleared")


# Singleton instance
_web_search_agent = None


def get_web_search() -> WebSearchAgent:
    """Получить singleton instance Web Search агента"""
    global _web_search_agent
    if _web_search_agent is None:
        _web_search_agent = WebSearchAgent()
    return _web_search_agent


if __name__ == "__main__":
    # Тесты
    logging.basicConfig(level=logging.INFO)

    agent = WebSearchAgent()

    print("=== Test 1: Quick Search ===")
    result = agent.quick_search("What is the current weather in New York?")
    print(result)
    print()

    print("=== Test 2: Find Documentation ===")
    result = agent.find_documentation("requests", "Python")
    print(result)
    print()

    print("=== Test 3: Current Info ===")
    result = agent.get_current_info("artificial intelligence trends")
    print(result)
    print()

    print("=== Test 4: Search History ===")
    history = agent.get_history()
    print(f"Total searches: {len(history)}")
    for i, search in enumerate(history, 1):
        query = search['query']
        tokens = search['tokens_used']
        print(f"{i}. {query} ({tokens} tokens)")
