---
type: business-context
spec_version: 1
feature: audit
file_type: business-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-15
frozen: false
tags: [audit, business-context]
---

# Audit Logging — business context

## Goal
Keep a trustworthy record of important administrative actions for accountability.

## User stories
- US1: As a Super Admin, I can review a log of important actions, so that I can audit who did what.

## Business rules
- BR1: Important administrative actions are logged.
- BR2: Each entry stores actor, action, timestamp, affected record and relevant old/new values where practical.
- BR3: At minimum, log permission changes, sensitive member changes, payments, finance, SMS sending, deletions and restorations.

## What this feature owns
- The audit trail and its Super-Admin viewer.

## What this feature does NOT own
- The actions themselves (owned by their features); exporting the audit log.

## Out of scope (not planned)
- Exporting the audit log (may be covered by reports later).

## Acceptance criteria

### AC1: Actions are logged
- **Trace**: US1, BR1, BR2, BR3
- **Given**: an admin performs a logged action (permission change, sensitive member change, payment, finance entry, SMS send, deletion or restoration)
- **When**: the action completes
- **Then**: an audit entry records actor, action, timestamp, affected record and old/new values where practical.

### Edge & error cases
- Non-Super-Admins cannot read the trail; a client cannot suppress an entry (DB triggers).
