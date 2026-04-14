# Story: Format Export (MP4/MOV)

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P3
- **Estimate:** 8h

## Problem

Usuários precisam de diferentes formatos de export (MP4, MOV) para diferentes use cases. Apenas MP4 disponível.

## Solution

Implementar format export:
- MP4 export (default)
- MOV export (ProRes for editing)
- Format selector na UI
- Configurable por export preset

## Scope

- In: Video config
- Out: Video output no format

## Tasks

1. [ ] Add MOV export support
2. [ ] Create format selector UI
3. [ ] Integrate com export presets
4. [ ] Write integration tests

## Acceptance Criteria

- [ ] MP4 export funciona
- [ ] MOV export funciona
- [ ] Format selector na UI
- [ ] Tests: 90% coverage

## Dependencies

- FASE 1: Multiple aspect ratios
- FFmpeg (existing)