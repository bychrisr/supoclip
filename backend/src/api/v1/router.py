from __future__ import annotations

from pathlib import Path
import logging
import secrets
import uuid

import aiofiles
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from ...config import Config
from ...database import get_db
from ...repositories.api_key_repository import ApiKeyRepository
from ...services.task_service import TaskService
from ...workers.job_queue import JobQueue
from .auth import require_api_user_id
from .schemas import (
    ApiKeyCreateRequest,
    ApiKeyCreateResponse,
    ApiKeyListItem,
    ApiKeyListResponse,
    ClipListResponse,
    JobStatusResponse,
    StartClippingJobRequest,
    StartClippingJobResponse,
    VideoUploadResponse,
)


logger = logging.getLogger(__name__)
config = Config()

router = APIRouter(prefix="/api/v1", tags=["api-v1"])


def _safe_join(base: Path, filename: str) -> Path:
    # Prevent path traversal; only allow plain filenames.
    if "/" in filename or "\\" in filename or filename.strip() != filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    resolved = (base / filename).resolve()
    if base.resolve() not in resolved.parents and resolved != base.resolve():
        raise HTTPException(status_code=400, detail="Invalid filename")
    return resolved


@router.post("/videos/upload", response_model=VideoUploadResponse)
async def upload_video(
    _: str = Depends(require_api_user_id),
    file: UploadFile = File(..., alias="file"),
):
    """
    Upload a video file and get back a `upload://...` URL for use in `POST /api/v1/jobs/clipping`.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing file name")

    uploads_dir = Path(config.temp_dir) / "uploads"
    uploads_dir.mkdir(parents=True, exist_ok=True)

    ext = Path(file.filename).suffix.lower() or ".mp4"
    unique_filename = f"{uuid.uuid4()}{ext}"
    video_path = uploads_dir / unique_filename

    try:
        async with aiofiles.open(video_path, "wb") as f:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                await f.write(chunk)
    except Exception as e:
        logger.error("Error uploading video: %s", e)
        raise HTTPException(status_code=500, detail="Error uploading video") from e

    return VideoUploadResponse(video_url=f"upload://{unique_filename}")


def _utc_iso(dt: datetime | None) -> str | None:
    if not dt:
        return None
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


@router.post("/keys", response_model=ApiKeyCreateResponse)
async def create_api_key(
    body: ApiKeyCreateRequest,
    user_id: str = Depends(require_api_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new API key for the authenticated user.
    The secret is returned only once. Only a hash is stored server-side.
    """
    if not config.api_key_pepper:
        raise HTTPException(status_code=500, detail="API key hashing is not configured")

    raw_secret = secrets.token_urlsafe(32)
    prefix = raw_secret[:16]

    from .auth import _hash_api_key  # local import to avoid circular init surprises

    key_hash = _hash_api_key(raw_secret)
    row = await ApiKeyRepository.create_key(
        db,
        user_id=user_id,
        key_hash=key_hash,
        prefix=prefix,
        name=body.name,
        scopes=body.scopes,
    )
    return ApiKeyCreateResponse(
        id=row.id,
        prefix=row.prefix,
        name=row.name,
        scopes=row.scopes,
        api_key=raw_secret,
    )


@router.get("/keys", response_model=ApiKeyListResponse)
async def list_api_keys(
    user_id: str = Depends(require_api_user_id),
    db: AsyncSession = Depends(get_db),
):
    rows = await ApiKeyRepository.list_keys(db, user_id=user_id)
    return ApiKeyListResponse(
        keys=[
            ApiKeyListItem(
                id=r.id,
                prefix=r.prefix,
                name=r.name,
                scopes=r.scopes,
                last_used_at=_utc_iso(r.last_used_at),
                revoked_at=_utc_iso(r.revoked_at),
                created_at=_utc_iso(r.created_at) or datetime.now(timezone.utc).isoformat(),
            )
            for r in rows
        ]
    )


@router.delete("/keys/{api_key_id}")
async def revoke_api_key(
    api_key_id: str,
    user_id: str = Depends(require_api_user_id),
    db: AsyncSession = Depends(get_db),
):
    ok = await ApiKeyRepository.revoke_key(db, user_id=user_id, api_key_id=api_key_id)
    if not ok:
        raise HTTPException(status_code=404, detail="API key not found")
    return {"revoked": True}


