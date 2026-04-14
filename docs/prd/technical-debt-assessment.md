# Technical Debt Assessment - FINAL

**Projeto:** SupoClip  
**Data:** 2026-04-14  
**Versão:** 1.0 FINAL  
**Autor:** @architect (Aria) — FASE 8 Brownfield Discovery

---

## Executive Summary

O SupoClip apresenta **72 débitos técnicos consolidados** nas áreas de sistema, banco de dados e frontend/UX, totalizando **~335.5 horas** de esforço estimado para correção completa.

### Consolidação de Revisões

| Área | Original | Ajustes | Adicionados | Removidos | Final |
|------|----------|---------|-------------|------------|-------|
| Sistema (SYS-*) | 18 | 0 | 6 (gaps QA) | 0 | **24** |
| Database (DB-*) | 31 | 4 | 3 | 2 | **32** |
| Frontend/UX (UX-*) | 10 | 4 | 5 | 1 | **14** |
| **TOTAL** | **59** | **8** | **14** | **3** | **72** |

### Distribuição por Severidade

| Severidade | Quantidade | Esforço |
|------------|------------|----------|
| CRÍTICA | 6 débitos | 40h |
| ALTA | 24 débitos | 120h |
| MÉDIA | 26 débitos | 103h |
| BAIXA | 16 débitos | 72.5h |

### Distribuição por Prioridade

| Prioridade | Quantidade | Esforço |
|------------|------------|----------|
| P0 (Crítico) | 10 débitos | ~72h |
| P1 (Alto) | 22 débitos | ~112h |
| P2 (Médio) | 26 débitos | ~95.5h |
| P3 (Baixo) | 14 débitos | ~56h |

---

## Débitos Validados por Área

### 1. Débitos de Sistema (24)

*Validados por @architect - FASE 4*

| ID | Débito | Severidade | Horas | Prioridade | Status |
|----|--------|------------|-------|------------|--------|
| SYS-001 | Ausência total de testes automatizados | CRÍTICA | 40h | P0 | VALIDADO |
| SYS-002 | Dupla fonte de schema (Prisma + init.sql + SQLAlchemy) | ALTA | 16h | P1 | VALIDADO |
| SYS-003 | Arquivos legados não removidos (main.py, código comentado) | MÉDIA | 4h | P2 | VALIDADO |
| SYS-004 | Hardcoded defaults em múltiplos locais (font_family, font_size) | MÉDIA | 8h | P2 | VALIDADO |
| SYS-005 | Pool de Redis não configurado (sem max_connections) | MÉDIA | 4h | P2 | VALIDADO |
| SYS-006 | Error handling inconsistente (exceptions genéricas em services) | ALTA | 12h | P1 | VALIDADO |
| SYS-007 | Falta de rate limiting na API pública | ALTA | 8h | P1 | VALIDADO |
| SYS-008 | Credenciais hardcoded no init.sql (postgres password) | ALTA | 2h | P1 | VALIDADO |
| SYS-009 | Logging sem campos estruturados | BAIXA | 8h | P2 | VALIDADO |
| SYS-010 | Ausência de graceful shutdown no worker | MÉDIA | 4h | P2 | VALIDADO |
| SYS-011 | 132+ cláusulas except sem logging adequado | ALTA | 16h | P1 | VALIDADO |
| SYS-012 | Variáveis de ambiente não validadas no startup | ALTA | 6h | P1 | VALIDADO |
| SYS-013 | Dead code em video_utils.py (código comentado) | BAIXA | 2h | P2 | VALIDADO |
| SYS-014 | Queries SQL não parametrizadas (concatenação em alguns casos) | ALTA | 8h | P1 | VALIDADO |
| SYS-015 | Falta de índice em generated_clips.virality_score | BAIXA | 1h | P2 | VALIDADO |
| SYS-016 | Dockerfile sem multi-stage build | MÉDIA | 4h | P2 | VALIDADO |
| SYS-017 | Código duplicado em main.py e main_refactored.py | ALTA | 8h | P1 | VALIDADO |
| SYS-018 | Processamento síncrono em asyncio.create_task (sem await) | ALTA | 4h | P1 | VALIDADO |

