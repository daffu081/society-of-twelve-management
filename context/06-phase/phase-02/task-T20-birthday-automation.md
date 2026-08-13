---
spec_version: 1
file_type: task
phase: 2
task_id: T20
feature: birthday
status: todo
---

# T20 — Birthday automation

## Description
Birthday automation (spec §13): a scheduled daily job finds members whose DOB matches today and automatically sends the birthday SMS with the member's real name, with no manual trigger. A yearly delivery log prevents duplicates, an admin birthday calendar shows upcoming birthdays, and the message body stays editable via the SMS templates (T19).

## Delivers these ACs
| AC | Title | Done? |
|----|-------|-------|
| AC3 | Admin birthday calendar | ⬜ |
| AC4 | Automatic once-per-year greeting | ⬜ |

## Implementation approach
1. Add a birthday_log table for once-per-year dedup
2. Build the admin birthday calendar/list from member DOBs
3. Create a scheduled edge function that finds today's birthdays and sends via T19
4. Verify {member_name} resolves correctly and log each send yearly

## Files to create / modify
| Action | File | Why |
|--------|------|-----|
| Create | `supabase/functions/birthday-cron/index.ts` | daily scheduled birthday send |
| Update | `supabase/schema.sql` | birthday_log (yearly dedup) |
| Update | `admin/dashboard.html` | birthday calendar/list |
| Update | `supabase/functions/send-sms/index.ts` | reuse the send path |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/phase-02/requirement/birthday/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/birthday/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/birthday/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
