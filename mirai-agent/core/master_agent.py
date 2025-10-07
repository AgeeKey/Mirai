"""
MASTER AGENT - Единое ядро Mirai Agent
Объединяет всю функциональность в одном месте
"""

import asyncio

from core.ai_engine import AIEngine
from core.config import Config
from modules.agent.autonomous import AutonomousAgent
from modules.trading.trader import Trader
from modules.api.server import APIServer
from modules.utils.logger import Logger


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

        # Трейдер
        self.trader = Trader(
            config=self.config.trading,
            ai_engine=self.ai_engine,
            logger=trader_logger,
            runtime_config={
                "cycle_interval": self.config.trader_settings.cycle_interval,
                "demo_mode": self.config.trader_settings.demo_mode,
            },
        )

        # API сервер
        self.api = APIServer(
            agent=self.autonomous,
            trader=self.trader,
            logger=api_logger,
        )

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

        await asyncio.gather(*tasks)

    async def stop(self):
        """Остановка"""
        self.logger.info("⏸️ Stopping MasterAgent...")

        await self.autonomous.stop()
        await self.trader.stop()
        await self.api.stop()

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
