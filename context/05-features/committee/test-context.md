---
type: test-context
spec_version: 1
feature: committee
file_type: test-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [committee, test-context]
---

# Executive Committee — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 manage committee entries | 🟢 manual | — |
| AC2 ordered public display | 🟢 manual | — |
| Hidden entries stay private | 🟢 manual | — |

## Manual checks
- AC1: add a member with every field → all persist and round-trip through edit.
- AC2: give three members orders 2, 0, 1 → the public page shows them 0, 1, 2.
- Hidden: set an entry Hidden → it disappears from `committee.html`; anon queries return no
  hidden rows (RLS).
