# Story: Role-Based Access Control (RBAC)

- **Epic:** epic-features.md
- **Fase:** FASE 3 - Team/Agency
- **Priority:** P0
- **Estimate:** 24h

## Problem

With team seats now available, agencies need granular control over what each team member can do. Currently there is no way to differentiate between workspace admins, content editors, and observers. Without RBAC:

- All workspace members have the same permissions
- Cannot restrict sensitive actions (billing, delete)
- Cannot create read-only access for stakeholders
- Risk of accidental data loss by non-admin members

## Solution

Implement a role-based permission system with three roles:

- **Admin:** Full access including billing, settings, member management, delete
- **Editor:** Can create, edit, and process clips; cannot manage members or billing
- **Viewer:** Read-only access to view and download clips only

## Scope

- **In:** Team seats system, workspace context
- **Out:** Custom permissions per resource, advanced audit logging

### In Scope
- Role enum (admin, editor, viewer)
- Permission check decorator/middleware
- Role-based UI element visibility
- API endpoint authorization
- Default role on invite

### Out of Scope
- Custom permission sets per user
- Resource-level permissions (per-clip)
- Audit logging of actions
- Two-factor authentication

## Tasks

1. [ ] Define role enum and permissions in backend
2. [ ] Create permission check decorator for API routes
3. [ ] Add role-based middleware for workspace context
4. [ ] Implement permission checks in all relevant endpoints
5. [ ] Create frontend permission hook (usePermission)
6. [ ] Add role-based UI component visibility
7. [ ] Update workspace member endpoints to check admin role
8. [ ] Add permission denied error handler
9. [ ] Document permission matrix

## Acceptance Criteria

- [ ] Admin can access all workspace features
- [ ] Editor cannot access member management or billing
- [ ] Viewer cannot create or edit clips
- [ ] API returns 403 for unauthorized actions
- [ ] UI hides elements based on user role
- [ ] Permission checks apply to all workspace resources
- [ ] Role displayed in team member list

## Dependencies

- Backend: FastAPI, SQLAlchemy (existing)
- Frontend: Next.js (existing)
- Database: PostgreSQL (existing)
- Plan: story-features-team-seats.md (member table required)