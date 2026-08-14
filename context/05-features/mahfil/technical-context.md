---
type: technical-context
spec_version: 1
feature: mahfil
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [mahfil, technical-context]
---

# mahfil — technical context

## Public surface
**Depends on:** admin-access; executive-admins (`mahfil_read`/`mahfil_write` keys).
**Exposed to:** public-site (`mahfil.html` and homepage cards read published rows).

**Exposes:**
```
public.mahfils   -- table; anon sees published = true only (RLS);
                 -- admin read/write via mahfil_read / mahfil_write
```
**Callers MUST NOT:** show unpublished mahfils publicly; bypass the permission keys.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Create mahfil with status | AC1 | ✅ built | running/previous select |
| Shown on public site | AC2, AC4 | ✅ built | `mahfil.html`; RLS filters to published |
| Full event details + publication | AC3 | ✅ built | date/time/venue/image/published |

## Logic
- `admin/mahfil.html`: guarded; create/edit with title, status, date, time, venue, image URL,
  description and a Published toggle.
- `mahfil.html` (public): lists what RLS exposes (published only), newest event first.
- `supabase/schema.sql`: `event_date`, `event_time`, `venue`, `published` columns.
- `supabase/rls.sql`: public read (published), keyed admin read/write.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/mahfil.html` | Mahfil management |
| `mahfil.html` | Public published-mahfil page |
| `supabase/schema.sql` | mahfils event/publication columns |
| `supabase/rls.sql` | mahfils policies |
| `admin/dashboard.html` | Mahfil card links here |

## API / data contracts
- Select (public, published-only) / keyed insert/update on `mahfils`.

## Known issues
- Image is a URL field until the storage split (T25).
