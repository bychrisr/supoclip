from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class WebhookDeliveryRow:
    id: str
    webhook_id: str
    user_id: str
    event: str
    payload: dict
    status: str
    attempt: int
    response_status: int | None
    response_body: str | None
    last_error: str | None
    delivered_at: datetime | None
    created_at: datetime


class WebhookDeliveryRepository:
    @staticmethod
    async def create_delivery(
        db: AsyncSession,
        *,
        webhook_id: str,
        user_id: str,
        event: str,
        payload: dict,
    ) -> WebhookDeliveryRow:
        result = await db.execute(
            text(
                """
                INSERT INTO webhook_deliveries (webhook_id, user_id, event, payload, status, attempt)
                VALUES (:webhook_id, :user_id, :event, :payload::jsonb, 'pending', 1)
                RETURNING
                  id, webhook_id, user_id, event, payload, status, attempt,
                  response_status, response_body, last_error, delivered_at, created_at
                """
            ),
            {
                "webhook_id": webhook_id,
                "user_id": user_id,
                "event": event,
                "payload": payload,
            },
        )
        row = result.fetchone()
        if not row:
            raise RuntimeError("Failed to create webhook delivery")
        await db.commit()
        return WebhookDeliveryRow(
            id=row.id,
            webhook_id=row.webhook_id,
            user_id=row.user_id,
            event=row.event,
            payload=dict(row.payload),
            status=row.status,
            attempt=int(row.attempt),
            response_status=row.response_status,
            response_body=row.response_body,
            last_error=row.last_error,
            delivered_at=row.delivered_at,
            created_at=row.created_at,
        )

    @staticmethod
    async def mark_attempt(
        db: AsyncSession,
        *,
        delivery_id: str,
        attempt: int,
        response_status: int | None = None,
        response_body: str | None = None,
        last_error: str | None = None,
        status: str | None = None,
    ) -> None:
        await db.execute(
            text(
                """
                UPDATE webhook_deliveries
                SET
                  attempt = :attempt,
                  response_status = COALESCE(:response_status, response_status),
                  response_body = COALESCE(:response_body, response_body),
                  last_error = COALESCE(:last_error, last_error),
                  status = COALESCE(:status, status),
                  delivered_at = CASE WHEN :mark_delivered THEN :now ELSE delivered_at END
                WHERE id = :id
                """
            ),
            {
                "id": delivery_id,
                "attempt": attempt,
                "response_status": response_status,
                "response_body": response_body,
                "last_error": last_error,
                "status": status,
                "mark_delivered": status == "success",
                "now": datetime.now(timezone.utc),
            },
        )
        await db.commit()

    @staticmethod
    async def list_deliveries_for_webhook(
        db: AsyncSession,
        *,
        user_id: str,
        webhook_id: str,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict]:
        result = await db.execute(
            text(
                """
                SELECT id, webhook_id, user_id, event, status, attempt,
                       response_status, response_body, last_error, delivered_at, created_at
                FROM webhook_deliveries
                WHERE user_id = :user_id AND webhook_id = :webhook_id
                ORDER BY created_at DESC
                LIMIT :limit OFFSET :offset
                """
            ),
            {
                "user_id": user_id,
                "webhook_id": webhook_id,
                "limit": limit,
                "offset": offset,
            },
        )
        rows = result.fetchall() or []
        return [
            {
                "id": r.id,
                "webhook_id": r.webhook_id,
                "event": r.event,
                "status": r.status,
                "attempt": int(r.attempt),
                "response_status": r.response_status,
                "response_body": r.response_body,
                "last_error": r.last_error,
                "delivered_at": r.delivered_at,
                "created_at": r.created_at,
            }
            for r in rows
        ]

