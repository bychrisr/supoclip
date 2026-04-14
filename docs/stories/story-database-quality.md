# Story 1.3: Database Quality

## Epic
[epic-technical-debt.md](epic-technical-debt.md)

## Prioridade
**P1** — Alto

## Esforço
~80h

## Responsável
@data-engineer + @dev

## Contexto

O banco de dados possui débitos de performance e integridade:
- Índices faltantes
- Normalização incompleta
- Dupla fonte de schema
- Versionamento ausente

## Débitos Alocados

| ID | Débito | Esforço |
|----|--------|---------|
| DB-002 | session sem índice em expiresAt | 1h |
| DB-003 | generated_clips_ids array não normalizado | 4h |
| DB-004 | Falta índice em tasks(user_id, status) | 1h |
| DB-005 | Falta índice em tasks(user_id, created_at DESC) | 1h |
| DB-010 | Falta índice em generated_clips(task_id, clip_order) | 1h |
| DB-011 | Falta índice em generated_clips(virality_score DESC) | 1h |
| DB-012 | sources sem índice em type | 1h |
| DB-013 | sources sem FK para users | 2h |
| DB-015 | Falta índice em processing_cache(source_type, created_at) | 1h |
| DB-016 | Sem TTL automático para cache | 4h |
| DB-017 | stripe_webhook_events sem índice em created_at | 1h |
| DB-018 | stripe_webhook_events sem índice em type | 1h |
| DB-020 | account sem constraint UNIQUE em (providerId, accountId) | 2h |
| DB-021 | account.providerId e account.accountId sem índices | 1h |
| DB-022 | verification sem constraint UNIQUE em (identifier, value) | 2h |
| DB-023 | Queries N+1 em tasks+clips | 4h |
| DB-024 | Sem covering indexes para queries comuns | 2h |
| DB-032 | Sem versionamento de migrations | 16h |
| DB-033 | Dupla fonte de schema (Prisma + init.sql) | 8h |
| DB-034 | Sem FK em sources para users | 2h |

## Tasks

### Índices (DB-002, DB-004, DB-005, DB-010, DB-011, DB-012, DB-015, DB-017, DB-018, DB-021)
- [ ] 1.3.1 Criar índice em session.expiresAt
- [ ] 1.3.2 Criar índice composto em tasks(user_id, status)
- [ ] 1.3.3 Criar índice composto em tasks(user_id, created_at)
- [ ] 1.3.4 Criar índice em generated_clips(task_id, clip_order)
- [ ] 1.3.5 Criar índice em generated_clips(virality_score)
- [ ] 1.3.6 Criar índice em sources.type
- [ ] 1.3.7 Criar índice em processing_cache(source_type, created_at)
- [ ] 1.3.8 Criar índice em stripe_webhook_events.created_at
- [ ] 1.3.9 Criar índice em stripe_webhook_events.type
- [ ] 1.3.10 Criar índices em account.providerId e account.accountId

### Constraints (DB-020, DB-022)
- [ ] 1.3.11 Adicionar UNIQUE constraint em account(providerId, accountId)
- [ ] 1.3.12 Adicionar UNIQUE constraint em verification(identifier, value)

### Cache TTL (DB-016)
- [ ] 1.3.13 Implementar cleanup automático de cache expirado
- [ ] 1.3.14 Adicionar índice para cleanup eficiente
- [ ] 1.3.15 Configurar scheduler para cleanup

### Normalização (DB-003, DB-013, DB-034)
- [ ] 1.3.16 Criar tabela task_clips para normalizar generated_clips_ids
- [ ] 1.3.17 Migrar dados existentes para task_clips
- [ ] 1.3.18 Adicionar FK em sources para users
- [ ] 1.3.19 Migrar dados sources existentes (se aplicável)
- [ ] 1.3.20 Remover generated_clips_ids de tasks

### Queries N+1 (DB-023)
- [ ] 1.3.21 Identificar queries com N+1 no código
- [ ] 1.3.22 Implementar eager loading com Prisma include
- [ ] 1.3.23 Criar endpoint otimizado para listar tasks com clips
- [ ] 1.3.24 Testar performance (deve estar < 100ms)

### Coverring Indexes (DB-024)
- [ ] 1.3.25 Analisar queries mais comuns
- [ ] 1.3.26 Criar covering index para task list (user_id, status, created_at)
- [ ] 1.3.27 Criar covering index para clip list (task_id, clip_order, id)

### Migrations (DB-032)
- [ ] 1.3.28 Setup Prisma migrate ou Alembic
- [ ] 1.3.29 Criar migrations iniciais
- [ ] 1.3.30 Remover init.sql como fonte de schema

### Schema Unificação (DB-033)
- [ ] 1.3.31 Definir Prisma como source of truth
- [ ] 1.3.32 Exportar schema do Prisma
- [ ] 1.3.33 Atualizar init.sql para refletir Prisma
- [ ] 1.3.34 Documentar processo de schema sync

## Critérios de Aceite

### Performance
- [ ] Queries de list tasks < 100ms
- [ ] Queries de clip generation < 50ms
- [ ] Cache cleanup < 1s para 10k registros

### Integridade
- [ ] FK constraints funcionando
- [ ] UNIQUE constraints prevenindo duplicatas
- [ ] Dados normalizados sem redundância

### Migração
- [ ] Schema unificado (Prisma como source)
- [ ] Migrations versionadas
- [ ] Zero breaking changes

## Definition of Done

1. [ ] Todos os índices criados e validados
2. [ ] Queries performance < 100ms
3. [ ] Schema unificado
4. [ ] Code review aprovado

## Dependencies

- **Bloqueada por:** Story 1.1 (Segurança Crítica) - RLS
- **Bloqueia:** Story 1.4 (Backend Quality)

## Notes

- Testar performance ANTES e DEPOIS de cada índice
- Usar EXPLAIN ANALYZE para validar uso de índices
-BACKUP antes de migrations de dados
