#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║                    MIRAI AUTONOMOUS AGENT                    ║
║                    Главная точка входа                       ║
╚══════════════════════════════════════════════════════════════╝

Автономный AI агент с возможностями:
- 🤖 Работает 24/7 без участия человека
- 🧠 Принимает решения через GPT-4 и Grok
- 🌐 API сервер для мониторинга
- 📱 Telegram бот для управления
- 📊 Логирование и статистика
- 💾 Память в SQLite
"""

import asyncio
import os
import signal
import sys
from pathlib import Path

# Добавляем корень проекта в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from core.master_agent import MasterAgent
from modules.utils.logger import Logger

logger = Logger("MiraiMain").logger


def signal_handler(sig, frame):
    """Обработчик сигналов для graceful shutdown"""
    logger.info("🛑 Получен сигнал остановки (%s). Завершение работы...", sig)
    sys.exit(0)


async def main():
    """Главная функция запуска Mirai Agent"""
    
    logger.info("═" * 70)
    logger.info("🚀 MIRAI AUTONOMOUS AGENT STARTING...")
    logger.info("═" * 70)
    
    # Проверка переменных окружения
    required_env = [
        "OPENAI_API_KEY",
        "GROK_API_KEY",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID_ADMIN",
    ]
    
    missing = [var for var in required_env if not os.getenv(var)]
    if missing:
        logger.error("❌ Отсутствуют обязательные переменные окружения:")
        for var in missing:
            logger.error("   - %s", var)
        logger.info("💡 Проверьте файл .env")
        sys.exit(1)
    
    # Вывод конфигурации
    logger.info("📋 Конфигурация:")
    logger.info("   • OpenAI API: %s", "✅ Настроен" if os.getenv("OPENAI_API_KEY") else "❌ Нет")
    logger.info("   • Grok API: %s", "✅ Настроен" if os.getenv("GROK_API_KEY") else "❌ Нет")
    logger.info("   • Telegram: %s", "✅ Активен" if os.getenv("ENABLE_TELEGRAM") == "true" else "⚠️ Выключен")
    logger.info("   • DRY RUN: %s", os.getenv("DRY_RUN", "true"))
    logger.info("   • Autonomous Mode: %s", os.getenv("AUTONOMOUS_MODE", "true"))
    logger.info("─" * 70)
    
    # Регистрация обработчиков сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Создание и запуск Master Agent
        logger.info("🤖 Инициализация MasterAgent...")
        agent = MasterAgent()
        
        logger.info("✅ MasterAgent создан успешно")
        logger.info("═" * 70)
        logger.info("🎯 Запуск автономного режима...")
        logger.info("═" * 70)
        
        # Запуск агента
        await agent.start()
        
    except KeyboardInterrupt:
        logger.info("🛑 Остановка по запросу пользователя")
    except Exception as e:
        logger.error("💥 Критическая ошибка: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Mirai Agent остановлен")
