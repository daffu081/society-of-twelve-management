---
type: test-context
spec_version: 1
feature: _cross-cutting
file_type: test-context
contract_version: 1
status: done
depends_on: []
last_review: 2026-08-13
frozen: false
tags: [_cross-cutting, test-context]
---

# Cross-cutting — test context

> No automated runner yet — manual checks.

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 no secret credentials in the public website | ✅ verified (by inspection) | — |

## Manual checks
- AC1: inspect `config.js` and all committed front-end files → only `SUPABASE_URL` + `SUPABASE_ANON_KEY` (public) present; no service-role key or other secret.
