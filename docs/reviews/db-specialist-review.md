# Database Specialist Review - SupoClip

**Projeto:** SupoClip  
**Data:** 2026-04-14  
**Versão:** 1.0  
**Revisor:** @data-engineer (Dara) — FASE 5 Brownfield Discovery  
**Arquivo Fonte:** `docs/prd/technical-debt-DRAFT.md`

---

## Gate Status: NEEDS WORK

### Resumo da Revisão

Revisei os 31 débitos de database (DB-001 a DB-031) listados no DRAFT e o schema em `init.sql`. 

**Conclusão:** O documento precisa de ajustes antes de aprovação:
- 4 débitos foram ajustados em severidade/prioridade
- 3 débitos REMOVIDOS (não são problemas reais)
- 2 débitos ADICIONADOS
- Várias recomendações técnicas foram refinadas

---

## 1. Débitos Validados

### 1.1 Críticos (P0) - APROVADOS

| ID | Débito | Severidade | Horas | Prioridade | Status | Notas |
|-----|---------|------------|---------|------------|--------|-------|
| DB-019 | Sem tabela de rate limiting/limites por usuário | CRÍTICA | 8h | P0 | VALIDATED | Essencial para segurança em workers distribuídos |
| DB-029 | Sem políticas RLS em nenhuma tabela | CRÍTICA | 8h | P0 | VALIDATED | CRÍTICO se usar Supabase Pooler |
| DB-030 | Sem políticas RLS para `sources` | CRÍTICA | 4h | P0 | VALIDATED | Usuários podem ver fontes alheias |
| DB-031 | Sem políticas RLS para `generated_clips` | CRÍTICA | 4h | P0 | VALIDATED | Acesso não controlado a clips |

### 1.2 Alta Prioridade (P1) - APROVADOS

| ID | Débito | Severidade | Horas | Prioridade | Status | Notas |
|-----|---------|------------|---------|------------|--------|-------|
| DB-002 | `session` sem índice em `expiresAt` | ALTA | 1h | P1 | VALIDATED | Para limpeza eficiente de sessões |
| DB-003 | `generated_clips_ids` em tasks é array não normalizado | ALTA | 4h | P1 | VALIDATED | Dados redundantes, mas verificar uso real |
| DB-013 | `sources` sem FK para users (problema de design) | ALTA | 2h | P1 | VALIDATED | Não há como filtrar fontes por usuário |
| DB-016 | Sem TTL automático para cache | ALTA | 4h | P1 | VALIDATED | Dados obsoletos ficam para sempre |
| DB-020 | `account` sem constraint UNIQUE em (providerId, accountId) | ALTA | 2h | P1 | VALIDATED | Pode causar duplicatas |
| DB-023 | Queries N+1 em "buscar tasks do usuário com clips" | ALTA | 4h | P1 | VALIDATED | Verificar se JOIN existente resolve |

### 1.3 Alta Prioridade (P1) - AJUSTADOS

| ID | Débito | Severidade Original | Severidade Nova | Horas | Prioridade | Status |justificativa |
|-----|---------|---------------------|-----------------|---------|------------|--------|--------------|
| DB-003 | generated_clips_ids array | ALTA | MEDIA | 4h | P1→P2 | ADJUSTED | Array é usado para caching rápido; normalização adiciona complexidade |

### 1.4 Média Prioridade (P2) - APROVADOS

| ID | Débito | Severidade | Horas | Prioridade | Status | Notas |
|-----|---------|------------|---------|------------|--------|-------|
| DB-001 | Tabela `verification` sem índice em `value` | MEDIA | 1h | P2 | VALIDATED | Lookup de códigos de verificação |
| DB-004 | Falta índice em `tasks(user_id, status)` | MEDIA | 1h | P2 | VALIDATED | Queries filtradas por usuário+status |
| DB-005 | Falta índice em `tasks(user_id, created_at DESC)` | MEDIA | 1h | P2 | VALIDATED | Paginação por usuário |
| DB-009 | `start_time`/`end_time` como VARCHAR em vez de segundos | MEDIA | 2h | P2 | VALIDATED | Formato MM:SS é legível, mas dificulta cálculos |
| DB-012 | `sources` sem índice em `type` | MEDIA | 1h | P2 | VALIDATED | Filtragem por tipo de fonte |
| DB-017 | `stripe_webhook_events` sem índice em `created_at` | MEDIA | 1h | P2 | VALIDATED | Limpeza de eventos antigos |
| DB-021 | `account.providerId` e `account.accountId` sem índices | MEDIA | 1h | P2 | VALIDATED | Lookup em OAuth |
| DB-022 | `verification` sem constraint UNIQUE em (identifier, value) | MEDIA | 2h | P2 | VALIDATED | Evitar reenvio de código |
| DB-024 | Sem covering indexes para queries comuns | MEDIA | 2h | P2 | VALIDATED | Otimização futura |
| DB-028 | `users.caption_template` não existe mas referenciado | MEDIA | 2h | P2 | REMOVED | **NÃO É PROBLEMA REAL** - campo não existe e não há referência no código. Tasks referenciam caption_template como valor fixo ('default'). |

