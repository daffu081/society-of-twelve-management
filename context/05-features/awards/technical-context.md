---
type: technical-context
spec_version: 1
feature: awards
file_type: technical-context
contract_version: 1
status: done
depends_on: [admin-access, members]
last_review: 2026-08-14
frozen: false
tags: [awards, technical-context]
---

# Awards & Achievements — technical context

## Public surface
**Depends on:** admin-access; members (optional `member_id` link); executive-admins
(`awards_read`/`awards_write` keys).
**Exposed to:** public-site (`awards.html` reads visible rows).

**Exposes:**
```
public.awards   -- table; anon sees visible = true only (RLS);
                -- recipient_name is a display snapshot (anon cannot join members)
```
**Callers MUST NOT:** join `members` from public pages (RLS blocks it) — use `recipient_name`.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Record award (full fields, optional member) | AC1 | ✅ built | needs live Supabase to verify |
| Admin-controlled public visibility | AC2 | ✅ built | RLS-enforced, default hidden |

## Logic
- `admin/awards.html`: guarded; member select (or free recipient name), date, image/document URL,
  description, Public/Hidden control. On save the selected member's name is snapshotted into
  `recipient_name` so the public page can display it without a members join.
- `awards.html` (public): lists what RLS exposes (visible only), newest first.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/awards.html` | Award management + visibility |
| `awards.html` | Public visible-awards page |
| `supabase/schema.sql` | `awards` table |
| `supabase/rls.sql` | awards policies |

## API / data contracts
- Select (public, visible-only) / keyed insert/update on `awards`.

## Known issues
- Image/document is a URL field until the storage split (T25).
- `recipient_name` snapshot can drift if the member is later renamed; re-save the award to refresh.
