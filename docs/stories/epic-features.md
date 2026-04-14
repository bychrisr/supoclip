# Epic: Features Enhancement - SupoClip 2026

## Objetivo

Ser a melhor ferramenta open-source de AI video clipping com features parity vs OpusClip Free + diferenciação brasileira (PT-BR nativo, API pay-per-use, self-hosted option).

## Escopo

| Fase | Escopo | Horas | Timeline |
|------|-------|-------|----------|
| FASE 1 | Essentials - Parity OpusClip Free | 38h | 2 semanas |
| FASE 2 | Differentiation - Diferenciais BR | 208h | 1-2 meses |
| FASE 3 | Team/Agency - Multi-client | 208h | 2-3 meses |
| FASE 4 | Premium - Features Pro | 454h | 3-6 meses |

**Total: ~908 horas**

---

## Critérios de Sucesso

- [ ] Parity com OpusClip Free (FASE 1)
- [ ] Animated captions funcionando (FASE 1)
- [ ] Multiple aspect ratios (9:16, 16:9, 1:1, 4:5) (FASE 1)
- [ ] Custom font upload via interface (FASE 1)
- [ ] Progress realtime com ETA (FASE 1)
- [ ] No watermark para usuários logados (FASE 1)
- [ ] PT-BR localization nativa (FASE 2)
- [ ] Social scheduler com calendar (FASE 2)
- [ ] Transparent billing por minuto (FASE 2)
- [ ] API pública pay-per-use (FASE 2)
- [ ] Webhooks event system (FASE 2)
- [ ] Workspaces multi-tenant (FASE 3)
- [ ] Team seats (ate 4 users) (FASE 3)
- [ ] Role-based permissions (FASE 3)
- [ ] Client sub-workspaces (FASE 3)
- [ ] Shared templates por workspace (FASE 3)
- [ ] Calendar view (FASE 3)
- [ ] Bulk processing (FASE 3)
- [ ] Features Pro equal OpusClip Pro (FASE 4)
- [ ] AI B-Roll (50 clips/dia) (FASE 4)
- [ ] Filler word removal (FASE 4)
- [ ] AI Voice-over (20/dia) (FASE 4)
- [ ] Brand templates (FASE 4)
- [ ] Direct social posting (FASE 4)
- [ ] SSO/SAML enterprise (FASE 4)

---

## Timeline

```
2026
────────────────────────────────────────────────────────────────────────────────────
ABR          MAI           JUN           JUL           AGO           SET
├────────────┴────────────┴────────────┴────────────┴────────────┴────────────
│
│ FASE 1: ESSENTIALS (2 semanas)
│ ■ Animated captions (16h)
│ ■ Multiple aspect ratios (8h)
│ ■ Custom font upload (8h)
│ ■ Progress realtime (4h)
│ ■ No watermark (2h)
│
├─────────────────────────────┬─────────────────────────────┬──────────────────────────
│ FASE 2: DIFFERENTIATION │ FASE 3: TEAM/AGENCY       │ FASE 4: PREMIUM
│ (1-2 meses)             │ (2-3 meses)               │ (3-6 meses)
│                         │                         │
│ ■ PT-BR localization   │ ■ Workspaces             │ ■ Auto reframe
│ ■ Social scheduler     │ ■ Team seats            │ ■ Virality scoring
│ ■ Transparent billing │ ■ Role permissions     │ ■ AI B-Roll
│ ■ API publica         │ ■ Client sub-workspaces│ ■ Filler word removal
│ ■ Webhooks            │ ■ Shared templates    │ ■ AI copilot
│ ■ GDrive/Vimeo/Loom   │ ■ Calendar view       │ ■ Auto censor
│                       │ ■ Bulk processing     │ ■ AI Voice-over
│                       │ ■ Annual billing     │ ■ Brand templates
│                       │                       │ ■ Direct posting
│                       │                       │ ... (21 features)
│
┌────────────────────────────────────────────────────────────────────────────────
│ TOTAL: ~908 horas
└────────────────────────────────────────────────────────────────────────────────
```

---

## Stories Vinculadas

### FASE 1: Essentials (38h)

1. [story-features-animated-captions.md](./story-features-animated-captions.md) - Animated captions (16h)
2. [story-features-aspect-ratios.md](./story-features-aspect-ratios.md) - Multiple aspect ratios (8h)
3. [story-features-custom-fonts.md](./story-features-custom-fonts.md) - Custom font upload (8h)
4. [story-features-progress-realtime.md](./story-features-progress-realtime.md) - Progress realtime com ETA (4h)
5. [story-features-no-watermark.md](./story-features-no-watermark.md) - No watermark option (2h)

### FASE 2: Differentiation (208h)

