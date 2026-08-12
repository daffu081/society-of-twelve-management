---
type: test-context
spec_version: 1
feature: admin-access
file_type: test-context
contract_version: 1
status: in_progress
depends_on: []
last_review: 2026-08-13
frozen: false
tags: [admin-access, test-context]
---

# Admin access — test context

> No automated test runner exists yet — "tested" below means the documented manual check.

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 request login link | Manual only | — |
| AC2 active admin gets in | Manual only | — |
| AC3 non-admin rejected | Manual only | — |
| AC4 logout | Manual only | — |

## Manual checks
- AC1: submit a valid email → "Login link sent" message; check inbox.
- AC2: click link as a seeded active admin → dashboard shows name + role.
- AC3: log in as a user with no `admins` row → alert + bounce to login.
- AC4: click Logout → back at login, session cleared.

## Rules for writing new tests
- Use a throwaway Supabase project; never a real one.
- Seed an active admin + a non-admin user as fixtures.
