---
type: test-context
spec_version: 1
feature: executive-admins
file_type: test-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [executive-admins, test-context]
---

# executive-admins — test context

> No automated runner yet — manual checks (needs live Supabase with rls.sql applied and one
> seeded Super Admin row).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC4 granular permissions enforced | 🟢 manual | — |
| AC5 last Super Admin protected | 🟢 manual | — |
| AC1–AC3 add/permissions/deactivate | 🟢 manual | — |
| Non-super blocked from the screen | 🟢 manual | — |

## Manual checks
- AC4: grant an executive only `members_read` → they can list members but an attempted insert
  (e.g. direct PostgREST call) is rejected by RLS; grant `members_write` → the insert succeeds.
  Repeat for `finance_read` vs the finance page.
- AC5: with one active Super Admin, try deactivating them / demoting to executive / deleting the
  row → each fails with the guard error; add a second super → the first can then be demoted.
- AC1–AC3: add an executive → row appears active with `{}` permissions; check keys and save →
  jsonb matches exactly; set Inactive → their login gate rejects them.
- Access: an executive opening `executives.html` sees the "Super Admin only" message and RLS
  returns only their own row.
