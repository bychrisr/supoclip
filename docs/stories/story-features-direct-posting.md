# Story: Direct Social Posting via OAuth

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P2
- **Estimate:** 48h

## Problem

Usuários precisam postar clips diretamente nas redes sociais sem download manual. OAuth integration multiplica eficiência.

## Solution

Implementar direct social posting:
- OAuth integration com TikTok, Instagram, YouTube, LinkedIn
- Direct upload API
- Platform-specific formatting
- Scheduling integration
- Post analytics

## Scope

- In: Processed clip + OAuth tokens
- Out: Published post

## Tasks

1. [ ] Implement TikTok OAuth
2. [ ] Implement Instagram OAuth
3. [ ] Implement YouTube OAuth
4. [ ] Implement LinkedIn OAuth
5. [ ] Create direct upload API
6. [ ] Add platform-specific formatting
7. [ ] Integrate with scheduler
8. [ ] Add post analytics
9. [ ] Write integration tests

## Acceptance Criteria

- [ ] OAuth flow para todas plataformas
- [ ] Direct upload funciona
- [ ] Platform-specific formatting
- [ ] Scheduler integration
- [ ] Post analytics
- [ ] Tests: 80% coverage

## Dependencies

- TikTok API
- Instagram API
- YouTube API
- LinkedIn API
- FASE 2: Social scheduler