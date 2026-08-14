---
type: business-context
spec_version: 1
feature: committee
file_type: business-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [committee, business-context]
---

# Executive Committee — business context

## Goal
Let admins maintain the executive committee roster shown publicly in a chosen order.

## User stories
- US1: As an admin, I can maintain committee members with their details and order, so that the public sees the current committee.

## Business rules
- BR1: A committee entry has photo, name, position, year, short biography, display order and public visibility.

## What this feature owns
- The committee roster and its public ordering/visibility.

## What this feature does NOT own
- Founding members (separate feature).

## Out of scope (not planned)
- Founding members (separate feature).

## Acceptance criteria

### AC1: Manage committee entries
- **Trace**: US1, BR1
- **Given**: an admin with committee permission
- **When**: they add or edit a committee member
- **Then**: photo, name, position, year, short biography, display order and public visibility are saved.

### AC2: Public committee display in order
- **Trace**: US1, BR1
- **Given**: committee entries marked public
- **When**: a visitor views the committee page
- **Then**: public entries are shown in the configured display order.

### Edge & error cases
- Hidden entries never appear publicly; empty roster shows an empty state.
