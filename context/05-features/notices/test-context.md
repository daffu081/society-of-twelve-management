---
type: test-context
spec_version: 1
feature: notices
file_type: test-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [notices, test-context]
---

# notices — test context

> No automated runner yet — manual checks (needs live Supabase with schema + rls applied).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC3 create & publish with ref no | 🟢 manual | — |
| AC4 meeting notice fields | 🟢 manual | — |
| AC5 reviewed SMS | 🟢 manual | — |
| Unpublished/archived stay private | 🟢 manual | — |

## Manual checks
- AC3: create a notice → saved as draft with a `SOT-NOT-YYYYMM-0001` ref; a second increments.
  Publish → appears on public `notices.html`; archive → disappears. An admin without
  `notices_publish` gets the trigger error when publishing.
- AC4: choosing "Meeting notice" requires date/time/venue; the public card shows all three.
- AC5: the SMS button (only with `sms_send`) opens a prefilled editable message; sending queues
  one pending `notice` row in `sms_logs` per active member with the edited text.
- Privacy: anon queries return only published, non-archived rows.
