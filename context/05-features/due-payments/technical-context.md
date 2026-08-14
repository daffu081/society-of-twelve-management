---
type: technical-context
spec_version: 1
feature: due-payments
file_type: technical-context
contract_version: 1
status: done
depends_on: [profession-fee, payments, sms]
last_review: 2026-08-14
frozen: false
tags: [due-payments, technical-context]
---

# Due Payment Management — technical context

## Public surface
**Depends on:** profession-fee (effective-fee rule), payments (payment history), sms (the
pending-row queue in `sms_logs`), admin-access.
**Exposed to:** dashboard (renders the due panel), reports (may read `member_dues`).

**Exposes:**
```
public.member_dues     -- view (admin-only): member_id, name, mobile, monthly_fee,
                       -- months_expected, total_paid, due_amount, last_payment_date
sms_logs 'due_reminder' -- convention: a pending row queued per sent reminder
```
**Callers MUST NOT:** recompute dues in JS floats; expose `member_dues` to non-admins.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Due calculation view + dashboard panel | AC1 | ✅ built | needs live Supabase to verify |
| Editable reminder composer → SMS queue | AC2 | ✅ built | delivery by T19 once provider set |

## Logic
- `member_dues` (in `rls.sql`): due = `coalesce(member.monthly_fee, category fee, 0) ×
  months(join month → current month) − total paid`, floored at 0; includes last payment date;
  the WHERE clause returns rows only to active admins.
- Dashboard panel: lists `due_amount > 0` sorted descending; "Remind" opens a prefilled Bangla
  reminder the admin edits, then queues a pending `due_reminder` row in `sms_logs`.

## Code file mapping
| File | Purpose |
|---|---|
| `supabase/rls.sql` | `member_dues` view |
| `admin/dashboard.html` | Due members panel + reminder composer |

## API / data contracts
- `select * from member_dues where due_amount > 0` (admin).
- Insert pending `due_reminder` rows into `sms_logs`.

## Known issues
- Dues assume the fee was constant since joining (`ponytail:` note in the view); per-month fee
  history is the upgrade if retroactive accuracy is needed.
- "Authorized admin" is currently any active admin — capability-level gating arrives with the
  permission matrix (T09).
