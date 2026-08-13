---
spec_version: 1
file_type: task
phase: 2
task_id: T14
feature: founding-members
status: todo
---

# T14 — Founding members

## Description
Founding-member records (spec §25): photo, name, historical role and short biography, admin-managed and shown on the public founding-members page.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Manage founding members | ⬜ |

## Implementation approach
1. Add a founding_members table
2. Build admin add/edit UI
3. Build the public founding-members page

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | founding_members table |
| Create | `admin/founding-members.html` | founding member management |
| Create | `founding-members.html` | public founding members page |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/founding-members/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/founding-members/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/founding-members/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
