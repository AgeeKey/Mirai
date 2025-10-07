import logging
from typing import Optional, Dict, Any
from .base import BrokerBase

logger = logging.getLogger(__name__)

class BybitBroker(BrokerBase):
    name = "bybit"

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet

    async def place_order(self, symbol: str, side: str, quantity: float, price: Optional[float] = None, order_type: str = "market") -> Dict[str, Any]:
        logger.info(f"[BYBIT] place_order {symbol} {side} qty={quantity} type={order_type} price={price}")
        return {"status": "ok", "order_id": f"bybit_{symbol}_123"}

    async def close_position(self, symbol: str) -> Dict[str, Any]:
        logger.info(f"[BYBIT] close_position {symbol}")
        return {"status": "ok"}

    async def get_balance(self) -> Dict[str, float]:
        return {"total": 10000.0, "available": 9500.0}

