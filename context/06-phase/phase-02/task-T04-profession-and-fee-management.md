---
spec_version: 1
file_type: task
phase: 2
task_id: T04
feature: profession-fee
status: done
---

# T04 — Profession & fee management

## Description
Implement admin-editable profession categories and monthly fees (spec §8: Business 200, Jobholder 100, Student 50, High Ranking Officer configurable, Special Fee arbitrary). Fees drive member dues from configuration, a per-member custom fee is supported, and changing a current fee must never rewrite historical payment amounts.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Configure profession fees | ✅ |
| AC2 | Custom fee per member | ✅ |
| AC3 | Fee change doesn't rewrite history | ✅ |

## Implementation approach
1. Add a profession/fee config table seeded with the initial tiers
2. Link each member to a profession plus an optional custom fee override
3. Build an admin settings screen to add/edit categories and amounts
4. Guarantee historical payments store their own amount, independent of later fee edits

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | profession_fee config table + member fee link |
| Create | `supabase/seed.sql` | initial fee tiers (200/100/50/…) |
| Create | `admin/settings.html` | profession & fee management UI |
| Update | `admin/admin.js` | fee config CRUD |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/profession-fee/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/profession-fee/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/profession-fee/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
