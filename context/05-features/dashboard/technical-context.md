---
type: technical-context
spec_version: 1
feature: dashboard
file_type: technical-context
contract_version: 1
status: done
depends_on: [admin-access, members, payments, finance, due-payments, notices, projects, birthday]
last_review: 2026-08-14
frozen: false
tags: [dashboard, technical-context]
---

# Admin Dashboard — technical context

## Public surface
**Depends on:** admin-access; the aggregate views below plus `finance_totals` (finance),
`member_dues` (due-payments); reads recent rows from payments/notices/projects; the birthday
panel (birthday feature) shares the page.
**Exposed to:** none (leaf page).

**Exposes:**
```
public.payments_summary        -- month_collection, today_collection (payments_read)
public.payments_by_method      -- method, total, n (payments_read)
public.payments_by_month       -- last 6 months, total per month (payments_read)
public.members_by_profession   -- active members per profession (members_read)
```
**Callers MUST NOT:** sum money client-side (ADR-002) — add a view instead; show a figure to an
admin lacking its permission (gate in SQL, not the UI).

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Summary cards + recents | AC1 | ✅ built | finance card hidden without finance_read |
| Four charts | AC2 | ✅ built | dependency-free CSS bars |

## Logic
- Aggregate views (in `rls.sql`): every money figure summed in Postgres; each view's WHERE clause
  checks the matching permission key, so an unpermitted admin gets zero rows.
- `admin/dashboard.html`: cards (members, due count, collection, finance), `barChart()` — a
  ~10-line CSS bar renderer (no chart library; the site stays build-free), recents (5 payments,
  3 notices, project running/previous split), plus the pre-existing due + birthday panels.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/dashboard.html` | Cards, charts, recents (plus due + birthday panels) |
| `supabase/rls.sql` | The four aggregate views |

## API / data contracts
- Selects on the aggregate views + small recent-row reads; all RLS/permission-limited.

## Known issues
- Charts are proportional CSS bars — upgrade to a charting approach only if the client asks for
  richer visuals (would need an ADR for the dependency).
