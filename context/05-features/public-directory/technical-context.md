---
type: technical-context
spec_version: 1
feature: public-directory
file_type: technical-context
contract_version: 1
status: done
depends_on: [members, member-profile]
last_review: 2026-08-14
frozen: false
tags: [public-directory, technical-context]
---

# Public Member Directory — technical context

## Public surface
**Depends on:** members / member-profile (the `members` table + `show_on_public_directory` flag,
and the members self-edit path that lets a member toggle it).
**Exposed to:** public-site (may link to / embed the directory).

**Exposes:**
```
public.members_public   -- view: name, profession, short_bio, photo_url
                        -- rows: show_on_public_directory = true AND active = true
                        -- granted to anon + authenticated
```
**Callers MUST NOT:** query the base `members` table from public pages; add any private/contact/
finance column to `members_public`.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Member controls public visibility (opt-in toggle) | AC1 | ✅ built | toggle on member/profile.html; guard trigger allows the flag |
| Safe public view + directory page | AC2 | ✅ built | `members_public` view + `directory.html` read only that view |

## Logic
- `members_public` (in `rls.sql`) selects only the four safe columns for opted-in, active members;
  security_definer so anon can read it without any base-table access.
- `directory.html` reads `members_public` and renders a card grid (photo or name-initial avatar).
- `member/profile.html` has a "Show me on the public directory" checkbox; the members self-edit
  guard trigger no longer reverts `show_on_public_directory`, so the member owns their visibility.

## Code file mapping
| File | Purpose |
|---|---|
| `directory.html` | Public directory page — reads only `members_public` |
| `supabase/rls.sql` | `members_public` safe view + anon grant; guard trigger permits the opt-in flag |
| `member/profile.html` | Opt-in toggle in the member self-edit form |
| `supabase/schema.sql` | `members.show_on_public_directory boolean default false` (pre-existing) |

## API / data contracts
- `select * from members_public` (anon) — returns only safe fields for opted-in members.

## Known issues
- "Approved short bio" has no separate approval state — the member's `short_bio` is shown as
  entered. Add a moderation flag if the society later needs pre-publication review.