@router.post("/jobs/clipping", response_model=StartClippingJobResponse)
async def start_clipping_job(
    body: StartClippingJobRequest,
    user_id: str = Depends(require_api_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a clipping task and enqueue it into the existing worker pipeline.
    """
    url = body.source.url
    if not url:
        raise HTTPException(status_code=400, detail="source.url is required")

    task_service = TaskService(db)

    processing_mode = body.processing_mode or config.default_processing_mode
    if processing_mode not in {"fast", "balanced", "quality"}:
        processing_mode = config.default_processing_mode

    output_format = body.output_format or "vertical"
    if output_format not in {"vertical", "original"}:
        output_format = "vertical"

    add_subtitles = True if body.add_subtitles is None else bool(body.add_subtitles)

    video_quality = body.video_quality or "best"
    if video_quality not in {"best", "1080p", "720p", "480p"}:
        video_quality = "best"

    font_family = body.font_family or "TikTokSans-Regular"
    font_size = int(body.font_size or 24)
    font_color = body.font_color or "#FFFFFF"
    caption_template = body.caption_template or "default"
    include_broll = bool(body.include_broll) if body.include_broll is not None else False

    try:
        task_id = await task_service.create_task_with_source(
            user_id=user_id,
            url=url,
            title=body.source.title,
            font_family=font_family,
            font_size=font_size,
            font_color=font_color,
            caption_template=caption_template,
            include_broll=include_broll,
            processing_mode=processing_mode,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.error("Error creating task: %s", e)
        raise HTTPException(status_code=500, detail="Error creating task") from e

    source_type = task_service.video_service.determine_source_type(url)

    try:
        queue_job_id = await JobQueue.enqueue_processing_job(
            "process_video_task",
            processing_mode,
            task_id,
            url,
            source_type,
            user_id,
            font_family,
            font_size,
            font_color,
            caption_template,
            processing_mode,
            output_format,
            add_subtitles,
            video_quality,
        )
    except Exception as e:
        logger.error("Error enqueueing job: %s", e)
        raise HTTPException(status_code=500, detail="Error enqueueing job") from e

    return StartClippingJobResponse(task_id=task_id, queue_job_id=queue_job_id)


@router.get("/jobs/{task_id}", response_model=JobStatusResponse)
async def get_job_status(
    task_id: str,
    user_id: str = Depends(require_api_user_id),
    db: AsyncSession = Depends(get_db),
):
    """
    Get job/task status (API-first).

    Note: this surfaces the task state tracked in Postgres (status/progress/message),
    which is the source of truth used by the existing UI and worker pipeline.
    """
    task_service = TaskService(db)
    task = await task_service.task_repo.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Not authorized for this task")

    return JobStatusResponse(
        task_id=task_id,
        status=task.get("status"),
        progress=task.get("progress"),
        message=task.get("progress_message"),
    )


@router.get("/jobs/{task_id}/clips", response_model=ClipListResponse)
async def list_task_clips(
    task_id: str,
    user_id: str = Depends(require_api_user_id),
    db: AsyncSession = Depends(get_db),
):
    task_service = TaskService(db)
    task = await task_service.task_repo.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.get("user_id") != user_id:
        raise HTTPException(status_code=403, detail="Not authorized for this task")

    task_with_clips = await task_service.get_task_with_clips(task_id)
    clips = (task_with_clips or {}).get("clips", []) if task_with_clips else []
    return ClipListResponse(task_id=task_id, clips=clips, total_clips=len(clips))


@router.get("/clips/{filename}/download")
async def download_clip(
    filename: str,
    _: str = Depends(require_api_user_id),
):
    """
    Download a generated clip by filename.

    This reuses the same storage location mounted at `/clips` in the main app.
    """
    clips_dir = Path(config.temp_dir) / "clips"
    clip_path = _safe_join(clips_dir, filename)
    if not clip_path.exists() or not clip_path.is_file():
        raise HTTPException(status_code=404, detail="Clip not found")

    return FileResponse(
        path=str(clip_path),
        media_type="video/mp4",
        filename=filename,
        headers={"Cache-Control": "private, max-age=31536000"},
    )

