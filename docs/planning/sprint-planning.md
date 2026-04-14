# Sprint Planning - SupoClip Features

> **Generated:** 2026-04-14  
> **Author:** @pm (Morgan - Product Manager)  
> **Status:** READY FOR EXECUTION

---

## 📊 Overview

| Metric | Value |
|--------|-------|
| Total Stories | 50 (41 features + 9 technical debt) |
| Total Effort | ~1,215h |
| Current Capacity | ~80h/mês (1 dev full-time) |
| Timeline | ~6 meses (15 sprints) |
| Sprints | ~40h cada (2 semanas) |

### Esforço por Categoria

| Categoria | Stories | Esforço |
|-----------|--------|---------|
| Features (FASE 1-4) | 41 | ~908h |
| Technical Debt | 9 | ~307h |
| **TOTAL** | **50** | **~1,215h** |

---

## 🎯 Sprint Strategy

### Abordagem

1. **Semana 1-2 (Sprint 1):** FASE 1 Features - Parity OpusClip Free
2. **Semana 3+: paralelizar Features + Technical Debt**
3. **Priorização:** Security Critical primeiro (débitos P0)
4. **Paralelização:** @dev (features) + @devops (TD) onde possível

### Capacidade Ajustada

- ~80h/mês = ~40h/sprint (2 semanas)
- 6 meses = 12 sprints = ~480h capacidade
- **Gap:** 1,215h - 480h = 735h de défict

### Mitigação do Gap

| Estratégia | Impacto |
|------------|---------|
| Async development (2 devs) | +80h/mês |
| Priorização ruthless | Cortar ~400h de escopo low-value |
| FASE 4 parcial | Adiadar FASE 4 não-critical |

---

## 🏃 Sprint 1-2: Foundation (Semana 1-4)

> **Foco:** Parity OpusClip Free + Security Critical

### Sprint 1: Essentials - Phase 1 (Semana 1-2)

**Goal:** Parity com OpusClip Free - funcionalidades core

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-no-watermark](./stories/story-features-no-watermark.md) | 2h | @dev | - |
| [story-features-aspect-ratios](./stories/story-features-aspect-ratios.md) | 8h | @dev | - |
| [story-features-animated-captions](./stories/story-features-animated-captions.md) | 16h | @dev | - |
| [story-features-custom-fonts](./stories/story-features-custom-fonts.md) | 8h | @dev | aspect-ratios |
| [story-features-progress-realtime](./stories/story-features-progress-realtime.md) | 4h | @dev | - |

**Subtotal:** 38h  
**Status:** BLOCKED BY: Nenhuma

---

### Sprint 2: Security First (Semana 3-4)

**Goal:** Segurança crítica + Test setup

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-security-critical](./stories/story-security-critical.md) | 42h | @data-engineer | - |
| [story-tests-automation](./stories/story-tests-automation.md) | 40h | @qa | - |

**Subtotal:** 82h (excede ~40h, OK para sprint duplo)  
**Status:** BLOCKED BY: Sprint 1 completion  
**Notes:** Começa em paralelo com Sprint 1 final

---

## 🚀 Sprint 3-6: Differentiation BR (Semana 5-12)

> **Foco:** Diferenciais brasileiros + Database Quality

### Sprint 3: Localization + Imports (Semana 5-6)

**Goal:** PT-BR localization + Google Drive import

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-localization](./stories/story-features-localization.md) | 24h | @dev | Sprint 1 |
| [story-features-google-drive-import](./stories/story-features-google-drive-import.md) | 16h | @dev | Sprint 1 |
| [story-features-vimeo-import](./stories/story-features-vimeo-import.md) | 12h | @dev | Sprint 1 |
| [story-features-loom-import](./stories/story-features-loom-import.md) | 12h | @dev | Sprint 1 |

**Subtotal:** 64h  
**Status:** BLOCKED BY: Sprint 1 complete

---

### Sprint 4: Database Quality (Semana 7-8)

**Goal:** Índices, normalização, migrations

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-database-quality](./stories/story-database-quality.md) | 80h | @data-engineer | Sprint 2 (security) |

**Subtotal:** 80h  
**Status:** BLOCKED BY: Sprint 2 complete

---

### Sprint 5: Billing + API (Semana 9-10)

**Goal:** Transparent billing + API pública

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-billing](./stories/story-features-billing.md) | 32h | @dev | Sprint 2 |
| [story-features-api-first](./stories/story-features-api-first.md) | 48h | @dev | Sprint 4 (DB quality) |
| [story-features-webhooks](./stories/story-features-webhooks.md) | 24h | @dev | API first |

**Subtotal:** 104h  
**Status:** BLOCKED BY: Sprint 4 complete

---

### Sprint 6: Social Scheduler (Semana 11-12)

**Goal:** Calendar view + Social scheduling

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-social-scheduler](./stories/story-features-social-scheduler.md) | 40h | @dev | Sprint 4 |
| [story-features-calendar-view](./stories/story-features-calendar-view.md) | 16h | @dev | Sprint 4 |

**Subtotal:** 56h  
**Status:** BLOCKED BY: Sprint 4 complete

