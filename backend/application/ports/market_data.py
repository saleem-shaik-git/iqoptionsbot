from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from datetime import datetime

from backend.domain.market import Candle


class MarketDataProvider(ABC):
    @abstractmethod
    async def historical(self, symbol: str, timeframe_seconds: int, start: datetime, end: datetime) -> list[Candle]: ...

    @abstractmethod
    async def stream(self, symbol: str, timeframe_seconds: int) -> AsyncIterator[Candle]: ...
