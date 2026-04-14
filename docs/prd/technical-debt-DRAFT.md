# Technical Debt Assessment - DRAFT

**Projeto:** SupoClip  
**Data:** 2026-04-14  
**Versão:** DRAFT v1.0  
**Autor:** @architect (Aria) — FASE 4 Brownfield Discovery

---

## Executive Summary

O SupoClip apresenta **54 débitos técnicos consolidados** nas áreas de sistema, banco de dados e frontend/UX, totalizando **~268.5 horas** de esforço estimado para correção completa. A análise foi baseada nos documentos das Fases 1-3 do workflow brownfield-discovery.

### Principais Achados

- **18 débitos de sistema** (SYS-001 a SYS-018): Testes automatizados ausentes, código legado, segurança, observabilidade
- **31 débitos de database** (DB-001 a DB-031): RLS ausente, índices faltantes, normalização, versionamento de migrations
- **10 débitos de frontend/UX** (UX-001 a UX-010): Server Components não utilizados, acessibilidade, estados inconsistentes

### Priorização Consolidada

| Prioridade | Quantidade | Esforço Total |
|------------|------------|---------------|
| P0 (Crítico) | 8 débitos | ~80h |
| P1 (Alto) | 20 débitos | ~96h |
| P2 (Médio) | 18 débitos | ~52h |
| P3 (Baixo) | 8 débitos | ~40h |

###战力⚠️ Seções para Validação

Este DRAFT requer validação especializada nas seguintes áreas:
- **Database**: @data-engineer (Dara) - para débitos DB-*, especialmente RLS e normalização
- **Frontend/UX**: @ux-design-expert (Uma) - para débitos UX-* e priorização
- **QA**: Validação de cobertura de testes proposta (SYS-001)

---

## Débitos por Área

### 1. Débitos de Sistema (18)

| ID | Débito | Área | Impacto | Esforço | Prioridade |
|----|--------|------|---------|---------|------------|
| SYS-001 | Ausência total de testes automatizados | Quality | Crítico | 40h | P0 |
| SYS-002 | Dupla fonte de schema (Prisma + init.sql + SQLAlchemy) | Database | Alto | 16h | P1 |
| SYS-003 | Arquivos legados não removidos (main.py, código comentado) | Maintainability | Médio | 4h | P2 |
| SYS-004 | Hardcoded defaults em múltiplos locais (font_family, font_size) | Config | Médio | 8h | P2 |
| SYS-005 | Pool de Redis não configurado (sem max_connections) | Performance | Médio | 4h | P2 |
| SYS-006 | Error handling inconsistente (exceptions genéricas em services) | Quality | Alto | 12h | P1 |
| SYS-007 | Falta de rate limiting na API pública | Security | Alto | 8h | P1 |
| SYS-008 | Credenciais hardcoded no init.sql (postgres password) | Security | Alto | 2h | P1 |
| SYS-009 | Logging sem campos estruturados | Observability | Baixo | 8h | P2 |
| SYS-010 | Ausência de graceful shutdown no worker | Reliability | Médio | 4h | P2 |
| SYS-011 | 132+ cláusulas except sem logging adequado | Quality/Security | Alto | 16h | P1 |
| SYS-012 | Variáveis de ambiente não validadas no startup | Config | Alto | 6h | P1 |
| SYS-013 | Dead code em video_utils.py (código comentado) | Maintainability | Baixo | 2h | P2 |
| SYS-014 | Queries SQL não parametrizadas (concatenação em alguns casos) | Security | Alto | 8h | P1 |
| SYS-015 | Falta de índice em generated_clips.virality_score | Performance | Baixo | 1h | P2 |
| SYS-016 | Dockerfile sem multi-stage build | DevOps | Médio | 4h | P2 |
| SYS-017 | Código duplicado em main.py e main_refactored.py | Maintainability | Alto | 8h | P1 |
| SYS-018 | Processamento síncrono em asyncio.create_task (sem await) | Reliability | Alto | 4h | P1 |

**Subtotal Sistema:** 155h

---

### 2. Débitos de Database (31)

