---
spec_version: 1
file_type: task
phase: 2
task_id: T23
feature: audit
status: done
---

# T23 — Audit logging

## Description
Audit logging (spec §28): record important administrative actions with actor, action, timestamp, affected table/record and relevant old/new values where practical. At minimum log permission changes, sensitive member changes, payments, finance, SMS sending, deletions and restorations, giving the Super Admin an accountability trail.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Actions are logged | ✅ |

## Implementation approach
1. Add an audit_log table capturing actor/action/timestamp/record/old-new
2. Add triggers or server-side hooks on the sensitive operations
3. Build a Super-Admin audit log viewer

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | audit_log table + triggers |
| Create | `admin/audit.html` | audit log viewer (Super Admin) |
| Update | `supabase/rls.sql` | audit read restricted to Super Admin |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/audit/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/audit/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/audit/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
