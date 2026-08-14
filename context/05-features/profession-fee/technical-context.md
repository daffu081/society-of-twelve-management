---
type: technical-context
spec_version: 1
feature: profession-fee
file_type: technical-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [profession-fee, technical-context]
---

# Profession & Fee Management — technical context

## Public surface
**Depends on:** admin-access (`checkAdminAccess()`, `supabaseClient`).
**Exposed to:** members (fee-category select on the member form), due-payments (effective-fee rule).

**Exposes:**
```
public.fee_categories          -- table: name (unique), monthly_fee numeric(12,2); admin-only RLS
effective monthly due (rule)   -- coalesce(members.monthly_fee, fee_categories.monthly_fee)
                               -- members.monthly_fee is the per-member custom override (null = category fee)
```
**Callers MUST NOT:** copy a category fee onto payment rows at read time (payments store their own
amount); do fee math in JS floats (ADR-002).

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Category CRUD + inline fee edit | AC1 | ✅ built | `admin/settings.html`, seeded tiers |
| Per-member custom fee override | AC2 | ✅ built | member form: category select + custom fee field |
| Fee edits never rewrite history | AC3 | ✅ structural | `payments.amount` is stored per payment; no link to config |

## Logic
- `admin/settings.html`: guarded by `checkAdminAccess()`; lists `fee_categories` with inline fee
  editing and an add-category form. Fees travel as strings into `numeric(12,2)`.
- `admin/members.html`: the fee-category select loads from `fee_categories` (name + fee); the
  custom-fee input overrides the category when set.
- `supabase/seed.sql`: seeds Business 200 / Jobholder 100 / Student 50 / High Ranking Officer 200
  with `on conflict do nothing`, so admin-edited amounts survive re-runs.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/settings.html` | Category list + inline fee edit + add form |
| `admin/members.html` | Fee-category select + custom-fee override on the member form |
| `supabase/schema.sql` | `fee_categories` table |
| `supabase/seed.sql` | Initial fee tiers (BR1) |
| `supabase/rls.sql` | `fee_categories_admin_all` policy |

## API / data contracts
- Supabase select/insert/update on `fee_categories`, admin-gated by RLS.

## Known issues
- Categories have no delete path yet (rename/zero the fee instead); soft-delete via `bin` can be
  added when a real need appears.
