from __future__ import annotations

import secrets
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from ...config import Config
from ...database import get_db
from ...auth_headers import get_signed_user_id, USER_ID_HEADER
from ...repositories.webhook_repository import WebhookRepository
from ...repositories.webhook_delivery_repository import WebhookDeliveryRepository


config = Config()
router = APIRouter(prefix="/webhooks", tags=["webhooks"])


def _get_user_id(request: Request) -> str:
    if config.monetization_enabled:
        return get_signed_user_id(request, config)
    user_id = request.headers.get("user_id") or request.headers.get(USER_ID_HEADER)
    if not user_id:
        raise HTTPException(status_code=401, detail="User authentication required")
    return user_id


@router.get("/")
async def list_webhooks(request: Request, db: AsyncSession = Depends(get_db)):
    user_id = _get_user_id(request)
    hooks = await WebhookRepository.list_webhooks(db, user_id=user_id)
    return {
        "webhooks": [
            {
                "id": h.id,
                "url": h.url,
                "events": h.events,
                "enabled": h.enabled,
                # secret intentionally omitted
                "created_at": h.created_at,
            }
            for h in hooks
        ]
    }


@router.post("/")
async def create_webhook(
    request: Request, db: AsyncSession = Depends(get_db)
) -> dict[str, Any]:
    user_id = _get_user_id(request)
    body = await request.json()
    url = (body.get("url") or "").strip()
    events = body.get("events") or []
    enabled = bool(body.get("enabled", True))
    if not url:
        raise HTTPException(status_code=400, detail="url is required")
    if not isinstance(events, list) or not all(isinstance(e, str) and e.strip() for e in events):
        raise HTTPException(status_code=400, detail="events must be a list of strings")

    secret = secrets.token_urlsafe(32)
    row = await WebhookRepository.create_webhook(
        db,
        user_id=user_id,
        url=url,
        events=[e.strip() for e in events],
        enabled=enabled,
        secret=secret,
    )
    return {
        "id": row.id,
        "url": row.url,
        "events": row.events,
        "enabled": row.enabled,
        "secret": secret,  # shown only on creation
        "created_at": row.created_at,
    }


@router.patch("/{webhook_id}")
async def update_webhook(webhook_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    user_id = _get_user_id(request)
    body = await request.json()
    url = body.get("url")
    events = body.get("events")
    enabled = body.get("enabled")

    if url is not None:
        url = str(url).strip()
        if not url:
            raise HTTPException(status_code=400, detail="url cannot be empty")
    if events is not None:
        if not isinstance(events, list) or not all(isinstance(e, str) and e.strip() for e in events):
            raise HTTPException(status_code=400, detail="events must be a list of strings")
        events = [e.strip() for e in events]
    if enabled is not None:
        enabled = bool(enabled)

    row = await WebhookRepository.update_webhook(
        db,
        user_id=user_id,
        webhook_id=webhook_id,
        url=url,
        events=events,
        enabled=enabled,
    )
    if not row:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return {
        "id": row.id,
        "url": row.url,
        "events": row.events,
        "enabled": row.enabled,
        "created_at": row.created_at,
    }


@router.delete("/{webhook_id}")
async def delete_webhook(webhook_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    user_id = _get_user_id(request)
    ok = await WebhookRepository.delete_webhook(db, user_id=user_id, webhook_id=webhook_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return {"deleted": True}


@router.get("/{webhook_id}/deliveries")
async def list_webhook_deliveries(
    webhook_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    limit: int = 100,
    offset: int = 0,
):
    user_id = _get_user_id(request)
    limit = max(1, min(int(limit), 500))
    offset = max(0, int(offset))
    deliveries = await WebhookDeliveryRepository.list_deliveries_for_webhook(
        db, user_id=user_id, webhook_id=webhook_id, limit=limit, offset=offset
    )
    return {"deliveries": deliveries, "limit": limit, "offset": offset}