*Adicionados por QA (FASE 7) - Débitos Operacionais*

| ID | Débito | Severidade | Horas | Prioridade | Status |
|----|--------|------------|-------|------------|--------|
| SYS-019 | CI/CD Pipeline ausente | ALTA | 8h | P1 | ADICIONADO QA |
| SYS-020 | Monitoring/Alerting ausente | MÉDIA | 8h | P2 | ADICIONADO QA |
| SYS-021 | Backup/Disaster Recovery não documentado | CRÍTICA | 8h | P0 | ADICIONADO QA |
| SYS-022 | API Documentation ausente | MÉDIA | 4h | P2 | ADICIONADO QA |
| SYS-023 | Data Retention Policy ausente | MÉDIA | 4h | P2 | ADICIONADO QA |
| SYS-024 | Security Headers ausentes (CSP, X-Frame-Options, HSTS) | ALTA | 4h | P1 | ADICIONADO QA |

**Subtotal Sistema:** 179h

---

### 2. Débitos de Database (32)

*Validados por @data-engineer - FASE 5*

| ID | Débito | Severidade | Horas | Prioridade | Status |
|-----|---------|------------|---------|------------|--------|
| DB-001 | Tabela `verification` sem índice em `value` | MÉDIA | 1h | P2 | VALIDADO |
| DB-002 | `session` sem índice em `expiresAt` | ALTA | 1h | P1 | VALIDADO |
| DB-003 | `generated_clips_ids` em tasks é array não normalizado | MÉDIA | 4h | P2 | AJUSTADO (P1→P2) |
| DB-004 | Falta índice em `tasks(user_id, status)` | MÉDIA | 1h | P2 | VALIDADO |
| DB-005 | Falta índice em `tasks(user_id, created_at DESC)` | MÉDIA | 1h | P2 | VALIDADO |
| DB-006 | Campo `error_code` sem CHECK constraint | BAIXA | 1h | P3 | VALIDADO |
| DB-007 | `status` sem CHECK constraint | BAIXA | 1h | P3 | VALIDADO |
| DB-008 | `processing_mode` sem CHECK constraint | BAIXA | 1h | P3 | VALIDADO |
| DB-009 | `start_time`/`end_time` como VARCHAR em vez de segundos | MÉDIA | 2h | P2 | VALIDADO |
| DB-010 | Falta índice em `generated_clips(task_id, clip_order)` | BAIXA | 1h | P3 | AJUSTADO |
| DB-011 | Falta índice em `generated_clips(virality_score DESC)` | BAIXA | 1h | P3 | VALIDADO |
| DB-012 | `sources` sem índice em `type` | MÉDIA | 1h | P2 | VALIDADO |
| DB-013 | `sources` sem FK para users (problema de design) | ALTA | 2h | P1 | VALIDADO |
| DB-014 | `processing_cache` sem trigger `updated_at` | BAIXA | 1h | P3 | VALIDADO |
| DB-015 | Falta índice em `processing_cache(source_type, created_at)` | BAIXA | 1h | P3 | VALIDADO |
| DB-016 | Sem TTL automático para cache | ALTA | 4h | P1 | VALIDADO |
| DB-017 | `stripe_webhook_events` sem índice em `created_at` | MÉDIA | 1h | P2 | VALIDADO |
| DB-018 | `stripe_webhook_events` sem índice em `type` | BAIXA | 1h | P3 | VALIDADO |
| DB-019 | Sem tabela de rate limiting/limites por usuário | CRÍTICA | 8h | P0 | VALIDADO |
| DB-020 | `account` sem constraint UNIQUE em (providerId, accountId) | ALTA | 2h | P1 | VALIDADO |
| DB-021 | `account.providerId` e `account.accountId` sem índices | MÉDIA | 1h | P2 | VALIDADO |
| DB-022 | `verification` sem constraint UNIQUE em (identifier, value) | MÉDIA | 2h | P2 | VALIDADO |
| DB-023 | Queries N+1 em "buscar tasks do usuário com clips" | ALTA | 4h | P1 | VALIDADO |
| DB-024 | Sem covering indexes para queries comuns | MÉDIA | 2h | P2 | VALIDADO |
| DB-025 | `processing_cache` sem partition por source_type | - | - | - | REMOVIDO (premature) |
| DB-026 | `users.plan` e `users.subscription_status` sem CHECK constraint | BAIXA | 1h | P3 | VALIDADO |
| DB-027 | Inconsistência nomenclatura: camelCase vs snake_case | BAIXA | 8h | P3 | AJUSTADO |
| DB-028 | `users.caption_template` não existe mas referenciado | - | - | - | REMOVIDO (não é problema) |
| DB-029 | Sem políticas RLS em nenhuma tabela | CRÍTICA | 8h | P0 | VALIDADO |
| DB-030 | Sem políticas RLS para `sources` | CRÍTICA | 4h | P0 | VALIDADO |
| DB-031 | Sem políticas RLS para `generated_clips` | CRÍTICA | 4h | P0 | VALIDADO |