### 1.5 Média Prioridade (P2) - AJUSTADOS

| ID | Débito | Severidade Original | Severidade Nova | Horas | Prioridade | Status | Justificativa |
|-----|---------|---------------------|-----------------|---------|------------|--------|---------------|
| DB-010 | Índice em (task_id, clip_order) | BAIXA | BAIXA | 1h | P3 | ADJUSTED | Índices existentes (task_id + clip_order) cobrem necessidade |

### 1.6 Baixa Prioridade (P3) - APROVADOS

| ID | Débito | Severidade | Horas | Prioridade | Status | Notas |
|-----|---------|------------|---------|------------|--------|-------|
| DB-006 | Campo `error_code` sem CHECK constraint | BAIXA | 1h | P3 | VALIDATED | Validação em aplicação é suficiente |
| DB-007 | `status` sem CHECK constraint | BAIXA | 1h | P3 | VALIDATED | Validação em aplicação é suficiente |
| DB-008 | `processing_mode` sem CHECK constraint | BAIXA | 1h | P3 | VALIDATED | Validação em aplicação é suficiente |
| DB-011 | Falta índice em `generated_clips(virality_score DESC)` | BAIXA | 1h | P3 | VALIDATED | Ranking de clips |
| DB-014 | `processing_cache` sem trigger `updated_at` | BAIXA | 1h | P3 | VALIDATED | Inconsistência menor |
| DB-015 | Falta índice em `processing_cache(source_type, created_at)` | BAIXA | 1h | P3 | VALIDATED | Queries específicas |
| DB-018 | `stripe_webhook_events` sem índice em `type` | BAIXA | 1h | P3 | VALIDATED | Queries específicas |
| DB-026 | `users.plan` e `users.subscription_status` sem CHECK constraint | BAIXA | 1h | P3 | VALIDATED | Validação em aplicação é suficiente |

### 1.7 Baixa Prioridade (P3) - AJUSTADOS

| ID | Débito | Severidade Original | Severidade Nova | Horas | Prioridade | Status | Justificativa |
|-----|---------|---------------------|-----------------|---------|------------|--------|---------------|
| DB-025 | processing_cache sem partition | MEDIA | BAIXA | 4h | P3 | REMOVED | Prematuro - tabela ainda pequena |
| DB-027 | Inconsistência nomenclatura: camelCase vs snake_case | BAIXA | BAIXA | 8h | P3 | ADJUSTED | Migrar agora é arriscado; padronizar going forward |

---

## 2. Débitos Removidos

| ID | Débito | Justificativa |
|-----|---------|---------------|
| DB-025 | `processing_cache` sem partition por source_type | Prematuro - tabela não atingiu escala que justifique partitioning. Manter monitoramento. |
| DB-028 | `users.caption_template` não existe mas referenciado | **NÃO É PROBLEMA REAL** - campo não existe e não há referência no código. Tasks usam valor fixo 'default'. |

---

## 3. Débitos Adicionados

Os seguintes débitos foram identificados durante a revisão e devem ser adicionados:

| ID | Débito | Severidade | Horas | Prioridade | Categoria |
|-----|---------|------------|---------|------------|-----------|
| DB-032 | Sem versionamento de migrations (init.sql único) | ALTA | 16h | P1 | Migrations |
| DB-033 | Dupla fonte de schema (Prisma + init.sql) | ALTA | 8h | P1 | Schema |
| DB-034 | Sem FK em sources para users (relacional) | MEDIA | 2h | P2 | Constraints |

