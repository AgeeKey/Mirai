"""
Торговый агент: упрощённая интеграция анализа и исполнения.
"""

import asyncio


class Trader:
    """Асинхронный торговый агент (демо-режим)."""

    def __init__(self, config, ai_engine, logger, runtime_config=None):
        self.config = config
        self.ai = ai_engine
        self.logger = logger
        self.runtime_config = runtime_config or {}
        self.demo_mode = self.runtime_config.get("demo_mode", True)

        self.running = False
        self.positions = {}
        self.balance = 10_000.0

        self.logger.info("✅ Trader initialized")

    async def analyze_market(self):
        self.logger.info("📊 Analyzing market...")

        analysis = await self.ai.think(
            "Analyze BTC/USDT market. Should I buy, sell, or hold? Give brief reasoning.",
            model="auto",
        )

        self.logger.info(f"💡 Analysis: {analysis[:100]}...")
        return analysis

    async def calculate_risk(self, _signal):
        risk_percent = getattr(self.config, "risk_per_trade", 2.0)
        max_position = self.balance * (risk_percent / 100)
        self.logger.info(f"🛡️ Max position size: ${max_position:.2f}")
        return max_position

    async def execute_trade(self, signal, size):
        mode = "DEMO" if self.demo_mode else "LIVE"
        self.logger.info(f"⚡ Executing {signal} with size ${size:.2f} [{mode}]")
        await asyncio.sleep(1)
        self.logger.info("✅ Trade executed")

    async def cycle(self):
        self.logger.info("🔄 Trading cycle")
        analysis = await self.analyze_market()
        await self.calculate_risk(analysis)
        self.logger.info(f"💰 Balance: ${self.balance:.2f}")
        self.logger.info(f"📈 Positions: {len(self.positions)}")

    async def run(self):
        self.running = True
        self.logger.info("🚀 Trader started")

        interval = self.runtime_config.get("cycle_interval", 600)
        while self.running:
            try:
                await self.cycle()
                await asyncio.sleep(interval)
            except Exception as exc:  # noqa: BLE001
                self.logger.error(f"❌ Error in trading cycle: {exc}")
                await asyncio.sleep(60)

    async def stop(self):
        self.running = False
        self.logger.info("⏸️ Trader stopped")
