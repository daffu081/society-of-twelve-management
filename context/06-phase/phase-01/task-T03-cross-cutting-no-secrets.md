---
spec_version: 1
file_type: task
phase: 1
task_id: T03
feature: _cross-cutting
status: todo
---

# T03 — No secret credentials in the public website

## Description
Ensure the public website served to visitors contains no secret or service-level credentials —
only safe, public-facing configuration. A foundational security guarantee for the whole system.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | No secret credentials in the public website | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-01/requirement/_cross-cutting/requirement.md` | the ACs (pure business) this task delivers |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
