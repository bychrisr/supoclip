"""
Billing record repository - persists and queries usage records.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class BillingRecordRepository:
    @staticmethod
    async def insert_billing_record(
        db: AsyncSession,
        *,
        user_id: str,
        task_id: str,
        minutes_processed: int,
        source_url: str | None,
        source_title: str | None,
    ) -> None:
        """
        Insert a billing record for a completed task.

        Idempotency: DB has a UNIQUE(task_id) constraint; retries are ignored.
        """
        await db.execute(
            text(
                """
                INSERT INTO billing_records (
                    user_id,
                    task_id,
                    minutes_processed,
                    source_url,
                    source_title,
                    created_at
                )
                VALUES (
                    :user_id,
                    :task_id,
                    :minutes_processed,
                    :source_url,
                    :source_title,
                    NOW()
                )
                ON CONFLICT (task_id) DO NOTHING
                """
            ),
            {
                "user_id": user_id,
                "task_id": task_id,
                "minutes_processed": minutes_processed,
                "source_url": source_url,
                "source_title": source_title,
            },
        )
        await db.commit()

    @staticmethod
    async def sum_minutes_processed(
        db: AsyncSession,
        *,
        user_id: str,
        period_start: datetime,
        period_end: datetime,
    ) -> int:
        result = await db.execute(
            text(
                """
                SELECT COALESCE(SUM(minutes_processed), 0)::int AS total
                FROM billing_records
                WHERE user_id = :user_id
                  AND created_at >= :period_start
                  AND created_at <= :period_end
                """
            ),
            {
                "user_id": user_id,
                "period_start": period_start,
                "period_end": period_end,
            },
        )
        row = result.fetchone()
        return int(row.total) if row and row.total is not None else 0

    @staticmethod
    async def list_billing_records(
        db: AsyncSession,
        *,
        user_id: str,
        period_start: datetime,
        period_end: datetime,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        result = await db.execute(
            text(
                """
                SELECT
                    id,
                    user_id,
                    task_id,
                    minutes_processed,
                    source_url,
                    source_title,
                    created_at
                FROM billing_records
                WHERE user_id = :user_id
                  AND created_at >= :period_start
                  AND created_at <= :period_end
                ORDER BY created_at DESC
                LIMIT :limit
                OFFSET :offset
                """
            ),
            {
                "user_id": user_id,
                "period_start": period_start,
                "period_end": period_end,
                "limit": limit,
                "offset": offset,
            },
        )
        rows = result.fetchall()
        return [
            {
                "id": r.id,
                "user_id": r.user_id,
                "task_id": r.task_id,
                "minutes_processed": int(r.minutes_processed or 0),
                "source_url": r.source_url,
                "source_title": r.source_title,
                "created_at": r.created_at,
            }
            for r in rows
        ]

    @staticmethod
    async def count_billing_records(
        db: AsyncSession,
        *,
        user_id: str,
        period_start: datetime,
        period_end: datetime,
    ) -> int:
        result = await db.execute(
            text(
                """
                SELECT COUNT(*)::int AS total
                FROM billing_records
                WHERE user_id = :user_id
                  AND created_at >= :period_start
                  AND created_at <= :period_end
                """
            ),
            {
                "user_id": user_id,
                "period_start": period_start,
                "period_end": period_end,
            },
        )
        row = result.fetchone()
        return int(row.total) if row and row.total is not None else 0

