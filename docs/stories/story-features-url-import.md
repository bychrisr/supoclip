# Story: Public URL Import

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P3
- **Estimate:** 12h

## Problem

Usuários precisam importar videos via URL pública (S3, Cloudflare Stream, etc) além de YouTube/Vimeo. URL import é mais flexível.

## Solution

Implementar public URL import:
- URL validation e fetch
- Support S3 presigned URLs
- Support Cloudflare Stream URLs
- Support any public MP4 URL
- Direct download to processing

## Scope

- In: Public video URL
- Out: Imported video

## Tasks

1. [ ] Implement URL validator
2. [ ] Add S3 presigned URL support
3. [ ] Add Cloudflare Stream support
4. [ ] Add generic URL fetch
5. [ ] Implement direct download
6. [ ] Write integration tests

## Acceptance Criteria

- [ ] S3 presigned URL funciona
- [ ] Cloudflare Stream funciona
- [ ] Generic URL fetch funciona
- [ ] Auto-conversion para processable format
- [ ] Tests: 90% coverage

## Dependencies

- FASE 2: Google Drive, Vimeo, Loom imports
- S3 or local storage