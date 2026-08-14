---
type: technical-context
spec_version: 1
feature: founding-members
file_type: technical-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [founding-members, technical-context]
---

# Founding Members — technical context

## Public surface
**Depends on:** admin-access; executive-admins (`committee_write` key — same custodians as the
committee roster, no separate key in the BR4 catalog).
**Exposed to:** public-site (`founding-members.html` reads the table).

**Exposes:**
```
public.founding_members  -- table; anon read-all; writes need committee_write
```
**Callers MUST NOT:** bypass the permission key for writes.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Manage founding members + public page | AC1 | ✅ built | needs live Supabase to verify |

## Logic
- `admin/founding-members.html`: guarded; add/edit form (name, historical role, photo URL,
  display order, short bio).
- `founding-members.html` (public): card grid ordered by `display_order` then name.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/founding-members.html` | Founding-member management |
| `founding-members.html` | Public founders page |
| `supabase/schema.sql` | `founding_members` table |
| `supabase/rls.sql` | founding-members policies |

## API / data contracts
- Select (public) / keyed insert/update on `founding_members`.

## Known issues
- Photo is a URL field until the storage split (T25).
