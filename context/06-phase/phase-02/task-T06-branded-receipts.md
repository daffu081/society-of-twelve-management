---
spec_version: 1
file_type: task
phase: 2
task_id: T06
feature: receipts
status: todo
---

# T06 — Branded receipts

## Description
Generate a professional branded receipt for every payment (spec §10) — logo, member name, member ID, house name, amount, purpose, method, receipt number, date and recorded-by. Receipts are reachable from both the member profile and payment history, print-friendly, downloadable as PDF, and emailable — never sent as a PDF over SMS.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Branded receipt generated | ⬜ |
| AC2 | Receipt reachable from profile & history | ⬜ |
| AC3 | Email a receipt | ⬜ |

## Implementation approach
1. Build a print-friendly receipt template populated from a payment
2. Add PDF generation for download
3. Link receipts from the profile and payment history
4. Add an email-receipt action via an email edge function and never route PDFs through SMS

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Create | `receipt.html` | branded print-friendly receipt template |
| Create | `supabase/functions/send-receipt-email/index.ts` | email the receipt/PDF |
| Update | `member/payments.html` | receipt links + download |
| Update | `admin/payments.html` | view/email receipt action |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/receipts/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/receipts/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/receipts/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
