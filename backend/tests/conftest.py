from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, AsyncIterator, Dict, Optional

import httpx
import pytest
from fastapi import FastAPI

# Ensure `import src.*` works in local pytest runs (mirrors PYTHONPATH=/app in Docker).
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


@pytest.fixture()
def app() -> FastAPI:
    """
    Lightweight FastAPI app for tests.

    We intentionally avoid importing the production app (`src.main_refactored:app`)
    because its lifespan initializes DB + Redis pools.
    """
    from src.api.routes import tasks as tasks_routes

    test_app = FastAPI()
    test_app.include_router(tasks_routes.router)
    return test_app


@pytest.fixture()
async def async_client(app: FastAPI) -> AsyncIterator[httpx.AsyncClient]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture()
def user_id() -> str:
    return "user_test_123"


@pytest.fixture()
def auth_headers(user_id: str) -> Dict[str, str]:
    # Default (self-host / monetization off) mode: accept plain user id headers.
    return {"user_id": user_id}


@dataclass(frozen=True)
class SignedAuth:
    user_id: str
    timestamp: str
    signature: str


def build_signed_auth(secret: str, user_id: str, *, ts: Optional[int] = None) -> SignedAuth:
    from src.auth_headers import _expected_signature

    ts_int = int(time.time()) if ts is None else int(ts)
    timestamp = str(ts_int)
    signature = _expected_signature(secret, user_id, timestamp)
    return SignedAuth(user_id=user_id, timestamp=timestamp, signature=signature)

