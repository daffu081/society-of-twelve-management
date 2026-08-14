---
spec_version: 1
file_type: task
phase: 2
task_id: T13
feature: committee
status: done
---

# T13 — Executive committee

## Description
Executive committee roster (spec §24): photo, name, position, year, short biography, display order and public visibility. Public entries render on the committee page in the configured display order.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Manage committee entries | ✅ |
| AC2 | Public committee display in order | ✅ |

## Implementation approach
1. Add a committee table with display_order and visibility
2. Build admin add/edit/reorder UI
3. Build the public committee page ordered by display_order

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | committee table |
| Create | `admin/committee.html` | committee management + ordering |
| Create | `committee.html` | public committee page |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/committee/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/committee/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/committee/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
