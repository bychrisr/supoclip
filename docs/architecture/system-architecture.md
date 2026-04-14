# SupoClip - System Architecture

> **Documento gerado em:** 2026-04-14  
> **Versão:** 0.2.1  
> **Autor:** @architect (Aria) - FASE 1 Brownfield Discovery

---

## Executive Summary

O **SupoClip** é uma plataforma open-source (licença AGPL-3.0) de clipping de vídeos utilizando IA, projetada para transformar conteúdo de formato longo em clips virais otimizados para plataformas como TikTok, Reels e YouTube Shorts. O sistema oferece processamento assíncrono de vídeos com pipeline completo que inclui download, transcrição, análise de IA com pontuação de viralidade, e geração de clips com legendas e transições.

A arquitetura atual apresenta uma divisão clara entre frontend Next.js e backend FastAPI, com processamento background distribuído via ARQ Workers e Redis como message queue. O projeto encontra-se em fase de refatoração, mantendo coexistência entre o código legado (main.py) e a versão refatorada (main_refactored.py), o que representa um débito técnico significativo que requer atenção nas próximas iterações.

O sistema foi recentemente refatorado (v0.2.0) para incluir job queue com ARQ, health checks robustos, observabilidade com tracing distribuído, e sistema de autenticação dual (self-hosted vs hosted monetization). A base de código demonstra uma arquitetura bem estruturada com separação clara de responsabilidades, mas apresenta gaps críticos em testes automatizados e validação de inputs.

---

## Stack Tecnológico

### Backend

| Componente | Versão | Propósito |
|------------|--------|-----------|
| **Python** | 3.11+ | Runtime principal |
| **FastAPI** | 0.110.0+ | Framework web assíncrono |
| **Uvicorn** | 0.27.0+ | ASGI server |
| **asyncpg** | 0.29.0+ | Driver PostgreSQL assíncrono |
| **SQLAlchemy** | 2.0.25+ | ORM (leve, para models) |
| **ARQ** | 0.26.0+ | Job queue assíncrono (Redis-backed) |
| **Redis** | 5.0.0+ | Cache, job queue, pub/sub |
| **Pydantic AI** | 0.4.9+ | Framework para LLM agents |
| **AssemblyAI** | 0.35.0+ | Transcrição de áudio (fallback) |
| **MoviePy** | 2.2.1+ | Processamento de vídeo |
| **OpenCV** | 4.8.0+ | Manipulação de vídeo frame-level |
| **MediaPipe** | 0.10.0+ | Detecção de face/crop inteligente |
| **yt-dlp** | 2025.7.21+ | Download de vídeos do YouTube |
| **sse-starlette** | 1.6.5+ | Server-Sent Events |

### Frontend

| Componente | Versão | Propósito |
|------------|--------|-----------|
| **Next.js** | 15.4.8 | Framework React (App Router) |
| **React** | 19.1.0 | UI library |
| **TailwindCSS** | 4.2.1 | Styling |
| **ShadCN UI** | Radix-based | Component library |
| **Better Auth** | 1.5.0 | Autenticação |
| **Prisma** | 6.19.2 | ORM client |
| **Stripe** | 20.4.0 | Pagamentos (monetization) |
| **Resend** | 6.9.3 | Email service |
| **Sonner** | 2.0.7 | Toast notifications |

### Infrastructure

| Componente | Versão | Propósito |
|------------|--------|-----------|
| **PostgreSQL** | 15-alpine | Banco de dados relacional |
| **Redis** | 7-alpine | Cache, job queue, pub/sub |
| **Docker** | docker-compose | Container orchestration |

---

## Estrutura de Diretórios