*Adicionados por @data-engineer (FASE 5)*

| ID | Débito | Severidade | Horas | Prioridade | Status |
|-----|---------|------------|---------|------------|--------|
| DB-032 | Sem versionamento de migrations (init.sql único) | ALTA | 16h | P1 | ADICIONADO |
| DB-033 | Dupla fonte de schema (Prisma + init.sql) | ALTA | 8h | P1 | ADICIONADO |
| DB-034 | Sem FK em sources para users (relacional) | MÉDIA | 2h | P2 | ADICIONADO |

**Subtotal Database:** 108h

---

### 3. Débitos de Frontend/UX (14)

*Validados por @ux-design-expert - FASE 6*

| ID | Débito | Severidade Original | Severidade Ajustada | Horas | Prioridade | Status |
|----|---------|---------------------|---------------------|-------|------------|--------|
| UX-001 | Quase todas as páginas com "use client" — sem Server Components | MEDIA | **ALTA** | 4h | P1 | VALIDADO |
| UX-002 | Inconsistent loading states — task edit não tem skeleton | BAIXA | BAIXA | 1h | P2 | VALIDADO |
| UX-003 | Empty state faltando em task edit page | BAIXA | BAIXA | 1h | P2 | VALIDADO |
| UX-004 | Botões icon sem aria-label (edit, delete clip) | MEDIA | **ALTA** | 2h | P0 | VALIDADO |
| UX-005 | Phone preview hidden em mobile | BAIXA | BAIXA | 0.5h | P2 | VALIDADO |
| UX-006 | Color contrast stone-500 em backgrounds claros | MEDIA | **REMOVIDO** | - | - | FALSO POSITIVO |
| UX-007 | Inconsistent button styles entre páginas | BAIXA | BAIXA | 1h | P2 | VALIDADO |
| UX-008 | Error handling direto com alert() | MEDIA | **ALTA** | 2h | P1 | VALIDADO |
| UX-009 | Direct fetch calls sem loading robusto | BAIXA | BAIXA | 1h | P2 | VALIDADO |
| UX-010 | Landing page heavy em client-side animations | MEDIA | MEDIA | 1h | P3 | VALIDADO |

*Adicionados por @ux-design-expert (FASE 6)*

