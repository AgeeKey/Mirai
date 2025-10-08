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


class AIEngine:
    """Единый AI движок для GPT-4 и Grok"""

    def __init__(self, openai_key: Optional[str] = None, grok_key: Optional[str] = None):
        self.openai_key = openai_key
        self.grok_key = grok_key
        self._openai_client = None

        if openai_key and OpenAI:
            try:
                self._openai_client = OpenAI(api_key=openai_key)
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

        # Авто-выбор модели с умной приоритизацией
        if model == "auto":
            # Определяем сложность задачи по ключевым словам
            complex_keywords = [
                "анализ", "стратегия", "решение", "plan", "strategy", 
                "analyze", "decide", "optimize", "calculate", "evaluate",
                "критическ", "важн", "critical", "important"
            ]
            is_complex = any(kw in prompt.lower() for kw in complex_keywords)
            
            if is_complex and self._openai_client:
                # Сложные задачи → GPT-4 (мозг)
                model = "gpt-4"
            elif self.grok_key:
                # Простые задачи → Grok (быстро и дёшево)
                model = "grok"
            elif self._openai_client:
                # Fallback на GPT-4 если Grok недоступен
                model = "gpt-4"
            else:
                model = "grok"  # Последний шанс

        if model == "gpt-4" and not self._openai_client:
            return "AI (OpenAI) не настроен"

        if model == "grok" and not self.grok_key:
            return "AI (Grok) не настроен"

        try:
            if model == "gpt-4" and self._openai_client:
                return await self._call_gpt4(prompt, temperature, max_tokens)

            if model == "grok" and self.grok_key:
                return await self._call_grok(prompt, temperature, max_tokens)

            return f"AI модель {model} недоступна"

        except Exception as exc:  # pragma: no cover - просто вернуть текст
            return f"AI Engine error: {exc}"

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
            )
            return completion.choices[0].message.content

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, _request)

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
                timeout=30,
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

        return await loop.run_in_executor(None, _request)
