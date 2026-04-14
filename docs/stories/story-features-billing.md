# Story: Transparent Per-Minute Billing

- **Epic:** epic-features.md
- **Fase:** FASE 2 - Differentiation
- **Priority:** P1
- **Estimate:** 32h

## Problem

Usuários não têm visibilidade clara de quanto estão gastando. Planos fixos mensais criam friction para novos usuários e pricing opaco. Concorrentes como OpusClip usam pricing fixo ($19/mo ou $49/mo) sem transparência de minutos usados.

O SupoClip pode diferenciar com billing pay-per-minute mais visível, permitindo usuários pagarem apenas pelo que usam.

## Solution

Implementar sistema de billing transparente que mostra:
1. Minutos processados no período atual
2. Crédito restante do plano mensal
3. Histórico detalhado de uso por vídeo
4. Alertas quando atingir 80% e 100% do limite
5. Opção de rollover de minutos não usado

## Scope

- **In:** Vídeos processados via worker
- **Out:** Credit packs (FASE 3), Annual billing (FASE 3)

## Tasks

1. [ ] Database schema para billing_records
2. [ ] API para tracked minutes por user
3. [ ] UI Dashboard mostrando uso atual
4. [ ] Alertas threshold (80%, 100%)
5. [ ] Historico de uso detalhado
6. [ ] Integracao com Stripe para billing
7. [ ] Plan selection UI (starter/pro/annual)

## Acceptance Criteria

- [ ] Dashboard mostra minutos usados este mês
- [ ] Histórico de uso por vídeo visível
- [ ] Alerta aos 80% do limite
- [ ] Bloqueio ao atingir 100% (ou upgrade prompt)
- [ ] Lista de invoices disponível
- [ ] Plan upgrade/downgrade funcional

## Dependencies

- Stripe integration
- User authentication (story-security-critical.md)

---

*Story ID: FEATURES-BILLING*
*Created: 2026-04-14*