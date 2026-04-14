# Story: Client Sub-Workspaces

- **Epic:** epic-features.md
- **Fase:** FASE 3 - Team/Agency
- **Priority:** P1
- **Estimate:** 32h

## Problem

Agencies managing multiple clients need to provide isolated workspaces for each client while maintaining control. Currently, all client content lives in the same workspace, making it difficult to:

- Separate content by client
- Control what each client can see
- Bill clients for their specific usage
- Provide client-facing portal for preview
- Maintain brand separation between clients

## Solution

Implement hierarchical workspaces allowing agencies to create sub-workspaces under their main workspace. Each sub-workspace acts as an independent environment but inherits some settings from the parent.

## Scope

- **In:** Multi-workspace system, RBAC
- **Out:** Cross-workspace sharing, client billing API

### In Scope
- Sub-workspace creation (max 10 per parent)
- Parent-child workspace relationship
- Sub-workspace admin (client) can manage their space
- Usage tracking per sub-workspace
- Sub-workspace deletion handling

### Out of Scope
- Client billing and invoicing
- Client-facing login portal
- Cross-workspace content sharing

## Tasks

1. [ ] Add parent_workspace_id to workspace table
2. [ ] Implement sub-workspace creation with validation
3. [ ] Create sub-workspace list endpoint (child workspaces)
4. [ ] Add sub-workspace quota enforcement
5. [ ] Implement sub-workspace ownership transfer
6. [ ] Add sub-workspace usage aggregation for parent
7. [ ] Build sub-workspace switcher UI
8. [ ] Add sub-workspace deletion with content cleanup
9. [ ] Add parent workspace can view all children setting

## Acceptance Criteria

- [ ] Agency can create up to 10 sub-workspaces
- [ ] Each sub-workspace has its own team and content
- [ ] Sub-workspace admin can be assigned per workspace
- [ ] Usage tracked per sub-workspace
- [ ] Deleting parent workspace removes sub-workspaces
- [ ] Sub-workspace appears in workspace switcher
- [ ] API enforces sub-workspace limits

## Dependencies

- Backend: FastAPI, SQLAlchemy (existing)
- Frontend: Next.js (existing)
- Database: PostgreSQL (existing)
- Plan: story-features-workspaces.md, story-features-team-seats.md