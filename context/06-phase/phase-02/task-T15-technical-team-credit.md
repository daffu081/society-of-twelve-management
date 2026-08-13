---
spec_version: 1
file_type: task
phase: 2
task_id: T15
feature: technical-team
status: todo
---

# T15 — Technical team credit

## Description
Public technical-team page (spec §26) displaying the developer credit Sabbir Ahmed Sakib — Developer. Static content; no admin data model required.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Technical team credit shown | ⬜ |

## Implementation approach
1. Build a static technical-team page showing the developer credit
2. Link it from the public nav/footer

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Create | `technical-team.html` | public developer/technical-team credit |
| Update | `index.html` | nav/footer link to technical-team |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/technical-team/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/technical-team/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/technical-team/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
