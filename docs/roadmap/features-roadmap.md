# Features Roadmap - SupoClip

## Visão 2026

### Meta
Ser a melhor ferramenta open-source de AI video clipping, com foco no mercado brasileiro e oportunidades de diferenciação contra OpusClip, Real Oficial e VidRush.

### Diferenciais Estratégicos
- Open Source com licença AGPL-3.0
- 100% local-first (self-hosted)
- PT-BR nativo
- API pay-per-use transparente
- Foco em agências (workspace multi-client)

---

## PARTE 1: O que já temos (DONE)

Baseado na análise completa em `docs/analysis/full-feature-audit.md`.

| Feature | Status | Notas |
|---------|--------|-------|
| YouTube import | ✅ DONE | yt-dlp |
| File upload (MP4) | ✅ DONE | Upload endpoint |
| AI clip selection | ✅ DONE | Pydantic AI (3-7 clips) |
| Virality scoring | ✅ DONE | hook/engagement/value/shareability |
| Face detection/cropping | ✅ DONE | MediaPipe + OpenCV |
| Word-synced subtitles | ✅ DONE | AssemblyAI timestamps |
| Transcript | ✅ DONE | AssemblyAI |
| B-roll overlays | ✅ DONE | Pexels API |
| Caption templates | ✅ DONE | Múltiplos estilos |
| Custom fonts | ✅ DONE | TTF em backend/fonts/ |
| Transition effects | ✅ DONE | MP4 em backend/transitions/ |
| Clip trimming | ✅ DONE | PATCH endpoint |
| Clip splitting | ✅ DONE | POST split |
| Clip merging | ✅ DONE | POST merge |
| Export presets | ✅ DONE | tiktok, instagram, youtube |
| SSE progress | ✅ DONE | Real-time updates |
| Task lifecycle | ✅ DONE | queued→processing→completed |
| Multi-provider LLM | ✅ DONE | Google/OpenAI/Anthropic/Ollama |
| Discord webhooks | ✅ DONE | Feedback |
| Health checks | ✅ DONE | /health endpoints |
| PostgreSQL + Redis | ✅ DONE | Docker compose |
| FastAPI backend | ✅ DONE | Clean architecture |

**Gap principal:** Sem social scheduler, team workspaces, multiple aspect ratios, PT-BR localization.

---

## PARTE 2: Roadmap por Fase

### FASE 1: Essentials (Próximas 2 semanas)
**Objetivo:** Equalar OpusClip Free (60min/mês com watermark)

Features prioritárias para eliminar barriers de entrada:

- [ ] **Animated captions** — Templates animated (captions que se movem com a fala)
- [ ] **Multiple aspect ratios** — Suporte 16:9, 1:1, 4:5 além do 9:16
- [ ] **Custom font upload** — Upload de TTF via interface
- [ ] **Progress real-time** — Melhorar UX de progresso com tempo estimado
- [ ] **No watermark option** — Remover branding para usuários logados

**Dependências internas:**
- Aspect ratio handler → Requer crop intelligent (face detection já existe)
- Animated captions → Requer caption renderer com animation support

**Métricas de sucesso:**
- 60+ min de processamento/mês por usuário free
- Export em todos os formatos (9:16, 16:9, 1:1, 4:5)
- Watermark removido para usuários com conta

---

### FASE 2: Differentiation (Próximas 1-2 meses)
**Objetivo:** Differenciar do mercado com features únicas

- [ ] **PT-BR localization** — Interface completa em português brasileiro (like BIA)
- [ ] **Social scheduler** — Calendar UI + scheduling backend + post queue
- [ ] **Transparent billing** — Cobrança por minuto real, sem créditos abstratos
- [ ] **API pública pay-per-use** — REST API aberta com pricing por minuto
- [ ] **Webhooks** — Event callback system para automation

**Novos input sources (Fase 2 parcial):**
- [ ] Google Drive import
- [ ] Vimeo import
- [ ] Loom import

**Diferenciais vs OpusClip:**
- API pay-per-use (OpusClip tem API closed beta)
- PT-BR nativo (OpusClip não tem)
- Transparent billing (não é abstract credits)
- Self-hosted option (enterprise)

