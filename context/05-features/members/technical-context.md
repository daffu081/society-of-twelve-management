---
type: technical-context
spec_version: 1
feature: members
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [members, technical-context]
---

# members — technical context

## Public surface
**Depends on:** admin-access; shares the `members` table with `member-profile`.
**Exposed to:** <!-- filled when consumers appear -->

**Exposes:** nothing programmatic — an admin page. Roster reads/writes go through
`admin/members.html` on the `members` table, guarded by `checkAdminAccess()`.

**Callers MUST NOT:** bypass `checkAdminAccess()`; hard-delete rows; use floats for money.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Create / edit member (full form) | AC1, AC4 | ✅ built | shared form with member-profile T01 |
| Activate / deactivate (no history loss) | AC4 | ✅ built | active flag; no delete path |
| List, search (name/ID/mobile) + status/profession filter | AC3, AC5 | ✅ built | client-side over the loaded roster |
| Public-directory consent | AC2 | ⬜ planned | owned by public-directory (T03) |

## Code file mapping
| File | Purpose |
|---|---|
| `admin/members.html` | Roster: full create/edit form + list with search + status/profession filters |
| `supabase/schema.sql` | `members` table + `active` flag + search indexes (active/profession/name) |
| `supabase/rls.sql` | `members_admin_all` policy enforces active-admin read/write |

## API / data contracts
- Supabase selects/inserts/updates on `members`, guarded by `checkAdminAccess()`.
- No `DELETE` — members are deactivated, never removed (BR5/BR6).

## Known issues
- Search/filter is client-side over the full roster (fine for a small society; see `ponytail:` note in `schema.sql`).
- Capability-level `members.read`/`members.write` enforcement (vs. blanket active-admin) is deferred to the executive permission matrix (T09).
