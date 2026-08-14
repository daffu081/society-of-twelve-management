---
type: test-context
spec_version: 1
feature: dashboard
file_type: test-context
contract_version: 1
status: done
depends_on: [admin-access, members, payments, finance, due-payments, notices, projects, birthday]
last_review: 2026-08-14
frozen: false
tags: [dashboard, test-context]
---

# Admin Dashboard — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls + seed applied
> and some data recorded).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 summary figures | 🟢 manual | — |
| AC2 charts | 🟢 manual | — |
| Permission gating | 🟢 manual | — |

## Manual checks
- AC1: as a super admin with members/payments/finance/notices/projects data present, every card
  and recent panel shows real values; money figures match the finance page exactly (decimal-string
  compare, T4).
- AC2: the four charts render bars proportional to their data; empty datasets show "No data yet".
- Gating: an executive without finance_read sees no finance card/chart and `finance_totals`
  returns no row; without payments_read the collection card shows the needs-permission note and
  the payment views return nothing.
