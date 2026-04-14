# Story: Genre-Specific Reframe

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P2
- **Estimate:** 24h

## Problem

Diferentes gêneros de conteúdo (podcast, tutorial, vlog) precisam de estratégias de reframe específicas. Reframe genérico não otimiza para cada formato.

## Solution

Implementar genre-specific reframe:
- Detect content genre classifier
- Genre-specific cropping strategies:
  - Podcast: speaker centered
  - Tutorial: focus on content + speaker
  - Vlog: dynamic + b-roll
- Genre presets configuráveis
- Manual override

## Scope

- In: Video input
- Out: Optimized reframe

## Tasks

1. [ ] Create content genre classifier
2. [ ] Implement podcast strategy
3. [ ] Implement tutorial strategy
4. [ ] Implement vlog strategy
5. [ ] Add genre presets
6. [ ] Implement manual override
7. [ ] Write integration tests

## Acceptance Criteria

- [ ] Auto-detect content genre
- [ ] Genre-specific strategies work
- [ ] Presets configurable
- [ ] Manual override funciona
- [ ] Tests: 85% coverage

## Dependencies

- FASE 4: Auto reframe (P0)
- Face detection (existing)