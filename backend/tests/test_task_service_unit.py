from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.services.task_service import TaskService


@pytest.mark.unit
def test_build_cache_key_is_stable_and_sensitive_to_inputs() -> None:
    k1 = TaskService._build_cache_key(" https://x.y/z ", "youtube", "fast")
    k2 = TaskService._build_cache_key("https://x.y/z", "youtube", "fast")
    assert k1 == k2

    k3 = TaskService._build_cache_key("https://x.y/z", "youtube", "quality")
    assert k3 != k1


@pytest.mark.unit
def test_is_stale_queued_task_false_when_not_queued() -> None:
    svc = TaskService(db=None)  # type: ignore[arg-type]
    assert svc._is_stale_queued_task({"status": "processing"}) is False


@pytest.mark.unit
def test_is_stale_queued_task_true_when_older_than_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    svc = TaskService(db=None)  # type: ignore[arg-type]
    svc.config.queued_task_timeout_seconds = 100

    updated_at = datetime.now(timezone.utc) - timedelta(seconds=101)
    created_at = updated_at
    assert (
        svc._is_stale_queued_task(
            {"status": "queued", "created_at": created_at, "updated_at": updated_at}
        )
        is True
    )


@pytest.mark.unit
def test_seconds_to_mmss_rounding() -> None:
    assert TaskService._seconds_to_mmss(0) == "00:00"
    assert TaskService._seconds_to_mmss(1.4) == "00:01"
    assert TaskService._seconds_to_mmss(61.2) == "01:01"

