---
spec_version: 1
file_type: task
phase: 2
task_id: T17
feature: rules
status: todo
---

# T17 — Rules & regulations

## Description
Rules & Regulations section (spec §22): a dedicated area the Super Admin can create/edit/publish/archive, retaining version/history where practical. Published rules are visible publicly.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Manage rules | ⬜ |
| AC2 | Version history | ⬜ |

## Implementation approach
1. Add a rules table with publish/archive and version history
2. Build Super-Admin-only create/edit/publish/archive UI
3. Retain prior versions on edit where practical
4. Build the public rules page

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Update | `supabase/schema.sql` | rules table + version history |
| Create | `admin/rules.html` | rules management |
| Create | `rules.html` | public rules page |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/rules/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/rules/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/rules/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
