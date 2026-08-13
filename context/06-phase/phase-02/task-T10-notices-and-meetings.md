---
spec_version: 1
file_type: task
phase: 2
task_id: T10
feature: notices
status: todo
---

# T10 — Notices & meetings

## Description
Notices & meetings management (spec §18): create, edit, publish and archive notices, each with an auto reference number SOT-NOT-YYYYMM-0001; meeting notices additionally capture date, time and venue. An authorized executive can send the associated SMS after reviewing/editing it. Feeds the homepage running-notice banner already built in Phase 01.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC3 | Create & publish with reference number | ⬜ |
| AC4 | Meeting notice fields | ⬜ |
| AC5 | Send notice SMS after review | ⬜ |

## Implementation approach
1. Add a notices table with reference-number generation and publish/archive states
2. Build admin create/edit/publish/archive UI with meeting date/time/venue fields
3. Add a reviewed-SMS send action gated by notices/sms permissions
4. Surface published notices to the public page and homepage banner

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | notices table + SOT-NOT reference sequence |
| Create | `admin/notices.html` | notice/meeting management |
| Create | `notices.html` | public notices page |
| Update | `admin/admin.js` | notice CRUD + SMS send |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/notices/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/notices/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/notices/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
