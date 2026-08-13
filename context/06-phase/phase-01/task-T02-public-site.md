---
spec_version: 1
file_type: task
phase: 1
task_id: T02
feature: public-site
status: done
---

# T02 — Public site (homepage + footer year + developer credit/branding)

## Description
Deliver the public Bengali homepage with consistent Society of Twelve branding and a footer that
shows the developer credit and the current year automatically. This is the public shell the
community sees before login.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Homepage renders | ✅ |
| AC2 | Footer year is current | ✅ |
| AC3 | Footer shows developer credit and consistent branding | ✅ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-01/requirement/public-site/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/public-site/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/public-site/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
