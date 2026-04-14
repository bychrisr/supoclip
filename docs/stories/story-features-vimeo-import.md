# Story: Vimeo Import

- **Epic:** epic-features.md
- **Fase:** FASE 2 - Differentiation
- **Priority:** P2
- **Estimate:** 12h

## Problem

Vimeo é usado por criadores profissionais e empresas para hospedagem de vídeos. Importar diretamente do Vimeo evita download manual.

## Solution

Implementar integrationcom Vimeo API para:
1. OAuth com Vimeo
2. List videos da conta Vimeo
3. Import direto para processamento

## Scope

- **In:** Vimeo video URLs
- **Out:** Direct upload from Vimeo

## Tasks

1. [ ] Vimeo Developer app setup
2. [ ] Vimeo OAuth integration
3. [ ] Video list API call
4. [ ] Import flow UI

## Acceptance Criteria

- [ ] Botão "Import from Vimeo"
- [ ] OAuth flow com Vimeo
- [ ] Lista de vídeos do Vimeo
- [ ] Import direto funciona

## Dependencies

- Vimeo Developer API
- OAuth base

---

*Story ID: FEATURES-VIMEO-IMPORT*
*Created: 2026-04-14*