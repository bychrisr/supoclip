# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SupoClip is an open-source alternative to OpusClip — an AI-powered video clipping tool that transforms long-form content into viral short clips. AGPL-3.0 licensed.

## Development Commands

### Docker (recommended)

```bash
docker-compose up -d              # Start all 5 services
docker-compose up -d --build      # Rebuild after changes
docker-compose logs -f backend    # Debug backend
docker-compose logs -f worker     # Debug video processing
docker-compose down               # Stop all services
```

Services: Frontend (:3000), Backend API (:8000, docs at /docs), Worker (ARQ), PostgreSQL (:5432), Redis (:6379)

### Backend (local)

Uses `uv` (not pip/poetry). Requires Python 3.11+, ffmpeg, running PostgreSQL and Redis.

```bash
cd backend
uv venv .venv && source .venv/bin/activate
uv sync

# API server (uses refactored entry point)
uvicorn src.main_refactored:app --reload --host 0.0.0.0 --port 8000

# Worker process (required for video processing)
arq src.workers.tasks.WorkerSettings
```

### Frontend (local)

```bash
cd frontend
npm install
npm run dev          # Dev server with Turbopack
npm run build        # Prisma generate + Next.js build
npm run lint
```

### Waitlist

```bash
cd waitlist
bun install          # Uses bun, not npm
bun run dev
```

### No tests

The project currently has no test files.

## Architecture

### System Overview

```
User → Frontend (Next.js 15) → Backend API (FastAPI) → Redis Queue → ARQ Worker
                                      ↓                                  ↓
                               PostgreSQL ←───────────────────────────────┘
```

Task creation returns immediately (<100ms). Video processing happens asynchronously in the worker. Frontend connects via SSE for real-time progress updates.

### Backend: Layered Architecture

The backend was refactored from monolithic (`main.py`, legacy) to layered (`main_refactored.py`, active):

```
api/routes/          → HTTP handlers (tasks.py, media.py)
services/            → Business logic (task_service.py, video_service.py)
repositories/        → Raw SQL via asyncpg (task_repository.py, clip_repository.py, source_repository.py)
workers/             → ARQ job queue (tasks.py, job_queue.py, progress.py)
utils/               → Thread pool helpers for blocking operations (async_helpers.py)
```

**Key patterns:**
- All DB access goes through repository classes using raw SQL (`text()` queries), not SQLAlchemy ORM
- Blocking operations (video processing, downloads, transcription) wrapped in `run_in_thread()` to avoid blocking the async event loop
- Progress tracking uses Redis pub/sub → SSE to frontend
- Task status flow: `queued → processing → completed/error/cancelled`

### Video Processing Pipeline

1. **Input** → YouTube URL (yt-dlp) or uploaded file
2. **Transcription** → AssemblyAI word-level timestamps (cached as `.transcript_cache.json`)
3. **AI Analysis** → Pydantic AI selects 3-7 viral segments (10-45s each) with virality scoring
4. **Clip Generation** → MoviePy creates 9:16 clips with:
   - Face-centered cropping: MediaPipe → OpenCV DNN → Haar cascade (fallback chain)
   - Word-synced subtitles from AssemblyAI
   - Custom fonts (TTF files in `backend/fonts/`)
   - Optional transition effects (`backend/transitions/`)
   - Optional B-roll overlays (Pexels API)
   - Caption templates with animation styles
5. **Storage** → Clips to `{TEMP_DIR}/clips/`, metadata to PostgreSQL

### Frontend Architecture

- **Next.js 15** with App Router, React 19, TailwindCSS v4
- **ShadCN UI** (New York style, stone base color, Radix primitives)
- **Better Auth** with Prisma adapter for email/password auth
- **No global state library** — React hooks only (`useState`, `useEffect`, `useSession`)
- All pages use `"use client"` — SSR is minimal
- Prisma client generated to `frontend/src/generated/prisma/` (custom output path)
- Build: `prisma generate && next build` (Prisma generate runs on both build and postinstall)

**Auth flow:** Frontend calls Better Auth → session cookie → `buildBackendAuthHeaders()` (`src/lib/backend-auth.ts`) signs requests with HMAC-SHA256 → backend verifies via `src/auth_headers.py`.

