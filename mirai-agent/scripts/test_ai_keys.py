#!/usr/bin/env python3
"""
Quick connectivity test for OpenAI and Grok (x.ai) API keys.

Reads keys from environment variables:
- OPENAI_API_KEY
- GROK_API_KEY or XAI_API_KEY

Usage:
  export OPENAI_API_KEY=...
  export GROK_API_KEY=...
  python scripts/test_ai_keys.py
"""

from __future__ import annotations

import os
import sys
import json
import time
from typing import Tuple

import requests


def test_openai() -> Tuple[bool, str]:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return False, "OPENAI_API_KEY не задан"

    try:
        # OpenAI v1 client
        from openai import OpenAI  # type: ignore

        client = OpenAI(api_key=api_key)
        start = time.time()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a health check."},
                {"role": "user", "content": "ping"},
            ],
            max_tokens=8,
            temperature=0.0,
        )
        latency = (time.time() - start) * 1000
        text = resp.choices[0].message.content or ""
        return True, f"OK ({latency:.0f} ms) → {text!r}"
    except Exception as e:  # noqa: BLE001
        # Подсказка: если ключ начинается с xai-, это Grok ключ, а не OpenAI
        api_key = os.getenv("OPENAI_API_KEY", "")
        hint = ""
        if api_key.startswith("xai-"):
            hint = " (похоже, в OPENAI_API_KEY записан Grok ключ)"
        return False, f"Ошибка: {e}{hint}"


def test_grok() -> Tuple[bool, str]:
    api_key = (os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY") or "").strip()
    if not api_key:
        return False, "GROK_API_KEY/XAI_API_KEY не задан"

    try:
        model_primary = os.getenv("GROK_MODEL", "grok-2-latest")
        payload = {
            "model": model_primary,
            "messages": [
                {"role": "system", "content": "You are a health check."},
                {"role": "user", "content": "ping"},
            ],
            "max_tokens": 8,
            "temperature": 0.0,
        }
        start = time.time()
        resp = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=20,
        )
        if resp.status_code >= 400:
            # Попробуем fallback на старую модель
            payload["model"] = "grok-beta"
            resp2 = requests.post(
                "https://api.x.ai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=20,
            )
            if resp2.status_code >= 400:
                return False, f"HTTP {resp2.status_code}: {resp2.text.strip()}"
            resp = resp2
        data = resp.json()
        latency = (time.time() - start) * 1000
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return True, f"OK ({latency:.0f} ms) → {text!r}"
    except Exception as e:  # noqa: BLE001
        return False, f"Ошибка: {e}"


def main() -> int:
    results = {}
    ok_oa, msg_oa = test_openai()
    results["openai"] = {"ok": ok_oa, "message": msg_oa}

    ok_grok, msg_grok = test_grok()
    results["grok"] = {"ok": ok_grok, "message": msg_grok}

    # Pretty print
    print(json.dumps(results, ensure_ascii=False, indent=2))

    # Exit code: 0 if all configured providers passed; 1 otherwise
    configured = 0
    passed = 0
    if os.getenv("OPENAI_API_KEY"):
        configured += 1
        if ok_oa:
            passed += 1
    if os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY"):
        configured += 1
        if ok_grok:
            passed += 1

    if configured == 0:
        print("Предупреждение: ключи не заданы, тестировать нечего.")
        return 0
    return 0 if passed == configured else 1


if __name__ == "__main__":
    sys.exit(main())
