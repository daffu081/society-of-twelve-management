---
spec_version: 1
file_type: task
phase: 2
task_id: T05
feature: payments
status: done
---

# T05 — Payment recording & history

## Description
Build full payment recording (spec §9): method (Online/Cash/Bank/bKash/Nagad/future), amount, purpose, timestamp, recorded-by, notes and an auto SOT-YYYYMM-0001 receipt number. Successful payments trigger the receipt (T06) and notification (T19) workflows, and members can view their own history and open each receipt, isolated from other members.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC3 | Record a full payment | ✅ |
| AC4 | Payment triggers receipt & notification | ✅ |
| AC5 | Member views own history | ✅ |

## Implementation approach
1. Add a payments table with an immutable amount and a SOT-YYYYMM-#### receipt-number generator
2. Build the admin record-payment form gated by payments.write
3. On save, fire receipt-generation and notification hooks
4. Build the member payment-history view scoped to the logged-in member only

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | payments table + receipt-number sequence |
| Create | `admin/payments.html` | record payment + payment list |
| Create | `member/payments.html` | member own payment history |
| Update | `supabase/rls.sql` | payments.read/write + member self-isolation |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/payments/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/payments/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/payments/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
