"""
Worker tasks - background jobs processed by arq workers.
"""

import logging
from typing import Dict, Any
import json
import math

from ..observability import configure_logging, set_trace_id

configure_logging()

logger = logging.getLogger(__name__)


async def process_video_task(
    ctx: Dict[str, Any],
    task_id: str,
    url: str,
    source_type: str,
    user_id: str,
    font_family: str = "TikTokSans-Regular",
    font_size: int = 24,
    font_color: str = "#FFFFFF",
    caption_template: str = "default",
    processing_mode: str = "fast",
    output_format: str = "vertical",
    add_subtitles: bool = True,
    video_quality: str = "best",
) -> Dict[str, Any]:
    """
    Background worker task to process a video.

    Args:
        ctx: arq context (provides Redis connection and other utilities)
        task_id: Task ID to update
        url: Video URL or file path
        source_type: "youtube" or "upload"
        user_id: User ID who created the task
        font_family: Font family for subtitles
        font_size: Font size for subtitles
        font_color: Font color for subtitles

    Returns:
        Dict with processing results
    """
    from ..database import AsyncSessionLocal
    from ..services.task_service import TaskService
    from ..workers.progress import ProgressTracker

    set_trace_id(f"task-{task_id}")
    logger.info(f"Worker processing task {task_id}")

    # Create progress tracker
    progress = ProgressTracker(ctx["redis"], task_id)

    async with AsyncSessionLocal() as db:
        # Worker must bypass RLS for maintenance/processing operations.
        from ..database import set_rls_context

        await set_rls_context(db, user_id=user_id, internal=True)
        task_service = TaskService(db)

        try:
            async def _emit_webhook(event: str, payload: dict[str, Any]) -> None:
                """
                Best-effort webhook dispatcher.
                Never fails the main processing task.
                """
                try:
                    from ..repositories.webhook_repository import WebhookRepository
                    from ..repositories.webhook_delivery_repository import (
                        WebhookDeliveryRepository,
                    )

                    hooks = await WebhookRepository.list_enabled_for_event(
                        db, user_id=user_id, event=event
                    )
                    for hook in hooks:
                        delivery = await WebhookDeliveryRepository.create_delivery(
                            db,
                            webhook_id=hook.id,
                            user_id=user_id,
                            event=event,
                            payload=payload,
                        )
                        await ctx["redis"].enqueue_job(
                            "deliver_webhook_event_task",
                            hook.id,
                            user_id,
                            delivery.id,
                            event,
                            payload,
                        )
                except Exception:
                    logger.exception(
                        "Webhook emit failed for event=%s task_id=%s", event, task_id
                    )

            # Progress callback
            async def update_progress(
                percent: int, message: str, status: str = "processing"
            ):
                await progress.update(percent, message, status)
                logger.info(f"Task {task_id}: {percent}% - {message}")

            async def should_cancel() -> bool:
                cancelled = await ctx["redis"].get(f"task_cancel:{task_id}")
                return bool(cancelled)

            # Process the video
            await _emit_webhook(
                "task.processing_started",
                {"task_id": task_id, "user_id": user_id, "source_url": url},
            )
            result = await task_service.process_task(
                task_id=task_id,
                url=url,
                source_type=source_type,
                font_family=font_family,
                font_size=font_size,
                font_color=font_color,
                caption_template=caption_template,
                processing_mode=processing_mode,
                output_format=output_format,
                add_subtitles=add_subtitles,
                video_quality=video_quality,
                progress_callback=update_progress,
                should_cancel=should_cancel,
            )

            try:
                from ..repositories.billing_record_repository import (
                    BillingRecordRepository,
                )

                duration_seconds = result.get("video_duration_seconds")
                minutes_processed = 0
                if isinstance(duration_seconds, (int, float)) and duration_seconds > 0:
                    minutes_processed = max(1, int(math.ceil(duration_seconds / 60.0)))

                task_row = await task_service.task_repo.get_task_by_id(db, task_id)
                source_url = None
                source_title = None
                if task_row:
                    source_url = task_row.get("source_url")
                    source_title = task_row.get("source_title")

                await BillingRecordRepository.insert_billing_record(
                    db,
                    user_id=user_id,
                    task_id=task_id,
                    minutes_processed=minutes_processed,
                    source_url=source_url,
                    source_title=source_title,
                )
            except Exception:
                logger.exception(
                    "Failed to insert billing record for completed task %s", task_id
                )

            await _emit_webhook(
                "task.processing_completed",
                {
                    "task_id": task_id,
                    "user_id": user_id,
                    "minutes_processed": minutes_processed,
                    "clips_count": len(result.get("clips") or []),
                },
            )

            logger.info(f"Task {task_id} completed successfully")
            return result

        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}", exc_info=True)
            await _emit_webhook(
                "task.processing_failed",
                {"task_id": task_id, "user_id": user_id, "error": str(e)},
            )
            try:
                job_try = int(ctx.get("job_try", 1))
                max_tries = int(getattr(WorkerSettings, "max_tries", 3))
                if job_try >= max_tries:
                    payload = {
                        "task_id": task_id,
                        "error": str(e),
                        "tries": job_try,
                    }
                    await ctx["redis"].set(
                        f"dead_letter:{task_id}", json.dumps(payload)
                    )
                    await ctx["redis"].sadd("tasks:dead_letter", task_id)
                    await progress.error("Task failed permanently after retries")
            except Exception:
                logger.exception("Failed to persist dead-letter payload")
            # Error will be caught by arq and task status will be updated
            raise


