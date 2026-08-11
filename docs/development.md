# Developer Setup

## Local

1. Copy `.env.example` to `.env`.
2. Change all secrets before using any non-local environment.
3. Start infrastructure and API:

```bash
docker compose up --build
```

4. Verify:

```bash
curl http://localhost:8000/health
```

5. API documentation is available at `http://localhost:8000/docs`.

## Native Python

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
uvicorn backend.main:app --reload
pytest
```

## Safety

Do not put IQ Option, Telegram, JWT, database, or cloud credentials in source control. Phase 1 contains no live trading implementation. Later phases must preserve paper-trading-first defaults and require explicit live-mode gates.