```
supoclip/
├── backend/                      # Backend Python
│   ├── src/
│   │   ├── api/
│   │   │   └── routes/          # HTTP handlers (FastAPI routers)
│   │   │       ├── tasks.py     # Task CRUD, clip operations (838 linhas)
│   │   │       ├── media.py     # Font listing, video upload
│   │   │       └── feedback.py  # Discord webhook integration
│   │   ├── services/            # Business logic layer
│   │   │   ├── task_service.py  # Task orchestration (712 linhas)
│   │   │   ├── video_service.py # Video processing logic (322 linhas)
│   │   │   ├── billing_service.py # Subscription management
│   │   │   └── transcription_service.py # Gemini/AssemblyAI fallback
│   │   ├── repositories/        # Data access layer (raw SQL)
│   │   │   ├── task_repository.py
│   │   │   ├── clip_repository.py
│   │   │   ├── source_repository.py
│   │   │   └── cache_repository.py
│   │   ├── workers/             # ARQ background workers
│   │   │   ├── tasks.py         # process_video_task job
│   │   │   ├── job_queue.py     # ARQ pool wrapper
│   │   │   └── progress.py      # SSE progress tracker
│   │   ├── migrations/          # SQL migrations
│   │   ├── utils/               # Utility functions
│   │   │   └── async_helpers.py # Thread pool wrappers
│   │   ├── ai.py                # Pydantic AI agent (transcript analysis)
│   │   ├── video_utils.py       # Video processing utilities (1700+ linhas)
│   │   ├── clip_editor.py       # Clip manipulation (trim, split, merge)
│   │   ├── youtube_utils.py     # yt-dlp download wrapper
│   │   ├── broll.py             # Pexels B-roll integration
│   │   ├── font_registry.py     # Font management
│   │   ├── caption_templates.py # Caption styling presets
│   │   ├── models.py            # SQLAlchemy models (251 linhas)
│   │   ├── database.py          # Async engine, session factory
│   │   ├── config.py            # Environment config
│   │   ├── observability.py     # Logging, tracing
│   │   ├── auth_headers.py      # HMAC signature validation
│   │   ├── main_refactored.py   # FastAPI app (v0.2.0) - ATIVO
│   │   ├── main.py              # Legacy entry (920 linhas) - LEGADO
│   │   └── worker_main.py       # Worker entry point
│   ├── fonts/                   # TTF font files (13 arquivos)
│   ├── transitions/             # .mp4 transition overlays
│   └── pyproject.toml           # Python dependencies (uv)
│
├── frontend/                    # Frontend Next.js
│   ├── src/
│   │   ├── app/                 # App Router pages
│   │   │   ├── page.tsx         # Landing page
│   │   │   ├── tasks/[id]/      # Task detail page
│   │   │   ├── sign-in/         # Auth pages
│   │   │   ├── settings/        # User settings
│   │   │   └── api/             # API routes (BFF pattern)
│   │   │       ├── auth/[...all]/  # Better Auth handler
│   │   │       ├── feedback/    # Feedback submission
│   │   │       ├── fonts/       # Font listing
│   │   │       └── billing/     # Stripe webhooks
│   │   ├── components/          # React components
│   │   │   ├── ui/              # ShadCN components (16 componentes)
│   │   │   ├── auth/            # Auth forms
│   │   │   └── admin/           # Admin components
│   │   └── lib/                 # Utilities
│   │       ├── auth.ts          # Better Auth config
│   │       ├── backend-auth.ts  # HMAC signature generator
│   │       ├── prisma.ts        # Prisma client
│   │       └── stripe.ts        # Stripe client
│   └── prisma/
│       └── schema.prisma        # Database schema
│
├── docker-compose.yml           # 5 services: frontend, backend, worker, redis, postgres
├── init.sql                     # Database initialization
├── start.sh                     # Quick start script
└── .env.example                 # Environment template
```

### Convenções de Nomenclatura

- **Python**: `snake_case` para arquivos, funções e variáveis, 4 espaços de indentação
- **TypeScript**: `PascalCase` para componentes, `camelCase` para variáveis, 2 espaços de indentação
- **Routes**: Kebab-case para URLs (`/tasks/{id}/clips`)
- **Imports**: Alias `@/*` no Next.js para imports absolutos

