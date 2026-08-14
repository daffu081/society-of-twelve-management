---
type: business-context
spec_version: 1
feature: bin
file_type: business-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-15
frozen: false
tags: [bin, business-context]
---

# Bin / Trash — business context

## Goal
Make important deletions recoverable for a limited window, with Super-Admin-only permanent removal.

## User stories
- US1: As a Super Admin, I can restore or permanently delete items in the Bin, so that I control recovery.
- US2: As the organization, eligible deleted records are cleaned up automatically after the window, so that the Bin doesn't grow forever.

## Business rules
- BR1: Important records use soft deletion — they move to the Bin instead of being removed.
- BR2: Deleted records remain recoverable for 30 days.
- BR3: Only a Super Admin has unrestricted restore and permanent-delete authority.
- BR4: Automated cleanup may permanently remove eligible records after the 30-day period.

## What this feature owns
- The Bin screen, restore/permanent-delete, and the scheduled cleanup.

## What this feature does NOT own
- Which record types are soft-deletable (each feature decides); the soft-delete write itself
  (each feature performs it via the ADR-003 pattern).

## Out of scope (not planned)
- Which record types are soft-deletable (defined by each feature).

## Acceptance criteria

### AC1: Deleted items are recoverable
- **Trace**: US1, BR1, BR2, BR3
- **Given**: a soft-deleted record in the Bin
- **When**: a Super Admin views the Bin within 30 days
- **Then**: they can restore it or permanently delete it, and non-Super-Admins cannot.

### AC2: Automatic cleanup after 30 days
- **Trace**: US2, BR4
- **Given**: a record deleted more than 30 days ago
- **When**: the cleanup runs
- **Then**: the eligible record is permanently removed automatically.

### Edge & error cases
- Non-Super-Admins cannot open the Bin or read/restore/purge its rows.
- Restoring re-creates the record from its snapshot; the Bin row is then removed.
