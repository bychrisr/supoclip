from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class ApiKeyRow:
    id: str
    user_id: str
    key_hash: str
    prefix: str
    name: str
    scopes: list[str]
    last_used_at: datetime | None
    revoked_at: datetime | None
    created_at: datetime


class ApiKeyRepository:
    @staticmethod
    async def create_key(
        db: AsyncSession,
        *,
        user_id: str,
        key_hash: str,
        prefix: str,
        name: str,
        scopes: list[str] | None = None,
    ) -> ApiKeyRow:
        scopes = scopes or []
        result = await db.execute(
            text(
                """
                INSERT INTO api_keys (user_id, key_hash, prefix, name, scopes)
                VALUES (:user_id, :key_hash, :prefix, :name, :scopes)
                RETURNING
                  id, user_id, key_hash, prefix, name, scopes, last_used_at, revoked_at, created_at
                """
            ),
            {
                "user_id": user_id,
                "key_hash": key_hash,
                "prefix": prefix,
                "name": name,
                "scopes": scopes,
            },
        )
        row = result.fetchone()
        if not row:
            raise RuntimeError("Failed to create API key")
        await db.commit()
        return ApiKeyRow(
            id=row.id,
            user_id=row.user_id,
            key_hash=row.key_hash,
            prefix=row.prefix,
            name=row.name,
            scopes=list(row.scopes or []),
            last_used_at=row.last_used_at,
            revoked_at=row.revoked_at,
            created_at=row.created_at,
        )

    @staticmethod
    async def list_keys(db: AsyncSession, *, user_id: str) -> list[ApiKeyRow]:
        result = await db.execute(
            text(
                """
                SELECT id, user_id, key_hash, prefix, name, scopes, last_used_at, revoked_at, created_at
                FROM api_keys
                WHERE user_id = :user_id
                ORDER BY created_at DESC
                """
            ),
            {"user_id": user_id},
        )
        rows = result.fetchall() or []
        return [
            ApiKeyRow(
                id=row.id,
                user_id=row.user_id,
                key_hash=row.key_hash,
                prefix=row.prefix,
                name=row.name,
                scopes=list(row.scopes or []),
                last_used_at=row.last_used_at,
                revoked_at=row.revoked_at,
                created_at=row.created_at,
            )
            for row in rows
        ]

    @staticmethod
    async def revoke_key(db: AsyncSession, *, user_id: str, api_key_id: str) -> bool:
        now = datetime.now(timezone.utc)
        result = await db.execute(
            text(
                """
                UPDATE api_keys
                SET revoked_at = :now
                WHERE id = :id
                  AND user_id = :user_id
                  AND revoked_at IS NULL
                """
            ),
            {"id": api_key_id, "user_id": user_id, "now": now},
        )
        await db.commit()
        return (result.rowcount or 0) > 0

    @staticmethod
    async def get_active_key_by_prefix_internal(
        db: AsyncSession, *, prefix: str
    ) -> ApiKeyRow | None:
        """
        Internal lookup for authentication.

        IMPORTANT: caller must be operating with app.internal=1 so RLS does not block
        before user_id is known.
        """
        result = await db.execute(
            text(
                """
                SELECT id, user_id, key_hash, prefix, name, scopes, last_used_at, revoked_at, created_at
                FROM api_keys
                WHERE prefix = :prefix
                  AND revoked_at IS NULL
                ORDER BY created_at DESC
                LIMIT 1
                """
            ),
            {"prefix": prefix},
        )
        row = result.fetchone()
        if not row:
            return None
        return ApiKeyRow(
            id=row.id,
            user_id=row.user_id,
            key_hash=row.key_hash,
            prefix=row.prefix,
            name=row.name,
            scopes=list(row.scopes or []),
            last_used_at=row.last_used_at,
            revoked_at=row.revoked_at,
            created_at=row.created_at,
        )

    @staticmethod
    async def touch_last_used_at_internal(db: AsyncSession, *, api_key_id: str) -> None:
        now = datetime.now(timezone.utc)
        await db.execute(
            text("UPDATE api_keys SET last_used_at = :now WHERE id = :id"),
            {"id": api_key_id, "now": now},
        )
        await db.commit()

