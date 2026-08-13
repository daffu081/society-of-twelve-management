---
spec_version: 1
file_type: task
phase: 2
task_id: T18
feature: public-site
status: todo
---

# T18 — Full public website

## Description
Expand the public website from the Phase-01 homepage to the full page set (spec §23): Home, About Us, Area History plus links to the module pages built in T03/T11–T17. Every page shows only safe, published content — never private member, payment or finance data. This task owns the public shell (nav/footer) and the About/History pages; module pages ship in their own tasks.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC4 | Full public page set | ⬜ |

## Implementation approach
1. Build the About Us and Area History static pages
2. Add a shared public nav/footer linking every public page
3. Ensure no public page pulls private data (relies on the safe views from T25/T03)

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Create | `about.html` | About Us page |
| Create | `history.html` | Area History page |
| Update | `index.html` | shared public nav/footer across pages |
| Update | `assets/css/style.css` | public page styles |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/public-site/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/public-site/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/public-site/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
