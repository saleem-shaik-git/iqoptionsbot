from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from backend.core.config import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Infrastructure initialization will be added in later phases.
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="AI trading research platform. Paper trading is the default safety boundary.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "environment": settings.app_env}


@app.get("/ready", tags=["system"])
async def readiness() -> dict[str, str]:
    return {"status": "ready"}
