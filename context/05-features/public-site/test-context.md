---
type: test-context
spec_version: 1
feature: public-site
file_type: test-context
contract_version: 1
status: in_progress
depends_on: []
last_review: 2026-08-13
frozen: false
tags: [public-site, test-context]
---

# Public site — test context

> No automated runner yet — manual checks.

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 homepage renders | ✅ verified (static, by inspection) | — |
| AC2 footer year current | ✅ verified (static, by inspection) | — |
| AC3 footer credit + branding | ✅ verified (static, by inspection) | — |

## Manual checks
- AC1: open `/` → all sections visible.
- AC2: footer shows the current year.
- AC3: footer shows "Developed By Sabbir Ahmed Sakib" and the SOT logo/branding is present.

## Rules for writing new tests
- Once dynamic content lands, stub the Supabase reads.
