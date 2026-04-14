# Story: Shared Templates

- **Epic:** epic-features.md
- **Fase:** FASE 3 - Team/Agency
- **Priority:** P1
- **Estimate:** 16h

## Problem

Currently, templates are user-specific. Agencies with multiple designers need to share consistent branding and styling across team members. Without shared templates:

- Each designer creates their own templates
- Inconsistent branding across client content
- Wasted time recreating templates for each user
- No way to enforce brand guidelines

## Solution

Implement workspace-level templates that are visible to all workspace members. Admins can create, edit, and delete shared templates, while editors and viewers can use them.

## Scope

- **In:** Workspace model, existing template system
- **Out:** Cross-workspace template sharing, template versioning

### In Scope
- Template visibility flag (personal vs workspace)
- Workspace template list endpoint
- Shared template CRUD for admins
- Template usage by workspace members
- Personal templates remain unaffected

### Out of Scope
- Template versioning and history
- Cross-workspace template export
- Template analytics
- Brand kit integration (FASE 4)

## Tasks

1. [ ] Add is_shared flag to templates table
2. [ ] Update template API to accept workspace_id
3. [ ] Create workspace templates endpoint
4. [ ] Implement shared template CRUD (admin only)
5. [ ] Add template visibility filter in list endpoint
6. [ ] Build shared templates section in UI
7. [ ] Add "create as shared" option in template editor
8. [ ] Update template duplication to respect workspace context

## Acceptance Criteria

- [ ] Admin can create shared templates visible to all members
- [ ] Editors and viewers can use shared templates
- [ ] Personal templates remain private
- [ ] Shared templates appear in workspace template list
- [ ] Only admins can edit/delete shared templates
- [ ] Users can switch between personal and workspace templates

## Dependencies

- Backend: FastAPI, SQLAlchemy (existing)
- Frontend: Next.js (existing)
- Database: PostgreSQL (existing)
- Plan: story-features-workspaces.md (workspace context)