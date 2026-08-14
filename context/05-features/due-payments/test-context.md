---
type: test-context
spec_version: 1
feature: due-payments
file_type: test-context
contract_version: 1
status: done
depends_on: [profession-fee, payments, sms]
last_review: 2026-08-14
frozen: false
tags: [due-payments, test-context]
---

# Due Payment Management — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls + seed applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 due calculation | 🟢 manual | — |
| AC2 editable reminder | 🟢 manual | — |
| Paid-up empty state | 🟢 manual | — |

## Manual checks
- AC1: give a member a category fee and a join date 3 months back with one payment of one month's
  fee → the dashboard shows them due exactly 2 × fee (compare exact decimal strings, T4) with the
  payment's date as last payment; a member who never paid shows "never".
- AC2: click "Remind" → the prefilled text is editable; edit it and send → `sms_logs` gains a
  pending `due_reminder` row containing the edited text.
- Paid-up: with no positive dues the panel shows the paid-up message.
