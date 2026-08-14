---
type: technical-context
spec_version: 1
feature: member-profile
file_type: technical-context
contract_version: 2
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [member-profile, technical-context]
---

# Member profile — technical context

## Public surface
**Depends on:** admin-access (`checkAdminAccess()`, `supabaseClient` from `admin/admin.js`)
**Exposed to:** none
**Exposes:**
- `public.members_self` — Postgres view returning the logged-in member's own row with the three
  private identity fields excluded. Read by the member portal; safe for any authenticated member.
- `public.is_active_admin()` — SQL helper (true when the current auth user is an active admin);
  reusable by later RLS policies on other tables.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Blood group on registration form | AC1 | 🔄 built, unverified | needs live Supabase + real `config.js` creds |
| Blood group shown in members list | AC2 | 🔄 built, unverified | needs live Supabase |
| Full profile capture + edit + auto SOT#### id | AC3 | ✅ built | needs live Supabase to verify |
| Private identity fields hidden via RLS + `members_self` view | AC4 | ✅ built | needs live Supabase to verify |
| Member self-service edit (permitted fields only) | AC5 | ✅ built | needs live Supabase to verify |

## Logic
- `admin/members.html` guards with `checkAdminAccess()`, then:
  - a full registration/edit form captures the complete member record (identity, contact, fee,
    status, photo URL, education/skills/interests/bio, and the three private identity fields);
    insert relies on the `member_id` sequence default, edit updates by row `id`.
  - a list below renders `member_id`, `name`, `mobile`, `blood_group`, `active`; clicking a row
    loads it into the form for editing.
- `member/login.html` + `member/member.js` + `member/profile.html`: a member logs in by magic link
  on their email, reads their own row via `members_self` (private fields excluded), and edits only
  education / skills / interests / short_bio.
- `supabase/rls.sql`: RLS on `members` — admins full access, anon none; member self-update policy +
  a `before update` guard trigger that restores all non-permitted columns for non-admins.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/members.html` | Full registration/edit form + members list |
| `admin/dashboard.html` | Members card links here |
| `member/login.html` | Member magic-link login |
| `member/member.js` | Member Supabase client + own-row loader (`loadMemberSelf`) |
| `member/profile.html` | Member self-service profile view + permitted-field edit |
| `supabase/schema.sql` | full `members` columns + `members_member_id_seq` SOT#### id default |
| `supabase/rls.sql` | members RLS, `is_active_admin()`, `members_self` view, self-edit guard trigger |

## Known issues
- `photo_url` is a plain URL field; direct storage upload is deferred to the storage split (T25).
- Column-level SELECT on the base `members` table is not revoked for members — the private-field
  guarantee relies on members reading through `members_self`; base-table hardening is T25.
- RLS must be applied manually via the Supabase SQL editor (no migration framework — D5).
