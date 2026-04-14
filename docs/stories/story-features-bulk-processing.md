# Story: Bulk Processing

- **Epic:** epic-features.md
- **Fase:** FASE 3 - Team/Agency
- **Priority:** P2
- **Estimate:** 24h

## Problem

Agencies processing multiple videos need to queue and process multiple clips at once. Currently, users must upload and process videos one at a time. Without bulk processing:

- Time wasted on repetitive manual steps
- Cannot process multiple client videos in batch
- No way to prioritize urgent clips in queue
- Limited visibility into batch progress

## Solution

Implement bulk upload and processing system allowing users to queue multiple videos for processing. The system processes videos sequentially or in parallel based on workspace plan.

## Scope

- **In:** Task queue system (ARQ), existing clip processing
- **Out:** Parallel processing across workspaces, batch templates

### In Scope
- Multi-file upload interface
- Bulk queue management
- Batch progress tracking
- Cancel individual items in batch
- Bulk processing status in task list
- Processing order/friority options

### Out of Scope
- Cross-workspace bulk processing
- Processing templates for bulk
- Automated bulk scheduling

## Tasks

1. [ ] Add bulk_upload endpoint accepting multiple files
2. [ ] Create bulk task tracking in database
3. [ ] Implement bulk queue in ARQ worker
4. [ ] Add bulk progress API (overall + individual)
5. [ ] Build bulk upload UI component
6. [ ] Add cancel individual item endpoint
7. [ ] Implement bulk status in task list
8. [ ] Add processing order options (sequential/priority)
9. [ ] Add bulk completion notification

## Acceptance Criteria

- [ ] Users can upload up to 10 videos in one batch
- [ ] Bulk progress shows overall completion percentage
- [ ] Individual items can be cancelled mid-processing
- [ ] Bulk tasks appear in task list with batch indicator
- [ ] Processing completes sequentially by default
- [ ] Bulk upload shows estimated time based on queue
- [ ] API returns batch status and progress

## Dependencies

- Backend: FastAPI, ARQ workers (existing)
- Frontend: Next.js (existing)
- Database: PostgreSQL (existing)
- Plan: story-features-social-scheduler.md (task queue base)