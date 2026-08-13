---
spec_version: 1
file_type: task
phase: 2
task_id: T12
feature: mahfil
status: todo
---

# T12 — Mahfil management

## Description
Mahfil event management (spec §20): title, date, time, venue, description, image and publication status, managed by admins or authorized executives. Published mahfils appear on a public mahfil page.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC3 | Manage mahfil with full details | ⬜ |
| AC4 | Public mahfil page | ⬜ |

## Implementation approach
1. Add a mahfil table with publication status and image
2. Build admin create/edit UI gated by mahfil.write
3. Build the public mahfil page for published events

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | mahfil table |
| Create | `admin/mahfil.html` | mahfil management |
| Create | `mahfil.html` | public mahfil page |
| Update | `supabase/rls.sql` | mahfil.read/write |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/mahfil/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/mahfil/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/mahfil/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