---

## Padrões de Código

### Backend: Layered Architecture

```
┌─────────────────────────────────────────┐
│            API Routes (tasks.py)         │  ← HTTP handlers, validation, auth
├─────────────────────────────────────────┤
│           Services (task_service.py)     │  ← Business logic, orchestration
├─────────────────────────────────────────┤
│        Repositories (task_repository.py) │  ← Data access, raw SQL
└─────────────────────────────────────────┘
```

**Características:**
- **Routes**: Handlers HTTP com validação Pydantic, autenticação, error handling
- **Services**: Lógica de negócio pura, orquestração de workflows, sem dependência HTTP
- **Repositories**: Acesso a dados via SQL raw com asyncpg, queries tipadas

### Frontend: App Router + Server Components

- **Server Components**: Default para pages, sem interatividade
- **Client Components**: Apenas quando necessário (`'use client'`)
- **API Routes**: BFF pattern para ações sensíveis (auth, feedback)

### Autenticação

**Dual Mode:**
1. **Self-hosted (`SELF_HOST=true`)**: Header `x-supoclip-user-id` simples
2. **Hosted monetization (`SELF_HOST=false`)**: HMAC signature com timestamp

```typescript
// Frontend (backend-auth.ts)
const signature = crypto.createHmac("sha256", secret)
  .update(`${userId}:${timestamp}`)
  .digest("hex");
```

```python
# Backend (auth_headers.py)
def get_signed_user_id(request: Request, config: Config) -> str:
    # Validate HMAC signature and timestamp TTL
    expected = hmac.new(secret.encode(), payload.encode(), sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(401, "Invalid auth signature")
```

### Tratamento de Erros

- **Global Exception Handlers** em `main_refactored.py`
- **Trace IDs** propagados em todas as responses (`x-trace-id` header)
- **Error Codes** estruturados no banco (`error_code` field)
- **Dead Letter Queue** no Redis para jobs que falharam após retries

---

## Integrações

### Diagrama de Arquitetura

```
┌──────────────┐      HTTP/SSE      ┌──────────────┐
│   Frontend   │ ◄─────────────────► │   Backend    │
│  (Next.js)   │                     │  (FastAPI)   │
└──────────────┘                     └──────┬───────┘
                                            │
                    ┌───────────────────────┼───────────────────────┐
                    │                       │                       │
                    ▼                       ▼                       ▼
            ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
            │  PostgreSQL   │       │    Redis      │       │    Worker    │
            │    (Data)     │       │(Queue/Cache)  │       │    (ARQ)     │
            └──────────────┘       └──────────────┘       └──────┬───────┘
                                                                │
                                            ┌───────────────────┼───────────────────┐
                                            │                   │                   │
                                            ▼                   ▼                   ▼
                                  ┌──────────────────┐ ┌──────────────┐  ┌────────────────┐
                                  │ AssemblyAI/Gemini│ │   OpenAI/     │  │  MoviePy       │
                                  │  (Transcription) │ │ Anthropic/    │  │  OpenCV        │
                                  └──────────────────┘ │    Google     │  │ (Video Edit)   │
                                                        └──────────────┘  └────────────────┘
```

### Backend ↔ Frontend

- **Protocolo**: HTTP REST + SSE
- **Endpoints Principais**:
  - `POST /tasks` → Cria task e enfileira job
  - `GET /tasks/{id}/progress` → SSE stream de progresso
  - `GET /tasks/{id}` → Detalhes da task com clips
  - `PATCH /tasks/{id}/clips/{clipId}` → Trim/edit operations

### Backend ↔ Database

- **Driver**: asyncpg (async, raw SQL)
- **Pool**: 10 conexões, max_overflow=20
- **Pattern**: Repository com queries SQL tipadas

