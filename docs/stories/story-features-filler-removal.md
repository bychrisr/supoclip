# Story: Filler Word Removal

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P1
- **Estimate:** 24h

## Problem

Vídeos containing filled words como "eh", "né", "bora", " aí", "vc sabe" têm quality reduzida. Remover manualmente é demorado e propenso a erros.

## Solution

Implementar filler word removal:
- Detect fill words via transcription analysis
- Configurable blocklist por idioma/estilo
- Preview de antes/depois
- Batch processing support
- Suporte PT-BR e EN patterns

## Scope

- In: Video com filled words
- Out: Video sem filled words

## Tasks

1. [ ] Define filler word patterns para PT-BR e EN
2. [ ] Implement filler detection via transcript
3. [ ] Create removal algorithm
4. [ ] Add preview mode
5. [ ] Implement batch processing
6. [ ] Add customizable blocklist
7. [ ] Write integration tests

## Acceptance Criteria

- [ ] Detecta +20 filler patterns PT-BR
- [ ] Detecta +15 filler patterns EN
- [ ] Preview mode berfungsi
- [ ] Batch processing support
- [ ] Tests: 90% coverage

## Dependencies

- FASE 1: Animated captions (for subtitle sync)
- AssemblyAI transcription (existing)
- Word-synced subtitles (existing)