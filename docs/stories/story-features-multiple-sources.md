# Story: Multiple Video Sources Integration

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P2
- **Estimate:** 40h

## Problem

Usuários usam diversas plataformas de video (Zoom, Rumble, Twitch, etc) mas import é limitado a YouTube/File. Expandir sources é diferencial.

## Solution

Implementar multiple video sources:
- Zoom API integration
- Rumble API integration
- Twitch VOD import
- Riverside FM integration
- Frame.io integration
- StreamYard integration
- Universal import adapter

## Scope

- In: External platform video URL
- Out: Imported video

## Tasks

1. [ ] Implement Zoom API integration
2. [ ] Implement Rumble API integration
3. [ ] Implement Twitch VOD import
4. [ ] Implement Riverside FM import
5. [ ] Implement Frame.io import
6. [ ] Implement StreamYard import
7. [ ] Create universal import adapter
8. [ ] Write integration tests

## Acceptance Criteria

- [ ] Zoom import funciona
- [ ] Rumble import funciona
- [ ] Twitch VOD import funciona
- [ ] Riverside FM import funciona
- [ ] Frame.io import funciona
- [ ] StreamYard import funciona
- [ ] Tests: 85% coverage

## Dependencies

- Zoom API
- Rumble API
- Twitch API
- Riverside FM API
- Frame.io API
- StreamYard API
- FASE 2: Google Drive, Vimeo, Loom imports