# Story: Animated Captions
- **Epic:** epic-features.md
- **Fase:** FASE 1 - Essentials
- **Priority:** P0
- **Estimate:** 16h

## Problem
Usuários querem legendas animadas que se movam com a fala, similar ao OpusClip.

## Solution
Implementar caption renderer com animation support usando MoviePy.

## Scope
- In: Caption text + timing from AssemblyAI
- Out: Animated MP4 with moving captions

## Tasks
- [ ] Research MoviePy animation patterns
- [ ] Create caption renderer with animation
- [ ] Create 3+ animation templates
- [ ] Add animation selection UI

## Acceptance Criteria
- [ ] Render animated captions
- [ ] 3+ animation styles
- [ ] Preview in UI

## Dependencies
- Caption renderer (backend/src/services/renderer.py)