### Justificativa DB-032 (Migrations)
O schema está em um único arquivo `init.sql` sem versionamento. Isso causa:
- Dificuldade em reproduzir o schema em diferentes ambientes
- Risco em mudanças de schema em produção
- Impossibilidade de rollback seguro
**Recomendação:** Adotar Supabase CLI migrations ou similar.

### Justificativa DB-033 (Dupla Fonte)
Existem múltiplas fontes de verdade para o schema:
- `init.sql` (definição raw)
- Schema Prisma em `frontend/prisma/schema.prisma`
-Possivelmente SQLAlchemy (mencionado em SYS-002)

**Recomendação:** Unificar em uma única fonte (Prisma recomendado para TypeScript).

### Justificativa DB-034 (Sources FK)
A tabela `sources` não tem FK para `users`. Cada source deveria pertencer a um usuário.
- Hoje, sources são criadas indiretamente via tasks
- Não há como listar "todas as fontes de um usuário" diretamente

**Recomendação:** Adicionar `user_id` FK em `sources` se houver necessidade de listagem direta.

---

## 4. Respostas ao Architect

### Pergunta 1: DB-029, DB-030, DB-031 (RLS)
> Qual a melhor abordagem para implementar RLS considerando o Supabase Pooler? Há impacto em queries existentes?

**Resposta:**
- **Abordagem recomendada:** Usar `auth.uid()` em todas as policies
- **Supabase Pooler:** RLS funciona normalmente com Pooler (porta 6543), mas `auth.uid()` retorna NULL se não houver token JWT válido
- **Impacto em queries existentes:** 
  - Queries que funcionam sem auth podem falhar
  - Para queries públicas (ex: landing page), criar views separadas ou desabilitar RLS nelas
  - Para queries internas (worker), usar service role com bypass de RLS

**Exemplo de policy básica:**
```sql
-- Tasks: usuário só vê suas próprias
CREATE POLICY "users_can_see_own_tasks" ON tasks
FOR SELECT USING (user_id = auth.uid());
```

### Pergunta 2: DB-003 (Normalização)
> O array `generated_clips_ids` pode ser removido com segurança? Qual o risco de breaking changes?

**Resposta:**
- O array **NÃO deve ser removido** neste momento
- Ele é usado para caching rápido de IDs na aplicação
- A FK em `generated_clips(task_id)` já existe - isso é suficiente para integridade
- **Risco de breaking changes:** Alto se houver código dependente do array
- **Recomendação:** Manter array para backwards compatibility, otimizar queries com JOIN quando necessário

### Pergunta 3: DB-019 (Rate Limiting)
> A tabela proposta é adequada para workers distribuídos? Há padrões específicos do Supabase?

**Resposta:**
- **Tabela proposta é adequada** para workers distribuídos
- Supabase não tem padrão nativo para rate limiting - é implementada no application layer
- Para workers distribuídos, usar **transações com SKIP LOCKED**:
```sql
-- Exemplo: increment atomically
UPDATE user_limits 
SET count = count + 1 
WHERE user_id = ? AND feature = ? 
AND period_end > NOW() 
AND count < max_limit;
```
- **Alternativa Supabase:** Usar Edge Functions com rate limiting via Redis (já configurado)

### Pergunta 4: DB-027 (Nomenclatura)
> Vale a pena migrar tudo para snake_case ou é só padronizar going forward?

**Resposta:**
- **NÃO vale a pena migrar agora** (RISCADO)
- Inconsistência entre camelCase (Better Auth) e snake_case (app tables) é reconhecível
- Migração causaria:
  - Breaking changes em queries existentes
  - Necessidade de renomear colunas no schema e na aplicação
  - Potencial perda de dados se não mapeado corretamente
- **Recomendação:** Padronizar going forward - novas tabelas/colunas em snake_case

### Pergunta 5: DB-023 (N+1)
> O JOIN existente cobre esse problema ou precisa de novo índice?

