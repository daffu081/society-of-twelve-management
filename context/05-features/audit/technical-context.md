---
type: technical-context
spec_version: 1
feature: audit
file_type: technical-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-15
frozen: false
tags: [audit, technical-context]
---

# Audit Logging — technical context

## Public surface
**Depends on:** admin-access (`is_active_admin`, `is_super_admin`); attaches to admins, members,
payments, income, expenses, sms_logs, bin.
**Exposed to:** none (Super-Admin viewer).

**Exposes:**
```
public.audit_log        -- actor_admin_id/name, action, entity_type/id, old_values, new_values, ts
public.audit_capture()  -- generic AFTER trigger fn; snapshots old/new + actor from auth.uid()
```
**Callers MUST NOT:** write `audit_log` by hand from app code (triggers own it); read it as a
non-Super-Admin.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Capture on sensitive tables | AC1 | ✅ built | triggers on 7 tables |
| Super-Admin viewer + filters | AC1 | ✅ built | table/action filter, field diff |

## Logic
- `audit_capture()` (in `rls.sql`): AFTER insert/update/delete on each sensitive table; resolves
  the actor from `auth.uid()` → `admins`, stores `to_jsonb(old)` / `to_jsonb(new)` and the entity
  id. Attached via a loop over `admins, members, payments, income, expenses, sms_logs, bin`.
- RLS: active admins insert (their own actions through triggers); only Super Admins select.
- `admin/audit.html`: Super-Admin-only; newest 200 entries, filter by table/action, per-row diff
  of changed fields (ignores `updated_at` noise).

## Code file mapping
| File | Purpose |
|---|---|
| `supabase/schema.sql` | `audit_log` table + index |
| `supabase/rls.sql` | `audit_capture()`, triggers, RLS |
| `admin/audit.html` | Super-Admin audit viewer |
| `admin/dashboard.html` | Audit card links here |

## API / data contracts
- Reads on `audit_log` (Super-Admin only); all writes are trigger-driven.

## Known issues
- Captures full row snapshots (not a curated field set) — simple and complete; prune columns only
  if storage becomes a concern.
- Audit log export is deferred (reports feature, if the client asks).
