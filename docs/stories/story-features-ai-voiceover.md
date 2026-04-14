# Story: AI Voice-Over Generation

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P2
- **Estimate:** 32h

## Problem

Usuários precisam criar versões narradas de seus clips para diferentes públicos ou idiomas. Voice-over manual é demorado e caro.

## Solution

Implementar AI voice-over:
- Integrar com OpenAI TTS e Google TTS
- Text-to-speech generation
- Limite: 20/day por workspace
- Multiple voice options
- Language support (PT-BR, EN, ES)
- Timing sync com video

## Scope

- In: Text script + video
- Out: Video com voice-over

## Tasks

1. [ ] Integrate OpenAI TTS
2. [ ] Integrate Google TTS
3. [ ] Implement text-to-speech generation
4. [ ] Add daily limit tracking (20/day)
5. [ ] Add voice options
6. [ ] Implement timing sync
7. [ ] Add language options
8. [ ] Write integration tests

## Acceptance Criteria

- [ ] 20 clips/dia por workspace
- [ ] Multiple voices available
- [ ] PT-BR, EN, ES supported
- [ ] Timing sync funciona
- [ ] Tests: 85% coverage

## Dependencies

- OpenAI TTS API
- Google TTS API
- FASE 1: Animated captions, Multiple aspect ratios