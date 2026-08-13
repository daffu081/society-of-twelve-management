---
spec_version: 1
file_type: task
phase: 1
task_id: T01
feature: admin-access
status: todo
---

# T01 — Admin access (magic-link login + active-admin gate + logout)

> **Built, unverified.** Code is in place; `login.html` password field removed (now magic-link only).
> ACs need a live Supabase + real `config.js` creds to verify — kept `status: todo` until then.

## Description
Deliver secure, passwordless admin sign-in and the gate that lets only active admins reach the
dashboard, plus logout. This is the foundation every admin module in later phases builds on.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Request login link | ⬜ |
| AC2 | Active admin gets in | ⬜ |
| AC3 | Non-admin is rejected | ⬜ |
| AC4 | Logout | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-01/requirement/admin-access/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/admin-access/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/admin-access/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
