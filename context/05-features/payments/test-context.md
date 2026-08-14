---
type: test-context
spec_version: 1
feature: payments
file_type: test-context
contract_version: 1
status: in_progress
depends_on: [admin-access, members]
last_review: 2026-08-14
frozen: false
tags: [payments, test-context]
---

# payments — test context

> No automated runner yet — manual checks (needs live Supabase with schema.sql + rls.sql applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC3 record a full payment | 🟢 manual | — |
| AC4 payment triggers receipt & notification | 🟢 manual | — |
| AC5 member views own history | 🟢 manual | — |
| AC1 / AC2 (phase-01 numbering, superseded by AC3/AC5) | covered by the above | — |

## Manual checks
- AC3: record a payment on `admin/payments.html` → it appears in the list with a
  `SOT-YYYYMM-0001`-format receipt number; record a second → the number increments. Amounts
  compare as exact decimal strings (T4).
- AC4: after saving, the success message links the receipt page, and `sms_logs` contains a new
  `payment_received` row with `status = 'pending'` for that member.
- AC5: log into `member/payments.html` as member A → only A's payments are listed; a second
  member's login shows only theirs; anon query on `payments` returns nothing.