### Backend ↔ Redis

- **Job Queue**: ARQ para processamento assíncrono
- **Pub/Sub**: Progress updates em tempo real
- **Cache**: Metadados de task (`task_source:{id}`)
- **Dead Letter**: Tasks que falharam (`tasks:dead_letter`)

### Backend ↔ External APIs

| Serviço | Uso | Fallback |
|---------|-----|----------|
| **Gemini API** | Transcrição primária | AssemblyAI |
| **AssemblyAI** | Transcrição (fallback) | - |
| **OpenAI/Anthropic/Google** | Análise de transcript | Ollama (local) |
| **Pexels** | B-roll footage | - |

---

## Configurações

### Variáveis de Ambiente Críticas

| Variável | Propósito | Default |
|----------|-----------|---------|
| `ASSEMBLY_AI_API_KEY` | Transcrição (fallback) | Required |
| `GOOGLE_API_KEY` | LLM + Gemini transcription | Optional |
| `OPENAI_API_KEY` | LLM provider | Optional |
| `ANTHROPIC_API_KEY` | LLM provider | Optional |
| `LLM` | Modelo LLM principal | `google-gla:gemini-3-flash-preview` |
| `DATABASE_URL` | PostgreSQL connection | `postgresql+asyncpg://...` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `SELF_HOST` | Modo self-hosted vs monetization | `true` |
| `BACKEND_AUTH_SECRET` | HMAC secret (hosted mode) | - |
| `BETTER_AUTH_SECRET` | Session encryption | - |
| `WHISPER_MODEL_SIZE` | Whisper model (legacy) | `medium` |
| `QUEUED_TASK_TIMEOUT_SECONDS` | Timeout para tasks stuck | `180` |
| `DEFAULT_PROCESSING_MODE` | fast/balanced/quality | `fast` |
| `CORS_ORIGINS` | Allowed origins | `http://localhost:3000` |

### Docker Compose Services

```yaml
services:
  frontend:   # Next.js on port 3001
  backend:    # FastAPI on port 8000
  worker:     # ARQ worker (same image as backend)
  postgres:   # PostgreSQL 15-alpine
  redis:      # Redis 7-alpine
```

### Health Checks

- **Backend**: `GET /health`, `GET /health/db`, `GET /health/redis`
- **Worker**: `run_startup_sweep` on startup (stale tasks cleanup)
- **Frontend**: `curl -f http://localhost:3000/`

---

## Débitos Técnicos Identificados (Sistema)

| ID | Débito | Área | Impacto | Esforço | Prioridade |
|----|--------|------|---------|---------|------------|
| SYS-001 | **Ausência total de testes automatizados** | Quality | Crítico | 40h | P0 |
| SYS-002 | **Dupla fonte de schema** (Prisma + init.sql + SQLAlchemy models) | Database | Alto | 16h | P1 |
| SYS-003 | **Arquivos legados não removidos** (`main.py`, código comentado) | Maintainability | Médio | 4h | P2 |
| SYS-004 | **Hardcoded defaults em múltiplos locais** (font_family, font_size) | Config | Médio | 8h | P2 |
| SYS-005 | **Pool de Redis não configurado** (sem max_connections) | Performance | Médio | 4h | P2 |
| SYS-006 | **Error handling inconsistente** (exceptions genéricas em services) | Quality | Alto | 12h | P1 |
| SYS-007 | **Falta de rate limiting** na API pública | Security | Alto | 8h | P1 |
| SYS-008 | **Credenciais hardcoded** no init.sql (postgres password) | Security | Alto | 2h | P1 |
| SYS-009 | **Logging sem campos estruturados** (apenas mensagem) | Observability | Baixo | 8h | P2 |
| SYS-010 | **Ausência de graceful shutdown** no worker | Reliability | Médio | 4h | P2 |
| SYS-011 | **132+ cláusulas except sem logging adequado** | Quality/Security | Alto | 16h | P1 |
| SYS-012 | **Variáveis de ambiente não validadas** no startup | Config | Alto | 6h | P1 |
| SYS-013 | **Dead code em video_utils.py** (código comentado AssemblyAI) | Maintainability | Baixo | 2h | P2 |
| SYS-014 | **Queries SQL não parametrizadas** (concatenação em alguns casos) | Security | Alto | 8h | P1 |
| SYS-015 | **Falta de índice em generated_clips.virality_score** | Performance | Baixo | 1h | P2 |
| SYS-016 | **Dockerfile sem multi-stage build** (imagem grande) | DevOps | Médio | 4h | P2 |
| SYS-017 | **Código duplicado em main.py e main_refactored.py** | Maintainability | Alto | 8h | P1 |
| SYS-018 | **Processamento síncrono em asyncio.create_task** (sem await) | Reliability | Alto | 4h | P1 |

