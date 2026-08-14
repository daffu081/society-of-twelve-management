---
type: business-context
spec_version: 1
feature: mahfil
file_type: business-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [mahfil, business-context]
---

# Mahfil — business context

## Goal
Manage and showcase mahfil (community/religious gathering) events, running and previous.

## User stories
- US1: As an admin, I can add a mahfil with a status.
- US2: As a visitor, I see running and previous mahfil.
- US3: As an admin, I can record a mahfil with full details and control its publication, so that it's documented and optionally shown publicly.

## Business rules
- BR1: A mahfil has a title and a status (default running).
- BR3: A mahfil has title, date, time, venue, description, image and publication status.
- BR4: Mahfil is managed by admins or authorized executives.
- BR5: A public mahfil page shows published mahfils.

## What this feature owns
- The `mahfils` table and mahfil CRUD.

## What this feature does NOT own
- Public rendering (feature `public-site`).

## Out of scope (not planned)
- Ticketing / attendance.

## Acceptance criteria

### AC1: Create mahfil with status
- **Trace**: US1, BR1
- **Given**: the mahfil admin page
- **When**: an admin adds a mahfil
- **Then**: it is stored with its status

### AC2: Shown on public site
- **Trace**: US2
- **Given**: mahfil exist
- **When**: a visitor opens the site
- **Then**: running and previous mahfil are listed

### AC3: Manage mahfil with full details
- **Trace**: US3, BR3, BR4
- **Given**: an admin or authorized executive
- **When**: they create or edit a mahfil
- **Then**: title, date, time, venue, description, image and publication status are saved.

### AC4: Public mahfil page
- **Trace**: US3, BR5
- **Given**: a published mahfil
- **When**: a visitor opens the public mahfil page
- **Then**: the published mahfil is shown.

### Edge & error cases
- Empty state shows nothing under Mahfil.