| ID | Débito | Severidade | Horas | Prioridade | Status |
|----|---------|------------|-------|------------|--------|
| UX-011 | Ausência de toast/notification para operações bem-sucedidas | BAIXA | 1h | P2 | ADICIONADO |
| UX-012 | Empty state genérico sem actionable content na task list | MÉDIA | 1h | P1 | ADICIONADO |
| UX-013 | Sem validação inline em formulários (sign-in/sign-up) | BAIXA | 1h | P2 | ADICIONADO |
| UX-014 | Loading states não bloqueiam interação durante submit | MÉDIA | 1h | P1 | ADICIONADO |
| UX-015 | Falta de keyboard navigation em task detail page | ALTA | 2h | P0 | ADICIONADO |

**Subtotal Frontend/UX:** 19.5h

---

## Matriz de Priorização Final

### Top 15 Débitos por Impacto

| Rank | ID | Débito | Severidade | Área | Esforço |
|------|-----|--------|------------|------|---------|
| 1 | SYS-001 | Ausência total de testes automatizados | CRÍTICA | Sistema | 40h |
| 2 | DB-029 | Sem políticas RLS em nenhuma tabela | CRÍTICA | Database | 8h |
| 3 | DB-030 | Sem políticas RLS para `sources` | CRÍTICA | Database | 4h |
| 4 | DB-031 | Sem políticas RLS para `generated_clips` | CRÍTICA | Database | 4h |
| 5 | DB-019 | Sem tabela de rate limiting/limites | CRÍTICA | Database | 8h |
| 6 | SYS-021 | Backup/Disaster Recovery não documentado | CRÍTICA | Sistema | 8h |
| 7 | UX-004 | Botões icon sem aria-label | ALTA | UX | 2h |
| 8 | UX-015 | Falta de keyboard navigation em task detail | ALTA | UX | 2h |
| 9 | SYS-011 | 132+ cláusulas except sem logging | ALTA | Sistema | 16h |
| 10 | SYS-002 | Dupla fonte de schema | ALTA | Sistema | 16h |
| 11 | SYS-006 | Error handling inconsistente | ALTA | Sistema | 12h |
| 12 | DB-003 | generated_clips_ids array não normalizado | MÉDIA | Database | 4h |
| 13 | DB-023 | Queries N+1 em tasks+clips | ALTA | Database | 4h |
| 14 | UX-001 | Sem Server Components | ALTA | UX | 4h |
| 15 | UX-008 | Error handling com alert() | ALTA | UX | 2h |

---

## Plano de Resolução

### Fase A: Segurança Crítica (Semanas 1-2) — ~56h

| Débito | Ação | Dependências |
|--------|------|--------------|
| DB-029 | Implementar RLS em tasks | - |
| DB-030 | Implementar RLS em sources | DB-029 |
| DB-031 | Implementar RLS em generated_clips | DB-029 |
| DB-019 | Criar tabela user_limits | - |
| SYS-007 | Implementar rate limiting no backend | DB-019 |
| SYS-008 | Remover credenciais hardcoded | - |
| SYS-021 | Documentar estratégia de backup | - |

### Fase B: Base de Qualidade (Semanas 3-6) — ~96h

| Débito | Ação | Dependências |
|--------|------|--------------|
| SYS-001 | Setup testes (pytest + Vitest) | CI/CD (SYS-019) |
| SYS-011 | Audit das 132+ cláusulas except | - |
| SYS-012 | Validação de environment variables | - |
| SYS-006 | Custom exceptions com error codes | - |
| SYS-019 | Configurar CI/CD pipeline | - |
| SYS-024 | Implementar Security Headers | - |

### Fase C: Arquitetura (Semanas 7-10) — ~72h

| Débito | Ação | Dependências |
|--------|------|--------------|
| SYS-002 | Unificar schema (Prisma como source) | DB-032 |
| DB-032 | Setup migrations versionamento | - |
| DB-033 | Remover duplicação schema | SYS-002 |
| DB-003 | Normalizar generated_clips_ids | - |
| DB-023 | Resolver N+1 queries | - |
| SYS-017 | Remover main.py duplicate | - |

### Fase D: Refinamento (Semanas 11+) — ~111.5h

