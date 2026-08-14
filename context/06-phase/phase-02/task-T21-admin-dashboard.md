---
spec_version: 1
file_type: task
phase: 2
task_id: T21
feature: dashboard
status: done
---

# T21 — Admin dashboard

## Description
Admin dashboard (spec §15): a permission-aware overview showing total/active/due members, monthly collection, total income/expense, current balance, today's collection, recent payments, upcoming birthdays, recent notices and a project/activity summary, plus charts for collection, income-vs-expense, professions and payment methods. Each figure respects the viewer's permissions (finance figures only for finance-permitted admins).

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Summary figures | ✅ |
| AC2 | Charts | ✅ |

## Implementation approach
1. Add aggregate queries/views for each summary figure
2. Build the dashboard cards, gating finance figures behind finance.read
3. Add charts for collection, income vs expense, professions and payment methods
4. Pull recent payments/birthdays/notices/projects from their features

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `admin/dashboard.html` | summary cards + charts |
| Update | `admin/admin.js` | aggregate queries + chart rendering |
| Create | `supabase/rls.sql` | permission-aware aggregate views |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/dashboard/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/dashboard/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/dashboard/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
