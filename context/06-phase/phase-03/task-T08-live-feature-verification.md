---
spec_version: 1
file_type: task
phase: 3
task_id: T08
feature: _cross-cutting
status: todo
---

# T08 — Live verification of every feature

## Description
Run each feature's manual checks against the real production setup (with real credentials in place),
confirming everything behaves as specified and recording any failures rather than assuming success.
Promoted from backlog row 15. Verification task — done by running the checks against live, not by an
automated test.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC6 | Every feature is verified against the live setup | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-03/requirement/_cross-cutting/requirement.md` | the AC (pure business) this task delivers |
| `context/05-features/*/test-context.md` | each feature's manual check list to run live |
| `context/05-features/_cross-cutting/technical-context.md` | live-config / credentials state |

## Definition of done
- [ ] AC6 confirmed by running every feature's checks against production
- [ ] Results recorded in the relevant `test-context.md` (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅

> ⚠️ Release gate: manual live verification, depends on T07 deploy — no automated test.
