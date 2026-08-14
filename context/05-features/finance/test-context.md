---
type: test-context
spec_version: 1
feature: finance
file_type: test-context
contract_version: 1
status: in_progress
depends_on: [admin-access, payments]
last_review: 2026-08-14
frozen: false
tags: [finance, test-context]
---

# finance — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC4 record income by source | 🟢 manual | — |
| AC5 record expense | 🟢 manual | — |
| AC6 totals, permission-gated | 🟢 manual | — |
| AC1–AC3 (earlier numbering) | covered by AC4–AC6 | — |
| No-permission executive blocked | 🟢 manual | — |

## Manual checks
- AC4: save an income entry with each of the six sources → each is stored with its source.
- AC5: save an expense → category, amount, date, description and recorded-by (created_by) persist.
- AC6: totals cards show income sum, expense sum and balance = income − expense as exact decimal
  strings (T4); an executive admin without `permissions.finance` sees the no-permission message,
  and direct queries on income/expenses return no rows (RLS); anon gets nothing.
