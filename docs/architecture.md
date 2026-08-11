# Architecture Blueprint

## Principles

- Clean Architecture: domain does not depend on frameworks or brokers.
- Paper trading is the default execution boundary.
- Broker integrations are adapters behind a stable interface.
- AI inference is deterministic and versioned where possible.
- Risk checks run before an order reaches an execution adapter.
- Every live-capable action is auditable.
- Secrets are injected at runtime and never committed.

## Planned flow

```text
Market Data -> Broker Adapter -> Application Services -> Feature Engine
                                      |                     |
                                      v                     v
                                 Risk Engine <- AI Inference
                                      |
                                      v
                               Strategy Signal
                                      |
                                      v
                              Paper/Live Executor
                                      |
                       +--------------+--------------+
                       |                             |
                   PostgreSQL                     Redis
                       |                             |
                  REST/WebSocket              Celery Workers
                       |
                  Next.js Dashboard
                       |
                  Telegram Adapter
```

## Safety boundary

The system will expose explicit `paper`, `demo`, and `live` modes. Live trading will require an explicit configuration gate and separate credentials. No model accuracy is assumed; all predictions are treated as probabilistic signals and must pass risk controls.
