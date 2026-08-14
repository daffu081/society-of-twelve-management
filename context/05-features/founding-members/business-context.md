---
type: business-context
spec_version: 1
feature: founding-members
file_type: business-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [founding-members, business-context]
---

# Founding Members — business context

## Goal
Let admins maintain founding-member records shown publicly with their historical role.

## User stories
- US1: As an admin, I can maintain founding-member records, so that the organization's founders are recognized publicly.

## Business rules
- BR1: A founding-member record has photo, name, historical role and short biography.

## What this feature owns
- The founding-member records and their public page.

## What this feature does NOT own
- Executive committee (separate feature).

## Out of scope (not planned)
- Executive committee (separate feature).

## Acceptance criteria

### AC1: Manage founding members
- **Trace**: US1, BR1
- **Given**: an admin
- **When**: they add or edit a founding member
- **Then**: photo, name, historical role and short biography are saved and shown on the public founding-members page.

### Edge & error cases
- Empty roster shows an empty state; a founder without a photo gets a name-initial avatar.
