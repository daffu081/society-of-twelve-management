---
type: business-context
spec_version: 1
feature: rules
file_type: business-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [rules, business-context]
---

# Rules & Regulations — business context

## Goal
Give the organization a dedicated Rules & Regulations section that the Super Admin maintains.

## User stories
- US1: As a Super Admin, I can create, edit, publish and archive rules, so that members always see current regulations.

## Business rules
- BR1: There is a dedicated Rules & Regulations section.
- BR2: Only the Super Admin can create, edit, publish and archive rules.
- BR3: Version/history is supported where practical.

## What this feature owns
- Rules content, lifecycle and version history.

## What this feature does NOT own
- The public rules page layout (public-site).

## Out of scope (not planned)
- The public rules page layout (covered by public-site).

## Acceptance criteria

### AC1: Manage rules
- **Trace**: US1, BR1, BR2
- **Given**: a Super Admin
- **When**: they create, edit, publish or archive a rule
- **Then**: the change is saved and published rules are visible to members/public.

### AC2: Version history
- **Trace**: BR3
- **Given**: a rule that has changed
- **When**: it is edited
- **Then**: prior versions/history are retained where practical.

### Edge & error cases
- Non-super admins cannot open the management screen; unpublished/archived rules stay private.
