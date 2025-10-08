"""
AI ENGINE - Единый интерфейс для всех AI моделей
"""

import asyncio
from typing import Optional

import requests

try:  # pragma: no cover - optional dependency
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None

# Import AI Tools
try:
    from .ai_tools import ai_tools
    AI_TOOLS_AVAILABLE = True
except ImportError:
    AI_TOOLS_AVAILABLE = False
    ai_tools = None


class AIEngine:
    """Единый AI движок для GPT-4 и Grok с дополнительными инструментами"""

    # API timeouts and limits
    DEFAULT_TIMEOUT = 60  # seconds
    MAX_RETRIES = 3
    RETRY_DELAY = 2  # seconds

    def __init__(self, openai_key: Optional[str] = None, grok_key: Optional[str] = None):
        self.openai_key = openai_key
        self.grok_key = grok_key
        self._openai_client = None
        self.tools = ai_tools if AI_TOOLS_AVAILABLE else None
        
        # Token usage tracking
        self.total_tokens_used = 0
        self.requests_count = 0

        if openai_key and OpenAI:
            try:
                self._openai_client = OpenAI(api_key=openai_key, timeout=self.DEFAULT_TIMEOUT)
            except Exception as exc:  # pragma: no cover
                self._openai_client = None
                print(f"⚠️ Не удалось инициализировать OpenAI клиента: {exc}")

    async def think(
        self,
        prompt: str,
        model: str = "auto",
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """
        Единый метод для мышления через AI

        Args:
            prompt: Запрос к AI
            model: \"gpt-4\", \"grok\", или \"auto\" (выбирает лучший)
            temperature: Креативность
            max_tokens: Макс длина ответа
        """

        # Авто-выбор модели - используем только GPT-4
        if model == "auto":
            model = "gpt-4" if self._openai_client else "grok"

        if model == "gpt-4" and not self._openai_client:
            return "AI (OpenAI) не настроен"

        if model == "grok" and not self.grok_key:
            return "AI (Grok) не настроен"

        # Retry logic with exponential backoff
        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                self.requests_count += 1
                
                if model == "gpt-4" and self._openai_client:
                    return await self._call_gpt4(prompt, temperature, max_tokens)

                if model == "grok" and self.grok_key:
                    return await self._call_grok(prompt, temperature, max_tokens)

                return f"AI модель {model} недоступна"

            except asyncio.TimeoutError as exc:
                last_error = f"Timeout after {self.DEFAULT_TIMEOUT}s"
                if attempt < self.MAX_RETRIES - 1:
                    await asyncio.sleep(self.RETRY_DELAY * (attempt + 1))
                    continue
            except Exception as exc:  # pragma: no cover
                last_error = str(exc)
                # Don't retry on authentication or configuration errors
                if "api" in str(exc).lower() and "key" in str(exc).lower():
                    break
                if attempt < self.MAX_RETRIES - 1:
                    await asyncio.sleep(self.RETRY_DELAY * (attempt + 1))
                    continue
        
        return f"AI Engine error after {self.MAX_RETRIES} attempts: {last_error}"
    
    def get_usage_stats(self) -> dict:
        """Получить статистику использования API"""
        return {
            "total_tokens": self.total_tokens_used,
            "requests_count": self.requests_count,
        }

    async def _call_gpt4(self, prompt: str, temp: float, tokens: int) -> str:
        """GPT-4 (via OpenAI>=1.0 client)."""

        def _request():
            completion = self._openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are Mirai, an autonomous AI agent."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temp,
                max_tokens=tokens,
                timeout=self.DEFAULT_TIMEOUT,
            )
            # Track token usage
            if hasattr(completion, 'usage') and completion.usage:
                self.total_tokens_used += completion.usage.total_tokens
            return completion.choices[0].message.content

        loop = asyncio.get_running_loop()
        # Add timeout wrapper
        return await asyncio.wait_for(
            loop.run_in_executor(None, _request),
            timeout=self.DEFAULT_TIMEOUT + 5
        )

    async def _call_grok(self, prompt: str, temp: float, tokens: int) -> str:
        """Grok"""

        loop = asyncio.get_running_loop()

        def _request():
            response = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.grok_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "grok-beta",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are Mirai, an autonomous AI agent.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": temp,
                    "max_tokens": tokens,
                },
                timeout=self.DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
            # Track token usage if available
            if "usage" in data and "total_tokens" in data["usage"]:
                self.total_tokens_used += data["usage"]["total_tokens"]
            return data["choices"][0]["message"]["content"]

        # Add timeout wrapper
        return await asyncio.wait_for(
            loop.run_in_executor(None, _request),
            timeout=self.DEFAULT_TIMEOUT + 5
        )
