---
type: test-context
spec_version: 1
feature: reports
file_type: test-context
contract_version: 1
status: done
depends_on: [admin-access, members, payments, finance, due-payments, projects, sms, birthday]
last_review: 2026-08-15
frozen: false
tags: [reports, test-context]
---

# Reports & Exports — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 view reports | 🟢 manual | — |
| AC2 export reports | 🟢 manual | — |
| Permission gating | 🟢 manual | — |

## Manual checks
- AC1: as a super admin, each of the nine reports opens and shows rows matching its source page.
- AC2: export a report → CSV opens in a spreadsheet with the same rows; Excel export opens in
  Excel; PDF (print) produces the table only. Money columns are exact decimal strings (T4).
- Gating: an executive with `reports_read` but not `finance_read` sees no income/expense reports
  in the picker, and `report_income`/`report_expense` return no rows if queried directly; without
  `reports_read` the picker is empty.