| ID | Débito | Área | Severidade | Esforço | Prioridade |
|-----|---------|------|------------|---------|------------|
| DB-001 | Tabela `verification` sem índice em `value` | Auth | MEDIA | 1h | P2 |
| DB-002 | `session` sem índice em `expiresAt` | Auth | ALTA | 1h | P1 |
| DB-003 | `generated_clips_ids` em tasks é array não normalizado | Tasks | ALTA | 4h | P1 |
| DB-004 | Falta índice em `tasks(user_id, status)` | Tasks | MEDIA | 1h | P2 |
| DB-005 | Falta índice em `tasks(user_id, created_at DESC)` | Tasks | MEDIA | 1h | P2 |
| DB-006 | Campo `error_code` sem CHECK constraint | Tasks | BAIXA | 1h | P3 |
| DB-007 | `status` sem CHECK constraint | Tasks | BAIXA | 1h | P3 |
| DB-008 | `processing_mode` sem CHECK constraint | Tasks | BAIXA | 1h | P3 |
| DB-009 | `start_time`/`end_time` como VARCHAR em vez de segundos | Clips | MEDIA | 2h | P2 |
| DB-010 | Falta índice em `generated_clips(task_id, clip_order)` | Clips | BAIXA | 1h | P3 |
| DB-011 | Falta índice em `generated_clips(virality_score DESC)` | Clips | BAIXA | 1h | P3 |
| DB-012 | `sources` sem índice em `type` | Sources | MEDIA | 1h | P2 |
| DB-013 | `sources` sem FK para users (problema de design) | Sources | ALTA | 2h | P1 |
| DB-014 | `processing_cache` sem trigger `updated_at` | Cache | BAIXA | 1h | P3 |
| DB-015 | Falta índice em `processing_cache(source_type, created_at)` | Cache | BAIXA | 1h | P3 |
| DB-016 | Sem TTL automático para cache | Cache | ALTA | 4h | P1 |
| DB-017 | `stripe_webhook_events` sem índice em `created_at` | Billing | MEDIA | 1h | P2 |
| DB-018 | `stripe_webhook_events` sem índice em `type` | Billing | BAIXA | 1h | P3 |
| DB-019 | Sem tabela de rate limiting/limites por usuário | Billing | ALTA | 8h | P0 |
| DB-020 | `account` sem constraint UNIQUE em (providerId, accountId) | Constraints | ALTA | 2h | P1 |
| DB-021 | `account.providerId` e `account.accountId` sem índices | Constraints | MEDIA | 1h | P2 |
| DB-022 | `verification` sem constraint UNIQUE em (identifier, value) | Constraints | MEDIA | 2h | P2 |
| DB-023 | Queries N+1 em "buscar tasks do usuário com clips" | Performance | ALTA | 4h | P1 |
| DB-024 | Sem covering indexes para queries comuns | Performance | MEDIA | 2h | P2 |
| DB-025 | `processing_cache` sem partition por source_type | Performance | MEDIA | 4h | P2 |
| DB-026 | `users.plan` e `users.subscription_status` sem CHECK constraint | Schema | BAIXA | 1h | P3 |
| DB-027 | Inconsistência nomenclatura: camelCase vs snake_case | Schema | BAIXA | 8h | P3 |
| DB-028 | `users.caption_template` não existe mas referenciado | Schema | MEDIA | 2h | P2 |
| DB-029 | Sem políticas RLS em nenhuma tabela | RLS | CRITICA | 8h | P0 |
| DB-030 | Sem políticas RLS para `sources` | RLS | CRITICA | 4h | P0 |
| DB-031 | Sem políticas RLS para `generated_clips` | RLS | CRITICA | 4h | P0 |

**Subtotal Database:** 92h

---

### 3. Débitos de Frontend/UX (10)

| ID | Débito | Área | Severidade | Esforço | Prioridade |
|-----|---------|------|------------|---------|------------|
| UX-001 | Quase todas as páginas com "use client" — sem Server Components | Performance | MEDIA | 2h | Alta |
| UX-002 | Inconsistent loading states — task edit não tem skeleton | UX | BAIXA | 1h | Média |
| UX-003 | Empty state faltando em task edit page | UX | BAIXA | 1h | Média |
| UX-004 | Botões icon sem aria-label (edit, delete clip) | A11y | MEDIA | 2h | Alta |
| UX-005 | Phone preview hidden em mobile | UX | BAIXA | 0.5h | Baixa |
| UX-006 | Color contrast stone-500 em backgrounds claros | A11y | MEDIA | 2h | Alta |
| UX-007 | Inconsistent button styles entre páginas | UX | BAIXA | 1h | Média |
| UX-008 | Error handling direto com alert() | UX | MEDIA | 1h | Média |
| UX-009 | Direct fetch calls sem loading robusto | UX | BAIXA | 1h | Média |
| UX-010 | Landing page heavy em client-side animations | Performance | MEDIA | 1h | Baixa |

