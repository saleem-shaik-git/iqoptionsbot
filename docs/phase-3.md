# Phase 3 — Broker abstraction and market data

## Design

Phase 3 introduces provider-neutral domain contracts so the trading engine does not depend on a specific broker SDK. `Broker` owns connection/account/order primitives while `MarketDataProvider` owns historical and streaming candle access.

The included `PaperBroker` is deterministic, in-memory, and safe for development/testing. The architecture intentionally does not implement live-money execution.

## Flow

```text
Broker adapter
     |
     +--> Broker interface --> Application services --> API / workers
     |
     +--> MarketDataProvider --> candles --> AI / strategies
```

`BrokerConnectionManager` provides a heartbeat/reconnect loop. A future provider can implement `Broker` without changing domain or strategy code.

## Test

```bash
docker compose run --rm backend pytest tests/test_market_data.py -q
```

## Run

```bash
docker compose up --build
```
