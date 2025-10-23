"""
Ollama Local LLM Client
Support for offline AI inference using Ollama
"""

import json
import logging
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for Ollama local LLM inference"""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "mistral:7b",
        timeout: int = 120,
    ):
        """
        Initialize Ollama client

        Args:
            base_url: Ollama server URL
            model: Model name (e.g., "mistral:7b", "llama2:7b")
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self._check_connection()

    def _check_connection(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                logger.info(f"✅ Ollama connected. Available models: {len(models)}")
                return True
            else:
                logger.warning(f"⚠️ Ollama server responded with {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            logger.warning(f"⚠️ Ollama not available: {e}")
            return False

    def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.3,
        max_tokens: int = 4000,
    ) -> str:
        """
        Generate text completion

        Args:
            prompt: User prompt
            system: System message
            temperature: Sampling temperature (0.0 - 1.0)
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        if system:
            payload["system"] = system

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama generation failed: {e}")
            raise

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
        max_tokens: int = 4000,
        tools: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        Chat completion with function calling support

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            tools: Optional list of tool/function definitions

        Returns:
            Response dict with message and optional tool calls
        """
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        # Add tools to system message if provided
        if tools:
            tools_description = self._format_tools_for_prompt(tools)
            # Inject tools into system message
            if messages and messages[0]["role"] == "system":
                messages[0]["content"] += f"\n\n{tools_description}"
            else:
                messages.insert(
                    0, {"role": "system", "content": tools_description}
                )

        try:
            response = requests.post(url, json=payload, timeout=self.timeout)
            response.raise_for_status()
            result = response.json()

            message = result.get("message", {})
            content = message.get("content", "")

            # Try to parse tool calls from response
            tool_calls = self._extract_tool_calls(content)

            return {
                "message": {"role": "assistant", "content": content},
                "tool_calls": tool_calls,
                "model": self.model,
                "done": result.get("done", True),
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama chat failed: {e}")
            raise

    def _format_tools_for_prompt(self, tools: List[Dict]) -> str:
        """Format tools as text for prompt injection"""
        tools_text = "# Available Tools\n\n"
        tools_text += "You can call tools by responding with JSON in this format:\n"
        tools_text += '```json\n{"tool": "tool_name", "arguments": {...}}\n```\n\n'
        tools_text += "Available tools:\n\n"

        for tool in tools:
            func = tool.get("function", {})
            name = func.get("name", "unknown")
            desc = func.get("description", "")
            params = func.get("parameters", {}).get("properties", {})

            tools_text += f"## {name}\n"
            tools_text += f"{desc}\n\n"
            tools_text += "Parameters:\n"
            for param_name, param_info in params.items():
                param_type = param_info.get("type", "string")
                param_desc = param_info.get("description", "")
                tools_text += f"- {param_name} ({param_type}): {param_desc}\n"
            tools_text += "\n"

        return tools_text

    def _extract_tool_calls(self, content: str) -> List[Dict]:
        """Extract tool calls from response content"""
        tool_calls = []

        # Look for JSON code blocks
        import re

        json_blocks = re.findall(r"```json\s*(.*?)\s*```", content, re.DOTALL)

        for block in json_blocks:
            try:
                data = json.loads(block)
                if "tool" in data and "arguments" in data:
                    tool_calls.append(
                        {
                            "id": f"call_{len(tool_calls)}",
                            "type": "function",
                            "function": {
                                "name": data["tool"],
                                "arguments": json.dumps(data["arguments"]),
                            },
                        }
                    )
            except json.JSONDecodeError:
                continue

        return tool_calls

    def pull_model(self, model_name: Optional[str] = None) -> bool:
        """
        Pull/download a model

        Args:
            model_name: Model to pull (defaults to self.model)

        Returns:
            True if successful
        """
        model = model_name or self.model
        url = f"{self.base_url}/api/pull"

        payload = {"name": model, "stream": False}

        try:
            logger.info(f"📥 Pulling model: {model}")
            response = requests.post(url, json=payload, timeout=600)
            response.raise_for_status()
            logger.info(f"✅ Model pulled: {model}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to pull model: {e}")
            return False

    def list_models(self) -> List[str]:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            models = response.json().get("models", [])
            return [m.get("name") for m in models]
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to list models: {e}")
            return []
