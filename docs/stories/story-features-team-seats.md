# Story: Team Seats

- **Epic:** epic-features.md
- **Fase:** FASE 3 - Team/Agency
- **Priority:** P0
- **Estimate:** 24h

## Problem

Currently, only workspace owners can access their workspaces. Agencies and teams need to invite team members to collaborate on clips and projects. Without team seats, agencies cannot:

- Add team members to client workspaces
- Manage access for designers and editors
- Control who can create/edit/view content
- Separate permissions by role

## Solution

Implement team seat management allowing workspace owners to invite up to 4 users per workspace (based on plan). Each seat can be assigned a role with specific permissions.

## Scope

- **In:** Existing workspace model, auth system
- **Out:** Advanced team analytics, external user invitations

### In Scope
- Invite team member API (email-based)
- Seat limit enforcement by plan
- Member list per workspace
- Remove member functionality
- Role assignment on invite

### Out of Scope
- Bulk import/export of members
- External guest accounts
- Team activity analytics (FASE 4)

## Tasks

1. [ ] Add workspace_members table with role column
2. [ ] Create invite endpoint (generates invite code)
3. [ ] Create accept invite endpoint
4. [ ] Implement seat limit checking in invite flow
5. [ ] Add member list endpoint per workspace
6. [ ] Create remove member endpoint
7. [ ] Add role validation middleware
8. [ ] Build team management UI in workspace settings
9. [ ] Add email notification for invites (future: can be stubbed)

## Acceptance Criteria

- [ ] Workspace owner can invite up to 4 team members
- [ ] Invitees receive and can accept invitation
- [ ] Each member has a role (admin, editor, viewer)
- [ ] Seat limits enforced based on plan
- [ ] Members can access workspace after accepting invite
- [ ] Owner can remove members
- [ ] API returns 403 when seat limit reached

## Dependencies

- Backend: FastAPI, SQLAlchemy (existing)
- Frontend: Next.js (existing)
- Database: PostgreSQL (existing)
- Plan: story-features-workspaces.md (workspace model required)