---
type: test-context
spec_version: 1
feature: profession-fee
file_type: test-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [profession-fee, test-context]
---

# Profession & Fee Management — test context

> No automated runner yet — manual checks (needs live Supabase with schema.sql + seed.sql + rls.sql applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 configure profession fees | 🟢 manual | — |
| AC2 custom fee per member | 🟢 manual | — |
| AC3 fee change doesn't rewrite history | 🟢 manual | — |
| Duplicate category rejected | 🟢 manual | — |

## Manual checks
- AC1: on `admin/settings.html`, edit Student's fee 50 → 60 and save → reload shows 60; add a new
  category → it appears in the member form's category select.
- AC2: on `admin/members.html`, give a member a custom fee → their record stores it; clearing it
  falls back to the category fee (coalesce rule).
- AC3: record a payment (payments feature) at fee 50, then change the category fee to 60 → the
  stored payment row still shows 50 (T4: compare exact decimal strings).
- Duplicate: adding a category with an existing name shows the unique-violation error.