async def deliver_webhook_event_task(
    ctx: Dict[str, Any],
    webhook_id: str,
    user_id: str,
    delivery_id: str,
    event: str,
    payload: dict[str, Any],
) -> None:
    """
    Separate ARQ task so delivery retries are handled by the queue.
    """
    from ..database import AsyncSessionLocal, set_rls_context
    from .webhooks import deliver_webhook_event

    attempt = int(ctx.get("job_try", 1))
    async with AsyncSessionLocal() as db:
        await set_rls_context(db, user_id=user_id, internal=True)
        await deliver_webhook_event(
            db=db,
            webhook_id=webhook_id,
            user_id=user_id,
            delivery_id=delivery_id,
            event=event,
            payload=payload,
            attempt=attempt,
        )


async def run_startup_sweep(ctx: Dict[str, Any]) -> None:
    """
    Varre tasks stuck em 'queued' além do timeout e as marca como error.
    Também inicializa o health check do provider de transcrição.
    Executado uma vez no startup do worker — nunca em requisições HTTP.
    """
    from ..database import AsyncSessionLocal
    from ..services.task_service import TaskService
    from ..services.transcription_service import TranscriptionService

    logger.info("[run_startup_sweep] start")

    # Health check do provider de transcrição (Gemini → AssemblyAI fallback)
    try:
        gemini_ok = await TranscriptionService.run_health_check()
        provider = "Gemini" if gemini_ok else "AssemblyAI"
        logger.info(f"[run_startup_sweep] Transcription provider: {provider}")
    except Exception as e:
        logger.error(f"[run_startup_sweep] transcription health check failed: {e}", exc_info=True)

    # Varre tasks stale
    try:
        async with AsyncSessionLocal() as db:
            task_service = TaskService(db)
            marked = await task_service.sweep_stale_tasks()
            if marked:
                logger.warning(
                    f"[run_startup_sweep] marked {len(marked)} stale task(s) as error: {marked}"
                )
            else:
                logger.info("[run_startup_sweep] no stale tasks found")
    except Exception as e:
        logger.error(f"[run_startup_sweep] failed: {e}", exc_info=True)


# Worker configuration for arq
class WorkerSettings:
    """Configuration for arq worker."""

    from ..config import Config
    from arq.connections import RedisSettings

    config = Config()

    # Functions to run
    functions = [process_video_task, deliver_webhook_event_task]
    queue_name = "supoclip_tasks"

    # Redis settings from environment
    redis_settings = RedisSettings(
        host=config.redis_host, port=config.redis_port, database=0
    )

    # Retry settings
    max_tries = 3  # Retry failed jobs up to 3 times
    job_timeout = 3600  # 1 hour timeout for video processing

    # Worker pool settings
    max_jobs = 4  # Process up to 4 jobs simultaneously

    # Startup hook — varre tasks stale antes de aceitar jobs
    on_startup = run_startup_sweep
