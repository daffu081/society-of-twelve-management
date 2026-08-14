---
spec_version: 1
file_type: task
phase: 2
task_id: T16
feature: awards
status: done
---

# T16 — Awards & achievements

## Description
Awards & achievements (spec §21): title, recipient/member (optional link), description, date, image/document and visibility. Publication is admin-controlled; the public awards page shows only awards made public.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Record an award | ✅ |
| AC2 | Control public visibility | ✅ |

## Implementation approach
1. Add an awards table with optional member link, visibility and document
2. Build admin create/edit UI including image/document upload
3. Build the public awards page for public awards only

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | awards table |
| Create | `admin/awards.html` | awards management |
| Create | `awards.html` | public awards page |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/awards/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/awards/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/awards/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
