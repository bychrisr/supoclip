# Story: API-First Platform

## Problem

Nenhum concorrente oferece API pública de forma acessível:
- **OpusClip**: API em closed-beta, apenas para planos Business (custom pricing)
- **Real Oficial**: Sem API
- **Ssemble**: API disponível em todos os planos ($7.50/mo)

O SupoClip tem oportunidade de ser **API-first desde o dia 1**, posicionando-se como plataforma para desenvolvedores, agencies e integrações customizadas. Isso cria moat defensivo e revenue stream B2B.

## Solution

Expor APIs RESTful públicas para as operações core do clipping, com autenticação via API keys e billing pay-per-use. API-first significa que o produto web usa as mesmas APIs que consumidores externos.

## Competitor Reference

- **Ssemble**: API disponível em todos os planos, pricing claro
- **OpusClip**: API closed-beta, só para Enterprise
- **Vizard**: Sem API pública documentada

## Scope

### In
- REST API para upload de vídeo
- REST API para iniciar processamento de clipping
- REST API para listar e baixar clips gerados
- API key management (criar, revogar, listar)
- API usage tracking (calls, minutos processados)
- Rate limiting por tier
- Documentação pública (OpenAPI/Swagger)
- Webhooks para notifications de processamento

### Out
- SDKs oficiais (Node, Python) — fase 2
- GraphQL — fase 2
- SSO/SAML para API — fase 2
- API playground/studio — fase 2

## Tasks

1. **API Design**
   - Definir endpoints REST (upload, process, list, download)
   - Definir schema de responses
   - Definir error codes

2. **API Implementation**
   - Implementar endpoints em FastAPI
   - Adicionar autenticação API key
   - Implementar rate limiting
   - Adicionar webhook delivery

3. **API Key Management**
   - Criar UI para gerar/revogar API keys
   - Criar dashboard de usage por key

4. **API Documentation**
   - Gerar OpenAPI spec
   - Criar docs no estilo Vercel/Stripe

5. **Billing Integration**
   - Track API usage por user
   - Integrar com billing system

## Acceptance Criteria

- [ ] POST /api/v1/videos — upload, retorna video_id
- [ ] POST /api/v1/clips — cria job, retorna job_id
- [ ] GET /api/v1/clips/{job_id} — status do job
- [ ] GET /api/v1/clips — lista clips do usuário
- [ ] GET /api/v1/clips/{clip_id}/download — baixa clip
- [ ] API keys podem ser criadas e revocadas via UI
- [ ] Rate limiting: 100 req/min (starter), unlimited (pro)
- [ ] Webhooks dispara event quando clip Pronto
- [ ] Documentação OpenAPI disponível em /docs/api
- [ ] API keys visíveis apenas no momento da criação

## Effort Estimate

**45 horas**
- API Design: 8h
- API Implementation: 20h
- API Key Management: 5h
- Documentation: 4h
- Webhooks: 4h
- Testing: 4h

## Priority

**P1** — Diferencial competitivo forte, revenue B2B, pode attract agencies early.

---

*Story ID: FEATURES-API-FIRST*
*Created: 2026-04-14*