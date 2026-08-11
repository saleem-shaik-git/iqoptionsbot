import pytest
from datetime import UTC, datetime, timedelta
from decimal import Decimal

from backend.application.services.connection_manager import BrokerConnectionManager
from backend.infrastructure.brokers.paper import PaperBroker
from backend.application.ports.market_data import MarketDataProvider
from backend.infrastructure.market_data.broker_provider import BrokerMarketDataProvider
from backend.domain.market import OrderRequest, TradeDirection


@pytest.mark.asyncio
async def test_paper_broker_account_and_order() -> None:
    broker = PaperBroker(Decimal("1000"))
    await broker.connect()
    account = await broker.get_account()
    assert account.balance == Decimal("1000")

    result = await broker.submit_order(OrderRequest("EURUSD", TradeDirection.CALL, Decimal("50"), 60, "client-1"))
    assert result.accepted
    assert (await broker.get_account()).balance == Decimal("950")


@pytest.mark.asyncio
async def test_historical_market_data() -> None:
    broker = PaperBroker()
    await broker.connect()
    provider: MarketDataProvider = BrokerMarketDataProvider(broker)
    start = datetime(2026, 1, 1, tzinfo=UTC)
    candles = await provider.historical("EURUSD", 60, start, start + timedelta(minutes=3))
    assert len(candles) == 3
    assert all(c.symbol == "EURUSD" for c in candles)


@pytest.mark.asyncio
async def test_disconnected_broker_rejects_operations() -> None:
    broker = PaperBroker()
    with pytest.raises(Exception):
        await broker.get_account()
