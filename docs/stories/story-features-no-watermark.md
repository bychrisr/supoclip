# Story: No Watermark for Logged Users
- **Epic:** epic-features.md
- **Fase:** FASE 1 - Essentials
- **Priority:** P1
- **Estimate:** 2h

## Problem
Usuários logados precisam exportar sem watermark para uso profissional.

## Solution
Remover watermark automaticamente para usuários autenticados.

## Scope
- In: User authentication status
- Out: MP4 sem watermark (se logged)

## Tasks
- [ ] Check user auth status before render
- [ ] Remove watermark conditional logic
- [ ] Test with free tier users
- [ ] Test with paid tier users

## Acceptance Criteria
- [ ] Free users: output com watermark
- [ ] Logged free users: output com watermark
- [ ] Logged paid users: output sem watermark
- [ ] Watermark removed only in final export

## Dependencies
- Video export (backend/src/services/renderer.py)
- Authentication (frontend/src/lib/auth.ts)