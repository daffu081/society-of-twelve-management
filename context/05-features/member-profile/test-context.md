---
type: test-context
spec_version: 1
feature: member-profile
file_type: test-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-13
frozen: false
tags: [member-profile, test-context]
---

# Member profile — test context

> No automated runner yet — manual checks.

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 blood group captured at registration | ⬜ unverified (needs live Supabase) | — |
| AC2 blood group shown on profile | ⬜ unverified (needs live Supabase) | — |

## Manual checks
- AC1: on `admin/members.html`, add a member with a blood group selected → "Member saved" shows.
- AC2: the members list row for that member shows the saved blood group.

## Rules for writing new tests
- Use a throwaway Supabase project; clean up test members (or use `bin`).
