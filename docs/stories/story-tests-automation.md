# Story 1.2: Testes Automatizados

## Epic
[epic-technical-debt.md](epic-technical-debt.md)

## Prioridade
**P0** — Crítico

## Esforço
~40h

## Responsável
@qa + @dev

## Contexto

O SupoClip não possui nenhum teste automatizado. Esta story estabelece a base de testes:
- Backend: pytest
- Frontend: Vitest
- E2E: Playwright ou similar

## Débitos Alocados

| ID | Débito | Esforço |
|----|--------|---------|
| SYS-001 | Ausência total de testes automatizados | 40h |

## Tasks

### Setup Backend Testing
- [ ] 1.2.1 Configurar pytest no projeto backend
- [ ] 1.2.2 Configurar pytest.ini com markers (unit, integration)
- [ ] 1.2.3 Setup fixtures para database (mock ou test container)
- [ ] 1.2.4 Setup fixtures para auth (mock user)
- [ ] 1.2.5 Setup fixtures para api client

### Setup Frontend Testing
- [ ] 1.2.6 Configurar Vitest no projeto frontend
- [ ] 1.2.7 Configurar setup.ts para mocks globais
- [ ] 1.2.8 Setup component testing com React Testing Library
- [ ] 1.2.9 Configurar coverage threshold (30%)

### Testes Unitários - Backend
- [ ] 1.2.10 Testar auth utilities (jwt decode, session validation)
- [ ] 1.2.11 Testar task service (CRUD operations)
- [ ] 1.2.12 Testar clip generation utils
- [ ] 1.2.13 Testar error handlers

### Testes Unitários - Frontend
- [ ] 1.2.14 Testar componentes de UI (Button, Input, Card)
- [ ] 1.2.15 Testar hooks (useTask, useAuth)
- [ ] 1.2.16 Testar utilitários de formatação

### Testes de Integração
- [ ] 1.2.17 Setup test database com docker-compose
- [ ] 1.2.18 Testar API endpoints (tasks CRUD)
- [ ] 1.2.19 Testar auth flow (signup → login)
- [ ] 1.2.20 Testar webhook handlers

### CI/CD Integration
- [ ] 1.2.21 Adicionar testes ao CI pipeline
- [ ] 1.2.22 Configurar coverage report
- [ ] 1.2.23 Configurarfail on coverage drop

## Critérios de Aceite

### Cobertura
- [ ] Backend coverage >= 40%
- [ ] Frontend coverage >= 30%
- [ ] Todos os endpoints testados

### Execução
- [ ] `npm test` executa todos os testes
- [ ] `pytest` executa todos os testes
- [ ] CI pipeline roda testes automaticamente

### Quality
- [ ] Zero testes falhando
- [ ] Testes com nomes descritivos
- [ ] Testes isolados (sem dependência entre si)

## Definition of Done

1. [ ] Cobertura >= 40% backend
2. [ ] Cobertura >= 30% frontend
3. [ ] Pipeline CI/CD configurado com testes
4. [ ] Code review aprovado
5. [ ] Documentação (TESTING.md)

## Dependencies

- **Bloqueada por:** Story 1.6 (Operações) - CI/CD pipeline
- **Bloqueia:** Story 1.4 (Backend Quality) - testes de regressão

## Notes

- Usar test containers (PostgreSQL, Redis) para integração
- Mockar APIs externas (AssemblyAI, Stripe)
- Manter testes rápidos (< 5min total)