**Subtotal Frontend/UX:** 11.5h

---

## Matriz Consolidada

### Por Severidade

| Severidade | Quantidade | Esforço |
|------------|------------|----------|
| CRITICA | 4 débitos | 24h |
| ALTA | 20 débitos | 96h |
| MEDIA | 22 débitos | 76.5h |
| BAIXA | 8 d��bitos | 72h |

### Top 10 Débitos Priorizados

| Rank | ID | Débito | Severidade | Esforço |
|------|-----|---------|------------|----------|
| 1 | SYS-001 | Ausência total de testes automatizados | CRITICA | 40h |
| 2 | DB-029 | Sem políticas RLS em nenhuma tabela | CRITICA | 8h |
| 3 | DB-030 | Sem políticas RLS para sources | CRITICA | 4h |
| 4 | DB-031 | Sem políticas RLS para generated_clips | CRITICA | 4h |
| 5 | DB-019 | Sem tabela de rate limiting/limites | CRITICA | 8h |
| 6 | SYS-011 | 132+ cláusulas except sem logging | ALTA | 16h |
| 7 | SYS-002 | Dupla fonte de schema | ALTA | 16h |
| 8 | SYS-006 | Error handling inconsistente | ALTA | 12h |
| 9 | DB-003 | generated_clips_ids não normalizado | ALTA | 4h |
| 10 | DB-023 | Queries N+1 em tasks+clips | ALTA | 4h |

---

## Perguntas para Especialistas

### @data-engineer (Dara)

1. **DB-029, DB-030, DB-031 (RLS)**: Qual a melhor abordagem para implementar RLS considerando o Supabase Pooler? Há impacto em queries existentes?
2. **DB-003 (Normalização)**: O array `generated_clips_ids` pode ser removido com безопасa? Qual o risco de breaking changes?
3. **DB-019 (Rate Limiting)**: A tabela提议adaé adequada para workers distribuídos? Há padrões específicos do Supabase?
4. **DB-027 (Nomenclatura)**: Vale a pena migrar tudo para snake_case ou é só padronizar going forward?
5. **DB-023 (N+1)**: O JOIN existente cobre esse problema ou precisa de novo índice?

### @ux-design-expert (Uma)

1. **UX-001 (Server Components)**: Quais páginas são candidatas viáveis para migração? Qual o impacto estimado?
2. **UX-004 (Aria Labels)**: Precisamos de uma convenção统一的 para labels?
3. **UX-006 (Color Contrast)**: A revisão de cores proposta atende WCAG AA? Quais tokens específico precisam change?
4. **UX-002, UX-003 (Empty/Loading States)**: Devem ser componentes reutilizáveis ou inline?
5. **UX-007 (Button Styles)**: Devemser tokens CSS ou variants de Button component?

### @qa

1. **SYS-001 (Testes)**: Qual a cobertura mínima recomendada (40% como no documento)?
2. **SYS-001**: Quais paths/core são priority para primeiros testes?
3. **SYS-011 (Exceptions)**: Como priorizar o audit das 132+ cláusulas?
4. **Há testes de integração ou E2E planejados?** Devemos include no escopo?

---

## Próximos Passos

### FASE 5: Validação Database (@data-engineer)
- Revisar débitos DB-001 a DB-031
- Confirmar/ajustar estimativas e priorização
- Propor soluções técnicas

### FASE 6: Validação UX (@ux-design-expert)
- Revisar débitos UX-001 a UX-010
- Validar viabilidade de Server Components
- Confirmar revisão de cores e acessibilidade

### FASE 7: Validação QA (@qa)
- Validar proposta de cobertura de testes
- Identificar testes críticos para P0s

### FASE 8: Revisão Final
- Consolidar feedback dos especialistas
- Gerar versão final do documento
- Definir roadmap de correção

---

## Notas

- **Total consolidado**: 54 débitos, ~268.5h estimadas
- **Fonte dos dados**:
  - Sistema: `docs/architecture/system-architecture.md` (18 SYS-*)
  - Database: `docs/architecture/db-audit.md` (31 DB-*)
  - Frontend: `docs/frontend/frontend-spec.md` (10 UX-*)
- **Débito IDs renumerados** de DB-AUTH-*, DB-TASK-* etc. para DB-001 a DB-031 sequencialmente
- **Estimativas de esforço** são aproximações inicials e sujeitas a ajuste após validação

---

*Documento gerado por @architect (Aria) — FASE 4 Brownfield Discovery*  
*Próxima fase: Validação especializada (FASES 5-7)*