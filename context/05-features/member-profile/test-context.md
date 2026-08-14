---
type: test-context
spec_version: 1
feature: member-profile
file_type: test-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
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
| AC3 full profile captured + auto SOT#### id | 🟢 manual (needs live Supabase) | — |
| AC4 private identity fields hidden | 🟢 manual (needs live Supabase) | — |
| AC5 member self-service edit | 🟢 manual (needs live Supabase) | — |

## Manual checks
- AC1: on `admin/members.html`, add a member with a blood group selected → "Member saved" shows.
- AC2: the members list row for that member shows the saved blood group.
- AC3: register a member filling the full form → saved with an auto `SOT####` id; add a second →
  the id increments and never repeats. Click a row → the form loads it; change a field → "Member updated".
- AC4: query `members_self` (or the public directory) as a non-admin → `nid_number`,
  `birth_registration_id`, `passport_number` are absent; querying `members` as anon returns nothing.
- AC5: log into `member/profile.html` as a member, change skills/interests/bio → "Saved"; attempting
  to change identity/fee/status (e.g. via a crafted update) leaves those columns unchanged (guard trigger).

## Rules for writing new tests
- Use a throwaway Supabase project; clean up test members (or use `bin`).