**Dependências:**
- PT-BR localization → i18n system
- Social scheduler → DB + cron jobs
- Transparent billing → Usage tracking
- API → Webhooks foundation
- Webhooks → Event system

---

### FASE 3: Team/Agency (2-3 meses)
**Objetivo:** Atender agências e multi-client workflows

- [ ] **Workspaces** — Multi-workspace por usuário
- [ ] **Team seats** — Assentos por workspace (até 4 users)
- [ ] **Role-based permissions** — RBAC (admin, editor, viewer)
- [ ] **Client sub-workspaces** — Workspaces para clientes de agência
- [ ] **Shared templates** — Templates compartilhados por workspace

**Features de scheduling:**
- [ ] **Calendar view** — Visualização calendário de posts
- [ ] **Bulk processing** — Processamento em massa

**Billing avançado:**
- [ ] **Annual billing** — Desconto anual (~50%)
- [ ] **Credit packs** — Compra avulsa

**Dependências:**
- Workspaces → Auth + User model extension
- Team seats → Workspace model
- Role permissions → RBAC system
- Client sub-workspaces → Hierarchical workspaces
- Shared templates → Template storage per workspace

---

### FASE 4: Premium (3-6 meses)
**Objetivo:** Features avançadas para competir com OpusClip Pro

**AI Features avançadas:**
- [ ] **Auto reframe (moving objects)** — Object tracking para auto-reframe
- [ ] **Virality scoring improved** — Algoritmo enhanced com mais parâmetros
- [ ] **AI B-Roll** — Geração automática de B-roll (50 clips/dia)
- [ ] **Filler word removal** — Remoção de "eh", "né", "bora", etc
- [ ] **AI copilot** — Topics search, prompt to clip
- [ ] **Auto censor** — Blocklist custom de palavras
- [ ] **Genre-specific reframe** — Otimização por gênero (podcast, tutorial, vlog)

**Video Features:**
- [ ] **AI Voice-over** — Geração de voice-over (20/day)
- [ ] **Brand templates** — Templates com logo/colors/font
- [ ] **Direct social posting** — OAuth apps (TikTok, IG, YT, LinkedIn)

**Output avançado:**
- [ ] **Multiple video sources** — Zoom, Rumble, Twitch, Riverside, Frame.io, StreamYard
- [ ] **Resolution options** — 720p, 1080p, 4K
- [ ] **Format export** — MP4, MOV

**Enterprise:**
- [ ] **Team workspace (4 users)** — Workspace expansion
- [ ] **30GB video storage** — Storage por workspace
- [ ] **Public MP4 URL import** — Import via URL pública
- [ ] **SSO/SAML** — Enterprise auth

**Analytics:**
- [ ] **Usage tracking** — Usage por usuário
- [ ] **Team analytics** — Analytics por workspace

**Concorrência com OpusClip Pro ($29/mês):**
- AI B-Roll (50/day) → SupoClip mesmo limite
- Filler word removal → SupoClip implementar
- Auto censor → SupoClip implementar
- AI Voice-over (20/day) → SupoClip implementar
- Team workspace (4) → SupoClip implementar
- Brand templates → SupoClip implementar

---

## PARTE 3: Technical Requirements

### FASE 1: Essentials

**Componentes necessários:**

| Componente | Descrição | Arquivo referência |
|-----------|-----------|-----------------|
| Caption renderer | MoviePy com animation support | `backend/src/services/renderer.py` |
| Aspect ratio handler | Resize + smart crop | `backend/src/services/cropper.py` |
| Font uploader | Upload + validation de TTF | `backend/src/api/routes/fonts.py` |
| Progress tracker | Tempo estimado + ETA | SSE endpoint extension |

**Arquitetura técnica:**

```python
# Aspect ratio handler - pseudo code
class AspectRatioHandler:
    def __init__(self, target_ratio: str):
        self.ratios = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}
    
    def resize_with_crop(self, video, target_ratio):
        # Face detection ja existe - usar para smart crop
        face_box = self.detect_face(video)
        return self.crop_to_ratio(video, target_ratio, face_box)
```

---

### FASE 2: Differentiation

**Componentes necessários:**

