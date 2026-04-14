import asyncio
import logging
import time

from sqlalchemy import text

from ..config import Config
from ..database import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def cleanup_expired_processing_cache(*, batch_size: int) -> int:
    """
    Delete expired rows from processing_cache in batches.
    Returns the number of rows deleted in this call.
    """
    deleted_total = 0
    started = time.perf_counter()

    async with AsyncSessionLocal() as session:
        while True:
            result = await session.execute(
                text(
                    """
                    WITH doomed AS (
                      SELECT ctid
                      FROM processing_cache
                      WHERE expires_at IS NOT NULL
                        AND expires_at <= NOW()
                      LIMIT :limit
                    )
                    DELETE FROM processing_cache
                    WHERE ctid IN (SELECT ctid FROM doomed)
                    """
                ),
                {"limit": batch_size},
            )
            await session.commit()
            deleted = int(result.rowcount or 0)
            deleted_total += deleted
            if deleted < batch_size:
                break

    elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
    if deleted_total:
        logger.info(
            "[processing_cache_cleanup] deleted=%s elapsed_ms=%s batch_size=%s",
            deleted_total,
            elapsed_ms,
            batch_size,
        )
    return deleted_total


async def processing_cache_cleanup_loop(stop_event: asyncio.Event) -> None:
    config = Config()
    interval = max(30, int(config.processing_cache_cleanup_interval_seconds))
    batch_size = max(100, int(config.processing_cache_cleanup_batch_size))

    logger.info(
        "[processing_cache_cleanup] loop started interval_s=%s batch_size=%s",
        interval,
        batch_size,
    )

    try:
        # Startup sweep (no delay)
        await cleanup_expired_processing_cache(batch_size=batch_size)

        while not stop_event.is_set():
            try:
                await asyncio.wait_for(stop_event.wait(), timeout=interval)
            except asyncio.TimeoutError:
                pass

            if stop_event.is_set():
                break

            await cleanup_expired_processing_cache(batch_size=batch_size)
    except asyncio.CancelledError:
        raise
    except Exception:
        logger.exception("[processing_cache_cleanup] loop error")
    finally:
        logger.info("[processing_cache_cleanup] loop stopped")

