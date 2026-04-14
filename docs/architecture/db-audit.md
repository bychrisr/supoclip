# SupoClip - DB Audit

## Visão Geral

Este documento lista os débitos técnicos identificados na análise do schema do banco de dados do SupoClip. Cada item inclui severidade, estimativa de esforço e priorização para correção.

---

## Débitos Identificados

### Autenticação & Session Management

| ID | Débito | Severidade | Esforço | Prioridade |
|-----|---------|------------|---------|------------|
| DB-AUTH-001 | Tabela `verification` não tem índice em `value` para lookup rápido de códigos | MEDIA | 1h | P2 |
| DB-AUTH-002 | `session` não tem índice em `expiresAt` para limpeza de sessões expiradas | ALTA | 1h | P1 |

### Domain - Tasks

| ID | Débito | Severidade | Esforço | Prioridade |
|-----|---------|------------|---------|------------|
| DB-TASK-001 | `generated_clips_ids` em `tasks` é array PostgreSQL - não normalizado, causa redundância | ALTA | 4h | P1 |
| DB-TASK-002 | Falta índice em `tasks(user_id, status)` para filtrar tasks por usuário e status | MEDIA | 1h | P2 |
| DB-TASK-003 | Falta índice em `tasks(user_id, created_at DESC)` para listagem por usuário | MEDIA | 1h | P2 |
| DB-TASK-004 | Campo `error_code` VARCHAR(80) sem CHECK constraint (valores válidos não definidos) | BAIXA | 1h | P3 |
| DB-TASK-005 | `status` VARCHAR(20) sem CHECK constraint (possíveis valores: pending, processing, completed, failed, cancelled) | BAIXA | 1h | P3 |
| DB-TASK-006 | `processing_mode` VARCHAR(20) sem CHECK constraint | BAIXA | 1h | P3 |

### Domain - Generated Clips

| ID | Débito | Severidade | Esforço | Prioridade |
|-----|---------|------------|---------|------------|
| DB-CLIP-001 | `start_time` e `end_time` são VARCHAR(20) em formato MM:SS - não normalizado, dificulta cálculos | MEDIA | 2h | P2 |
| DB-CLIP-002 | Falta índice em `generated_clips(task_id, clip_order)` para ordenação | BAIXA | 1h | P3 |
| DB-CLIP-003 | Falta índice em `generated_clips(virality_score DESC)` para ranking de clips | BAIXA | 1h | P3 |

### Domain - Sources

| ID | Débito | Severidade | Esforço | Prioridade |
|-----|---------|------------|---------|------------|
| DB-SRC-001 | `sources` sem qualquer índice em `type` para filtragem por tipo de fonte | MEDIA | 1h | P2 |
| DB-SRC-002 | `sources` sem índice em `(user_id)` - mas não há FK para users (problema de design) | ALTA | 2h | P1 |

### Domain - Processing Cache

| ID | Débito | Severidade | Esforço | Prioridade |
|-----|---------|------------|---------|------------|
| DB-CACHE-001 | Tabela `processing_cache` não tem trigger de `updated_at` (inconsistente com outras tabelas) | BAIXA | 1h | P3 |
| DB-CACHE-002 | Falta índice em `(source_type, created_at)` para查询 por tipo e data | BAIXA | 1h | P3 |
| DB-CACHE-003 | Sem TTL automático para cache (dados obsoletos ficam para sempre) | ALTA | 4h | P1 |

### Billing & Monetização

| ID | Débito | Severidade | Esforço | Prioridade |
|-----|---------|------------|---------|------------|
| DB-BILL-001 | `stripe_webhook_events` sem índice em `created_at` para limpeza de eventos antigos | MEDIA | 1h | P2 |
| DB-BILL-002 | `stripe_webhook_events` sem índice em `type` para filtragem por tipo de evento | BAIXA | 1h | P3 |
| DB-BILL-003 | Sem tabela de logs de uso/limites por usuário (rate limiting) | ALTA | 8h | P0 |

###Constraints e Integridade