| Componente | Descrição | Dependência |
|-----------|-----------|-------------|
| i18n system | PT-BR, EN, ES support | Frontend + Backend |
| Scheduler | DB table + cron | PostgreSQL |
| Usage tracker | Billing por segundo | PostgreSQL |
| Public API | REST OpenAPI | FastAPI |
| Webhook system | Event dispatch | Redis + DB |

**DB Schema - Scheduler:**

```sql
CREATE TABLE scheduled_posts (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    clip_id UUID REFERENCES clips(id),
    platform VARCHAR(20), -- tiktok, instagram, youtube
    scheduled_at TIMESTAMP NOT NULL,
    status VARCHAR(20), -- pending, published, failed
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

### FASE 3: Team/Agency

**Componentes necessários:**

| Componente | Descrição | Dependência |
|-----------|-----------|-------------|
| Workspace model | Multi-tenant extension | Auth + DB |
| RBAC system | Permissions por role | Better Auth |
| Template storage | Per-workspace templates | S3/Local storage |
| Bulk processor | Queue massiva | ARQ workers |

**DB Schema - Workspaces:**

```sql
CREATE TABLE workspaces (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    owner_id UUID REFERENCES users(id),
    plan VARCHAR(50), -- free, starter, pro, business
    storage_limit_gb INTEGER DEFAULT 5,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE workspace_members (
    workspace_id UUID REFERENCES workspaces(id),
    user_id UUID REFERENCES users(id),
    role VARCHAR(20), -- admin, editor, viewer
    PRIMARY KEY (workspace_id, user_id)
);
```

---

### FASE 4: Premium

**Componentes necessários:**

| Componente | Descrição | Dependência |
|-----------|-----------|-------------|
| Object tracking | MediaPipe multi-object | MediaPipe |
| Scoring algorithm | Enhanced virality | ML model |
| Voice-over | TTS integration | OpenAI/Google TTS |
| OAuth apps | Social login | Multiple providers |
| Template engine | Dynamic templates | Template system |

**DB Schema - Brands:**

```sql
CREATE TABLE brand_templates (
    id UUID PRIMARY KEY,
    workspace_id UUID REFERENCES workspaces(id),
    name VARCHAR(255),
    logo_url TEXT,
    colors VARCHAR[], -- hex codes
    font_family VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## PARTE 4: Dependencies

### Mapa de dependências

```
FASE 1 (2 semanas)
├── Animated captions ← Caption renderer
├── Multiple aspect ratios ← Face detection (existente!)
├── Custom font upload ← Font uploader
├── Progress real-time ← SSE enhancement
└── No watermark ← Auth + Plan check

FASE 2 (1-2 meses)
├── PT-BR localization ← i18n system
├── Social scheduler ← FASE 3: Workspaces
├── Transparent billing ← Usage tracking
├── API pública ← FASE 2: Webhooks
├── Webhooks ← Event system
├── Google Drive ← G-Drive API
├── Vimeo ← Vimeo API
└── Loom ← Loom API

FASE 3 (2-3 meses) ← REQUER FASE 1+2
├── Workspaces ← Auth extension
├── Team seats ← Workspaces
├── Role permissions ← RBAC
├── Client sub-workspaces ← Hierarchical workspaces
├── Shared templates ← Template storage
├── Calendar view ← Scheduler
├── Bulk processing ← ARQ enhancement
├── Annual billing ← Stripe
└── Credit packs ← Stripe

FASE 4 (3-6 meses) ← REQUER FASE 3
├── Auto reframe ← MediaPipe tracking
├── Virality scoring ← ML model
├── AI B-Roll ← Pexels/Media search
├── Filler word removal ← Transcription AI
├── AI copilot ← Pydantic AI extension
├── Auto censor ← Blocklist system
├── Genre reframe ← Classifier
├── AI Voice-over ← TTS
├── Brand templates ← Template engine
├── Direct posting ← OAuth
├── Multiple sources ← Multiple APIs
├── Resolution options ← Renderer config
├── Format export ← FFmpeg
├── Team workspace expansion ← FASE 3: Workspaces
├── Storage expansion ← S3/Local
├── Public URL import ← URL fetcher
├── SSO/SAML ← Auth extension
├── Usage tracking ← Billing
└── Team analytics ← Workspaces
```

### Critical path

**Path mais longo:** FASE 1 → FASE 2 → FASE 3 → FASE 4 = ~6 meses

**Path mínimo (MVP):** FASE 1 (2 sem) → Social scheduler (FASE 2 pode paralelizar com FASE 3)

---

## PARTE 5: Effort Estimates

### FASE 1: Essentials

| Feature | Hours | Priority | Dependencies |
|---------|-------|----------|--------------|
| Animated captions | 16h | P0 | Caption renderer |
| Multiple aspect ratios | 8h | P0 | Face detection (existente!) |
| Custom font upload | 8h | P1 | Font storage |
| Progress real-time | 4h | P1 | SSE |
| No watermark | 2h | P1 | Auth |

**Total FASE 1:** 38 horas

---

### FASE 2: Differentiation

| Feature | Hours | Priority | Dependencies |
|---------|-------|----------|--------------|
| PT-BR localization | 24h | P0 | i18n system |
| Social scheduler | 40h | P0 | Workspaces base |
| Transparent billing | 32h | P1 | Usage tracking |
| API pública | 48h | P1 | Webhooks |
| Webhooks | 24h | P1 | Event system |
| Google Drive import | 16h | P2 | Google API |
| Vimeo import | 12h | P2 | Vimeo API |
| Loom import | 12h | P2 | Loom API |

**Total FASE 2:** 208 horas

---

### FASE 3: Team/Agency

| Feature | Hours | Priority | Dependencies |
|---------|-------|----------|--------------|
| Workspaces | 40h | P0 | Auth extension |
| Team seats | 24h | P0 | Workspaces |
| Role permissions | 24h | P0 | RBAC |
| Client sub-workspaces | 32h | P1 | Hierarchical workspaces |
| Shared templates | 16h | P1 | Template storage |
| Calendar view | 16h | P1 | Scheduler |
| Bulk processing | 24h | P2 | ARQ |
| Annual billing | 16h | P2 | Stripe |
| Credit packs | 16h | P2 | Stripe |

**Total FASE 3:** 208 horas

---

### FASE 4: Premium

| Feature | Hours | Priority | Dependencies |
|---------|-------|----------|--------------|
| Auto reframe | 40h | P0 | Object tracking |
| Virality scoring | 32h | P0 | ML model |
| AI B-Roll | 24h | P1 | Media search |
| Filler word removal | 24h | P1 | Transcription AI |
| AI copilot | 32h | P1 | Pydantic AI |
| Auto censor | 16h | P1 | Blocklist |
| Genre reframe | 24h | P2 | Classifier |
| AI Voice-over | 32h | P2 | TTS |
| Brand templates | 32h | P2 | Template engine |
| Direct social posting | 48h | P2 | OAuth |
| Multiple sources | 40h | P2 | Multiple APIs |
| Resolution options | 8h | P3 | FFmpeg |
| Format export | 8h | P3 | FFmpeg |
| Team workspace | 8h | P3 | Workspaces |
| Storage expansion | 16h | P3 | S3 |
| Public URL import | 12h | P3 | URL fetcher |
| SSO/SAML | 40h | P3 | Auth |
| Usage tracking | 16h | P3 | Billing |
| Team analytics | 24h | P3 | Analytics |

**Total FASE 4:** 454 horas

---

## PARTE 6: Roadmap Visual Timeline

```
2026
─────────────────────────────────────────────────────────────────────────────────────
ABRIL          MAI           JUN           JUL           AGO           SET
├──────────────┴──────────────┴──────────────┴──────────────┴──────────────┴─────
│
│ FASE 1: ESSENTIALS (2 sem)
│ ■ Animated captions
│ ■ Multiple aspect ratios
│ ■ Custom fonts
│ ■ Progress realtime
│ ■ No watermark
│
├─────────────────────────────┬─────────────────────────────┬────────────────────
│ FASE 2: DIFFERENTIATION      │ FASE 3: TEAM/AGENCY          │ FASE 4: PREMIUM
│ (1-2 meses)                  │ (2-3 meses)                  │ (3-6 meses)
│                              │                              │
│ ■ PT-BR localization         │ ■ Workspaces                 │ ■ Auto reframe
│ ■ Social scheduler           │ ■ Team seats                │ ■ Virality scoring
│ ■ Transparent billing        │ ■ Role permissions          │ ■ AI B-Roll
│ ■ API pública                │ ■ Client sub-workspaces       │ ■ Filler word removal
│ ■ Webhooks                   │ ■ Shared templates          │ ■ AI copilot
│ ■ GDrive/Vimeo/Loom           │ ■ Calendar view            │ ■ Auto censor
│                              │ ■ Bulk processing          │ ■ Genre reframe
│                              │ ■ Annual billing           │ ■ AI Voice-over
│                              │                              │ ■ Brand templates
│                              │                              │ ■ Direct post
│                              │                              │ ■ Multiple sources
│                              │                              │ ...

┌────────────────────────────────────────────────────────────────────────
│ TOTAL: ~908 horas (~6 meses full-time equivalent)
└────────────────────────────────────────────────────────────────────────
```

---

## PARTE 7: Competitor Feature Matrix

### Concorrência direta

| Feature | OpusClip | Real Oficial | VidRush | Ssemble | SupoClip Meta |
|---------|----------|--------------|---------|---------|--------------|
| **Pricing** | $15-29/mo | R$60-150/mo | $99-639/mo | $9.99/mo | Pay-per-use |
| **Open source** | ❌ | ❌ | ❌ | ❌ | ✅ AGPL-3.0 |
| **PT-BR** | ❌ | ✅ | ❌ | ❌ | ✅ native |
| **Self-hosted** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **API pay-per-use** | ❌ (closed) | ❌ | ❌ | ❌ | ✅ target |
| **Team workspaces** | ✅ | ❓ | ✅ | ❌ | FASE 3 |
| **Social scheduler** | ✅ | ❓ | ❓ | ❌ | FASE 2 |
| **AI B-Roll** | ✅ | ❓ | ❓ | ❌ | FASE 4 |
| **Filler removal** | ✅ | ❓ | ❓ | ❌ | FASE 4 |
| **Auto censor** | ✅ | ❓ | ❓ | ❌ | FASE 4 |

### Oportunidades de mercado

1. **API Developers** — OpusClip tem API closed beta; demanda por API aberta
2. **Brasil** — Real Oficial validou mercado; sem competitor open source
3. **Enterprise Self-hosted** — Empresas que não querem dados em cloud
4. **Agências** — Workspace multi-client que OpusClip não suporta bem
5. ** pay-per-use** — Cobrança transparente por minuto

---

## PARTE 8: riscos e Mitigações

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| scope creep | Roadmap esticado | Focar em FASE 1 primeiro |
| API complexity | Webhooks muito complexo | MVP simples primeiro |
| OAuth apps | Rejeição por plataformas | Public scheduling primeiro |
| ML model accuracy | Virality scoring impreciso | Iterar com dados reais |
| Enterprise sales | Long sales cycle | Focar em SMB primeiro |

---

## PARTE 9: Priorização Recomendada

### Recomendação: FASE 1 primeiro

1. **Animated captions** — Usuários pedem muito
2. **Multiple aspect ratios** — TikTok/YT/IG = múltiplas saídas
3. **PT-BR localization** — Diferencial rápido

### Depois FASE 2

4. **Social scheduler** — Retenção de usuários
5. **API pública** — Revenue stream
6. **Webhooks** — Automation para devs

### Depois FASE 3

7. **Workspaces** — Sales para agências
8. **Team seats** — Revenue por usuário

### Depois FASE 4

9. **Auto reframe** — Feature de destaque
10. **AI B-Roll** — Complemento de valor

---

## Documentos de Referência

| Documento | Caminho |
|-----------|---------|
| Full Feature Audit | `docs/analysis/full-feature-audit.md` |
| Competitor Analysis | `docs/analysis/competitor-analysis.md` |
| Feature Opportunities | `docs/analysis/feature-opportunities.md` |
| DB Schema | `docs/architecture/database-schema.md` |
| System Architecture | `docs/architecture/system-architecture.md` |

---

*Generated: Features Roadmap v1.0*
*Date: 2026-04-14*
*Author: @pm*