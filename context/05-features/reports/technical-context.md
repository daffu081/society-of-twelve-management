---
type: technical-context
spec_version: 1
feature: reports
file_type: technical-context
contract_version: 1
status: done
depends_on: [admin-access, members, payments, finance, due-payments, projects, sms, birthday]
last_review: 2026-08-15
frozen: false
tags: [reports, technical-context]
---

# Reports & Exports — technical context

## Public surface
**Depends on:** admin-access; the source features (members, payments, finance, due-payments,
projects, sms, birthday); executive-admins (`reports_read`, `reports_export`, and each source
area's own key).
**Exposed to:** none (leaf page).

**Exposes:**
```
public.report_member_list / report_payment_history / report_monthly_collection /
report_due_members / report_income / report_expense / report_project_finance /
report_sms_log / report_birthday_log
  -- each view: rows only when has_permission('reports_read') AND the source area's key
```
**Callers MUST NOT:** build a report by reading base tables directly (bypasses the double gate);
add a report exposing a private field.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| View the nine reports | AC1 | ✅ built | permission-filtered picker + table |
| Export CSV / Excel / PDF | AC2 | ✅ built | native Blob/print; no library |

## Logic
- Nine report views (in `rls.sql`): each WHERE requires `reports_read` plus the source area's
  permission, so both view and export inherit BR3 gating.
- `admin/reports.html`: the report menu is filtered to the admin's permissions; selecting one
  renders the view as a table; CSV = UTF-8 text, Excel = BOM'd `.xls` CSV (opens cleanly in
  Excel), PDF = the browser print-to-PDF over the table (print CSS hides chrome).

## Code file mapping
| File | Purpose |
|---|---|
| `admin/reports.html` | Report picker, table view, CSV/Excel/PDF export |
| `supabase/rls.sql` | The nine `report_*` views |
| `admin/dashboard.html` | Reports card links here |

## API / data contracts
- `select * from report_*` (authenticated; each view double-gated).

## Known issues
- Excel export is CSV-as-.xls, not a true XLSX workbook — adequate for these flat reports; a real
  xlsx writer would need a dependency (ADR).
- `reports_export` is not separately enforced from `reports_read` yet — anyone who can view can
  export; split the keys if the client needs view-without-export.
