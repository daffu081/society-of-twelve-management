---
type: technical-context
spec_version: 1
feature: birthday
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: [sms, members]
last_review: 2026-08-14
frozen: false
tags: [birthday, technical-context]
---

# Birthday automation — technical context

## Public surface
**Depends on:** members (`dob`, `mobile`), sms (the `birthday_wish` template + provider secrets).
**Exposed to:** dashboard (renders the upcoming-birthdays panel).

**Exposes:**
```
birthday-cron (edge fn)   -- CRON_SECRET-gated daily job; sends today's greetings
public.birthday_logs      -- yearly dedup: unique(member_id, birthday_year), links sms_log_id
```
**Callers MUST NOT:** trigger greetings manually from app code (BR3 — scheduler only);
insert `birthday_logs` outside the cron.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Detect today's birthdays | AC1 | ✅ built | dob month-day match, active + mobile only |
| Once-per-year send + log | AC2, AC4 | ✅ built | logs written on success only → auto-retry |
| Admin birthday calendar | AC3 | ✅ built | next-30-days panel on the dashboard |

## Logic
- `birthday-cron` fn: gated by `Authorization: Bearer CRON_SECRET`; loads the editable
  `birthday_wish` template, filters active members with today's month-day not yet in
  `birthday_logs` for this year, posts each greeting through the same provider config as
  `send-sms`, then records `sms_logs` (sent) + `birthday_logs`. Failure/absent provider → no
  rows, so tomorrow's run retries (documented edge case).
- Dashboard panel: computes each member's next birthday client-side and lists those within 30
  days, soonest first ("🎂 today" on the day).

## Code file mapping
| File | Purpose |
|---|---|
| `supabase/functions/birthday-cron/index.ts` | Daily scheduled greeting job |
| `admin/dashboard.html` | Upcoming-birthdays panel |
| `supabase/schema.sql` | `birthday_logs` table (pre-existing) |

## API / data contracts
- Scheduler → `POST functions/v1/birthday-cron` with the CRON_SECRET bearer → summary JSON.
- Deploy note: schedule daily (e.g. `0 4 * * *`) via Supabase cron; set `CRON_SECRET` plus the
  shared SMS provider secrets.

## Known issues
- Delivery inactive until an SMS provider is contracted (backlog #14); the calendar works today.
- `birthday_logs` has no RLS yet — covered by the remaining-tables hardening (backlog #16 / T25).
