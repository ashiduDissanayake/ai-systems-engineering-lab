from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from fastapi import FastAPI, Query

app = FastAPI(
    title="AI Systems Engineering Lab",
    version="0.1.0",
    description="A small service for HTTP performance experiments.",
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/work")
async def work(
    delay_ms: int = Query(default=20, ge=0, le=5000),
) -> dict[str, int | str]:
    """Simulate non-blocking I/O work using asyncio.sleep."""
    await asyncio.sleep(delay_ms / 1000)
    return {
        "message": "completed",
        "delay_ms": delay_ms,
    }
