from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class WebhookRow:
    id: str
    user_id: str
    url: str
    events: list[str]
    enabled: bool
    secret: str
    created_at: str


class WebhookRepository:
    @staticmethod
    async def list_webhooks(db: AsyncSession, *, user_id: str) -> list[WebhookRow]:
        result = await db.execute(
            text(
                """
                SELECT id, user_id, url, events, enabled, secret, created_at
                FROM webhooks
                WHERE user_id = :user_id
                ORDER BY created_at DESC
                """
            ),
            {"user_id": user_id},
        )
        rows = result.fetchall() or []
        return [
            WebhookRow(
                id=r.id,
                user_id=r.user_id,
                url=r.url,
                events=list(r.events or []),
                enabled=bool(r.enabled),
                secret=r.secret,
                created_at=r.created_at.isoformat() if hasattr(r.created_at, "isoformat") else str(r.created_at),
            )
            for r in rows
        ]

    @staticmethod
    async def create_webhook(
        db: AsyncSession,
        *,
        user_id: str,
        url: str,
        events: list[str],
        enabled: bool,
        secret: str,
    ) -> WebhookRow:
        result = await db.execute(
            text(
                """
                INSERT INTO webhooks (user_id, url, events, enabled, secret)
                VALUES (:user_id, :url, :events, :enabled, :secret)
                RETURNING id, user_id, url, events, enabled, secret, created_at
                """
            ),
            {
                "user_id": user_id,
                "url": url,
                "events": events,
                "enabled": enabled,
                "secret": secret,
            },
        )
        row = result.fetchone()
        if not row:
            raise RuntimeError("Failed to create webhook")
        await db.commit()
        return WebhookRow(
            id=row.id,
            user_id=row.user_id,
            url=row.url,
            events=list(row.events or []),
            enabled=bool(row.enabled),
            secret=row.secret,
            created_at=row.created_at.isoformat()
            if hasattr(row.created_at, "isoformat")
            else str(row.created_at),
        )

    @staticmethod
    async def update_webhook(
        db: AsyncSession,
        *,
        user_id: str,
        webhook_id: str,
        url: str | None = None,
        events: list[str] | None = None,
        enabled: bool | None = None,
    ) -> WebhookRow | None:
        result = await db.execute(
            text(
                """
                UPDATE webhooks
                SET
                  url = COALESCE(:url, url),
                  events = COALESCE(:events, events),
                  enabled = COALESCE(:enabled, enabled)
                WHERE id = :id AND user_id = :user_id
                RETURNING id, user_id, url, events, enabled, secret, created_at
                """
            ),
            {
                "id": webhook_id,
                "user_id": user_id,
                "url": url,
                "events": events,
                "enabled": enabled,
            },
        )
        row = result.fetchone()
        if not row:
            await db.rollback()
            return None
        await db.commit()
        return WebhookRow(
            id=row.id,
            user_id=row.user_id,
            url=row.url,
            events=list(row.events or []),
            enabled=bool(row.enabled),
            secret=row.secret,
            created_at=row.created_at.isoformat()
            if hasattr(row.created_at, "isoformat")
            else str(row.created_at),
        )

    @staticmethod
    async def delete_webhook(db: AsyncSession, *, user_id: str, webhook_id: str) -> bool:
        result = await db.execute(
            text("DELETE FROM webhooks WHERE id = :id AND user_id = :user_id"),
            {"id": webhook_id, "user_id": user_id},
        )
        await db.commit()
        return (result.rowcount or 0) > 0

    @staticmethod
    async def list_enabled_for_event(db: AsyncSession, *, user_id: str, event: str) -> list[WebhookRow]:
        result = await db.execute(
            text(
                """
                SELECT id, user_id, url, events, enabled, secret, created_at
                FROM webhooks
                WHERE user_id = :user_id
                  AND enabled = true
                  AND :event = ANY(events)
                ORDER BY created_at DESC
                """
            ),
            {"user_id": user_id, "event": event},
        )
        rows = result.fetchall() or []
        return [
            WebhookRow(
                id=r.id,
                user_id=r.user_id,
                url=r.url,
                events=list(r.events or []),
                enabled=bool(r.enabled),
                secret=r.secret,
                created_at=r.created_at.isoformat() if hasattr(r.created_at, "isoformat") else str(r.created_at),
            )
            for r in rows
        ]

