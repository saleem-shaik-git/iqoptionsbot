from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum


class BrokerEnvironment(StrEnum):
    PAPER = "paper"
    DEMO = "demo"


class TradeDirection(StrEnum):
    CALL = "call"
    PUT = "put"


@dataclass(frozen=True, slots=True)
class Candle:
    symbol: str
    timeframe_seconds: int
    timestamp: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: Decimal | None = None


@dataclass(frozen=True, slots=True)
class AccountSnapshot:
    account_id: str
    balance: Decimal
    currency: str
    environment: BrokerEnvironment
    connected: bool


@dataclass(frozen=True, slots=True)
class OrderRequest:
    symbol: str
    direction: TradeDirection
    amount: Decimal
    duration_seconds: int
    client_order_id: str


@dataclass(frozen=True, slots=True)
class OrderResult:
    order_id: str
    client_order_id: str
    accepted: bool
    status: str
    message: str | None = None


class BrokerError(Exception):
    """Base exception for broker adapter failures."""


class BrokerConnectionError(BrokerError):
    """Raised when a broker connection cannot be established or maintained."""


class BrokerNotSupportedError(BrokerError):
    """Raised when an operation is not supported by an adapter."""
