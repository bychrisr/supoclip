from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional

from fastapi import HTTPException, Request
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class RateLimitResult:
    remaining: int
    limit: int
    retry_after_seconds: int
    window_seconds: int


_INCR_EXPIRE_LUA = """
local key = KEYS[1]
local window = tonumber(ARGV[1])
local current = redis.call("INCR", key)
if current == 1 then
  redis.call("EXPIRE", key, window)
end
local ttl = redis.call("TTL", key)
return {current, ttl}
"""


def get_client_ip(request: Request) -> str:
    # NOTE: We intentionally do not trust X-Forwarded-For here without a proxy
    # trust list; a spoofed header would allow bypassing the limiter.
    host = request.client.host if request.client else None
    return host or "unknown"


async def get_user_limit_override_per_minute(
    db: AsyncSession,
    redis_client: Redis,
    user_id: str,
    scope: str,
    *,
    cache_ttl_seconds: int = 60,
) -> Optional[int]:
    cache_key = f"user_limit:{user_id}:{scope}"
    cached = await redis_client.get(cache_key)
    if cached is not None:
        try:
            parsed = int(cached)
        except ValueError:
            return None
        return parsed

    result = await db.execute(
        text(
            """
            SELECT limit_per_minute
            FROM user_limits
            WHERE user_id = :user_id AND scope = :scope
            LIMIT 1
            """
        ),
        {"user_id": user_id, "scope": scope},
    )
    row = result.first()
    limit = int(row[0]) if row and row[0] is not None else None

    if limit is None:
        await redis_client.setex(cache_key, cache_ttl_seconds, "-1")
        return None

    await redis_client.setex(cache_key, cache_ttl_seconds, str(limit))
    return limit


async def enforce_rate_limit(
    *,
    request: Request,
    db: AsyncSession,
    redis_client: Redis,
    scope: str,
    default_limit_per_minute: int,
    window_seconds: int = 60,
    user_id: Optional[str],
) -> RateLimitResult:
    now_bucket = int(time.time() // window_seconds)

    if user_id:
        key_identity = f"user:{user_id}"
        override = await get_user_limit_override_per_minute(
            db, redis_client, user_id, scope
        )
        effective_limit = (
            override if (override is not None and override >= 0) else default_limit_per_minute
        )
    else:
        ip = get_client_ip(request)
        key_identity = f"ip:{ip}"
        effective_limit = default_limit_per_minute

    key = f"rate:{scope}:{key_identity}:{now_bucket}"

    current, ttl = await redis_client.eval(_INCR_EXPIRE_LUA, 1, key, window_seconds)
    current_int = int(current)
    ttl_int = int(ttl) if ttl is not None else window_seconds
    retry_after = max(1, ttl_int) if current_int > effective_limit else 0
    remaining = max(0, effective_limit - current_int)

    if current_int > effective_limit:
        raise HTTPException(
            status_code=429,
            detail={
                "code": "RATE_LIMITED",
                "message": "Too many requests. Please retry later.",
                "scope": scope,
                "limit_per_minute": effective_limit,
                "window_seconds": window_seconds,
                "retry_after_seconds": retry_after,
            },
            headers={"Retry-After": str(retry_after)},
        )

    return RateLimitResult(
        remaining=remaining,
        limit=effective_limit,
        retry_after_seconds=retry_after,
        window_seconds=window_seconds,
    )

