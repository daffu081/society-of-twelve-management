---
spec_version: 1
file_type: task
phase: 2
task_id: T22
feature: reports
status: todo
---

# T22 — Reports & exports

## Description
Reports & exports (spec §31): member list, payment history, monthly collection, due member, income, expense, project finance, SMS log and birthday delivery log — each viewable and exportable as CSV/Excel/PDF where appropriate. Reports and exports are permission-controlled so a user only sees what their role allows.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | View reports | ⬜ |
| AC2 | Export reports | ⬜ |

## Implementation approach
1. Build report views for each report type
2. Build an admin reports screen listing available reports (permission-filtered)
3. Add CSV/Excel/PDF export per report
4. Enforce reports.read/export on both view and export

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Create | `admin/reports.html` | report views + export buttons |
| Update | `admin/admin.js` | report queries + CSV/Excel/PDF export |
| Create | `supabase/rls.sql` | report views + reports.read/export enforcement |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/reports/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/reports/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/reports/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
