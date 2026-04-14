# Epic: Resolução de Débitos Técnicos - SupoClip

## Objetivo

Eliminar todos os 72 débitos técnicos identificados no assessment, garantindo:
- Segurança: RLS, rate limiting, credentials
- Qualidade: Testes automatizados, error handling
- Performance: Índices, normalização, queries
- Operações: CI/CD, backup, monitoring
- UX: A11y, server components, feedback

**Meta:** Transformar o SupoClip de MVP inseguro para produto pronto para escala.

## Escopo

### Débitos Incluídos (72 total)

| Área | Quantidade | Esforço |
|------|------------|----------|
| Sistema (SYS-*) | 24 | 179h |
| Database (DB-*) | 32 | 108h |
| Frontend/UX (UX-*) | 14 | 19.5h |
| **TOTAL** | **72** | **~306.5h** |

### Débitos Excluídos

Nenhum - todos os débitos validados serão endereçados.

## Critérios de Sucesso

### Métricas de Qualidade

- [ ] Pipeline CI/CD configurado com testes automatizados
- [ ] Cobertura mínima 40% em backend (pytest)
- [ ] Cobertura mínima 30% em frontend (Vitest)
- [ ] Security tests passam (RLS, rate limiting)
- [ ] Performance baseline: queries <100ms
- [ ] A11y audit passa (WCAG AA)
- [ ] Zero breaking changes em produção
- [ ] RLS ativo em todas as tabelas de usuário
- [ ] Rate limiting ativo na API pública
- [ ] Backup documentado e testado

### Definição de Done

1. Todos os débitos P0 resolvidos
2. Todos os testes passando
3. Code review aprovado
4. Documentação atualizada
5. Zero vulnerabilidades de segurança críticas

## Timeline

| Fase | Semanas | Stories | Esforço |
|------|---------|---------|---------|
| 1 | 1-2 | Segurança Crítica | ~42h |
| 2 | 3-4 | Testes Automatizados | ~40h |
| 3 | 5-8 | Database Quality | ~80h |
| 4 | 9-10 | Backend Quality | ~64h |
| 5 | 11-12 | Frontend Server + A11y | ~24h |
| 6 | 13-14 | Operações | ~32h |
| 7 | 15-16 | UX/UI Finalização | ~24h |
| **TOTAL** | **16 semanas** | **7 stories** | **~306.5h** |

## Budget

| Categoria | Estimativa |
|-----------|------------|
| Desenvolvimento | 250h |
| Code Review | 32h |
| Testing/QA | 24.5h |
| **TOTAL** | **~306.5h** |

---

## Stories

### Story 1.1: Segurança Crítica
**Arquivo:** `docs/stories/story-security-critical.md`

Resolver débitos críticos de segurança:
- RLS em tasks, sources, generated_clips
- Rate limiting com tabela user_limits
- Remoção de credenciais hardcoded
- Security headers

**P0 Débitos:** DB-029, DB-030, DB-031, DB-019, SYS-007, SYS-008, SYS-024  
**Esforço:** ~42h  
**Responsável:** @dev + @data-engineer

---

### Story 1.2: Testes Automatizados
**Arquivo:** `docs/stories/story-tests-automation.md`

Setup completo de testes:
- pytest para backend
- Vitest para frontend
- E2E tests básico

**P0 Débitos:** SYS-001  
**Esforço:** ~40h  
**Responsável:** @qa + @dev

---

### Story 1.3: Database Quality
**Arquivo:** `docs/stories/story-database-quality.md`

Índices, normalização e migrations:
- Índices em todas as tabelas
- Normalização de generated_clips_ids
- Versionamento de migrations
- Unificação de schema

**P1 Débitos:** DB-002, DB-004, DB-005, DB-010, DB-011, DB-012, DB-013, DB-015, DB-016, DB-017, DB-018, DB-020, DB-021, DB-022, DB-024, DB-032, DB-033, DB-034 + DB-003, DB-023  
**Esforço:** ~80h  
**Responsável:** @data-engineer + @dev

---

### Story 1.4: Backend Quality
**Arquivo:** `docs/stories/story-backend-quality.md`

Qualidade de código backend:
- Custom exceptions com error codes
- Audit de cláusulas except
- Validação de env vars
- Queries parametrizadas
- Remoção de código duplicado

**P1 Débitos:** SYS-002, SYS-006, SYS-011, SYS-012, SYS-014, SYS-017, SYS-018  
**Esforço:** ~64h  
**Responsável:** @dev + @architect

---

### Story 1.5: Frontend Server Components
**Arquivo:** `docs/stories/story-frontend-server.md`

Migração para Server Components:
- Remover "use client" desnecessário
- Loading states robustos
- Error handling correto

**P1 Débitos:** UX-001, UX-008, UX-009  
**Esforço:** ~24h  
**Responsável:** @dev

---

### Story 1.6: Operações
**Arquivo:** `docs/stories/story-operations.md`

Infraestrutura e operações:
- CI/CD pipeline
- Backup/Disaster Recovery
- Monitoring/Alerting
- API Documentation
- Data Retention Policy

**P2 Débitos:** SYS-019, SYS-020, SYS-021, SYS-022, SYS-023, SYS-016  
**Esforço:** ~32h  
**Responsável:** @devops

---

### Story 1.7: UX/UI A11y e Estados
**Arquivo:** `docs/stories/story-ux-ui-final.md**

Acessibilidade e UX:
- aria-labels em botões icon
- Keyboard navigation
- Empty states actionáveis
- Toast notifications
- Validação inline
- Bloqueio de double-submit

**P2 Débitos:** UX-002, UX-003, UX-004, UX-005, UX-007, UX-010, UX-011, UX-012, UX-013, UX-014, UX-015  
**Esforço:** ~24h  
**Responsável:** @ux-design-expert + @dev

---

## Riscos e Mitigações

| Risco | Mitigação |
|-------|-----------|
| RLS que quebra queries existentes | Testar TODAS queries antes de ativar |
| Schema sync breaking | Manter Prisma como source of truth |
| Testes quebrando durante refatoração | Usar mocks de dependências |
| Frontend-Backend contract breaking | Sincronizar normalização DB com API |

---

## Dependencies

- **Bloqueada por:** Nenhuma (começa immediately)
- **Bloqueia:** Nenhuma

---

## Metadata

| Campo | Valor |
|-------|-------|
| Total Débitos | 72 |
| Esforço Total | ~306.5h |
| P0 (Crítico) | 10 |
| P1 (Alto) | 22 |
| P2 (Médio) | 26 |
| P3 (Baixo) | 14 |
| Status | READY FOR PLANNING |
| Criado em | 2026-04-14 |
| Criado por | @pm (Morgan) |
