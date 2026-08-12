---
type: business-context
spec_version: 1
feature: mahfil
file_type: business-context
contract_version: 1
status: planned
depends_on: [admin-access]
last_review: 2026-08-13
frozen: false
tags: [mahfil, business-context]
---

# Mahfil — business context

## Goal
Manage and showcase mahfil (community/religious gathering) events, running and previous.

## User stories
- US1: As an admin, I can add a mahfil with a status.
- US2: As a visitor, I see running and previous mahfil.

## Business rules
- BR1: A mahfil has a title and a status (default running).

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

### Edge & error cases
- Empty state shows nothing under Mahfil.
