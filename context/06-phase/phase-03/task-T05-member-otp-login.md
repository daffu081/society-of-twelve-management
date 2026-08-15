---
spec_version: 1
file_type: task
phase: 3
task_id: T05
feature: member-profile
status: todo
---

# T05 — Member mobile one-time-code (OTP) login

## Description
Let a member sign in with a one-time code sent to their mobile, once an SMS provider is connected.
Codes are short-lived, single-use and scoped to the member they were sent to. Promoted from backlog
row 12 — **blocked until an SMS provider is connected**; the sending path depends on that provider.

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC7 | Member logs in with a mobile one-time code | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-03/requirement/member-profile/requirement.md` | the AC (pure business) this task delivers |
| `context/05-features/member-profile/technical-context.md` | current member portal + login state |
| `context/05-features/sms/technical-context.md` | SMS provider surface the code is sent through |
| `context/05-features/member-profile/test-context.md` | existing coverage table |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅

> ⚠️ Blocked: requires a connected SMS provider before AC7 can be exercised end-to-end.