| # | Story | Estimate | Priority |
|---|-------|---------|---------|
| 6 | [story-features-localization.md](./story-features-localization.md) | 24h | P0 |
| 7 | [story-features-social-scheduler.md](./story-features-social-scheduler.md) | 40h | P0 |
| 8 | [story-features-billing.md](./story-features-billing.md) | 32h | P1 |
| 9 | [story-features-api-first.md](./story-features-api-first.md) | 48h | P1 |
| 10 | [story-features-webhooks.md](./story-features-webhooks.md) | 24h | P1 |
| 11 | [story-features-google-drive-import.md](./story-features-google-drive-import.md) | 16h | P2 |
| 12 | [story-features-vimeo-import.md](./story-features-vimeo-import.md) | 12h | P2 |
| 13 | [story-features-loom-import.md](./story-features-loom-import.md) | 12h | P2 |

### FASE 3: Team/Agency (208h)

14. [story-features-workspaces.md](./story-features-workspaces.md) - Workspaces (40h)
15. [story-features-team-seats.md](./story-features-team-seats.md) - Team seats (24h)
16. [story-features-role-permissions.md](./story-features-role-permissions.md) - Role permissions (24h)
17. [story-features-client-subworkspaces.md](./story-features-client-subworkspaces.md) - Client sub-workspaces (32h)
18. [story-features-shared-templates.md](./story-features-shared-templates.md) - Shared templates (16h)
19. [story-features-calendar-view.md](./story-features-calendar-view.md) - Calendar view (16h)
20. [story-features-bulk-processing.md](./story-features-bulk-processing.md) - Bulk processing (24h)
21. [story-features-annual-billing.md](./story-features-annual-billing.md) - Annual billing (16h)
22. [story-features-credit-packs.md](./story-features-credit-packs.md) - Credit packs (16h)

### FASE 4: Premium (454h)

23. [story-features-auto-reframe.md](./story-features-auto-reframe.md) - Auto reframe (40h)
24. [story-features-virality-scoring.md](./story-features-virality-scoring.md) - Virality scoring improved (32h)
25. [story-features-ai-broll.md](./story-features-ai-broll.md) - AI B-Roll (24h)
26. [story-features-filler-removal.md](./story-features-filler-removal.md) - Filler word removal (24h)
27. [story-features-ai-copilot.md](./story-features-ai-copilot.md) - AI copilot (32h)
28. [story-features-auto-censor.md](./story-features-auto-censor.md) - Auto censor (16h)
29. [story-features-genre-reframe.md](./story-features-genre-reframe.md) - Genre-specific reframe (24h)
30. [story-features-ai-voiceover.md](./story-features-ai-voiceover.md) - AI Voice-over (32h)
31. [story-features-brand-templates.md](./story-features-brand-templates.md) - Brand templates (32h)
32. [story-features-direct-posting.md](./story-features-direct-posting.md) - Direct social posting (48h)
33. [story-features-multiple-sources.md](./story-features-multiple-sources.md) - Multiple video sources (40h)
34. [story-features-resolution-options.md](./story-features-resolution-options.md) - Resolution options (8h)
35. [story-features-format-export.md](./story-features-format-export.md) - Format export (8h)
36. [story-features-team-expansion.md](./story-features-team-expansion.md) - Team workspace (8h)
37. [story-features-storage-expansion.md](./story-features-storage-expansion.md) - Storage expansion (16h)
38. [story-features-url-import.md](./story-features-url-import.md) - Public URL import (12h)
39. [story-features-sso.md](./story-features-sso.md) - SSO/SAML (40h)
40. [story-features-usage-tracking.md](./story-features-usage-tracking.md) - Usage tracking (16h)
41. [story-features-team-analytics.md](./story-features-team-analytics.md) - Team analytics (24h)

---

## Dependências Externas

| Recurso | Provedor | Uso |
|---------|----------|-----|
| Google Drive API | Google | Video import |
| Vimeo API | Vimeo | Video import |
| Loom API | Loom | Video import |
| Stripe | Stripe | Billing (annual, credits) |
| Pexels/Media | Pexels | AI B-Roll |
| OpenAI TTS | OpenAI | AI Voice-over |
| Google TTS | Google | AI Voice-over |
| Better Auth | Auth | SSO/SAML |

---

## Referências

| Documento | Caminho |
|----------|---------|
| Features Roadmap | `docs/roadmap/features-roadmap.md` |
| Full Feature Audit | `docs/analysis/full-feature-audit.md` |
| Competitor Analysis | `docs/analysis/competitor-analysis.md` |
| DB Schema | `docs/architecture/database-schema.md` |

---

*Generated: Epic Features v1.0*
*Date: 2026-04-14*
*Author: @pm*