| ID | Débito | Severidade | Esforço | Prioridade |
|-----|---------|------------|---------|------------|
| DB-CONST-001 | `account` sem constraint UNIQUE em (providerId, accountId) - pode ter contas duplicadas | ALTA | 2h | P1 |
| DB-CONST-002 | `account.providerId` e `account.accountId` sem índices para lookup | MEDIA | 1h | P2 |
| DB-CONST-003 | `verification` sem constraint UNIQUE em (identifier, value) - possível reenvio de código | MEDIA | 2h | P2 |

### Performance & Query Patterns

| ID | Débito | Severidade | Esforço | Prioridade |
|-----|---------|------------|---------|------------|
| DB-PERF-001 | Queries do tipo "buscar tasks do usuário com clips" fazem N+1 (sem JOIN eficiente) | ALTA | 4h | P1 |
| DB-PERF-002 | Sem covering indexes para queries comuns (ex: tasks + source info) | MEDIA | 2h | P2 |
| DB-PERF-003 | `processing_cache` sem partition por source_type (tabela pode crescer muito) | MEDIA | 4h | P2 |

### Schema Design Issues

| ID | Débito | Severidade | Esforço | Prioridade |
|-----|---------|------------|---------|------------|
| DB-SCHEMA-001 | `users.plan` e `users.subscription_status` sem CHECK constraint (valores válidos não documentados) | BAIXA | 1h | P3 |
| DB-SCHEMA-002 | Inconsistência nomenclatura: camelCase vs snake_case dentro do mesmo schema | BAIXA | 8h | P3 |
| DB-SCHEMA-003 | `users.caption_template` não existe na tabela, mas referenced em tasks - gap de dados? | MEDIA | 2h | P2 |

### Missing RLS (Row Level Security)

| ID | Débito | Severidade | Esforço | Prioridade |
|-----|---------|------------|---------|------------|
| DB-RLS-001 | Sem políticas RLS em nenhuma tabela - dados expostos se Connected via Pooler | CRITICA | 8h | P0 |
| DB-RLS-002 | Sem políticas RLS para `sources` - usuário pode ver fontes de outros | CRITICA | 4h | P0 |
| DB-RLS-003 | Sem políticas RLS para `generated_clips` - acesso não controlado | CRITICA | 4h | P0 |

### Migration & Versioning

| ID | Débito | Severidade | Esforço | Prioridade |
|-----|---------|------------|---------|------------|
| DB-MIGR-001 | Schema em único arquivo `init.sql` - sem versionamento de migrations | ALTA | 16h | P1 |
| DB-MIGR-002 | Sem rollbacks documentados para mudanças no schema | ALTA | 8h | P1 |
| DB-MIGR-003 | `stripe_webhook_events` sem campo `processed_at` para tracking de processamento | MEDIA | 1h | P2 |

---

## Resumo por Prioridade

### P0 - Crítico (Implementar Imediato)

| ID | Débito | Impacto |
|-----|---------|---------|
| DB-RLS-001 | Sem políticas RLS em nenhuma tabela | Exposição de dados se pooler usado |
| DB-RLS-002 | Sem políticas RLS para sources | Acesso não autorizado a fontes |
| DB-RLS-003 | Sem políticas RLS para generated_clips | Acesso não autorizado a clips |
| DB-BILL-003 | Sem tabela de rate limiting/limites | Abuso de recursos sem controle |

### P1 - Alta (Próximas 2 Semanas)

| ID | Débito | Impacto |
|-----|---------|---------|
| DB-AUTH-002 | Sem índice em session.expiresAt | Limpezaineficiente de sessões |
| DB-TASK-001 | generated_clips_ids não normalizado | Dados redundantes, inconsistentes |
| DB-SRC-002 | Sources sem FK para users | Não há como filtrar fontes por usuário |
| DB-CONST-001 | Account sem UNIQUE em provider+account | Duplicatas de conta |
| DB-MIGR-001 | Sem versionamento de migrations | Difícil mudança de schema |
| DB-MIGR-002 | Sem rollbacks documentados | Risco em mudanças |
| DB-PERF-001 | N+1 queries em tasks+clips | Performance degradada |

### P2 - Média (Próximo Mês)

