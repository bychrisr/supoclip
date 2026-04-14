from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import pytest


class _FakeBillingService:
    def __init__(self, db: Any):  # noqa: ANN401, ARG002
        pass

    async def assert_can_create_task(self, user_id: str) -> None:  # noqa: ARG002
        return None


class _FakeJobQueue:
    @staticmethod
    async def enqueue_processing_job(*_args: Any, **_kwargs: Any) -> str:  # noqa: ANN401
        return "job_test_1"


class _FakeTaskRepo:
    def __init__(self) -> None:
        self._tasks: Dict[str, Dict[str, Any]] = {}

    async def get_task_by_id(self, _db: Any, task_id: str) -> Optional[Dict[str, Any]]:  # noqa: ANN401
        return self._tasks.get(task_id)


class _FakeTaskService:
    def __init__(self, db: Any):  # noqa: ANN401, ARG002
        self.task_repo = _FakeTaskRepo()
        self._user_tasks: Dict[str, List[Dict[str, Any]]] = {}

        class _VS:
            @staticmethod
            def determine_source_type(_url: str) -> str:
                return "youtube"

        self.video_service = _VS()

    async def create_task_with_source(self, user_id: str, url: str, **_kwargs: Any) -> str:  # noqa: ANN401
        task_id = "task_test_1"
        # mirror minimal shape used by owner checks / downstream reads
        self.task_repo._tasks[task_id] = {"id": task_id, "user_id": user_id, "status": "queued", "source_url": url, "source_type": "youtube"}  # type: ignore[attr-defined]
        self._user_tasks.setdefault(user_id, []).append(self.task_repo._tasks[task_id])  # type: ignore[attr-defined]
        return task_id

    async def get_user_tasks(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:  # noqa: ARG002
        return list(self._user_tasks.get(user_id, []))

    async def get_task_with_clips(self, task_id: str) -> Optional[Dict[str, Any]]:
        task = await self.task_repo.get_task_by_id(None, task_id)
        if not task:
            return None
        task = dict(task)
        task["clips"] = []
        task["clips_count"] = 0
        return task


@pytest.fixture()
def _patched_tasks_module(monkeypatch: pytest.MonkeyPatch) -> Dict[str, Any]:
    """
    Patch external integrations inside `src.api.routes.tasks` so we can exercise routes
    without DB/Redis/worker.
    """
    from src.api.routes import tasks as tasks_routes

    # Ensure self-host mode for these tests: plain header auth
    tasks_routes.config.monetization_enabled = False

    # Patch integrations
    monkeypatch.setattr(tasks_routes, "BillingService", _FakeBillingService)
    monkeypatch.setattr(tasks_routes, "JobQueue", _FakeJobQueue)
    singleton_task_service = _FakeTaskService(db=None)
    monkeypatch.setattr(tasks_routes, "TaskService", lambda _db: singleton_task_service)
    # Rate limiting is covered separately; disable for these mocked route tests.
    async def _noop_enforce_rate_limit(*_args: Any, **_kwargs: Any) -> None:  # noqa: ANN401
        return None

    class _DummyRedis:
        async def aclose(self) -> None:
            return None

    async def _dummy_get_redis_client() -> Any:  # noqa: ANN401
        return _DummyRedis()

    monkeypatch.setattr(tasks_routes, "enforce_rate_limit", _noop_enforce_rate_limit)
    monkeypatch.setattr(tasks_routes, "_get_redis_client", _dummy_get_redis_client)

    fake_redis_store: Dict[str, str] = {}

    class _RedisFactory:
        def __init__(self, *args: Any, **kwargs: Any):  # noqa: ANN401, ARG002
            pass

        async def set(self, key: str, value: str, ex: Optional[int] = None) -> None:  # noqa: ARG002
            fake_redis_store[key] = value

        async def close(self) -> None:
            return None

    monkeypatch.setattr(tasks_routes.redis, "Redis", _RedisFactory)

    return {"tasks_routes": tasks_routes, "redis_store": fake_redis_store}


@pytest.mark.integration
async def test_list_tasks_requires_user_header(async_client, _patched_tasks_module) -> None:
    resp = await async_client.get("/tasks/")
    assert resp.status_code == 401


@pytest.mark.integration
async def test_create_task_and_list_tasks_happy_path(async_client, auth_headers, _patched_tasks_module) -> None:
    # Create
    payload = {"source": {"url": "https://youtube.com/watch?v=abc"}}
    resp = await async_client.post("/tasks/", json=payload, headers=auth_headers)
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["task_id"] == "task_test_1"
    assert data["job_id"] == "job_test_1"

    # List should include created task
    resp2 = await async_client.get("/tasks/", headers=auth_headers)
    assert resp2.status_code == 200, resp2.text
    items = resp2.json()
    assert items["total"] == 1
    assert items["tasks"][0]["id"] == "task_test_1"


@pytest.mark.integration
async def test_get_task_enforces_ownership(async_client, _patched_tasks_module) -> None:
    # Create under user_a
    payload = {"source": {"url": "https://youtube.com/watch?v=abc"}}
    resp = await async_client.post("/tasks/", json=payload, headers={"user_id": "user_a"})
    assert resp.status_code == 200

    # Fetch as user_b should 403
    resp2 = await async_client.get("/tasks/task_test_1", headers={"user_id": "user_b"})
    assert resp2.status_code == 403

