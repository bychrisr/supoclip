from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac

from fastapi import Depends, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ...config import Config
from ...database import get_db
from ...repositories.api_key_repository import ApiKeyRepository

config = Config()


@dataclass(frozen=True)
class ApiPrincipal:
    user_id: str
    api_key_id: str | None = None


def _hash_api_key(raw_secret: str) -> str:
    pepper = config.api_key_pepper
    if not pepper:
        # In hosted mode we should treat this as misconfiguration.
        raise HTTPException(status_code=500, detail="API key hashing is not configured")
    digest = hashlib.sha256((pepper + raw_secret).encode("utf-8")).hexdigest()
    return digest


def _extract_api_key_from_request(request: Request) -> str | None:
    authz = request.headers.get("authorization") or request.headers.get("Authorization")
    if authz and authz.lower().startswith("bearer "):
        return authz.split(" ", 1)[1].strip() or None
    header = request.headers.get("x-api-key")
    return header.strip() if header and header.strip() else None


async def _verify_api_key(db: AsyncSession, raw_secret: str) -> ApiPrincipal:
    if not raw_secret or not raw_secret.strip():
        raise HTTPException(status_code=401, detail="Invalid API key")

    prefix = raw_secret.strip()[:16]
    expected_hash = _hash_api_key(raw_secret.strip())

    # RLS bypass for lookup before we know user_id.
    await db.execute(text("SELECT set_config('app.internal', '1', true)"))
    row = await ApiKeyRepository.get_active_key_by_prefix_internal(db, prefix=prefix)
    if not row:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if not hmac.compare_digest(row.key_hash, expected_hash):
        raise HTTPException(status_code=401, detail="Invalid API key")

    # Best-effort audit
    try:
        await ApiKeyRepository.touch_last_used_at_internal(db, api_key_id=row.id)
    except Exception:
        pass

    return ApiPrincipal(user_id=row.user_id, api_key_id=row.id)


async def require_api_principal(
    request: Request, db: AsyncSession = Depends(get_db)
) -> ApiPrincipal:
    raw = _extract_api_key_from_request(request)
    if not raw:
        raise HTTPException(status_code=401, detail="API key required")
    return await _verify_api_key(db, raw)


async def require_api_user_id(principal: ApiPrincipal = Depends(require_api_principal)) -> str:
    return principal.user_id