---

## 👥 Sprint 7-10: Team/Agency (Semana 13-20)

> **Foco:** Multi-tenant + Team management

### Sprint 7: Workspaces (Semana 13-14)

**Goal:** Multi-tenant workspaces

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-workspaces](./stories/story-features-workspaces.md) | 40h | @dev | Sprint 4 |
| [story-features-team-seats](./stories/story-features-team-seats.md) | 24h | @dev | Workspaces |

**Subtotal:** 64h  
**Status:** BLOCKED BY: Sprint 5 complete

---

### Sprint 8: Roles + Permissions (Semana 15-16)

**Goal:** Role-based access control

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-role-permissions](./stories/story-features-role-permissions.md) | 24h | @dev | Sprint 7 |
| [story-backend-quality](./stories/story-backend-quality.md) | 64h | @dev | Sprint 2 |
| [story-frontend-server](./stories/story-frontend-server.md) | 24h | @dev | Sprint 1 |

**Subtotal:** 112h  
**Status:** BLOCKED BY: Sprint 7 complete

---

### Sprint 9: Client Sub-workspaces (Semana 17-18)

**Goal:** Sub-workspaces + Shared templates

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-client-subworkspaces](./stories/story-features-client-subworkspaces.md) | 32h | @dev | Sprint 7 |
| [story-features-shared-templates](./stories/story-features-shared-templates.md) | 16h | @dev | Sprint 7 |
| [story-features-bulk-processing](./stories/story-features-bulk-processing.md) | 24h | @dev | Sprint 5 |

**Subtotal:** 72h  
**Status:** BLOCKED BY: Sprint 8 complete

---

### Sprint 10: Billing Extras (Semana 19-20)

**Goal:** Annual billing + Credit packs

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-annual-billing](./stories/story-features-annual-billing.md) | 16h | @dev | Sprint 5 |
| [story-features-credit-packs](./stories/story-features-credit-packs.md) | 16h | @dev | Sprint 5 |
| [story-operations](./stories/story-operations.md) | 32h | @devops | Sprint 2 |

**Subtotal:** 64h  
**Status:** BLOCKED BY: Sprint 9 complete

---

## ⭐ Sprint 11-15: Premium Features (Semana 21-30)

> **Foco:** Features Pro - Diferenciação advanced

### Sprint 11: AI Core (Semana 21-22)

**Goal:** AI-powered features

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-auto-reframe](./stories/story-features-auto-reframe.md) | 40h | @dev | Sprint 4 |
| [story-features-ai-copilot](./stories/story-features-ai-copilot.md) | 32h | @dev | Sprint 4 |

**Subtotal:** 72h  
**Status:** BLOCKED BY: Sprint 10 complete

---

### Sprint 12: AI Audio (Semana 23-24)

**Goal:** Audio processing AI

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-filler-removal](./stories/story-features-filler-removal.md) | 24h | @dev | Sprint 11 |
| [story-features-ai-voiceover](./stories/story-features-ai-voiceover.md) | 32h | @dev | Sprint 11 |
| [story-features-ai-broll](./stories/story-features-ai-broll.md) | 24h | @dev | Sprint 11 |

**Subtotal:** 80h  
**Status:** BLOCKED BY: Sprint 11 complete

---

### Sprint 13: Publishing (Semana 25-26)

**Goal:** Direct posting + Format options

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-direct-posting](./stories/story-features-direct-posting.md) | 48h | @dev | Sprint 6 |
| [story-features-format-export](./stories/story-features-format-export.md) | 8h | @dev | Sprint 1 |
| [story-features-resolution-options](./stories/story-features-resolution-options.md) | 8h | @dev | Sprint 1 |

**Subtotal:** 64h  
**Status:** BLOCKED BY: Sprint 12 complete

---

### Sprint 14: Virality + Genre (Semana 27-28)

**Goal:** Virality scoring + Genre-specific

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-virality-scoring](./stories/story-features-virality-scoring.md) | 32h | @dev | Sprint 11 |
| [story-features-genre-reframe](./stories/story-features-genre-reframe.md) | 24h | @dev | Sprint 11 |
| [story-features-auto-censor](./stories/story-features-auto-censor.md) | 16h | @dev | Sprint 11 |

**Subtotal:** 72h  
**Status:** BLOCKED BY: Sprint 13 complete

---

### Sprint 15: Enterprise (Semana 29-30)

**Goal:** Enterprise features

| Story | Estimate | Assignee | Dependencies |
|-------|----------|----------|--------------|
| [story-features-sso](./stories/story-features-sso.md) | 40h | @dev | Sprint 8 |
| [story-features-brand-templates](./stories/story-features-brand-templates.md) | 32h | @dev | Sprint 9 |
| [story-features-multiple-sources](./stories/story-features-multiple-sources.md) | 40h | @dev | Sprint 4 |
| [story-features-url-import](./stories/story-features-url-import.md) | 12h | @dev | Sprint 3 |

**Subtotal:** 124h  
**Status:** BLOCKED BY: Sprint 14 complete

---

## 📦 Technical Debt Sprints - Resumo

