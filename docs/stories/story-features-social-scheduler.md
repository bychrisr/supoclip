# Story: Social Scheduler & Calendar

- **Epic:** epic-features.md
- **Fase:** FASE 2 - Differentiation
- **Priority:** P0
- **Estimate:** 40h

## Problem

Usuários precisam agendar posts para redes sociais de forma estratégica, mas atualmente o SupoClip não oferece essa capacidade. Concorrentes como OpusClip e Real Oficial também não têm scheduler integrado, criando oportunidade de diferenciação para agencies e criadores de conteúdo que usam third-party tools (Later, Buffer, Hootsuite) manualmente.

## Solution

Implementar sistema de agendamento com calendar view onde usuários podem:
1. Visualizar clips gerados em calendar mensal/semanal
2. Arrastar e soltar para agendar post em data/hora específica
3. Conectar contas de redes sociais via OAuth para auto-posting (futuro FASE 4)
4. Receber notificações de reminder antes do horário agendado

## Scope

- **In:** Clips processados disponíveis na biblioteca do usuário
- **Out:** Direct posting para TikTok/Instagram/YouTube (FASE 4)

## Tasks

1. [ ] Database schema para scheduled_posts
2. [ ] API endpoints CRUD para scheduling
3. [ ] Calendar component React (month/week view)
4. [ ] Drag-and-drop para scheduling
5. [ ] Timezone handling (armazenar em UTC, exibir em local)
6. [ ] Reminder notifications (email/push)
7. [ ] UI para listar/editar/agendar clips

## Acceptance Criteria

- [ ] Calendar view mostra clips em timeline
- [ ] Usuário pode agendar clip para data/hora específica
- [ ] Scheduled posts aparecem em lista
- [ ] Timezone correta (usuários BR = UTC-3)
- [ ] Edit/cancel scheduling funcional
- [ ] Notificação reminder 1h antes do horário

## Dependencies

- Database schema updates (story-operations.md)
- Notification system (future)
- OAuth integrations (FASE 4)

---

*Story ID: FEATURES-SOCIAL-SCHEDULER*
*Created: 2026-04-14*