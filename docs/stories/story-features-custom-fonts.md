# Story: Custom Fonts
- **Epic:** epic-features.md
- **Fase:** FASE 1 - Essentials
- **Priority:** P1
- **Estimate:** 8h

## Problem
Usuários querem usar fontes personalizadas para manter consistent brand identity.

## Solution
Adicionar font upload e selection via interface.

## Scope
- In: TTF/OTF font files
- Out: Custom font applied to captions

## Tasks
- [ ] Add font upload endpoint
- [ ] Create font management UI
- [ ] Implement font caching
- [ ] Add fallback fonts handling

## Acceptance Criteria
- [ ] Upload custom TTF/OTF fonts
- [ ] Select from uploaded fonts
- [ ] Apply custom font to captions
- [ ] Show font preview

## Dependencies
- Caption renderer (backend/src/services/renderer.py)