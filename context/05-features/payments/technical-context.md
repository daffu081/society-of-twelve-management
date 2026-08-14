---
type: technical-context
spec_version: 1
feature: payments
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: [admin-access, members]
last_review: 2026-08-14
frozen: false
tags: [payments, technical-context]
---

# payments — technical context

## Public surface
**Depends on:** admin-access (`checkAdminAccess()`), members (a payment references a member row).
**Exposed to:** receipts (reads a payment by `receipt_no`), finance (income may link a payment),
sms (consumes pending `payment_received` rows in `sms_logs`).

**Exposes:**
```
public.payments                -- table: receipt_no unique (default next_receipt_no()), member_id,
                               -- amount numeric(12,2), purpose, payment_method, payment_date,
                               -- notes, created_by; admin-only RLS
public.next_receipt_no()       -- SOT-YYYYMM-0001 generator (per-month atomic counter)
public.payments_self           -- view: the logged-in member's own payments (by email match);
                               -- receipt_no, amount, purpose, payment_method, payment_date, notes
sms_logs 'payment_received'    -- convention: a pending row queued per payment = notification start
```
**Callers MUST NOT:** bypass `checkAdminAccess()`; hard-delete rows; use floats for money;
generate receipt numbers client-side.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Record full payment + SOT-YYYYMM-#### receipt no | AC1, AC3 | ✅ built | needs live Supabase to verify |
| Receipt + notification triggered on save | AC4 | ✅ built | receipt link + pending sms_logs row |
| Member views own history | AC5 | ✅ built | `payments_self` view + member page |
| Admin views a member's history | AC2 | 🔄 partial | recent-payments list; per-member filter later |

## Logic
- `admin/payments.html`: guarded; form inserts a payment (amount as string → `numeric(12,2)`,
  `created_by` = admin id); `receipt_no` comes from the DB default. On success it links
  `receipt.html?no=<receipt_no>` (T06) and queues a pending `payment_received` row in `sms_logs`
  (T19 sends). Notification failure never blocks the payment.
- `member/payments.html`: lists the member's own rows from `payments_self`, each linking its receipt.
- `supabase/schema.sql`: `receipt_counters` (month → counter) + `next_receipt_no()` upserted
  atomically — race-free, never reused, resets monthly (BR5).
- `supabase/rls.sql`: RLS on payments — admin all, anon none; `payments_self` isolates member rows.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/payments.html` | Record-payment form + recent payments list |
| `member/payments.html` | Member own payment history |
| `supabase/schema.sql` | `payments` table, `receipt_counters`, `next_receipt_no()` |
| `supabase/rls.sql` | payments RLS + `payments_self` view |

## API / data contracts
- Insert on `payments` (admin), select on `payments_self` (member), both via Supabase.

## Known issues
- Payment amounts are immutable by convention (no edit UI); a DB trigger forbidding amount updates
  can be added in the hardening pass (T25) if needed.
- Admin per-member history filter not built yet — the roster page will link here when needed.
