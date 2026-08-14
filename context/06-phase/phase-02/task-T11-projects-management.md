---
spec_version: 1
file_type: task
phase: 2
task_id: T11
feature: projects
status: done
---

# T11 — Projects management

## Description
Projects management (spec §19): title, description, images, start/end dates, status and financial information. Projects use soft deletion — deleted projects move to the Bin (T24) and only a Super Admin can restore or permanently delete them. Published projects appear on the public projects page.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC3 | Manage project with details & finance | ✅ |
| AC4 | Soft-delete and restore | ✅ |

## Implementation approach
1. Add a projects table with soft-delete metadata and financial fields
2. Build admin create/edit UI including image upload and status
3. Wire delete to move rows to the Bin, with restore/purge restricted to Super Admin
4. Build the public projects page for published projects

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | projects table + soft-delete columns |
| Create | `admin/projects.html` | project management + images |
| Create | `projects.html` | public projects page |
| Update | `supabase/rls.sql` | projects.read/write + soft-delete/restore |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/projects/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/projects/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/projects/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
