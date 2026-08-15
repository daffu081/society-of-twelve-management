---
spec_version: 1
file_type: task
phase: 3
task_id: T07
feature: _cross-cutting
status: todo
---

# T07 — Production deployment runbook

## Description
Bring the system live in the correct, repeatable order: apply the schema, access rules and seed data,
deploy the server-side functions with their secrets set, then grant permission keys to every executive
so they gain area access. Promoted from backlog row 14. Ops task — verified by carrying out the runbook
against production, not by an automated test.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC5 | Deployment brings the system live in the correct order | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-03/requirement/_cross-cutting/requirement.md` | the AC (pure business) this task delivers |
| `context/05-features/_cross-cutting/technical-context.md` | deployment surface, credentials handling |
| `context/05-features/executive-admins/technical-context.md` | the permission-key matrix keys are granted through |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] AC5 confirmed by executing the runbook against production
- [ ] `technical-context.md` updated with the runbook (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅

> ⚠️ Release gate: manual, run against live infrastructure — no automated test.
