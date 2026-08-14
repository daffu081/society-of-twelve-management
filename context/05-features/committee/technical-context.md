---
type: technical-context
spec_version: 1
feature: committee
file_type: technical-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [committee, technical-context]
---

# Executive Committee — technical context

## Public surface
**Depends on:** admin-access; executive-admins (`committee_read`/`committee_write` keys).
**Exposed to:** public-site (`committee.html` reads visible rows).

**Exposes:**
```
public.committee_members  -- table; anon sees visible = true only (RLS);
                          -- ordered publicly by display_order, then name
```
**Callers MUST NOT:** show hidden entries publicly; bypass the permission keys.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Manage entries (full fields + order + visibility) | AC1 | ✅ built | needs live Supabase to verify |
| Ordered public display | AC2 | ✅ built | `order by display_order, name` |

## Logic
- `admin/committee.html`: guarded; add/edit form with display_order (integer) and a
  Visible/Hidden select; list sorted the same way the public page renders.
- `committee.html` (public): card grid of what RLS exposes (visible only), ordered by
  `display_order` then name; photo or name-initial avatar.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/committee.html` | Committee management + ordering |
| `committee.html` | Public ordered committee page |
| `supabase/schema.sql` | `committee_members` table |
| `supabase/rls.sql` | committee policies |

## API / data contracts
- Select (public, visible-only) / keyed insert/update on `committee_members`.

## Known issues
- Photo is a URL field until the storage split (T25); ordering is manual integers (drag-reorder
  only if the client asks).
