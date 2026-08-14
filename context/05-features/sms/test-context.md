---
type: test-context
spec_version: 1
feature: sms
file_type: test-context
contract_version: 1
status: in_progress
depends_on: [admin-access, members]
last_review: 2026-08-14
frozen: false
tags: [sms, test-context]
---

# sms — test context

> No automated runner yet — manual checks (needs live Supabase; AC5/AC6 delivery additionally
> needs the send-sms function deployed and a provider configured).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC4 edit templates | 🟢 manual | — |
| AC5 send and log | 🟢 manual | — |
| AC6 provider replaceable + secret-safe | 🟢 manual | — |
| AC1–AC3 (earlier numbering) | covered by AC4–AC6 | — |
| No-provider path | 🟢 manual | — |

## Manual checks
- AC4: edit a template's Bangla wording (with `sms_template_edit`) → saved; the composer preview
  uses the new wording. An admin without the key sees read-only bodies and RLS rejects edits.
- AC5: pick a member + due_reminder → `{member_name}` and `{due_amount}` resolve; edit and send →
  the log row shows sent (or pending on 503) with recipient, template, timestamp, status, sender.
- AC6: grep the repo — no provider secret appears in any browser file; switching provider =
  changing SMS_PROVIDER_URL/SMS_API_KEY secrets only, no code edit.
- No-provider: with SMS_PROVIDER_URL unset the send reports the 503 message and the row stays
  pending, retryable via "Send now".
