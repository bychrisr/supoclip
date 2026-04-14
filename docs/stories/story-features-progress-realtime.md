# Story: Real-time Progress with ETA
- **Epic:** epic-features.md
- **Fase:** FASE 1 - Essentials
- **Priority:** P1
- **Estimate:** 4h

## Problem
Usuários não sabem quanto falta para o processamento terminar, causando frustração.

## Solution
Implementar progress real-time com ETA calculation.

## Scope
- In: Video processing job
- Out: Real-time progress + ETA display

## Tasks
- [ ] Research ETA calculation logic
- [ ] Add progress percentage tracking
- [ ] Implement ETA prediction
- [ ] Update UI with progress bar

## Acceptance Criteria
- [ ] Show progress percentage
- [ ] Show ETA in minutes
- [ ] Update every 2 seconds
- [ ] Handle edge cases (slow/fast processing)

## Dependencies
- Video processing (backend/src/services/renderer.py)