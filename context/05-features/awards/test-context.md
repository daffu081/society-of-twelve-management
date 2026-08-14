---
type: test-context
spec_version: 1
feature: awards
file_type: test-context
contract_version: 1
status: done
depends_on: [admin-access, members]
last_review: 2026-08-14
frozen: false
tags: [awards, test-context]
---

# Awards & Achievements — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 record an award | 🟢 manual | — |
| AC2 visibility control | 🟢 manual | — |

## Manual checks
- AC1: save an award linked to a member → all fields persist; the recipient shows the member's
  name; save one with a free recipient name → it persists too.
- AC2: a new award defaults to Hidden and is absent from public `awards.html`; set Public → it
  appears; set Hidden again → it disappears; anon queries return no hidden rows (RLS).
