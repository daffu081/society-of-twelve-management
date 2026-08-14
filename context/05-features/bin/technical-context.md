---
type: technical-context
spec_version: 1
feature: bin
file_type: technical-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-15
frozen: false
tags: [bin, technical-context]
---

# Bin / Trash — technical context

## Public surface
**Depends on:** admin-access (`is_super_admin`, `is_active_admin`).
**Exposed to:** every feature with soft-deletable records (projects today; others later).

**Exposes:**
```
public.bin                 -- entity_type, entity_id, deleted_by, deleted_at,
                           -- expires_at (deleted_at + 30 days), snapshot jsonb
                           -- insert: active admin; select/delete: Super Admin only
cleanup-bin (edge fn)      -- CRON_SECRET-gated daily purge of rows past expires_at
soft-delete pattern (ADR-003) -- snapshot row → insert into bin → delete from source
```
**Callers MUST NOT:** hard-delete a domain row without the bin snapshot; read/restore/purge as a
non-Super-Admin.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Recoverable Bin (restore / purge) | AC1 | ✅ built | cross-entity, Super-Admin-only |
| Automatic 30-day cleanup | AC2 | ✅ built | `cleanup-bin` scheduled fn |

## Logic
- `admin/bin.html`: Super-Admin-only; lists all `bin` rows with a type filter and days-to-expiry
  (warns under 3 days); Restore re-inserts `snapshot` into `entity_type` then deletes the bin row;
  Delete-forever removes the bin row after confirm.
- `cleanup-bin` fn: `delete from bin where expires_at < now()`, returning the purged count.
- Schema/RLS already exist (T11): `bin` table with `expires_at default now()+30 days`, and the
  `bin_admin_insert` / `bin_super_read` / `bin_super_delete` policies.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/bin.html` | Cross-entity Bin: restore + permanent delete |
| `supabase/functions/cleanup-bin/index.ts` | Scheduled 30-day purge |
| `supabase/schema.sql` | `bin` table (from T11) |
| `supabase/rls.sql` | bin policies (from T11) |
| `admin/dashboard.html` | Bin card links here |

## API / data contracts
- Select/delete on `bin` (Super-Admin); restore = insert into the source table.
- Scheduler → `POST functions/v1/cleanup-bin` with the CRON_SECRET bearer → `{ purged }`.

## Known issues
- Restore re-inserts with the original id; if that id was re-used since deletion the insert fails
  (rare — the source row was deleted at soft-delete time).
- Only `projects` currently soft-deletes into the Bin; other features adopt the ADR-003 pattern as
  they gain destructive actions.