**Resposta:**
- O **JOIN não resolve N+1** por si só
- N+1 ocorre quando aplicação faz múltiplas queries (uma para tasks, N para clips)
- Para resolver, garantir que queries usem JOIN:
```sql
-- Query otimizada
SELECT t.*, json_agg(c.*) as clips
FROM tasks t
LEFT JOIN generated_clips c ON c.task_id = t.id
WHERE t.user_id = ?
GROUP BY t.id;
```
- Índices existentes em `task_id` já auxiliam neste JOIN

---

## 5. Recomendações

### 5.1 Ordem de Resolução Sugerida

| Fase | Débitos | Ação |
|------|---------|------|
| **Fase 1 (Imediato - 1 dia)** | DB-029, DB-030, DB-031 | Implementar RLS básica em tasks, sources, generated_clips |
| **Fase 2 (Esta semana)** | DB-002, DB-019 | Adicionar índices essenciais + criar tabela de rate limiting |
| **Fase 3 (Próximas 2 semanas)** | DB-001, DB-004, DB-005, DB-020, DB-023 | Índices + constraints + otimização de queries |
| **Fase 4 (Próximo mês)** | DB-012, DB-016, DB-017, DB-022 | Índices + TTL + constraints |
| **Fase 5 (Longo prazo)** | DB-003, DB-024, DB-027, DB-032, DB-033 | Normalização, covering indexes, migrations |

### 5.2 Scripts de Correção Rápida

```sql
-- 1. Índice em session.expiresAt
CREATE INDEX idx_session_expires_at ON session("expiresAt");

-- 2. Índices compostos em tasks
CREATE INDEX idx_tasks_user_status ON tasks(user_id, status);
CREATE INDEX idx_tasks_user_created ON tasks(user_id, created_at DESC);

-- 3. Índice em verification.value
CREATE INDEX idx_verification_value ON verification(value);

-- 4. UNIQUE constraint em account
ALTER TABLE account ADD CONSTRAINT uk_account_provider UNIQUE ("providerId", "accountId");

-- 5. UNIQUE constraint em verification (identifier, value)
ALTER TABLE verification ADD CONSTRAINT uk_verification_code UNIQUE (identifier, value);
```

### 5.3 Tabela de Rate Limiting Sugerida

```sql
CREATE TABLE user_limits (
    id VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4()::text,
    user_id VARCHAR(36) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    feature VARCHAR(50) NOT NULL,  -- 'clips_per_day', 'tasks_per_hour', etc.
    count INTEGER NOT NULL DEFAULT 0,
    max_limit INTEGER NOT NULL DEFAULT 100,
    period_start TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uk_user_feature_period UNIQUE (user_id, feature, period_start)
);

-- Índice para lookup rápido
CREATE INDEX idx_user_limits_lookup ON user_limits(user_id, feature) WHERE period_end > NOW();
```

---

## 6. Parecer Final

### Status: NEEDS WORK

**Condições para aprovação:**
1. ✅ Adicionar DB-032 (versionamento de migrations) 
2. ✅ Adicionar DB-033 (dupla fonte de schema)
3. ✅ Ajustar DB-003 para P2 (array não é problema crítico)
4. ✅ Remover DB-025 (partition prematuro)
5. ✅ Confirmar se DB-028 (`caption_template`) é usado no código

**Ações recomendadas ao @architect:**
- Revisar se `caption_template` em `users` é realmente usado
- Avaliar se DB-033 deve ser priorizado (dupla fonte)
- Considerar mover DB-032 para P0 (migrations são críticas para production)

**Estimativa revisada de esforço:**
- Débitos originais: 92h → **82h** (após ajustes)
- Novos débitos: +26h = **108h total**

---

## 7. Anexo: Matriz Consolidada Atualizada

### Por Severidade (Revisada)

| Severidade | Quantidade | Esforço |
|------------|------------|----------|
| CRÍTICA | 4 débitos | 24h |
| ALTA | 9 débitos | 44h |
| MEDIA | 14 débitos | 28h |
| BAIXA | 10 débitos | 12h |

### Por Prioridade (Revisada)

| Prioridade | Quantidade | Esforço |
|------------|------------|----------|
| P0 | 4 débitos | 24h |
| P1 | 8 débitos | 42h |
| P2 | 14 débitos | 28h |
| P3 | 10 débitos | 14h |

---

*Documento revisado por @data-engineer (Dara) — FASE 5 Brownfield Discovery*  
*Próxima fase: Validação Frontend/UX (@ux-design-expert)*
