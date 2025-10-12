#!/usr/bin/env python3
"""
MIRAI - Упрощенный запуск ТОЛЬКО с OpenAI
Без Telegram, без Binance, без лишних зависимостей
"""

import os
import asyncio
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

from core.autonomous_agent import AutonomousAgent


async def main():
    """Простой запуск автономного агента"""
    
    print("=" * 70)
    print("🤖 MIRAI - АВТОНОМНЫЙ AI АГЕНТ")
    print("=" * 70)
    
    # Проверка OpenAI ключа
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Ошибка: OPENAI_API_KEY не найден в .env")
        print("💡 Добавьте ключ в файл /root/mirai/mirai-agent/.env")
        return
    
    print(f"✅ OpenAI API Key: {api_key[:20]}...")
    print("-" * 70)
    
    # Создаем агента
    agent = AutonomousAgent()
    print(f"✅ Агент инициализирован")
    print(f"📊 Модель: {agent.model}")
    print(f"🛠️  Инструментов: {len(agent.tools)}")
    print("-" * 70)
    
    # Даем агенту начальную задачу
    print("\n🎯 Запускаю автономный режим...")
    print("Агент будет работать и выполнять задачи самостоятельно")
    print("Нажмите Ctrl+C для остановки\n")
    print("=" * 70)
    
    try:
        # Цикл автономной работы
        iteration = 1
        while True:
            print(f"\n🔄 Итерация #{iteration}")
            print("-" * 70)
            
            # Агент сам решает что делать
            result = agent.think(
                """Ты автономный AI агент MIRAI. 
                
Твоя задача - самостоятельно работать и улучшать проект.

Что ты можешь сделать прямо сейчас:
1. Изучить структуру проекта (read_file)
2. Написать полезный код (write_file)
3. Найти информацию в интернете (search_web)
4. Выполнить код для проверки (execute_python)
5. Создать новую задачу для себя (create_task)

Выбери одно действие и выполни его. Будь полезным и проактивным!"""
            )
            
            print(f"\n📝 Результат:\n{result}\n")
            print("=" * 70)
            
            iteration += 1
            
            # Пауза между итерациями
            await asyncio.sleep(30)  # 30 секунд между циклами
            
    except KeyboardInterrupt:
        print("\n\n🛑 Остановка агента по запросу пользователя")
        print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