| Sprint | Story | Esforço | Fase |
|--------|-------|--------|------|
| Sprint 2 | story-security-critical | 42h |-semana 3-4 |
| Sprint 2 | story-tests-automation | 40h |semana 3-4 |
| Sprint 4 | story-database-quality | 80h |semana 7-8 |
| Sprint 8 | story-backend-quality | 64h |semana 15-16 |
| Sprint 8 | story-frontend-server | 24h |semana 15-16 |
| Sprint 10 | story-operations | 32h |semana 19-20 |
| Sprint TBD | story-ux-ui-final | 24h |TBD |

---

## 📅 Timeline Visual

```
2026
├──────────────────────────────────────────────────────────────────────────────────────────
│ SPRINT 1-2: FOUNDATION
│ ■ story-features-no-watermark (2h)
│ ■ story-features-aspect-ratios (8h)
│ ■ story-features-animated-captions (16h)
│ ■ story-features-custom-fonts (8h)
│ ■ story-features-progress-realtime (4h)
│
│ ■ story-security-critical (42h)
│ ■ story-tests-automation (40h)
├──────────────────────────────────────────────────────────────────────────────────────────
│ SPRINT 3-6: DIFFERENTIATION BR
│ ■ story-features-localization (24h)
│ ■ story-features-google-drive-import (16h)
│ ■ story-features-vimeo-import (12h)
│ ■ story-features-loom-import (12h)
│
│ ■ story-database-quality (80h)
│
│ ■ story-features-billing (32h)
│ ■ story-features-api-first (48h)
│ ■ story-features-webhooks (24h)
│
│ ■ story-features-social-scheduler (40h)
│ ■ story-features-calendar-view (16h)
├──────────────────────────────────────────────────────────────────────────────────────────
│ SPRINT 7-10: TEAM/AGENCY  
│ ■ story-features-workspaces (40h)
│ ■ story-features-team-seats (24h)
│
│ ■ story-features-role-permissions (24h)
│ ■ story-backend-quality (64h)
│ ■ story-frontend-server (24h)
│
│ ■ story-features-client-subworkspaces (32h)
│ ■ story-features-shared-templates (16h)
│ ■ story-features-bulk-processing (24h)
│
│ ■ story-features-annual-billing (16h)
│ ■ story-features-credit-packs (16h)
│ ■ story-operations (32h)
├──────────────────────────────────────────────────────────────────────────────────────────
│ SPRINT 11-15: PREMIUM
│ ■ story-features-auto-reframe (40h)
│ ■ story-features-ai-copilot (32h)
│
│ ■ story-features-filler-removal (24h)
│ ■ story-features-ai-voiceover (32h)
│ ■ story-features-ai-broll (24h)
│
│ ■ story-features-direct-posting (48h)
│ ■ story-features-format-export (8h)
│ ■ story-features-resolution-options (8h)
│
│ ■ story-features-virality-scoring (32h)
│ ■ story-features-genre-reframe (24h)
│ ■ story-features-auto-censor (16h)
│
│ ■ story-features-sso (40h)
│ ■ story-features-brand-templates (32h)
│ ■ story-features-multiple-sources (40h)
│ ■ story-features-url-import (12h)
└────��───────────────────────────────────────────────────────────────────────────────────
```

---

## 🎯 Priorização Final

| Rank | Feature | Sprint | Justificativa |
|------|---------|--------|---------------|
| 1 | Animated captions | Sprint 1 | Core value |
| 2 | Aspect ratios | Sprint 1 | Core value |
| 3 | Progress realtime | Sprint 1 | UX 필수 |
| 4 | No watermark | Sprint 1 | Parity |
| 5 | Custom fonts | Sprint 1 | UX differentiation |
| 6 | Security Critical | Sprint 2 | P0 risk |
| 7 | Test automation | Sprint 2 | Enable velocity |
| 8 | Database quality | Sprint 4 | Enable features |
| 9 | PT-BR localization | Sprint 3 | BR market |
| 10 | Social scheduler | Sprint 6 | Revenue driver |

---

## ⚠️ Risks & Mitigations

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|----------|
| Sprint overrun | Alta | Alta | Buffer 20% |
| API integration delays | Média | Alta | Mock-first approach |
| RLS breaking queries | Média | Crítico | Test-first, rollback plan |
| Feature scope creep | Alta | Média | Strict definition of done |

---

## ✅ Definition of Done (por Sprint)

- [ ] Todas as stories completas (acceptance criteria atingido)
- [ ] Tests passando (unit + integration)
- [ ] Code review aprovado
- [ ] Documentação atualizada
- [ ] Zero blocking issues no sprint review

---

## 📄 Referências

| Documento | Caminho |
|-----------|---------|
| Epic Features | `docs/stories/epic-features.md` |
| Epic Technical Debt | `docs/stories/epic-technical-debt.md` |
| Features Roadmap | `docs/roadmap/features-roadmap.md` |
| Full Feature Audit | `docs/analysis/full-feature-audit.md` |

---

*Generated: Sprint Planning v1.0*  
*Date: 2026-04-14*  
*Author: @pm (Morgan)*