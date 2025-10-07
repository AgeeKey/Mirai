from typing import Optional, Dict, Any


class BrokerBase:
    """Common interface for broker connectors"""

    name = "base"

    async def place_order(self, symbol: str, side: str, quantity: float, price: Optional[float] = None, order_type: str = "market") -> Dict[str, Any]:
        raise NotImplementedError

    async def close_position(self, symbol: str) -> Dict[str, Any]:
        raise NotImplementedError

    async def get_position(self, symbol: str) -> Optional[Dict[str, Any]]:
        return None

    async def get_balance(self) -> Dict[str, float]:
        return {"total": 0.0, "available": 0.0}

