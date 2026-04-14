# Story: Storage Expansion (30GB+)

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P3
- **Estimate:** 16h

## Problem

Armazenamento atual de 5GB por workspace é insuficiente para agências com múltiplos clientes. Precisa expansão.

## Solution

Implementar storage expansion:
- 30GB storage option
- Support 100GB para enterprise
- Storage usage tracking
- Storage tiered pricing
- Auto-cleanup policies

## Scope

- In: Workspace storage config
- Out: Expanded storage

## Tasks

1. [ ] Implement 30GB storage tier
2. [ ] Implement 100GB enterprise tier
3. [ ] Add storage usage tracking
4. [ ] Add tiered pricing
5. [ ] Implement auto-cleanup
6. [ ] Write integration tests

## Acceptance Criteria

- [ ] 30GB tier disponível
- [ ] 100GB enterprise tier disponível
- [ ] Storage tracking funciona
- [ ] Tiered pricing funciona
- [ ] Auto-cleanup policies work
- [ ] Tests: 85% coverage

## Dependencies

- FASE 3: Workspaces
- Storage: 5GB (FASE 3)