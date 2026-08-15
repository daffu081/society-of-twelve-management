---
spec_version: 1
file_type: task
phase: 3
task_id: T01
feature: payments
status: todo
---

# T01 — Bank / QR collection details (inactive until ready)

## Description
Let an admin enter and save the organization's bank / QR payment details ahead of time and keep them
switched off until a bank account is confirmed. Belongs in this phase because v2 asks for the details
to exist but stay inactive, without changing any existing payment record.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC6 | Configure bank / QR collection details (may stay inactive) | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-03/requirement/payments/requirement.md` | the AC (pure business) this task delivers |
| `context/05-features/payments/technical-context.md` | current state, public surface, file mapping |
| `context/05-features/payments/test-context.md` | existing coverage table |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
