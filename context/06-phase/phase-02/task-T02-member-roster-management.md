---
spec_version: 1
file_type: task
phase: 2
task_id: T02
feature: members
status: done
---

# T02 — Member roster management

## Description
Build the admin-facing membership roster on top of the full profile (T01): create, edit and activate/deactivate members without ever destroying history, plus list, search (name/ID/mobile) and filter (status/profession). This is the primary day-to-day admin surface for the member base and feeds dashboard/report counts.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC4 | Manage the roster | ✅ |
| AC5 | List, search and filter | ✅ |

## Implementation approach
1. Reuse the T01 member fields and add an active/inactive toggle that preserves all records
2. Build a paginated member list with a search box and status/profession filters
3. Wire create/edit to the shared member form, gated by members.write
4. Ensure deactivation never cascades to payment/receipt history

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `admin/members.html` | roster list + search/filter + create/edit |
| Update | `admin/admin.js` | member list/search/CRUD calls |
| Update | `supabase/schema.sql` | search indexes + active flag |
| Update | `supabase/rls.sql` | members.read/write enforcement |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/members/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/members/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/members/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
