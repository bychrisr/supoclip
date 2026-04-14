# Story: Webhook Event System

- **Epic:** epic-features.md
- **Fase:** FASE 2 - Differentiation
- **Priority:** P1
- **Estimate:** 24h

## Problem

Usuários avançados e agencies precisam de automações baseadas em eventos do processamento. API consumers precisam de notifications quando jobs completam. Sem webhooks, usuários precisam poll a API manualmente.

## Solution

Implementar sistema de webhooks que dispara eventos quando:
1. Video uploaded
2. Processing started
3. Processing completed (success)
4. Processing failed (error)
5. Clip generated
6. User sign up / sign in

## Scope

- **In:** Worker job events
- **Out:** Custom webhook payloads (FASE 4)

## Tasks

1. [ ] Database schema para webhooks
2. [ ] Webhook CRUD endpoints
3. [ ] Event dispatcher no worker
4. [ ] Retry logic (exponential backoff)
5. [ ] Webhook logs UI
6. [ ] Signature verification (HMAC)
7. [ ] Test webhook UI

## Acceptance Criteria

- [ ] Usuário pode criar webhook URL
- [ ] Webhook dispara em events configurados
- [ ] Retry ate 3x em failure
- [ ] Signature header para verificacao
- [ ] Webhook delivery logs visivel
- [ ] Enable/disable individual webhooks

## Dependencies

- API-first story (story-features-api-first.md)
- Worker events

---

*Story ID: FEATURES-WEBHOOKS*
*Created: 2026-04-14*