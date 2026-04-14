# Story: Resolution Options (720p/1080p/4K)

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P3
- **Estimate:** 8h

## Problem

Usuários precisam de diferentes resoluções de output (720p, 1080p, 4K) depending on platform. Apenas 1080p disponível atualmente.

## Solution

Implementar resolution options:
- 720p output (web/email)
- 1080p output (default)
- 4K output (high quality)
- Resolution selector na UI
- Configurable por export preset

## Scope

- In: Video config
- Out: Video output na resolution

## Tasks

1. [ ] Add resolution options to renderer
2. [ ] Create resolution selector UI
3. [ ] Integrate com export presets
4. [ ] Write integration tests

## Acceptance Criteria

- [ ] 720p output funciona
- [ ] 1080p output funciona
- [ ] 4K output funciona
- [ ] Resolution selector na UI
- [ ] Tests: 90% coverage

## Dependencies

- FASE 1: Multiple aspect ratios
- FFmpeg (existing)