### Análise Detalhada dos Débitos

#### SYS-001: Ausência total de testes automatizados
- **Problema**: Nenhum arquivo de teste encontrado (`tests/` vazio, `*.test.ts` inexistente)
- **Impacto**: Regressões frequentes, refactoring arriscado, deploy sem garantias
- **Recomendação**: Implementar pytest + pytest-asyncio no backend, Jest/Vitest no frontend
- **Estimativa**: 40h para cobertura mínima (40% core paths)

#### SYS-002: Dupla fonte de schema
- **Problema**: Schema definido em 3 lugares: `init.sql`, `prisma/schema.prisma`, `models.py`
- **Impacto**: Inconsistências, migrations manuais propensas a erro
- **Recomendação**: Usar Prisma como fonte única, gerar init.sql via `prisma migrate`
- **Estimativa**: 16h para unificar e criar pipeline de migrations

#### SYS-003: Arquivos legados não removidos
- **Problema**: `main.py` ainda presente (legacy, 920 linhas), código comentado em `video_utils.py`
- **Impacto**: Confusão sobre entrypoint correto, manutenção de código morto
- **Recomendação**: Remover `main.py`, eliminar código comentado
- **Estimativa**: 4h para cleanup e validação

#### SYS-004: Hardcoded defaults em múltiplos locais
- **Problema**: Defaults como `TikTokSans-Regular`, `24`, `#FFFFFF` repetidos em services, routes, models
- **Impacto**: Mudanças exigem edição em múltiplos arquivos
- **Recomendação**: Centralizar em `config.py` ou `constants.py`
- **Estimativa**: 8h para refatoração

#### SYS-005: Pool de Redis não configurado
- **Problema**: `redis.asyncio.Redis()` criado sem `max_connections`, possível connection leak
- **Impacto**: Sobrecarga de conexões sob carga alta
- **Recomendação**: Usar `ConnectionPool` com limites
- **Estimativa**: 4h para implementar pool gerenciado

#### SYS-006: Error handling inconsistente
- **Problema**: Services lançam `ValueError` genérico, errors não estruturados
- **Impacto**: Debugging difícil, mensagens de erro pouco úteis
- **Recomendação**: Criar hierarchy de exceptions customizadas
- **Estimativa**: 12h para implementar error handling consistente

#### SYS-007: Falta de rate limiting
- **Problema**: API pública sem rate limiting, vulnerável a abuso
- **Impacto**: DoS, uso indevido de recursos pagos
- **Recomendação**: Implementar `slowapi` ou middleware customizado
- **Estimativa**: 8h para implementar com Redis backend

#### SYS-008: Credenciais hardcoded no init.sql
- **Problema**: Senha do Postgres hardcoded em `init.sql` (`supoclip_password`)
- **Impacto**: Security risk em produção
- **Recomendação**: Mover para secrets/environment
- **Estimativa**: 2h para refatoração

