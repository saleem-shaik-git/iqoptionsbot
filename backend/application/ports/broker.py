from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from datetime import datetime

from backend.domain.market import AccountSnapshot, Candle, OrderRequest, OrderResult


class Broker(ABC):
    """Provider-neutral interface for broker integrations.

    Implementations must remain paper/demo-safe by default. Live-money execution is
    intentionally outside this platform's execution boundary.
    """

    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    @abstractmethod
    async def heartbeat(self) -> bool: ...

    @abstractmethod
    async def get_account(self) -> AccountSnapshot: ...

    @abstractmethod
    async def get_historical_candles(
        self, symbol: str, timeframe_seconds: int, start: datetime, end: datetime
    ) -> list[Candle]: ...

    @abstractmethod
    async def stream_candles(self, symbol: str, timeframe_seconds: int) -> AsyncIterator[Candle]: ...

    @abstractmethod
    async def submit_order(self, request: OrderRequest) -> OrderResult: ...

    @abstractmethod
    async def get_order(self, order_id: str) -> OrderResult: ...
