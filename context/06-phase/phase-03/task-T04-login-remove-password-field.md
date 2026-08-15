---
spec_version: 1
file_type: task
phase: 3
task_id: T04
feature: admin-access
status: todo
---

# T04 — Remove unused password field from the sign-in screen

## Description
The admin sign-in screen shows a password field, but login is link-based and the password is never
checked. Remove it so the screen only offers the working login-link method. Promoted from backlog row 9.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC5 | Sign-in screen shows only the working login method | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-03/requirement/admin-access/requirement.md` | the AC (pure business) this task delivers |
| `context/05-features/admin-access/technical-context.md` | current login state, public surface, file mapping |
| `context/05-features/admin-access/test-context.md` | existing coverage table |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
