---
type: technical-context
spec_version: 1
feature: member-profile
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-13
frozen: false
tags: [member-profile, technical-context]
---

# Member profile — technical context

## Public surface
**Depends on:** admin-access (`checkAdminAccess()`, `supabaseClient` from `admin/admin.js`)
**Exposed to:** none
**Exposes:** nothing programmatic — an admin page.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Blood group on registration form | AC1 | 🔄 built, unverified | needs live Supabase + real `config.js` creds |
| Blood group shown in members list | AC2 | 🔄 built, unverified | needs live Supabase |

## Logic
- `admin/members.html` guards with `checkAdminAccess()`, then:
  - a registration form (name, mobile, blood group) inserts into `members` with an auto `member_id` (`SOT####`).
  - a list below renders each member's `member_id`, `name`, `blood_group` (the profile display for AC2).

## Code file mapping
| File | Purpose |
|---|---|
| `admin/members.html` | Registration form + members list (blood group capture + display) |
| `admin/dashboard.html` | Members card links here |
| `supabase/schema.sql` | `members.blood_group text` (+ idempotent `alter table ... add column if not exists`) |

## Known issues
- `member_id` is count-based and races under concurrent adds — proper `SOT####` sequencing belongs to the `members` feature when it is built (see `ponytail:` note in `members.html`).
- No Postgres RLS on `members` yet — inherits the admin-access RLS gap (ADR-001).
