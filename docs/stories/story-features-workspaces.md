# Story: Multi-Workspace Support

- **Epic:** epic-features.md
- **Fase:** FASE 3 - Team/Agency
- **Priority:** P0
- **Estimate:** 40h

## Problem

Currently the system only supports single-user workspaces. Agencies and content teams need to manage multiple independent workspaces (one per client or project) while maintaining centralized billing and user management. Without multi-workspace support, users cannot:

- Separate content by client or project
- Apply different settings per workspace
- Manage access across multiple teams
- Track costs per workspace independently

## Solution

Implement multi-workspace architecture where users can create, manage, and switch between multiple workspaces. Each workspace operates as an isolated environment with its own:

- Projects and clips
- Team members
- Templates
- Billing and credits

## Scope

- **In:** User authenticated, existing user model
- **Out:** Workspace hierarchy, cross-workspace billing

### In Scope
- Workspace CRUD API
- Workspace switcher UI
- Workspace context in all API calls
- Default workspace per user
- Workspace list and detail endpoints

### Out of Scope
- Cross-workspace collaboration (future feature)
- Workspace hierarchy/deep nesting
- Consolidated billing across workspaces

## Tasks

1. [ ] Create workspace database table with migration
2. [ ] Add workspace_id to existing tables (projects, clips, tasks, templates)
3. [ ] Implement workspace API endpoints (create, list, update, delete)
4. [ ] Add workspace context middleware to extract workspace_id from request
5. [ ] Create workspace switcher component in frontend
6. [ ] Update all queries to filter by workspace_id
7. [ ] Add workspace owner/admin role logic
8. [ ] Implement workspace deletion with data handling
9. [ ] Add workspace limits based on plan

## Acceptance Criteria

- [ ] User can create up to 5 workspaces (free tier)
- [ ] User can switch between workspaces in UI
- [ ] All data is isolated per workspace
- [ ] API requires workspace_id context
- [ ] Workspace owner can manage workspace settings
- [ ] Deleting workspace removes all related data
- [ ] API returns 403 for unauthorized workspace access

## Dependencies

- Backend: FastAPI, SQLAlchemy (existing)
- Frontend: Next.js (existing)
- Database: PostgreSQL (existing)
- Plan: story-features-no-watermark.md (auth base)