---
type: technical-context
spec_version: 1
feature: projects
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [projects, technical-context]
---

# projects — technical context

## Public surface
**Depends on:** admin-access; executive-admins (`projects_write` key); bin (soft-delete target).
**Exposed to:** public-site (`projects.html` and homepage cards read the table).

**Exposes:**
```
public.projects   -- table; anon read-all (running/previous showcase);
                  -- insert/update/delete need projects_write
bin 'projects'    -- convention: soft-deleted projects live in bin with a full snapshot
```
**Callers MUST NOT:** hard-delete without the bin snapshot step (ADR-003); write money fields
as JS floats.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Create project with status | AC1 | ✅ built | shared form |
| Shown on public site | AC2 | ✅ built | `projects.html` running/previous split |
| Full details + finance | AC3 | ✅ built | images = URLs until T25 storage |
| Soft-delete + super-only restore/purge | AC4 | ✅ built | bin RLS enforces BR5 |

## Logic
- `admin/projects.html`: guarded; full form (title, status, dates, budget/spent as strings →
  `numeric(12,2)`, description, image URLs); delete = snapshot → `bin` insert → row delete;
  Super Admins additionally see the Bin panel (restore re-inserts the snapshot then removes the
  bin row; purge deletes the bin row after confirm).
- `supabase/rls.sql`: projects public-read / keyed-write; bin insert for active admins,
  select/delete for Super Admins only — restore/purge are structurally super-only (BR5).
- `projects.html` (public): running and previous sections with images.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/projects.html` | Project management + Bin panel |
| `projects.html` | Public running/previous showcase |
| `supabase/schema.sql` | projects detail/finance columns |
| `supabase/rls.sql` | projects + bin policies |
| `admin/dashboard.html` | Projects card links here |

## API / data contracts
- Select (public) / insert / update / delete (keyed) on `projects`; bin insert on soft-delete.

## Known issues
- Images are URL strings; direct upload arrives with the storage split (T25).
- Bin listing here is scoped to projects; the full cross-entity Bin screen is T24.