#### SYS-011: Excessivas cláusulas except sem logging
- **Problema**: 132+ cláusulas `except` encontradas, muitas sem logging adequado
- **Impacto**: Exceções silenciadas, impossível diagnosticar falhas
- **Recomendação**: Audit em todas as cláusulas, adicionar logger.exception()
- **Estimativa**: 16h para audit e correção

#### SYS-014: Queries SQL não parametrizadas
- **Problema**: Algumas queries usam f-strings ou concatenação
- **Impacto**: SQL injection risk potencial
- **Recomendação**: Auditar todas as queries, usar parametrização
- **Estimativa**: 8h para audit e fix

#### SYS-017: Código duplicado main.py e main_refactored.py
- **Problema**: Ambos os arquivos implementam endpoints similares, duplicação de lógica
- **Impacto**: Manutenção duplicada, confusão sobre qual usar em produção
- **Recomendação**: Consolidar em main_refactored.py, remover main.py
- **Estimativa**: 8h para merge e validação

#### SYS-018: asyncio.create_task sem await adequado
- **Problema**: `asyncio.create_task()` usado em `main.py` para background processing sem manejo adequado de erros
- **Impacto**: Tasks podem falhar silenciosamente, sem tracking de erro
- **Recomendação**: Migrar para ARQ job queue (já implementado em refactored)
- **Estimativa**: 4h para migração completa

---

## Próximos Passos

### Curto Prazo (P0 - Esta Sprint)

1. **Implementar suite de testes** - Começar com testes unitários em repositories e services
2. **Validar variáveis de ambiente no startup** - Fail fast com mensagens claras
3. **Adicionar rate limiting** - Proteger endpoints públicos

### Médio Prazo (P1 - Próximas 2 Sprints)

4. **Unificar fonte de schema** - Migrar para Prisma migrations
5. **Implementar error handling consistente** - Custom exceptions, error codes
6. **Auditar queries SQL** - Eliminar concatenação insegura
7. **Remover código legado** - Eliminar main.py, consolidar em main_refactored.py

### Longo Prazo (P2 - Backlog)

8. **Implementar structured logging** - Campos estruturados para observabilidade
9. **Graceful shutdown no worker** - Signal handlers
10. **Multi-stage Docker builds** - Reduzir tamanho da imagem

---

## Métricas de Saúde do Sistema

| Métrica | Valor Atual | Meta |
|---------|-------------|------|
| Test Coverage | 0% | 60% |
| Lines of Code (Backend) | ~15k | - |
| Files (Backend) | 35 Python files | - |
| Files (Frontend) | ~30 TSX files | - |
| Docker Services | 5 | - |
| External Dependencies | 15+ APIs | Minimize |
| TODOs/FIXMEs no código | 0 found | Maintain 0 |
| Except clauses sem logging | 132+ | 0 |

---

## Conclusão

O SupoClip apresenta uma arquitetura moderna e bem estruturada para um sistema de processamento de vídeo com IA. A refatoração para v0.2.0 introduziu melhorias significativas (job queue, observabilidade, health checks), mas ainda existem gaps importantes em **testes automatizados**, **consistência de schema**, e **segurança** que devem ser endereçados prioritariamente.

A separação clara entre API síncrona e workers assíncronos é um ponto forte, permitindo escalabilidade horizontal do processamento de vídeo. A arquitetura de autenticação dual (self-hosted vs hosted) demonstra flexibilidade para diferentes modelos de deployment. O código refatorado em `main_refactored.py` representa a direção correta, mas a coexistência com o legado em `main.py` cria confusão e manutenção duplicada.

**Recomendação:** Focar P0s antes de adicionar novas features. A falta de testes é o maior risco técnico atual, seguida de perto pela necessidade de remover o código legado duplicado.

---

*Documento gerado por @architect (Aria) - FASE 1 Brownfield Discovery*  
*Próxima fase: FASE 2 - Análise de Impacto para mudanças planejadas*
