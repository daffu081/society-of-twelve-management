---
type: test-context
spec_version: 1
feature: public-directory
file_type: test-context
contract_version: 1
status: done
depends_on: [members, member-profile]
last_review: 2026-08-14
frozen: false
tags: [public-directory, test-context]
---

# Public Member Directory — test context

> No automated runner yet — manual checks (needs live Supabase with schema.sql + rls.sql applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 member controls visibility | 🟢 manual | — |
| AC2 directory exposes only safe fields | 🟢 manual | — |
| Empty state / no-photo avatar | 🟢 manual | — |

## Manual checks
- AC1: on `member/profile.html`, tick "Show me on the public directory" and save → the member
  appears on `directory.html`; untick and save → they disappear.
- AC2: on `directory.html` a listed member shows only photo, name, profession, short bio. Query
  `members_public` as anon → the private/contact/fee columns are not present, so none is retrievable.
- Empty/avatar: with no opted-in members the page shows an empty state; a member without a
  `photo_url` renders a name-initial avatar.

## Rules for writing new tests
- Use a throwaway Supabase project; never expose real member data.
