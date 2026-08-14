---
type: test-context
spec_version: 1
feature: birthday
file_type: test-context
contract_version: 1
status: in_progress
depends_on: [sms, members]
last_review: 2026-08-14
frozen: false
tags: [birthday, test-context]
---

# Birthday automation — test context

> No automated runner yet — manual checks (AC4 needs the function deployed with CRON_SECRET and
> a configured SMS provider; use a test provider endpoint).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC3 birthday calendar | 🟢 manual | — |
| AC4 automatic once-per-year greeting | 🟢 manual | — |
| Retry on provider failure | 🟢 manual | — |

## Manual checks
- AC3: give members DOBs within the next 30 days → the dashboard panel lists them soonest-first;
  a member whose birthday is today shows "🎂 today"; members without a DOB are absent.
- AC4: set a member's dob to today and invoke the cron with the CRON_SECRET → an sms_logs row
  (sent, real name in the body) plus a birthday_logs row for this year appear; invoke again →
  nothing new (yearly dedup). Wrong/missing secret → 403.
- Retry: with the provider unreachable, the run reports failure and writes no rows; the next run
  picks the member up again.
