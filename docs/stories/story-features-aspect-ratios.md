# Story: Multiple Aspect Ratios
- **Epic:** epic-features.md
- **Fase:** FASE 1 - Essentials
- **Priority:** P0
- **Estimate:** 8h

## Problem
Usuários precisam exportar em diferentes formatos para plataformas distintas (YouTube, Instagram, TikTok).

## Solution
Adicionar suporte a múltiplas aspect ratios com crop inteligente.

## Scope
- In: Source video
- Out: Video export em 16:9, 1:1, ou 4:5

## Tasks
- [ ] Add aspect ratio selection to export UI
- [ ] Implement smart crop algorithm
- [ ] Add center-focused crop option
- [ ] Add face-detection crop option

## Acceptance Criteria
- [ ] Export 16:9 (YouTube)
- [ ] Export 1:1 (Instagram Feed)
- [ ] Export 4:5 (Instagram/TikTok)
- [ ] Preserve quality after crop

## Dependencies
- Video processing (backend/src/services/renderer.py)