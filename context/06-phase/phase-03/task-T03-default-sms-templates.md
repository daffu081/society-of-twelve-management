---
spec_version: 1
file_type: task
phase: 3
task_id: T03
feature: sms
status: todo
---

# T03 — Six default Bangla SMS templates ship pre-populated

## Description
Ship the six standard Bangla messages (payment success, due reminder, meeting notice, birthday wish,
general notice, payment thank-you) pre-populated and editable when the system starts, each keeping its
fill-in placeholders. Belongs in this phase so admins can send common notifications immediately.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC7 | Six default Bangla templates ship ready to use | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-03/requirement/sms/requirement.md` | the AC (pure business) this task delivers |
| `context/05-features/sms/technical-context.md` | current template management state, public surface, file mapping |
| `context/05-features/sms/test-context.md` | existing coverage table |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
