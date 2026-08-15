---
spec_version: 1
file_type: task
phase: 3
task_id: T06
feature: _cross-cutting
status: todo
---

# T06 — Protect remaining sensitive tables

## Description
Lock down the last unprotected data tables — message logs, birthday logs, message templates and
counters — so nobody holding only the public key can read or change them. Promoted from backlog row 16.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC7 | Remaining sensitive tables are protected | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-03/requirement/_cross-cutting/requirement.md` | the AC (pure business) this task delivers |
| `context/05-features/_cross-cutting/technical-context.md` | current access-control state, public surface |
| `context/05-features/_cross-cutting/test-context.md` | existing coverage table |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
