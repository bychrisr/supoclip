# Story: Calendar View

- **Epic:** epic-features.md
- **Fase:** FASE 3 - Team/Agency
- **Priority:** P1
- **Estimate:** 16h

## Problem

With the social scheduler implemented in FASE 2, users need a visual way to see scheduled posts over time. Currently, scheduled posts are only visible in a list format, making it difficult to:

- Visualize content distribution over the month
- Identify scheduling conflicts
- Plan content calendar by date
- See which days have no scheduled content

## Solution

Implement a calendar view that displays scheduled posts on their scheduled dates. Users can switch between list and calendar views for scheduled content.

## Scope

- **In:** Social scheduler (FASE 2), scheduled_posts table
- **Out:** Drag-and-drop rescheduling, recurring posts

### In Scope
- Calendar component with month/week views
- Scheduled posts displayed on calendar
- Click on date to see posts for that day
- Switch between month and week views
- Today indicator
- Navigate between months
- Color coding by platform (TikTok, Instagram, YouTube)

### Out of Scope
- Drag-and-drop to reschedule
- Recurring/recurring post templates
- Calendar integration (Google, iCal)

## Tasks

1. [ ] Create calendar UI component (month and week views)
2. [ ] Implement scheduled posts fetch by date range
3. [ ] Add platform color coding
4. [ ] Build date click handler to show day details
5. [ ] Add month/week view toggle
6. [ ] Implement navigation (prev/next month)
7. [ ] Add today indicator and quick navigation
8. [ ] Integrate with existing scheduler list view
9. [ ] Responsive calendar design for mobile

## Acceptance Criteria

- [ ] Calendar displays scheduled posts on correct dates
- [ ] Users can navigate between months
- [ ] Clicking a date shows posts scheduled for that day
- [ ] Platform icons/colors differentiate post types
- [ ] Week view shows 7-day horizontal layout
- [ ] Today is highlighted
- [ ] Empty dates show no scheduled posts indicator

## Dependencies

- Backend: FastAPI (existing)
- Frontend: Next.js (existing)
- Plan: story-features-social-scheduler.md (scheduled_posts table)