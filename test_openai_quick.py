#!/usr/bin/env python3
"""
Быстрый тест OpenAI API
Только проверка что ключ работает
"""

import os
from openai import OpenAI


# Читаем ключ из .env
def load_env():
    env_path = "/root/mirai/mirai-agent/.env"
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key.strip()] = value.strip()


load_env()

# Проверка ключа
api_key = os.getenv("OPENAI_API_KEY")
print(f"🔑 OpenAI Key: {api_key[:20]}...{api_key[-10:]}")
print(f"📏 Key length: {len(api_key)}")
print()

# Попытка подключения
try:
    client = OpenAI(api_key=api_key)

    print("📡 Testing OpenAI connection...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Connection successful!' in Russian"},
        ],
        max_tokens=50,
    )

    print("✅ SUCCESS!")
    print(f"🤖 Response: {response.choices[0].message.content}")
    print(f"📊 Model: {response.model}")
    print(f"🎯 Tokens used: {response.usage.total_tokens}")

except Exception as e:
    print(f"❌ ERROR: {e}")
    print()
    print("Possible issues:")
    print("  - Invalid API key")
    print("  - No internet connection")
    print("  - OpenAI service down")
