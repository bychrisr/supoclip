# Story: SSO/SAML Enterprise Auth

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P3
- **Estimate:** 40h

## Problem

Empresas precisam de SSO/SAML para compliance e gestão centralizada de usuários. Auth atual não suporta enterprise identity.

## Solution

Implementar SSO/SAML:
- SAML 2.0 integration
- OIDC integration
- Custom identity provider support
- SCIM provisioning
- Role mapping
- Directory sync

## Scope

- In: Enterprise auth config
- Out: SSO login flow

## Tasks

1. [ ] Integrate SAML 2.0 provider
2. [ ] Integrate OIDC provider
3. [ ] Add custom IdP support
4. [ ] Implement SCIM provisioning
5. [ ] Add role mapping
6. [ ] Implement directory sync
7. [ ] Write integration tests

## Acceptance Criteria

- [ ] SAML login funciona
- [ ] OIDC login funciona
- [ ] Custom IdP support
- [ ] SCIM provisioning works
- [ ] Role mapping funciona
- [ ] Directory sync works
- [ ] Tests: 85% coverage

## Dependencies

- Better Auth (existing)
- SAML library
- OIDC library
- FASE 3: Workspaces, Role permissions