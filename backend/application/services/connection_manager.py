import asyncio
from collections.abc import Awaitable, Callable

from backend.application.ports.broker import Broker
from backend.domain.market import BrokerConnectionError


class BrokerConnectionManager:
    def __init__(self, broker: Broker, reconnect_delay_seconds: float = 2.0) -> None:
        self._broker = broker
        self._delay = reconnect_delay_seconds
        self._running = False

    async def start(self) -> None:
        self._running = True
        while self._running:
            try:
                if not await self._broker.heartbeat():
                    await self._broker.connect()
                await asyncio.sleep(self._delay)
            except (BrokerConnectionError, OSError):
                await asyncio.sleep(self._delay)

    async def stop(self) -> None:
        self._running = False
        await self._broker.disconnect()
