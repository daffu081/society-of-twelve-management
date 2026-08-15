---
spec_version: 1
file_type: task
phase: 3
task_id: T02
feature: member-profile
status: todo
---

# T02 — Member portal login

## Description
Give each member an explicit way to sign in to their own member portal and reach only their own
profile, payment history and receipts. Belongs in this phase to make the member-side access v2
describes concrete; mobile one-time-code login stays deferred until an SMS provider is connected.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC6 | Member logs in to their own portal | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-03/requirement/member-profile/requirement.md` | the AC (pure business) this task delivers |
| `context/05-features/member-profile/technical-context.md` | current state, public surface, file mapping |
| `context/05-features/member-profile/test-context.md` | existing coverage table |
| `context/05-features/admin-access/technical-context.md` | existing login-link auth pattern to mirror |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
