# Testing SupoClip

## Core Principles

- **Empirical Evidence**: Every major feature must have automated tests.
- **Isolation**: Unit tests should not depend on external APIs (YouTube/AssemblyAI).
- **Integration**: Route tests should use mocks for third-party services.

## Backend (pytest)

The backend uses `pytest` with `pytest-asyncio` for asynchronous testing.

### Running Tests

```bash
cd backend
uv run pytest
```

### Coverage Areas

| Suite | Description |
|-------|-------------|
| `tests/test_caption_renderer_unit.py` | Subtitle animations and MoviePy v2 compatibility. |
| `tests/test_youtube_utils_unit.py` | Proxy rotation and cookie handling logic. |
| `tests/test_user_repository_unit.py` | User settings and integration persistence. |
| `tests/test_tasks_routes_integration.py` | Video processing pipeline orchestration. |
| `tests/test_users_routes_integration.py` | Integration endpoints for cookies and user settings. |
| `tests/test_previews_routes_integration.py` | Short MP4 preview generation endpoints. |

### Markers

- `pytest -m unit`: Run only unit tests (fast, no DB).
- `pytest -m integration`: Run tests that require a database.

## Frontend (Vitest)

The frontend uses `Vitest` for component and logic testing.

```bash
cd frontend
npm run test
```

## Performance & Load Testing

To monitor video processing performance:

```bash
curl http://localhost:8000/tasks/metrics/performance
```

## Manual E2E Validation

For end-to-end testing of the YouTube bypass:
1. Go to `/settings` and add valid cookies.
2. Add a proxy to `.env` (`PROXY_SERVICE_URL`).
3. Run a task with a restricted YouTube URL.
