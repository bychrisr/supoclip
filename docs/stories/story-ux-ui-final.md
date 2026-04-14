# Story 1.7: UX/UI A11y e Estados

## Epic
[epic-technical-debt.md](epic-technical-debt.md)

## Prioridade
**P2** — Médio

## Esforço
~24h

## Responsável
@ux-design-expert + @dev

## Contexto

Débitos de acessibilidade e experiência do usuário:
- Botões sem aria-labels
- Navegação por teclado incompleta
- Empty states não actionáveis
- Sem feedback de operações

## Débitos Alocados

| ID | Débito | Esforço |
|----|--------|---------|
| UX-002 | Inconsistent loading states | 1h |
| UX-003 | Empty state faltando em task edit | 1h |
| UX-004 | Botões icon sem aria-label | 2h |
| UX-005 | Phone preview hidden em mobile | 0.5h |
| UX-007 | Inconsistent button styles | 1h |
| UX-010 | Landing page heavy em client-side animations | 1h |
| UX-011 | Ausência de toast/notification | 1h |
| UX-012 | Empty state genérico não actionável | 1h |
| UX-013 | Sem validação inline em formulários | 1h |
| UX-014 | Loading states não bloqueiam interação durante submit | 1h |
| UX-015 | Falta de keyboard navigation em task detail | 2h |

## Tasks

### A11y - Aria Labels (UX-004, UX-015)
- [ ] 1.7.1 Audit de todos os botões icon
- [ ] 1.7.2 Adicionar aria-label em edit, delete, download
- [ ] 1.7.3 Implementar keyboard navigation em TaskDetail
- [ ] 1.7.4 Adicionar focus indicators visíveis
- [ ] 1.7.5 Testar com screen reader

### Empty States (UX-003, UX-012)
- [ ] 1.7.6 Criar EmptyState component reutilizável
- [ ] 1.7.7 Adicionar EmptyState em TaskEdit
- [ ] 1.7.8 Adicionar EmptyState em TaskList
- [ ] 1.7.9 Incluir actionable content (CTA buttons)
- [ ] 1.7.10 Adicionar EmptyState em Sources

### Toast Notifications (UX-011)
- [ ] 1.7.11 Criar Toast component
- [ ] 1.7.12 Implementar toast context/hook
- [ ] 1.7.13 Adicionar toast em operações (create, update, delete)
- [ ] 1.7.14 Configurar toast types (success, error, info)
- [ ] 1.7.15 Adicionar auto-dismiss

### Loading States (UX-002, UX-014)
- [ ] 1.7.16 Padronizar skeleton components
- [ ] 1.7.17 Adicionar skeleton em TaskEdit
- [ ] 1.7.18 Criar LoadingButton component
- [ ] 1.7.19 Bloquear interação durante submit (disabled + loading)
- [ ] 1.7.20 Adicionar loading em task list pagination

### Form Validation (UX-013)
- [ ] 1.7.21 Implementar inline validation em SignIn
- [ ] 1.7.22 Implementar inline validation em SignUp
- [ ] 1.7.23 Adicionar real-time validation (email, password)
- [ ] 1.7.24 Mostrar mensagens de erro específicas
- [ ] 1.7.25 Adicionar validation em TaskForm

### Button Consistency (UX-007)
- [ ] 1.7.26 Audit de button styles
- [ ] 1.7.27 Criar Button variants (primary, secondary, ghost)
- [ ] 1.7.28 Padronizar sizes (sm, md, lg)
- [ ] 1.7.29 Aplicar consistentemente

### Mobile (UX-005)
- [ ] 1.7.30 Mostrar phone preview em mobile (breakpoint)
- [ ] 1.7.31 Testar responsividade
- [ ] 1.7.32 Ajustar layout para mobile

### Animations (UX-010)
- [ ] 1.7.33 Reduzir client-side animations na landing
- [ ] 1.7.34 Usar CSS animations vs JS
- [ ] 1.7.35 Adicionar prefers-reduced-motion

## Critérios de Aceite

### A11y
- [ ] WCAG AA audit passando
- [ ] Zero aria-labels faltando
- [ ] Keyboard navigation funcionando

### UX
- [ ] Empty states com CTAs
- [ ] Toasts em todas operações
- [ ] Loading states consistentes
- [ ] Form validation inline

### Mobile
- [ ] Phone preview visível em mobile
- [ ] Layout responsivo
- [ ] Touch targets adequados

## Definition of Done

1. [ ] WCAG AA audit passando
2. [ ] Todos os states implementados
3. [ ] Code review aprovado
4. [ ] Testado com screen reader

## Dependencies

- **Bloqueada por:** Story 1.5 (Frontend Server)
- **Bloqueia:** Nenhuma

## Notes

- Usar radix-ui ou headlessui para componentes acessíveis
- Testar com NVDA, VoiceOver
- Follow prefers-reduced-motion
