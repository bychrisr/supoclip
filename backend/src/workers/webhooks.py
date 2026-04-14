from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories.webhook_delivery_repository import WebhookDeliveryRepository
from ..repositories.webhook_repository import WebhookRepository


def _sign(secret: str, timestamp: str, body: bytes) -> str:
    msg = timestamp.encode("utf-8") + b"." + body
    return hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()


async def deliver_webhook_event(
    *,
    db: AsyncSession,
    webhook_id: str,
    user_id: str,
    delivery_id: str,
    event: str,
    payload: dict[str, Any],
    attempt: int,
) -> None:
    # Load webhook in owner context (db already has RLS context set for user_id by caller).
    hooks = await WebhookRepository.list_webhooks(db, user_id=user_id)
    hook = next((h for h in hooks if h.id == webhook_id), None)
    if not hook or not hook.enabled:
        await WebhookDeliveryRepository.mark_attempt(
            db,
            delivery_id=delivery_id,
            attempt=attempt,
            status="failed",
            last_error="Webhook disabled or not found",
        )
        return

    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ts = str(int(time.time()))
    signature = _sign(hook.secret, ts, body)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "supoclip-webhooks/1.0",
        "X-SupoClip-Event": event,
        "X-SupoClip-Timestamp": ts,
        "X-SupoClip-Signature": signature,
    }

    async with httpx.AsyncClient(follow_redirects=False, timeout=10.0) as client:
        try:
            resp = await client.post(hook.url, content=body, headers=headers)
            status = "success" if 200 <= resp.status_code < 300 else "failed"
            await WebhookDeliveryRepository.mark_attempt(
                db,
                delivery_id=delivery_id,
                attempt=attempt,
                response_status=resp.status_code,
                response_body=(resp.text[:4000] if resp.text else None),
                status=status,
                last_error=None if status == "success" else f"Non-2xx status: {resp.status_code}",
            )
            if status != "success":
                raise RuntimeError(f"Webhook non-2xx status: {resp.status_code}")
        except Exception as e:
            await WebhookDeliveryRepository.mark_attempt(
                db,
                delivery_id=delivery_id,
                attempt=attempt,
                status="failed",
                last_error=str(e)[:4000],
            )
            raise

