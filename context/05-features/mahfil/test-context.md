---
type: test-context
spec_version: 1
feature: mahfil
file_type: test-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [mahfil, test-context]
---

# mahfil — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC3 full details + publication | 🟢 manual | — |
| AC4 public page shows published only | 🟢 manual | — |
| AC1/AC2 status + public display | 🟢 manual | — |

## Manual checks
- AC3: save a mahfil with all fields → each persists and round-trips through edit; the Published
  toggle flips visibility.
- AC4: a published mahfil appears on public `mahfil.html` with date/time/venue; unpublish → it
  disappears; anon queries return no draft rows (RLS).