| ID | Débito | Impacto |
|-----|---------|---------|
| DB-AUTH-001 | Sem índice em verification.value | Lookup lento de códigos |
| DB-TASK-002 | Falta índice composto user_id+status | Queries filtradas lentas |
| DB-TASK-003 | Falta índice para listagem por usuário | Paginação lenta |
| DB-CLIP-001 | start_time/end_time como VARCHAR | Cálculos dificultados |
| DB-CACHE-003 | Sem TTL para cache | Dados obsoletos |
| DB-BILL-001 | Sem índice em webhook_events.created_at | Limpeza ineficiente |
| DB-CONST-002 | Sem índices em account provider lookup | Queries lentas |
| DB-CONST-003 | Sem UNIQUE em verification | Possível reenvio de código |
| DB-SCHEMA-003 | Gap: caption_template em users referenciado em tasks |

### P3 - Baixa ( backlog)

| ID | Débito | Impacto |
|-----|---------|---------|
| DB-TASK-004/005/006 | CHECK constraints em status, error_code, processing_mode | Consistência de dados |
| DB-CLIP-002/003 | Índices para ordering e ranking | Queries específicas |
| DB-SRC-001 | Índice em sources.type | Filtragem por tipo |
| DB-CACHE-001 | Trigger para processing_cache | Consistência |
| DB-CACHE-002 | Índice composto cache | Queries específicas |
| DB-BILL-002 | Índice em webhook type | Queries específicas |
| DB-SCHEMA-001 | CHECK constraints em plan/subscription | Consistência |
| DB-SCHEMA-002 | Normalização de nomenclatura | Manutenção |

---

## Recomendações Priorizadas

### Curto Prazo (Esta Semana)

1. **Implementar RLS básica** (P0)
   - Policy em `tasks`: `user_id = auth.uid()`
   - Policy em `sources`: filtrar por tasks do usuário
   - Policy em `generated_clips`: via tasks → user

2. **Adicionar índice em session.expiresAt** (P1)
   ```sql
   CREATE INDEX idx_session_expires_at ON session("expiresAt");
   ```

3. **Adicionar índice composto para tasks** (P1)
   ```sql
   CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
   CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
   ```

### Médio Prazo (Próximas 2 Semanas)

4. **Versionar migrations** (P1)
   - Separar init.sql em migrations numeradas
   - Criar rollbacks para cada mudança
   - Usar Supabase CLI ou ferramenta similar

5. **Normalizar generated_clips_ids** (P1)
   - Remover array, usar FK em generated_clips
   - Query: `SELECT * FROM generated_clips WHERE task_id = ?`

6. **Adicionar UNIQUE em account** (P1)
   ```sql
   ALTER TABLE account ADD CONSTRAINT uk_account_provider UNIQUE ("providerId", "accountId");
   ```

7. **Criar tabela de rate limiting** (P0/P1)
   - `user_limits(id, user_id, feature, count, period_start, period_end)`
   - Implementar no backend/worker

### Longo Prazo (Próximo Mês+)

8. **Consistência de nomenclatura** (P3)
   - Padronizar snake_case ou camelCase
   - Migration de rename se necessário

9. **CHECK constraints para campos enumerados** (P3)
   - `status`: pending, processing, completed, failed, cancelled
   - `plan`: free, starter, pro, enterprise
   - `subscription_status`: active, inactive, trialing, past_due

10. **TTL para cache** (P2)
    - POLICY de DELETE em processing_cache
    - Cleanup de registros com mais de 7 dias

---

## Scripts de Correção Rápida

###índice expiresAt em session

```sql
CREATE INDEX idx_session_expires_at ON session("expiresAt")
WHERE "expiresAt" > CURRENT_TIMESTAMP;
```

### Índice composto em tasks

```sql
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);
```

### Índice em verification.value

```sql
CREATE INDEX idx_verification_value ON verification(value);
```

### UNIQUE em account (provider + account)

```sql
ALTER TABLE account ADD CONSTRAINT uk_account_provider 
UNIQUE ("providerId", "accountId");
```

---

## Notas

- **RLS é crítico** se o SupoClip usar Supabase Pooler (connection pooler) - sem RLS, qualquer pessoa conectada ao pool pode ver todos os dados
- **generated_clips_ids array** causa duplicação de dados - cada clip deve ter sua própria linha com FK para task
- **Versionamento de migrations** é essencial para colaboração e deployment seguro
- **Rate limiting** em tabela (não em memória) é necessário para workers distribuídos