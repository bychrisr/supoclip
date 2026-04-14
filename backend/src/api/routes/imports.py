"""
Import endpoints for external video sources (Google Drive, Vimeo, Loom).

MVP: accepts either:
- a public share URL
- a provider API token (dev)
- a direct/presigned download URL (allowlisted)
"""

import logging
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from redis.asyncio import Redis

from ...config import Config
from ...database import get_db
from ...auth_headers import get_signed_user_id, USER_ID_HEADER
from ...rate_limit import enforce_rate_limit
from ...services.import_service import ImportService, ImportError

logger = logging.getLogger(__name__)
config = Config()
router = APIRouter(prefix="/imports", tags=["imports"])


class ImportResolveRequest(BaseModel):
    provider: Optional[str] = Field(
        default=None,
        description="One of: google_drive, vimeo, loom, direct. If omitted, inferred from URL.",
    )
    url: str = Field(..., min_length=1, max_length=4000)
    api_token: Optional[str] = Field(
        default=None,
        description="Provider API token (dev). If IMPORT_DEV_TOKEN is set, requires x-import-dev-token header.",
    )


class ImportResolveResponse(BaseModel):
    provider: str
    original_url: str
    download_url: str
    title: Optional[str] = None
    filename: Optional[str] = None
    headers: dict[str, str] = Field(default_factory=dict, description="Headers needed to download")


class ImportDownloadRequest(ImportResolveRequest):
    pass


class ImportDownloadResponse(BaseModel):
    provider: str
    source_url: str
    download_url: str
    video_path: str = Field(..., description="upload://<filename> reference for task creation")
    bytes: int
    title: Optional[str] = None


async def _get_redis_client() -> Redis:
    return redis.Redis(host=config.redis_host, port=config.redis_port, decode_responses=True)


def _get_authenticated_user_id(request: Request) -> str:
    if config.monetization_enabled:
        return get_signed_user_id(request, config)
    user_id = request.headers.get("user_id") or request.headers.get(USER_ID_HEADER)
    if not user_id:
        raise HTTPException(status_code=401, detail="User authentication required")
    return user_id


async def _rate_limit_imports(request: Request, db: AsyncSession = Depends(get_db)) -> None:
    redis_client = await _get_redis_client()
    try:
        await enforce_rate_limit(
            request=request,
            db=db,
            redis_client=redis_client,
            scope="imports",
            default_limit_per_minute=20,
            user_id=None,
        )
    finally:
        await redis_client.aclose()


def _assert_dev_token_if_needed(request: Request, body: ImportResolveRequest) -> None:
    if not body.api_token:
        return
    required = config.import_dev_token
    if not required:
        return
    provided = request.headers.get("x-import-dev-token")
    if not provided or provided.strip() != required:
        raise HTTPException(status_code=403, detail="Missing or invalid import dev token")


@router.post("/resolve", response_model=ImportResolveResponse)
async def resolve_import(
    body: ImportResolveRequest,
    request: Request,
    _: None = Depends(_rate_limit_imports),
) -> Any:
    _get_authenticated_user_id(request)
    _assert_dev_token_if_needed(request, body)

    service = ImportService()
    try:
        resolved = await service.resolve_import(
            provider=body.provider,
            source_url=body.url,
            api_token=body.api_token,
        )
    except ImportError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.exception("Import resolve failed")
        raise HTTPException(status_code=500, detail="Import resolve failed") from e

    return {
        "provider": resolved.provider,
        "original_url": resolved.original_url,
        "download_url": resolved.download_url,
        "title": resolved.title,
        "filename": resolved.filename,
        "headers": resolved.headers,
    }


@router.post("/download", response_model=ImportDownloadResponse)
async def download_import(
    body: ImportDownloadRequest,
    request: Request,
    _: None = Depends(_rate_limit_imports),
) -> Any:
    _get_authenticated_user_id(request)
    _assert_dev_token_if_needed(request, body)

    service = ImportService()
    try:
        resolved = await service.resolve_import(
            provider=body.provider,
            source_url=body.url,
            api_token=body.api_token,
        )
        result = await service.download_to_upload(resolved=resolved)
        return result
    except ImportError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        logger.exception("Import download failed")
        raise HTTPException(status_code=500, detail="Import download failed") from e

