"""
MASTER AGENT - Единое ядро Mirai Agent
Объединяет всю функциональность в одном месте
"""

import asyncio
import os

from core.ai_engine import AIEngine
from core.config import Config
from modules.agent.autonomous import AutonomousAgent
from modules.trading.trader import Trader
from modules.api.server import APIServer
from modules.utils.logger import Logger

# Telegram бот (опционально)
try:
    from modules.telegram_bot.bot import create_bot_from_env
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False


class MasterAgent:
    """Главный агент - управляет всем"""

    def __init__(self):
        # Конфигурация
        self.config = Config.load()

        # Логгеры
        self.logger = Logger("MasterAgent")
        agent_logger = Logger("AutonomousAgent")
        trader_logger = Logger("Trader")
        api_logger = Logger("APIServer")

        # AI движок
        self.ai_engine = AIEngine(
            openai_key=self.config.openai_key,
            grok_key=self.config.grok_key,
        )

        # Автономный агент
        self.autonomous = AutonomousAgent(
            ai_engine=self.ai_engine,
            logger=agent_logger,
            config={
                "data_dir": str(self.config.data_dir),
                "logs_dir": str(self.config.logs_dir),
                "cycle_interval": self.config.agent_settings.cycle_interval,
                "max_goals": self.config.agent_settings.max_goals,
                "learning_sessions_limit": self.config.agent_settings.learning_sessions_limit,
            },
        )

        # Безопасные флаги окружения
        dry_run_flag = (os.getenv("DRY_RUN", "true").lower() == "true")
        enable_telegram = (os.getenv("ENABLE_TELEGRAM", "false").lower() == "true")
        enable_binance = (os.getenv("ENABLE_BINANCE", "false").lower() == "true")

        self.logger.info(
            "Startup flags: DRY_RUN=%s, ENABLE_TELEGRAM=%s, ENABLE_BINANCE=%s",
            dry_run_flag,
            enable_telegram,
            enable_binance,
        )

        # Трейдер
        self.trader = Trader(
            config=self.config.trading,
            ai_engine=self.ai_engine,
            logger=trader_logger,
            runtime_config={
                "cycle_interval": self.config.trader_settings.cycle_interval,
                # Enforce DRY_RUN for safety unless explicitly disabled
                "demo_mode": True if dry_run_flag else self.config.trader_settings.demo_mode,
            },
        )

        # API сервер
        self.api = APIServer(
            agent=self.autonomous,
            trader=self.trader,
            logger=api_logger,
        )

        # Telegram бот
        self.telegram_bot = None
        if enable_telegram and TELEGRAM_AVAILABLE:
            try:
                # Установка переменных окружения для бота
                os.environ["TELEGRAM_TOKEN"] = os.getenv("TELEGRAM_BOT_TOKEN", "")
                os.environ["TELEGRAM_CHAT_ID"] = os.getenv("TELEGRAM_CHAT_ID_ADMIN", "")
                
                self.telegram_bot = create_bot_from_env()
                if self.telegram_bot and self.telegram_bot.is_enabled():
                    self.logger.info("✅ Telegram бот инициализирован")
                else:
                    self.logger.warning("⚠️ Telegram бот не активен")
                    self.telegram_bot = None
            except Exception as e:
                self.logger.error("❌ Ошибка инициализации Telegram бота: %s", e)
                self.telegram_bot = None
        elif enable_telegram and not TELEGRAM_AVAILABLE:
            self.logger.warning("⚠️ Telegram модуль недоступен")

        self.logger.info("🤖 MasterAgent initialized")

    async def start(self):
        """Запуск всех компонентов"""
        self.logger.info("🚀 Starting MasterAgent...")

        # Запускаем компоненты параллельно
        tasks = [
            self.autonomous.run(),  # Автономный агент
            self.trader.run(),  # Трейдер
            self.api.run(),  # API сервер
        ]

        # Добавляем Telegram бот если доступен
        if self.telegram_bot:
            self.logger.info("📱 Запуск Telegram бота...")
            tasks.append(self.telegram_bot.start_polling())

        await asyncio.gather(*tasks)

    async def stop(self):
        """Остановка"""
        self.logger.info("⏸️ Stopping MasterAgent...")

        await self.autonomous.stop()
        await self.trader.stop()
        await self.api.stop()
        
        if self.telegram_bot:
            self.logger.info("📱 Остановка Telegram бота...")
            # Telegram бот остановится при завершении программы

        self.logger.info("✅ MasterAgent stopped")


async def main():
    """Точка входа"""
    agent = MasterAgent()

    try:
        await agent.start()
    except KeyboardInterrupt:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())
