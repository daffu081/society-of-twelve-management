---
type: test-context
spec_version: 1
feature: members
file_type: test-context
contract_version: 1
status: planned
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [members, test-context]
---

# members — test context

> No automated runner yet — manual checks (needs live Supabase).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC4 manage roster (create/edit/activate) | 🟢 manual | — |
| AC5 list, search, filter | 🟢 manual | — |
| AC1/AC2/AC3 | ⬜ AC1/AC3 met by roster form; AC2 is public-directory (T03) | — |

## Manual checks
- AC4: create a member, edit them, toggle active→inactive→active → each change saves; no member is ever deleted.
- AC5: type a name/ID/mobile fragment → the list narrows; pick a status or profession filter → only matching members show; combine both.
