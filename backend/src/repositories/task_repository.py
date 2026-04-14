"""
Task repository - handles all database operations for tasks.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class TaskRepository:
    """Repository for task-related database operations."""

    @staticmethod
    async def create_task(
        db: AsyncSession,
        user_id: str,
        source_id: str,
        status: str = "processing",
        font_family: str = "TikTokSans-Regular",
        font_size: int = 24,
        font_color: str = "#FFFFFF",
        caption_template: str = "default",
        include_broll: bool = False,
        processing_mode: str = "fast",
    ) -> str:
        """Create a new task and return its ID."""
        try:
            result = await db.execute(
                text("""
                    INSERT INTO tasks (
                        user_id, source_id, status, font_family, font_size, font_color,
                        caption_template, include_broll, processing_mode, created_at, updated_at
                    )
                    VALUES (
                        :user_id, :source_id, :status, :font_family, :font_size, :font_color,
                        :caption_template, :include_broll, :processing_mode, NOW(), NOW()
                    )
                    RETURNING id
                """),
                {
                    "user_id": user_id,
                    "source_id": source_id,
                    "status": status,
                    "font_family": font_family,
                    "font_size": font_size,
                    "font_color": font_color,
                    "caption_template": caption_template,
                    "include_broll": include_broll,
                    "processing_mode": processing_mode,
                },
            )
        except Exception:
            await db.rollback()
            result = await db.execute(
                text("""
                    INSERT INTO tasks (
                        user_id, source_id, status, font_family, font_size, font_color,
                        created_at, updated_at
                    )
                    VALUES (
                        :user_id, :source_id, :status, :font_family, :font_size, :font_color,
                        NOW(), NOW()
                    )
                    RETURNING id
                """),
                {
                    "user_id": user_id,
                    "source_id": source_id,
                    "status": status,
                    "font_family": font_family,
                    "font_size": font_size,
                    "font_color": font_color,
                },
            )
        await db.commit()
        task_id = result.scalar()
        if not task_id:
            raise RuntimeError("Failed to create task: no ID returned")
        logger.info(f"Created task {task_id} for user {user_id}")
        return str(task_id)

    @staticmethod
    async def get_task_by_id(
        db: AsyncSession, task_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get task by ID with source information."""
        try:
            result = await db.execute(
                text("""
                    SELECT t.*, s.title as source_title, s.type as source_type, s.url as source_url
                    FROM tasks t
                    LEFT JOIN sources s ON t.source_id = s.id
                    WHERE t.id = :task_id
                """),
                {"task_id": task_id},
            )
        except Exception:
            await db.rollback()
            result = await db.execute(
                text("""
                    SELECT t.*, s.title as source_title, s.type as source_type
                    FROM tasks t
                    LEFT JOIN sources s ON t.source_id = s.id
                    WHERE t.id = :task_id
                """),
                {"task_id": task_id},
            )
        row = result.fetchone()

        if not row:
            return None

        # Best-effort: if task_clips exists and has rows, expose generated_clips_ids
        # from the normalized ordering table to keep API compatibility.
        try:
            clip_ids_result = await db.execute(
                text(
                    """
                    SELECT clip_id
                    FROM task_clips
                    WHERE task_id = :task_id
                    ORDER BY position ASC
                    """
                ),
                {"task_id": task_id},
            )
            clip_ids_rows = clip_ids_result.fetchall()
            normalized_clip_ids = [r.clip_id for r in clip_ids_rows] if clip_ids_rows else None
        except Exception:
            normalized_clip_ids = None

        return {
            "id": row.id,
            "user_id": row.user_id,
            "source_id": row.source_id,
            "source_title": row.source_title,
            "source_type": row.source_type,
            "status": row.status,
            "progress": getattr(row, "progress", None),
            "progress_message": getattr(row, "progress_message", None),
            "generated_clips_ids": normalized_clip_ids or row.generated_clips_ids,
            "font_family": row.font_family,
            "font_size": row.font_size,
            "font_color": row.font_color,
            "caption_template": getattr(row, "caption_template", "default"),
            "include_broll": getattr(row, "include_broll", False),
            "processing_mode": getattr(row, "processing_mode", "fast"),
            "cache_hit": getattr(row, "cache_hit", False),
            "error_code": getattr(row, "error_code", None),
            "stage_timings_json": getattr(row, "stage_timings_json", None),
            "started_at": getattr(row, "started_at", None),
            "completed_at": getattr(row, "completed_at", None),
            "source_url": getattr(row, "source_url", None),
            "created_at": row.created_at,
            "updated_at": row.updated_at,
        }

    @staticmethod
    async def update_task_runtime_metadata(
        db: AsyncSession,
        task_id: str,
        cache_hit: Optional[bool] = None,
        error_code: Optional[str] = None,
        stage_timings_json: Optional[str] = None,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
    ) -> None:
        params: Dict[str, Any] = {"task_id": task_id}
        set_parts = []

        if cache_hit is not None:
            set_parts.append("cache_hit = :cache_hit")
            params["cache_hit"] = cache_hit

        if error_code is not None:
            set_parts.append("error_code = :error_code")
            params["error_code"] = error_code

        if stage_timings_json is not None:
            set_parts.append("stage_timings_json = :stage_timings_json")
            params["stage_timings_json"] = stage_timings_json

        if started_at is not None:
            set_parts.append("started_at = :started_at")
            params["started_at"] = started_at

        if completed_at is not None:
            set_parts.append("completed_at = :completed_at")
            params["completed_at"] = completed_at

        if not set_parts:
            return

        set_parts.append("updated_at = NOW()")
        query = f"UPDATE tasks SET {', '.join(set_parts)} WHERE id = :task_id"
        await db.execute(text(query), params)
        await db.commit()

    @staticmethod
    async def get_performance_metrics(db: AsyncSession) -> Dict[str, Any]:
        result = await db.execute(
            text(
                """
                SELECT
                    processing_mode,
                    COUNT(*) AS total_tasks,
                    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) AS avg_seconds,
                    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (completed_at - started_at))) AS p50_seconds,
                    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY EXTRACT(EPOCH FROM (completed_at - started_at))) AS p95_seconds,
                    SUM(CASE WHEN cache_hit THEN 1 ELSE 0 END) AS cache_hits
                FROM tasks
                WHERE started_at IS NOT NULL AND completed_at IS NOT NULL
                GROUP BY processing_mode
                ORDER BY processing_mode
                """
            )
        )

        rows = result.fetchall()
        metrics = []
        for row in rows:
            total = int(row.total_tasks or 0)
            cache_hits = int(row.cache_hits or 0)
            metrics.append(
                {
                    "processing_mode": row.processing_mode,
                    "total_tasks": total,
                    "avg_seconds": float(row.avg_seconds or 0),
                    "p50_seconds": float(row.p50_seconds or 0),
                    "p95_seconds": float(row.p95_seconds or 0),
                    "cache_hit_rate": (cache_hits / total) if total else 0,
                }
            )

        return {"modes": metrics}

    @staticmethod
    async def update_task_settings(
        db: AsyncSession,
        task_id: str,
        font_family: str,
        font_size: int,
        font_color: str,
        caption_template: str,
        include_broll: bool,
    ) -> None:
        """Update task styling settings."""
        try:
            await db.execute(
                text(
                    """
                    UPDATE tasks
                    SET font_family = :font_family,
                        font_size = :font_size,
                        font_color = :font_color,
                        caption_template = :caption_template,
                        include_broll = :include_broll,
                        updated_at = NOW()
                    WHERE id = :task_id
                    """
                ),
                {
                    "task_id": task_id,
                    "font_family": font_family,
                    "font_size": font_size,
                    "font_color": font_color,
                    "caption_template": caption_template,
                    "include_broll": include_broll,
                },
            )
        except Exception:
            await db.rollback()
            await db.execute(
                text(
                    """
                    UPDATE tasks
                    SET font_family = :font_family,
                        font_size = :font_size,
                        font_color = :font_color,
                        updated_at = NOW()
                    WHERE id = :task_id
                    """
                ),
                {
                    "task_id": task_id,
                    "font_family": font_family,
                    "font_size": font_size,
                    "font_color": font_color,
                },
            )
        await db.commit()

    @staticmethod
    async def update_task_status(
        db: AsyncSession,
        task_id: str,
        status: str,
        progress: Optional[int] = None,
        progress_message: Optional[str] = None,
    ) -> None:
        """Update task status and optional progress."""
        params = {
            "task_id": task_id,
            "status": status,
            "progress": progress,
            "progress_message": progress_message,
        }

        # Build dynamic query based on what's provided
        set_parts = ["status = :status"]

        if progress is not None:
            set_parts.append("progress = :progress")

        if progress_message is not None:
            set_parts.append("progress_message = :progress_message")

        set_parts.append("updated_at = NOW()")

        query = f"UPDATE tasks SET {', '.join(set_parts)} WHERE id = :task_id"

        await db.execute(text(query), params)
        await db.commit()
        logger.info(
            f"Updated task {task_id} status to {status}"
            + (f" (progress: {progress}%)" if progress else "")
        )

    @staticmethod
    async def update_task_clips(
        db: AsyncSession, task_id: str, clip_ids: List[str]
    ) -> None:
        """Update task with generated clip IDs."""
        await db.execute(
            text(
                "UPDATE tasks SET generated_clips_ids = :clip_ids, updated_at = NOW() WHERE id = :task_id"
            ),
            {"clip_ids": clip_ids, "task_id": task_id},
        )
        # Keep normalized ordering table in sync when present.
        # NOTE: tasks.generated_clips_ids is still kept for backward compatibility.
        if clip_ids:
            await db.execute(
                text("DELETE FROM task_clips WHERE task_id = :task_id"),
                {"task_id": task_id},
            )
            # position is 1-indexed
            await db.execute(
                text(
                    """
                    INSERT INTO task_clips (task_id, clip_id, position, created_at)
                    SELECT :task_id, x.clip_id, x.position, NOW()
                    FROM unnest(:clip_ids::varchar[]) WITH ORDINALITY AS x(clip_id, position)
                    """
                ),
                {"task_id": task_id, "clip_ids": clip_ids},
            )
        await db.commit()
        logger.info(f"Updated task {task_id} with {len(clip_ids)} clips")

    @staticmethod
    async def get_user_tasks(
        db: AsyncSession, user_id: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get all tasks for a user."""
        result = await db.execute(
            text(
                """
                WITH user_tasks AS (
                    SELECT
                        t.*,
                        s.title AS source_title,
                        s.type AS source_type
                    FROM tasks t
                    LEFT JOIN sources s ON t.source_id = s.id
                    WHERE t.user_id = :user_id
                    ORDER BY t.created_at DESC
                    LIMIT :limit
                ),
                clips_agg AS (
                    SELECT
                        gc.task_id,
                        COUNT(*)::int AS clips_count
                    FROM generated_clips gc
                    WHERE gc.task_id IN (SELECT id FROM user_tasks)
                    GROUP BY gc.task_id
                )
                SELECT
                    ut.*,
                    ut.source_title,
                    ut.source_type,
                    COALESCE(ca.clips_count, 0) AS clips_count
                FROM user_tasks ut
                LEFT JOIN clips_agg ca ON ca.task_id = ut.id
                ORDER BY ut.created_at DESC
                """
            ),
            {"user_id": user_id, "limit": limit},
        )

        tasks = []
        for row in result.fetchall():
            tasks.append(
                {
                    "id": row.id,
                    "user_id": row.user_id,
                    "source_id": row.source_id,
                    "source_title": row.source_title,
                    "source_type": row.source_type,
                    "status": row.status,
                    "processing_mode": getattr(row, "processing_mode", "fast"),
                    "clips_count": row.clips_count,
                    "created_at": row.created_at,
                    "updated_at": row.updated_at,
                }
            )

        return tasks

    @staticmethod
    async def get_tasks_by_status(
        db: AsyncSession, status: str
    ) -> List[Dict[str, Any]]:
        """Get all tasks with a given status."""
        result = await db.execute(
            text("""
                SELECT t.id, t.user_id, t.status, t.created_at, t.updated_at
                FROM tasks t
                WHERE t.status = :status
            """),
            {"status": status},
        )
        tasks = []
        for row in result.fetchall():
            tasks.append(
                {
                    "id": str(row.id),
                    "user_id": row.user_id,
                    "status": row.status,
                    "created_at": row.created_at,
                    "updated_at": row.updated_at,
                }
            )
        logger.debug(
            f"[get_tasks_by_status] found {len(tasks)} task(s) with status='{status}'"
        )
        return tasks

    @staticmethod
    async def user_exists(db: AsyncSession, user_id: str) -> bool:
        """Check if a user exists in the database."""
        result = await db.execute(
            text("SELECT 1 FROM users WHERE id = :user_id"), {"user_id": user_id}
        )
        return result.fetchone() is not None

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: str) -> None:
        """Delete a task by ID."""
        await db.execute(
            text("DELETE FROM tasks WHERE id = :task_id"), {"task_id": task_id}
        )
        await db.commit()
        logger.info(f"Deleted task {task_id}")