- Without `BACKEND_AUTH_SECRET` (default self-hosted): frontend sends plain `x-supoclip-user-id` header
- With `BACKEND_AUTH_SECRET`: frontend sends `x-supoclip-user-id` + `x-supoclip-ts` + `x-supoclip-signature` (HMAC)

### Database

PostgreSQL 15. Schema in `init.sql`. Mixed naming conventions:
- `tasks`, `sources`, `generated_clips` → snake_case
- `session`, `account`, `verification`, `users` → camelCase (Better Auth)
- UUIDs stored as VARCHAR(36)
- Auto-update triggers on `updated_at`/`updatedAt` columns

## Key Backend Files

| File | Purpose |
|------|---------|
| `src/main_refactored.py` | Active FastAPI entry point (129 lines) |
| `src/main.py` | Legacy monolithic entry point (do not use for new work) |
| `src/api/routes/tasks.py` | Task CRUD, SSE progress, clip editing endpoints (711 lines) |
| `src/api/routes/media.py` | Fonts, transitions, uploads, templates |
| `src/services/task_service.py` | Task orchestration, clip editing logic (574 lines) |
| `src/services/video_service.py` | Video download, transcription, AI analysis, clip generation |
| `src/workers/tasks.py` | ARQ worker task definitions |
| `src/workers/job_queue.py` | Job queue management |
| `src/workers/progress.py` | Real-time progress via Redis |
| `src/ai.py` | Pydantic AI agents, system prompt, segment validation |
| `src/video_utils.py` | Video processing, cropping, subtitles (~820 lines) |
| `src/clip_editor.py` | Clip trim, split, merge, export presets |
| `src/broll.py` | Pexels API B-roll integration |
| `src/caption_templates.py` | Caption template system |
| `src/config.py` | Environment variable configuration |
| `src/observability.py` | Structured JSON logging + trace ID middleware (`LOG_LEVEL` env var, logs to `logs/`) |
| `src/models.py` | Pydantic request/response models |
| `src/auth_headers.py` | Backend-side HMAC signature verification for frontend requests |
| `src/youtube_utils.py` | YouTube URL validation and yt-dlp download helpers |
| `src/migrations/sql/` | Raw SQL migration files |

## API Endpoints (routes in `api/routes/`)

**Task lifecycle:**
- `POST /start-with-progress` — Create task, enqueue to worker (returns task_id)
- `GET /tasks/` — List user tasks
- `GET /tasks/{id}` — Get task with clips
- `GET /tasks/{id}/progress` — SSE real-time progress stream
- `POST /tasks/{id}/cancel` — Cancel processing
- `POST /tasks/{id}/resume` — Resume cancelled/errored task
- `DELETE /tasks/{id}` — Delete task

**Clip editing:**
- `PATCH /tasks/{id}/clips/{clip_id}` — Trim clip
- `POST /tasks/{id}/clips/{clip_id}/split` — Split at timestamp
- `POST /tasks/{id}/clips/merge` — Merge selected clips
- `PATCH /tasks/{id}/clips/{clip_id}/captions` — Update captions
- `GET /tasks/{id}/clips/{clip_id}/export?preset=tiktok` — Export with platform preset

**Media:**
- `GET /fonts`, `GET /transitions`, `GET /caption-templates`, `GET /broll/status`
- `POST /upload` — Upload video file
- `GET /clips/{filename}` — Serve generated clips

**Other:**
- `POST /feedback` — Submit feedback (Discord webhook via `src/api/routes/feedback.py`)
- `GET /health`, `GET /health/db`, `GET /health/redis` — Health checks

## Environment Variables

Required in `.env` (root) or `backend/.env`:

