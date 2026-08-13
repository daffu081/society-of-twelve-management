---
spec_version: 1
file_type: task
phase: 2
task_id: T24
feature: bin
status: todo
---

# T24 — Bin / trash

## Description
Bin/Trash (spec §27): important records use soft deletion and stay recoverable for 30 days; only a Super Admin has unrestricted restore and permanent-delete authority; automated cleanup permanently removes eligible records after the 30-day window. Provides the shared soft-delete/restore mechanics used by projects and other features.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Deleted items are recoverable | ⬜ |
| AC2 | Automatic cleanup after 30 days | ⬜ |

## Implementation approach
1. Add shared soft-delete metadata (deleted_at, expires_at) convention
2. Build a Bin screen listing recoverable records with restore/permanent-delete (Super Admin only)
3. Create a scheduled cleanup edge function purging records past 30 days

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | soft-delete metadata + bin view |
| Create | `admin/bin.html` | Bin/Trash restore + permanent delete |
| Create | `supabase/functions/cleanup-bin/index.ts` | 30-day scheduled purge |
| Update | `supabase/rls.sql` | restore/purge restricted to Super Admin |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/bin/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/bin/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/bin/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
