# Story 1.6: Operações

## Epic
[epic-technical-debt.md](epic-technical-debt.md)

## Prioridade
**P2** — Médio

## Esforço
~32h

## Responsável
@devops

## Contexto

Falta infraestrutura operacional crítica:
- CI/CD pipeline
- Backup/Disaster Recovery
- Monitoring/Alerting
- Documentação de API

## Débitos Alocados

| ID | Débito | Esforço |
|----|--------|---------|
| SYS-019 | CI/CD Pipeline ausente | 8h |
| SYS-020 | Monitoring/Alerting ausente | 8h |
| SYS-021 | Backup/Disaster Recovery não documentado | 8h |
| SYS-022 | API Documentation ausente | 4h |
| SYS-023 | Data Retention Policy ausente | 4h |
| SYS-016 | Dockerfile sem multi-stage build | 4h |

## Tasks

### CI/CD Pipeline (SYS-019)
- [ ] 1.6.1 Configurar GitHub Actions workflow
- [ ] 1.6.2 Setup lint stage (ESLint, Ruff)
- [ ] 1.6.3 Setup typecheck stage (TypeScript, mypy)
- [ ] 1.6.4 Setup test stage (pytest, Vitest)
- [ ] 1.6.5 Setup build stage (Docker)
- [ ] 1.6.6 Configurar deploy to staging
- [ ] 1.6.7 Configurar manual approval para production

### Monitoring (SYS-020)
- [ ] 1.6.8 Integrar Sentry ou similar
- [ ] 1.6.9 Setup error tracking
- [ ] 1.6.10 Setup performance monitoring
- [ ] 1.6.11 Configurar alertas críticos
- [ ] 1.6.12 Criar dashboard de métricas

### Backup/Disaster Recovery (SYS-021)
- [ ] 1.6.13 Documentar estratégia de backup
- [ ] 1.6.14 Configurar backup automático (pg_dump)
- [ ] 1.6.15 Documentar processo de restore
- [ ] 1.6.16 Testar restore em ambiente isolado
- [ ] 1.6.17 Definir RTO/RPO

### API Documentation (SYS-022)
- [ ] 1.6.18 Gerar OpenAPI spec do FastAPI
- [ ] 1.6.19 Setup Swagger UI em /docs
- [ ] 1.6.20 Documentar auth endpoints
- [ ] 1.6.21 Documentar rate limits

### Data Retention (SYS-023)
- [ ] 1.6.22 Definir política de retenção de dados
- [ ] 1.6.23 Documentar dados coletados
- [ ] 1.6.24 Implementar cleanup de dados antigos
- [ ] 1.6.25 Configurar TTL para cache

### Docker Multi-stage (SYS-016)
- [ ] 1.6.26 Refatorar Dockerfile com multi-stage
- [ ] 1.6.27 Otimizar layers
- [ ] 1.6.28 Reduzir tamanho da imagem

## Critérios de Aceite

### CI/CD
- [ ] Pipeline executando em cada PR
- [ ] Lint + tests passando para merge
- [ ] Deploy automático para staging

### Observability
- [ ] Erros sendo capturados
- [ ] Alertas configurados
- [ ] Dashboard disponível

### Operações
- [ ] Backup documentado e testado
- [ ] Restore procedure funcionando
- [ ] API docs em /docs

## Definition of Done

1. [ ] CI/CD configurado e funcionando
2. [ ] Monitoring ativo
3. [ ] Backup testado
4. [ ] Documentação completa

## Dependencies

- **Bloqueada por:** Story 1.2 (Testes) - testes no CI
- **Bloqueia:** Nenhuma

## Notes

- Usar GitHub Actions (já integrado)
- Considerar self-hosted runner para custos
- Documentar everything no README.md
