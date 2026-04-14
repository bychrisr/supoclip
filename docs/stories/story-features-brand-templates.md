# Story: Brand Templates

- **Epic:** epic-features.md
- **Fase:** FASE 4 - Premium
- **Priority:** P2
- **Estimate:** 32h

## Problem

Agências precisam manter consistência de marca nos clips de múltiplos clientes. Templates genéricos não permitem branding customizado por cliente.

## Solution

Implementar brand templates:
- Logo overlay positioning
- Custom colors (hex codes)
- Font family customization
- Intro/outro cards customizáveis
- Watermark removal por brand
- Template sharing por workspace

## Scope

- In: Template config + video
- Out: Branded video

## Tasks

1. [ ] Create brand template model
2. [ ] Implement logo overlay
3. [ ] Add custom colors support
4. [ ] Add custom font support
5. [ ] Create intro/outro cards
6. [ ] Add template sharing
7. [ ] Write integration tests

## Acceptance Criteria

- [ ] Logo overlay positioning works
- [ ] Custom colors aplicado
- [ ] Custom fonts applied
- [ ] Intro/outro cards funcionam
- [ ] Template sharing por workspace
- [ ] Tests: 90% coverage

## Dependencies

- FASE 1: Custom fonts, Animated captions
- FASE 3: Workspaces, Shared templates
- Template system (existing)