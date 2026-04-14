# Story: AI B-Roll Generation

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P1
- **Estimate:** 24h

## Problem

Usuários precisam de B-roll manual para enrichment de clips, mas o proceso é manual e demorado. AI B-Roll automático seria diferencial competitivo vs OpusClip.

## Solution

Implementar AI B-Roll automático:
- Integrar com Pexels API para busca de videos
- Analyze contexto do clip para sugerir B-roll relevante
- Limite: 50 clips/dia por workspace
- Auto-insert com transition effects
- Manual override para seleção customizada

## Scope

- In: Processed clip com contexto
- Out: Clip com B-roll overlay

## Tasks

1. [ ] Integrate Pexels API
2. [ ] Implement context-based B-roll search
3. [ ] Create auto-insert workflow
4. [ ] Add daily limit tracking (50/day)
5. [ ] Implement manual override UI
6. [ ] Add transition effects para B-roll
7. [ ] Write integration tests

## Acceptance Criteria

- [ ] 50 clips/dia por workspace
- [ ] Busca por contexto do video
- [ ] Auto-insert com transitions
- [ ] Manual override disponível
- [ ] Tests: 85% coverage

## Dependencies

- Pexels API
- FASE 1: Animated captions, Multiple aspect ratios
- B-roll overlays (existing)