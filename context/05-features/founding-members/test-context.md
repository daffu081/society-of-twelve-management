---
type: test-context
spec_version: 1
feature: founding-members
file_type: test-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [founding-members, test-context]
---

# Founding Members — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 manage founding members | 🟢 manual | — |

## Manual checks
- AC1: add a founding member with photo URL, role and bio → all persist, round-trip through
  edit, and the entry appears on public `founding-members.html`; an admin without
  `committee_write` gets an RLS rejection on save.
