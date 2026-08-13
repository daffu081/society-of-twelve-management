---
spec_version: 1
file_type: task
phase: 2
task_id: T08
feature: finance
status: todo
---

# T08 — Finance income & expense

## Description
Admin-controlled income and expense management (spec §17). Income is recorded against defined sources (Monthly Subscription, Project/Mahfil/Special Donation, Other, Historical/Offline); expenses carry category, amount, date, description and recorded-by. A finance dashboard shows cumulative income, expense and balance. Finance data is never public and executive access requires explicit permission.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC4 | Record income by source | ⬜ |
| AC5 | Record expense | ⬜ |
| AC6 | Finance dashboard totals | ⬜ |

## Implementation approach
1. Add income and expense tables with the defined source/category sets
2. Build admin income/expense entry forms gated by finance.write
3. Compute cumulative income/expense/balance for the finance dashboard
4. Lock finance behind finance.read and never expose it publicly

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | income + expense tables |
| Create | `admin/finance.html` | income/expense entry + balance view |
| Update | `admin/admin.js` | finance CRUD + totals |
| Update | `supabase/rls.sql` | finance.read/write, no public access |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/finance/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/finance/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/finance/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
