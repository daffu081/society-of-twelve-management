---
type: technical-context
spec_version: 1
feature: notices
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [notices, technical-context]
---

# notices — technical context

## Public surface
**Depends on:** admin-access; executive-admins (`has_permission()` keys `notices_read`,
`notices_write`, `notices_publish`, `sms_send`); sms (the pending-row queue).
**Exposed to:** public-site (running-notice banner reads published rows; `notices.html` lists them).

**Exposes:**
```
public.notices           -- table; anon sees published AND NOT archived only (RLS)
next_notice_ref_no()     -- SOT-NOT-YYYYMM-0001 generator (ref_no default)
sms_logs 'notice'        -- convention: one pending row per active member per notice send
```
**Callers MUST NOT:** flip `published` without the `notices_publish` key (a trigger blocks it);
show unpublished/archived notices publicly.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Create/publish notice + ref no | AC1, AC3 | ✅ built | draft → publish → archive lifecycle |
| Running notice flag | AC2 | ✅ built | flag on the form; homepage banner is public-site |
| Meeting fields (date/time/venue) | AC4 | ✅ built | required for meeting type, validated client-side |
| Reviewed SMS to active members | AC5 | ✅ built | sms_send-gated; editable composer |

## Logic
- `admin/notices.html`: guarded; conditional meeting fields; save leaves a draft (`ref_no` from
  the DB default); list actions publish/unpublish (trigger checks `notices_publish`, stamps
  `published_at`), archive (clears running), edit, and an SMS composer queueing one pending
  `notice` row per active member.
- `notices.html` (public): lists what RLS exposes — published, non-archived, newest first, with
  meeting details and a Running tag.
- `supabase/rls.sql`: public read policy + keyed admin policies + the publish guard trigger.
- `supabase/schema.sql`: meeting columns, `archived`, `notice_counters` + `next_notice_ref_no()`.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/notices.html` | Notice/meeting management + SMS composer |
| `notices.html` | Public published-notices page |
| `supabase/schema.sql` | notices columns + ref-no generator |
| `supabase/rls.sql` | notices RLS + publish guard |
| `admin/dashboard.html` | Notices card links here |

## API / data contracts
- Select/insert/update on `notices` (keyed); public select limited by RLS.

## Known issues
- The Phase-01 homepage running-notice banner is static text — wiring it to live running notices
  belongs to public-site (T18).
