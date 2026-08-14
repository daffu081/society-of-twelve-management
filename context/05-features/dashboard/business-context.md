---
type: business-context
spec_version: 1
feature: dashboard
file_type: business-context
contract_version: 1
status: done
depends_on: [admin-access, members, payments, finance, due-payments, notices, projects, birthday]
last_review: 2026-08-14
frozen: false
tags: [dashboard, business-context]
---

# Admin Dashboard — business context

## Goal
Give admins an at-a-glance overview of the organization's health with key numbers and charts.

## User stories
- US1: As an admin, I can see key membership and money figures on one screen, so that I understand status quickly.
- US2: As an admin, I can see useful charts, so that I can spot trends.

## Business rules
- BR1: Each figure respects the viewer's permissions (e.g. finance figures only for finance-permitted admins).

## What this feature owns
- The dashboard's aggregate presentation (cards, charts, recents).

## What this feature does NOT own
- The underlying records (owned by their own features).

## Out of scope (not planned)
- The underlying records (owned by their own features).

## Acceptance criteria

### AC1: Summary figures
- **Trace**: US1, BR1
- **Given**: an admin on the dashboard
- **When**: it loads
- **Then**: it shows total members, active members, due members, monthly collection, total income, total expense, current balance, today's collection, recent payments, upcoming birthdays, recent notices and a project/activity summary.

### AC2: Charts
- **Trace**: US2
- **Given**: available data
- **When**: the dashboard loads
- **Then**: it shows useful charts for collection, income vs expense, professions and payment methods.

### Edge & error cases
- An admin without a figure's permission sees a "needs permission" note (or the card hidden), never the number.
- Empty datasets render "No data yet" charts.
