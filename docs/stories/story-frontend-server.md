# Story 1.5: Frontend Server Components

## Epic
[epic-technical-debt.md](epic-technical-debt.md)

## Prioridade
**P1** — Alto

## Esforço
~24h

## Responsável
@dev

## Contexto

O frontend usa "use client" em quase todas as páginas, perdendo benefícios de Server Components:
- Loading mais lento
- Maior bundle size
- SEO reduzido

## Débitos Alocados

| ID | Débito | Esforço |
|----|--------|---------|
| UX-001 | Quase todas as páginas com "use client" | 4h |
| UX-008 | Error handling direto com alert() | 2h |
| UX-009 | Direct fetch calls sem loading robusto | 1h |

## Tasks

### Server Components (UX-001)
- [ ] 1.5.1 Audit de todos os componentes com "use client"
- [ ] 1.5.2 Identificar quais podem ser Server Components
- [ ] 1.5.3 Migrar TaskList para Server Component
- [ ] 1.5.4 Migrar TaskDetail para Server Component
- [ ] 1.5.5 Migrar LandingPage para Server Component
- [ ] 1.5.6 Migrar páginas de Auth (SignIn, SignUp)
- [ ] 1.5.7 Manter apenas "use client" onde necessário (interatividade)

### Error Handling (UX-008)
- [ ] 1.5.8 Criar componente ErrorBoundary
- [ ] 1.5.9 Substituir alert() por UI de erro adequada
- [ ] 1.5.10 Implementar ErrorBoundary nas páginas
- [ ] 1.5.11 Adicionar retry logic

### Loading States (UX-009)
- [ ] 1.5.12 Criar Suspense boundaries
- [ ] 1.5.13 Implementar loading.tsx em rotas
- [ ] 1.5.14 Melhorar skeletons existentes
- [ ] 1.5.15 Adicionar LoadingButton para submit

## Critérios de Aceite

### Performance
- [ ] Bundle size reduzido em >= 20%
- [ ] TTFB reduzido em >= 30%
- [ ] Server Components funcionando

### UX
- [ ] Zero alert() no código
- [ ] Loading states em todas as páginas
- [ ] Error states amigáveis

### SEO
- [ ] Meta tags em Server Components
- [ ] Semantic HTML
- [ ] Estrutura crawlável

## Definition of Done

1. [ ] Server Components migra dos
2. [ ] Zero alert() no código
3. [ ] Loading states robustos
4. [ ] Code review aprovado

## Dependencies

- **Bloqueada por:** Nenhuma
- **Bloqueia:** Story 1.7 (UX/UI Finalização)

## Notes

- Manter "use client" apenas onde necessário (eventos, state, hooks)
- Usar React Server Components (RSC) para data fetching
- Implementar Suspense com loaders apropriados
