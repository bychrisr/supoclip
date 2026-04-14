# Story 1.4: Backend Quality

## Epic
[epic-technical-debt.md](epic-technical-debt.md)

## Prioridade
**P1** — Alto

## Esforço
~64h

## Responsável
@dev + @architect

## Contexto

O backend possui débitos de qualidade de código:
- Error handling inconsistente
- 132+ exceções sem logging
- Variáveis não validadas
- Código duplicado
- Queries vulneráveis

## Débitos Alocados

| ID | Débito | Esforço |
|----|--------|---------|
| SYS-002 | Dupla fonte de schema | 16h |
| SYS-006 | Error handling inconsistente | 12h |
| SYS-011 | 132+ cláusulas except sem logging | 16h |
| SYS-012 | Variáveis de ambiente não validadas | 6h |
| SYS-014 | Queries SQL não parametrizadas | 8h |
| SYS-017 | Código duplicado em main.py | 8h |
| SYS-018 | Processamento síncrono em asyncio.create_task | 4h |

## Tasks

### Error Handling (SYS-006, SYS-011)
- [ ] 1.4.1 Criar módulo de exceções customizadas (SupoClipError, AuthError, ValidationError, etc.)
- [ ] 1.4.2 Definir error codes (ERR_001, ERR_002, etc.)
- [ ] 1.4.3 Implementar exception handler no FastAPI
- [ ] 1.4.4 Audit de todas as cláusulas except
- [ ] 1.4.5 Adicionar logging em cada except (level, message, stack trace)
- [ ] 1.4.6 Padronizar estrutura de resposta de erro

### Validação de Environment (SYS-012)
- [ ] 1.4.7 Criar validador de variáveis de ambiente
- [ ] 1.4.8 Verificar variáveis obrigatórias no startup
- [ ] 1.4.9 Adicionar health check de dependências (DB, Redis)
- [ ] 1.4.10 Criar documentação de variáveis requeridas

### Queries Parametrizadas (SYS-014)
- [ ] 1.4.11 Audit de queries SQL no código
- [ ] 1.4.12 Identificar queries com concatenação
- [ ] 1.4.13 Refatorar para queries parametrizadas
- [ ] 1.4.14 Adicionar sanitização de inputs

### Remoção de Duplicação (SYS-017)
- [ ] 1.4.15 Comparar main.py e main_refactored.py
- [ ] 1.4.16 Unificar em uma única implementação
- [ ] 1.4.17 Remover arquivo duplicado
- [ ] 1.4.18 Verificar imports e rotas

### Async Processing (SYS-018)
- [ ] 1.4.19 Audit de asyncio.create_task sem await
- [ ] 1.4.20 Identificar onde await é necessário
- [ ] 1.4.21 Corrigir async calls
- [ ] 1.4.22 Testar fluxos assíncronos

### Dupla Fonte Schema (SYS-002)
- [ ] 1.4.23 Verificar consistência Prisma vs SQLAlchemy vs init.sql
- [ ] 1.4.24 Unificar schema (refere DB-033)
- [ ] 1.4.25 Documentar fonte oficial

## Critérios de Aceite

### Error Handling
- [ ] Todas exceções com logging estruturado
- [ ] Error codes consistentes
- [ ] Respostas de erro padronizadas

### Segurança
- [ ] Zero queries com concatenação
- [ ] Inputs validados e sanitizados
- [ ] Variáveis obrigatórias verificadas no startup

### Qualidade
- [ ] Código duplicado removido
- [ ] Async calls corretas
- [ ] Schema unificado

## Definition of Done

1. [ ] Todas exceções com logging
2. [ ] Queries parametrizadas
3. [ ] Código duplicado removido
4. [ ] Code review aprovado

## Dependencies

- **Bloqueada por:** Story 1.2 (Testes) - testes de regressão
- **Bloqueia:** Story 1.6 (Operações)

## Notes

- Usar logging estruturado (JSON com level, timestamp, user_id)
- Manter backward compatibility
- Documentar novos error codes
