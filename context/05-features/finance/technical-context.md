---
type: technical-context
spec_version: 1
feature: finance
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: [admin-access, payments]
last_review: 2026-08-14
frozen: false
tags: [finance, technical-context]
---

# finance — technical context

## Public surface
**Depends on:** admin-access; payments (income rows may link a payment via `payment_id`).
**Exposed to:** dashboard/reports (may read `finance_totals` with the finance permission).

**Exposes:**
```
public.income / public.expenses  -- tables; RLS: has_permission('finance') only
public.finance_totals            -- view: total_income, total_expense, balance (SQL sums)
public.has_permission(cap text)  -- capability helper: super_admin, or permissions->>cap = true
                                 -- (shared — the T09 permission matrix builds on this)
```
**Callers MUST NOT:** sum money in JS floats; expose any finance row publicly (BR6).

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Record income by defined source | AC1, AC4 | ✅ built | six BR4 sources in the form |
| Record expense (full detail + recorded-by) | AC2, AC5 | ✅ built | `created_by` added to both tables |
| Cumulative totals, permission-gated | AC3, AC6 | ✅ built | `finance_totals`; RLS on tables |

## Logic
- `admin/finance.html`: guarded; early friendly message unless super_admin or
  `permissions.finance = true` (RLS enforces the same server-side). Income form uses the fixed
  BR4 source list; expense form captures category/amount/date/description; both stamp
  `created_by = admin.id`. Totals cards read `finance_totals`; a merged recent-entries list shows
  the last 20 of each.
- `supabase/rls.sql`: `has_permission()` helper; RLS on `income`/`expenses`; `finance_totals`
  computes sums in Postgres.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/finance.html` | Income/expense entry + totals + recent entries |
| `supabase/schema.sql` | `income`/`expenses` tables + `created_by` columns |
| `supabase/rls.sql` | `has_permission()`, finance RLS, `finance_totals` view |
| `admin/dashboard.html` | Finance card links here |

## API / data contracts
- Insert/select on `income` and `expenses`; select on `finance_totals` — all finance-permitted.

## Known issues
- Income→payment linking (`payment_id`) exists in the schema but has no UI yet (AC1's optional
  link); add when monthly-subscription income is reconciled against payments.