| Débito | Ação | Dependências |
|--------|------|--------------|
| UX-004 | Adicionar aria-labels | - |
| UX-015 | Keyboard navigation | - |
| UX-001 | Server Components | - |
| UX-008 | Substituir alert() por Toast | UX-011 |
| UX-011 | Criar componente de Toast | - |
| UX-012 | Empty states actionáveis | - |
| UX-014 | Bloquear double-submit | - |
| SYS-010 | Graceful shutdown worker | - |
| SYS-009 | Logging estruturado | - |
| DB-002 | Índice session.expiresAt | - |
| DB-020 | UNIQUE constraint account | - |

---

## Riscos e Mitigações

### Riscos de Segurança

| Risco | Mitigação |
|-------|-----------|
| RLS + Pooler Exposição | Audit de queries antes de implementar; usar view para públicas |
| Auth Bypass em SELF_HOST | Manter modo atual durante transição; não breaking |
| SQL Injection Residual | Audit rigoroso em repositories; parameterized queries |
| Hardcoded Credentials | Usar secrets management (env vars) |

### Riscos de Regressão

| Risco | Mitigação |
|-------|-----------|
| Schema Sync Breaking | Ao corrigir, garantir sync das 3 fontes |
| RLS Policy Restritiva | Testar TODAS queries existentes APÓS implementar |
| Array Normalization | Migrar dados ANTES de remover campo |
| Testes quebrando backend | Usar mock de dependências |

### Riscos de Integração

| Risco | Mitigação |
|-------|-----------|
| Frontend-Backend Contract | Sincronizar normalização DB com frontend API |
| Worker-DB Connection | Graceful shutdown deve fechar conexões |
| Redis Connection Leaks | Configurar pool corretamente |

---

## Critérios de Sucesso

### Métricas de Qualidade

- [ ] Pipeline CI/CD configurado com testes automatizados
- [ ] Cobertura mínima 40% em backend (pytest)
- [ ] Cobertura mínima 30% em frontend (Vitest)
- [ ] Security tests passam (RLS, rate limiting)
- [ ] Performance baseline: queries <100ms
- [ ] A11y audit passa (WCAG AA)
- [ ] Zero breaking changes em produção

### Testes de Integração Requeridos

| Teste | Escopo | Prioridade |
|-------|--------|------------|
| E2E: Auth Flow | Sign up → Login → Create task → Download clip | P0 |
| E2E: Task Lifecycle | Create → Processing → Completed → Edit → Delete | P0 |
| Security: RLS Bypass | Tentativa de acesso cross-user via Pooler | P0 |
| Performance: Concurrent Tasks | Múltiplas tasks simultâneas | P1 |
| Integration: Stripe Webhook | Subscription → plan update | P1 |

---

## Validações Concluídas

| Fase | Revisor | Status | Ajustes |
|------|---------|--------|---------|
| FASE 4 | @architect (Aria) | ✅ | Draft inicial - 59 débitos |
| FASE 5 | @data-engineer (Dara) | NEEDS WORK→APPROVED | +3 DB-*, -2 DB-*, 4 ajustes |
| FASE 6 | @ux-design-expert (Uma) | APPROVED | +5 UX-*, -1 UX-*, 4 ajustes |
| FASE 7 | @qa (Quinn) | APPROVED | +6 SYS- (operacionais) |
| FASE 8 | @architect (Aria) | **FINAL** | Consolidação completa |

---

## Metadata

| Campo | Valor |
|-------|-------|
| Total Débitos | 72 |
| Esforço Total | ~335.5h |
| P0 (Crítico) | 10 |
| P1 (Alto) | 22 |
| P2 (Médio) | 26 |
| P3 (Baixo) | 14 |
| Gate Status | APPROVED para planejamento |

---

*Documento consolidado por @architect (Aria) — FASE 8 Brownfield Discovery*  
*Este documento serve como base para planejamento de correção de débitos técnicos.*
