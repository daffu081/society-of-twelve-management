---
type: runbook
title: "Disaster Recovery"
last_review: 2026-08-13
---

# Disaster recovery runbook

## What can fail
- Supabase project outage → whole app (auth + data) unavailable; static pages still load but show no data.
- Accidental data deletion by an admin → mitigated by soft-delete (`bin`, 30-day window) (ADR-003).
- Bad `supabase/schema.sql` change applied in the SQL editor → schema breakage.
- Lost/rotated Supabase anon key or wrong `config.js` → client can't connect.
- Static host outage → site down (no data loss; just redeploy).

## Backups
- **Primary**: Supabase automated Postgres backups (per your Supabase plan — verify the retention on the free/paid tier).
- **Schema**: `supabase/schema.sql` is version-controlled in git — the source of truth for structure.
- **Soft-delete**: `bin` holds deleted rows for 30 days.
- <!-- TODO(user): confirm Supabase backup cadence/retention for your plan; consider a periodic `pg_dump` export. -->

## Restore procedure
1. Supabase down → check Supabase status; wait or restore from a Supabase backup (dashboard → Database → Backups).
2. Row deleted in error → find it in `bin` by `entity_type`/`entity_id` and re-insert from `snapshot` (within 30 days).
3. Static site down → redeploy the repo to the static host; set `config.js` with valid Supabase creds.
4. Lost creds → regenerate the anon key in Supabase, update `config.js`, redeploy.

## Migration rollback
- Schema changes are additive and idempotent; there is no migration framework.
- To roll back a change: apply a compensating SQL statement in the Supabase SQL editor and update `supabase/schema.sql` to match.
- Test schema changes on a throwaway Supabase project before production.
