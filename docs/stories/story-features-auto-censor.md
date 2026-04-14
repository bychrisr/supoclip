# Story: Auto Censor with Custom Blocklist

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P1
- **Estimate:** 16h

## Problem

Conteúdo sensível (profanity, brand mentions, competidoras) precisa ser censurado. Blocklist estático não atende necessidades específicas por cliente.

## Solution

Implementar auto censor com customizable blocklist:
- Configurable blocklist por workspace
- Preset blocklists (profanity, competitors, legal)
- Auto-censor via transcription
- Visual blur/censor effects
- Preview mode

## Scope

- In: Video + blocklist config
- Out: Censored video

## Tasks

1. [ ] Create blocklist model
2. [ ] Implement preset blocklists
3. [ ] Add workspace customization
4. [ ] Implement auto-detection
5. [ ] Add visual censor effects
6. [ ] Create preview mode
7. [ ] Write integration tests

## Acceptance Criteria

- [ ] Custom blocklists por workspace
- [ ] Presets available
- [ ] Visual blur funciona
- [ ] Preview mode disponível
- [ ] Tests: 90% coverage

## Dependencies

- FASE 1: Animated captions (for subtitle sync)
- AssemblyAI transcription (existing)
- Word-synced subtitles (existing)