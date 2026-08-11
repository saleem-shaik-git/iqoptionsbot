from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

from backend.domain.market import (
    AccountSnapshot,
    BrokerConnectionError,
    BrokerEnvironment,
    Candle,
    OrderRequest,
    OrderResult,
)
from backend.domain.market import TradeDirection
from backend.application.ports.broker import Broker


class PaperBroker(Broker):
    """Deterministic in-memory broker for development, testing and simulation."""

    def __init__(self, initial_balance: Decimal = Decimal("10000")) -> None:
        self._balance = initial_balance
        self._connected = False
        self._orders: dict[str, OrderResult] = {}

    async def connect(self) -> None:
        self._connected = True

    async def disconnect(self) -> None:
        self._connected = False

    async def heartbeat(self) -> bool:
        return self._connected

    def _require_connection(self) -> None:
        if not self._connected:
            raise BrokerConnectionError("Paper broker is not connected")

    async def get_account(self) -> AccountSnapshot:
        self._require_connection()
        return AccountSnapshot("paper", self._balance, "USD", BrokerEnvironment.PAPER, True)

    async def get_historical_candles(
        self, symbol: str, timeframe_seconds: int, start: datetime, end: datetime
    ) -> list[Candle]:
        self._require_connection()
        if end <= start:
            return []
        candles: list[Candle] = []
        current = start
        price = Decimal("100")
        while current < end:
            close = price + Decimal("0.10")
            candles.append(Candle(symbol, timeframe_seconds, current, price, close, price, close, Decimal("1000")))
            price = close
            current += timedelta(seconds=timeframe_seconds)
        return candles

    async def stream_candles(self, symbol: str, timeframe_seconds: int) -> AsyncIterator[Candle]:
        self._require_connection()
        price = Decimal("100")
        while self._connected:
            now = datetime.now(UTC).replace(microsecond=0)
            close = price + Decimal("0.10")
            yield Candle(symbol, timeframe_seconds, now, price, close, price, close, Decimal("1000"))
            price = close
            break

    async def submit_order(self, request: OrderRequest) -> OrderResult:
        self._require_connection()
        if request.amount <= 0:
            return OrderResult("", request.client_order_id, False, "rejected", "Amount must be positive")
        if request.direction not in (TradeDirection.CALL, TradeDirection.PUT):
            return OrderResult("", request.client_order_id, False, "rejected", "Unsupported direction")
        if request.amount > self._balance:
            return OrderResult("", request.client_order_id, False, "rejected", "Insufficient paper balance")
        self._balance -= request.amount
        order_id = str(uuid4())
        result = OrderResult(order_id, request.client_order_id, True, "accepted")
        self._orders[order_id] = result
        return result

    async def get_order(self, order_id: str) -> OrderResult:
        self._require_connection()
        return self._orders.get(order_id, OrderResult(order_id, "", False, "unknown", "Order not found"))
