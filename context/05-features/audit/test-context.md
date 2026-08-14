---
type: test-context
spec_version: 1
feature: audit
file_type: test-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-15
frozen: false
tags: [audit, test-context]
---

# Audit Logging — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 actions are logged | 🟢 manual | — |
| Super-Admin-only read | 🟢 manual | — |

## Manual checks
- AC1: as an admin, change a permission, edit a member, record a payment, add an expense, queue an
  SMS, soft-delete and restore a project → `admin/audit.html` shows one entry each with the actor's
  name, action, table, record id and (for updates) a field-level diff.
- Read gate: an executive opening `audit.html` sees the super-only message and a direct
  `select from audit_log` returns nothing (RLS).