```bash
# === Required ===
ASSEMBLY_AI_API_KEY=...              # Video transcription
LLM=google-gla:gemini-3-flash-preview # Format: provider:model-name
GOOGLE_API_KEY=...                   # Or OPENAI_API_KEY / ANTHROPIC_API_KEY
DATABASE_URL=postgresql+asyncpg://...
BETTER_AUTH_SECRET=...               # Frontend auth secret (Better Auth)

# === AI Providers (at least one required) ===
OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_API_KEY=...                   # Only for Ollama Cloud

# === Optional: Features ===
PEXELS_API_KEY=...                   # B-roll stock footage
WHISPER_MODEL=base                   # tiny|base|small|medium|large (fallback transcription)
DEFAULT_PROCESSING_MODE=fast         # fast|normal — fast uses fewer clips + lighter transcript model
FAST_MODE_MAX_CLIPS=4
FAST_MODE_TRANSCRIPT_MODEL=nano

# === Optional: Limits ===
MAX_CLIPS=10
CLIP_DURATION=30                     # seconds
MAX_VIDEO_DURATION=3600              # seconds
FREE_PLAN_TASK_LIMIT=10              # 0 = unlimited
PRO_PLAN_TASK_LIMIT=0                # 0 = unlimited

# === Optional: Infrastructure ===
REDIS_HOST=localhost
REDIS_PORT=6379
QUEUED_TASK_TIMEOUT_SECONDS=180      # Fail-safe for stuck tasks
TEMP_DIR=/tmp
OUTPUT_DIR=outputs
LOG_LEVEL=INFO                       # DEBUG|INFO|WARN|ERROR — logs to backend/logs/

# === Optional: Security & Auth ===
BACKEND_AUTH_SECRET=...              # HMAC secret for frontend→backend request signing
AUTH_SIGNATURE_TTL_SECONDS=300       # Signature expiry window
CORS_ORIGINS=http://localhost:3000   # Comma-separated allowed origins

# === Optional: Hosting Mode ===
SELF_HOST=true                       # true = disables monetization features entirely

# === Optional: Integrations ===
DISCORD_FEEDBACK_WEBHOOK_URL=...
DISCORD_SALES_WEBHOOK_URL=...
```

## Common Workflows

### Adding fonts/transitions

Drop `.ttf` files into `backend/fonts/` or `.mp4` files into `backend/transitions/`. They auto-appear via their respective `GET` endpoints.

### Modifying AI clip selection

Edit `backend/src/ai.py`: `simplified_system_prompt` controls selection criteria, `TranscriptSegment` defines the output model, `get_most_relevant_parts_by_transcript()` runs analysis with validation.

### Video processing constraints

- Output: 9:16 vertical format, H.264, even pixel dimensions (`round_to_even()`)
- Subtitles positioned at 75% down the frame
- Virality scoring: `hook_score`, `engagement_score`, `value_score`, `shareability_score` (0-25 each, summed to `virality_score` 0-100)

---

## Planning & Documentation (April 2026)

### Technical Debt Assessment

Conducted brownfield discovery identifying 72 technical debts (~335.5h):

- `docs/prd/technical-debt-assessment.md` - Full assessment
- Key debts: Zero tests (40h), RLS missing, rate limiting

### Competitive Analysis

Analyzed OpusClip, Real Oficial, VidRush + alternatives:

- `docs/analysis/full-feature-audit.md` - Complete competitive audit
- Gaps: Animated captions, PT-BR, API, scheduler, workspaces

### Features Roadmap

41 feature stories across 4 phases (~908h total):

| Phase | Focus | Stories | Hours |
|-------|-------|--------|-------|
| FASE 1 | Essentials | 5 | 38h |
| FASE 2 | Differentiation | 8 | 208h |
| FASE 3 | Team/Agency | 9 | 208h |
| FASE 4 | Premium | 19 | 454h |

- `docs/roadmap/features-roadmap.md`

### Sprint Planning

15 sprints (~6 months, ~1,215h total):

```
Sprint 1-2:  Foundation + Security
Sprint 3-6:  Differentiation BR
Sprint 7-10: Team/Agency
Sprint 11-15: Premium
```

- `docs/planning/sprint-planning.md`

---

## Documentation References

| Path | Description |
|------|------------|
| `docs/stories/epic-features.md` | Main features epic |
| `docs/stories/epic-technical-debt.md` | TD epic |
| `docs/roadmap/features-roadmap.md` | Full roadmap |
| `docs/planning/sprint-planning.md` | Sprint plan |
| `docs/analysis/full-feature-audit.md` | Competitive audit |
| `docs/prd/technical-debt-assessment.md` | TD assessment |

```bash
# View planning
cat docs/planning/sprint-planning.md
ls docs/stories/story-*.md | wc -l  # 50 stories
