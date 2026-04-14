# Story: Team Workspaces & Collaboration

## Problem

Agências e times precisam gerenciar múltiplos clientes/projetos:
- **OpusClip**: Team workspaces básico (apenas Pro tier, 2-4 seats)
- **Vizard**: 20 seats, mas sem sub-workspaces por cliente
- **VidRush**: Multi-workspace disponível
- **Nenhum**: Suporta sub-workspaces por cliente para agencies

O SupoClip pode capturar o mercado de agencies com workspaces isolados por cliente — cada cliente com seu próprio espaço, billing e configurações.

## Solution

Implementar sistema de workspaces hierárquicos:
- Workspace principal (organization)
- Sub-workspaces por cliente/projeto
- Roles e permissões granulares
- Billing separado por sub-workspace

## Competitor Reference

- **Vizard**: Team collaboration, 20 seats, brand kits
- **OpusClip**: Basic team workspaces (2-4 users)
- **Ssemble**: Collaborative editing básico
- **Real Oficial**: Sem features de team

## Scope

### In
- Organization (workspace principal)
- Sub-workspaces (clientes/projetos)
- Membros com roles (owner, admin, editor, viewer)
- Convite por email
- Billing por workspace
- Brand templates por workspace
- Asset library por workspace

### Out
- White-label custom domain — fase 2
- SSO/SAML — fase 2
- API access por workspace — fase 2
- Audit logs avançados — fase 2

## Tasks

1. **Data Model**
   - Tabela organizations
   - Tabela workspaces (sub-workspaces)
   - Tabela members com roles
   - Tabela invitations

2. **Workspace Management UI**
   - Dashboard de workspaces
   - Criar/editar workspace
   - Settings de workspace (name, logo, colors)

3. **Team Management**
   - Adicionar membros
   - Definir roles
   - Convite por email
   - Remove membro

4. **Permission System**
   - RBAC implementation
   - Middleware para verificar permissions
   - UI para permission matrix

5. **Billing Integration**
   - Associate subscription ao workspace
   - Usage tracking por workspace

6. **Brand Templates**
   - Upload de logo
   - Cores custom
   - Intro/outro templates

## Acceptance Criteria

- [ ] Criar organization (default workspace)
- [ ] Criar sub-workspaces (máx 10 no tier starter)
- [ ] Roles: owner, admin, editor, viewer
- [ ] Adicionar membro via email
- [ ] Convite expira em 7 dias
- [ ] Owner pode remover membros
- [ ] Editor pode criar clips
- [ ] Viewer pode apenas visualizar
- [ ] Cada workspace tem brand settings
- [ ] Billing separate por workspace

## Effort Estimate

**48 horas**
- Data Model: 8h
- Workspace UI: 12h
- Team Management: 10h
- Permissions: 8h
- Billing Integration: 6h
- Brand Templates: 4h

## Priority

**P1** — Importante para agencies, alto LTV. Diferencial vs OpusClip (sub-workspaces).

---

*Story ID: FEATURES-TEAM*
*Created: 2026-04-14*