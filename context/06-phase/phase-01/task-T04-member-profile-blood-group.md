---
spec_version: 1
file_type: task
phase: 1
task_id: T04
feature: member-profile
status: todo
---

# T04 — Member profile blood group

> **Built, unverified.** Blood-group column added; minimal `admin/members.html` (registration form
> + list) hosts capture & display. ACs need a live Supabase to verify — kept `status: todo` until then.

## Description
Capture a member's blood group on the registration form and show it on their member profile.
This brings the first member-profile field into the foundation phase.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC1 | Blood group captured at registration | ⬜ |
| AC2 | Blood group shown on the member profile | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-01/requirement/member-profile/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/member-profile/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/member-profile/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
