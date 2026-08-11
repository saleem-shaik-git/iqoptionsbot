from collections.abc import AsyncIterator
from datetime import datetime

from backend.application.ports.market_data import MarketDataProvider
from backend.domain.market import Candle
from backend.application.ports.broker import Broker


class BrokerMarketDataProvider(MarketDataProvider):
    def __init__(self, broker: Broker) -> None:
        self._broker = broker

    async def historical(self, symbol: str, timeframe_seconds: int, start: datetime, end: datetime) -> list[Candle]:
        return await self._broker.get_historical_candles(symbol, timeframe_seconds, start, end)

    async def stream(self, symbol: str, timeframe_seconds: int) -> AsyncIterator[Candle]:
        async for candle in self._broker.stream_candles(symbol, timeframe_seconds):
            yield candle
