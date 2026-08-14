---
type: test-context
spec_version: 1
feature: bin
file_type: test-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-15
frozen: false
tags: [bin, test-context]
---

# Bin / Trash — test context

> No automated runner yet — manual checks (AC2 needs the cleanup function deployed with
> CRON_SECRET).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 recoverable Bin | 🟢 manual | — |
| AC2 automatic 30-day cleanup | 🟢 manual | — |
| Super-Admin-only | 🟢 manual | — |

## Manual checks
- AC1: soft-delete a project (projects page) → it appears in `admin/bin.html`; Restore → the
  project returns intact and the Bin row is gone; Delete-forever → the row is removed and cannot
  be restored.
- AC2: insert a bin row with `expires_at` in the past → invoke `cleanup-bin` with the CRON_SECRET
  → the row is purged and the response reports the count; a not-yet-expired row survives.
- Access: an executive opening `bin.html` sees the super-only message; direct select/delete on
  `bin` returns nothing / is rejected (RLS).
