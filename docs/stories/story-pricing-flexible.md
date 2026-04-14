# Story: Flexible & Transparent Pricing

## Problem

**Nenhum concorrente cobra de forma transparente:**
- **OpusClip**: Créditos opacos — usuário não sabe quanto custa 1 vídeo
- **Real Oficial**: Créditos também — 600 créditos = ~10h mas não é claro
- **VidRush**: Per-minute mas sem transparência de quanto custa cada vídeo

O modelo de créditos é anti-pattern: usuário não sabe o custo real por vídeo, gera desconfiança. Ssemble证明了 per-video pricing é 3-4x melhor valor para usuário.

## Solution

Implementar pricing transparente por minuto de vídeo processado:
- Preço claro por minuto de source video
- Não créditos opacos
- Per-video option para usuários que processam vídeos longos
- Annual billing com desconto

## Competitor Reference

- **Ssemble**: Per-video pricing ($0.25/video), API em todos os planos
- **OpusClip**: Per-minute via créditos ($0.048/credit = ~$0.048/min)
- **Reap**: Per-minute também
- **OpusClip annual**: 17% discount

## Scope

### In
- Pricing por minuto de vídeo processado
- Per-video pricing option
- Free tier: 60 min/mês (sem cartão)
- Planos: Starter ($9.90), Creator ($19.90), Pro ($39.90)
- Annual billing com 20% discount
- Billing dashboard showing usage
- Usage alerts (email quando atinge 80%, 100%)

### Out
- Pay-per-use avulso — apenas planos
- Credits pack avulso — fase 2
- Enterprise custom — fase 2

## Tasks

1. **Pricing Structure**
   - Definir preços por minuto
   - Definir limites por plano
   - Calcular annual discount
   - Documentar pricing page

2. **Billing Implementation**
   - Track minutos processados por user
   - Implementar hard limit (bloqueia ao atingir limite)
   - Implementar soft limit (avisa em 80%)
   - Billing cycle (mensal)

3. **Usage Dashboard**
   - Mostrar minutos usados vs limite
   - Histórico de uso por mês
   - Gráfico de tendências

4. **Payment Integration**
   - Stripe checkout
   - Subscription management
   - Invoice generation
   - Cancel flow

5. **Free Tier Logic**
   - 60 min/mês sem cartão
   - Watermark no free tier
   - Upgrade CTA

## Acceptance Criteria

- [ ] Pricing page mostra preço por minuto claramente
- [ ] Usuário sabe custo exato de cada vídeo antes de processar
- [ ] Free tier: 60 min/mês, 1080p, watermark
- [ ] Starter: $9.90/mo, 300 min, sem watermark
- [ ] Creator: $19.90/mo, 1,000 min, includes API basic
- [ ] Pro: $39.90/mo, unlimited min, full API
- [ ] Annual: 20% discount
- [ ] Dashboard mostra minutos usados
- [ ] Alerta em 80% do limite
- [ ] Bloqueio em 100% do limite
- [ ] Cancel flow funcional

## Effort Estimate

**40 horas**
- Pricing Design: 4h
- Billing Implementation: 16h
- Usage Dashboard: 8h
- Payment Integration: 8h
- Testing: 4h

## Priority

**P0** — Fundamental para monetização. Pricing transparente é difercial vs OpusClip.

---

*Story ID: PRICING-FLEXIBLE*
*Created: 2026-04-14*