# Story: Per-User Usage Tracking

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P3
- **Estimate:** 16h

## Problem

Workspaces precisam de tracking de usage por usuário para billing granular e analytics. Usage tracking atual é por workspace.

## Solution

Implementar per-user usage tracking:
- Per-user minute tracking
- Per-user feature tracking
- Usage breakdown UI
- Export reports
- Alert thresholds

## Scope

- In: Usage events
- Out: Per-user usage data

## Tasks

1. [ ] Implement per-user tracking
2. [ ] Add feature-level tracking
3. [ ] Create usage breakdown UI
4. [ ] Add export reports
5. [ ] Implement alert thresholds
6. [ ] Write integration tests

## Acceptance Criteria

- [ ] Per-user tracking funciona
- [ ] Feature-level breakdown
- [ ] Usage UI disponível
- [ ] Export reports work
- [ ] Alert thresholds work
- [ ] Tests: 90% coverage

## Dependencies

- FASE 2: Transparent billing
- FASE 3: Workspaces, Team seats
- Usage tracking (existing, per-workspace)