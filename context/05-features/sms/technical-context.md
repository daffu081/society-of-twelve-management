---
type: technical-context
spec_version: 1
feature: sms
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: [admin-access, members]
last_review: 2026-08-14
frozen: false
tags: [sms, technical-context]
---

# sms — technical context

## Public surface
**Depends on:** admin-access, members (recipient mobile); executive-admins (`sms_read`,
`sms_send`, `sms_template_edit` keys).
**Exposed to:** payments (`payment_success` queue rows), due-payments (`due_reminder`),
notices (`general_notice`/`meeting_notice`), birthday (`birthday_wish`).

**Exposes:**
```
public.sms_templates      -- table; six seeded Bangla templates with placeholders;
                          -- editing needs sms_template_edit
public.sms_logs           -- the queue + log: producers insert status='pending' rows
                          -- {member_id, template_key, message_body, sent_by};
                          -- send-sms flips them to sent/failed
send-sms (edge fn)        -- POST { log_id }; sms_send-gated; provider-agnostic via
                          -- SMS_PROVIDER_URL / SMS_API_KEY / SMS_SENDER_ID secrets
```
**Callers MUST NOT:** put provider secrets in browser code (BR8); send outside the queue;
route PDFs over SMS (receipts BR5).

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Manage templates | AC1, AC4 | ✅ built | inline editor; seed survives re-runs |
| Send & log | AC2, AC5 | ✅ built | queue → edge fn → sent/failed + recipient snapshot |
| Provider integration | AC3, AC6 | ✅ built (unconfigured) | 503 + stays pending until SMS_PROVIDER_URL set |

## Logic
- `admin/sms.html`: template table (editable with `sms_template_edit`); composer resolves
  `{member_name}`/`{due_amount}` into an editable body, queues a pending row, then invokes
  `send-sms`; queue/log view with per-row "Send now" for pending rows (incl. rows queued by
  payments/due/notices).
- `send-sms` fn: re-checks `sms_send` server-side, loads the pending row + member mobile, posts
  one generic JSON payload (`to`, `message`, `sender_id`) to `SMS_PROVIDER_URL`, updates the row
  (status, provider_message_id, recipient_mobile, sent_at). `ponytail:` a per-provider adapter is
  added only when a contracted provider's API demands it.
- RLS (in `rls.sql`): templates admin-read / keyed-edit; logs keyed-read / admin-queue; status
  updates only via the function's service role.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/sms.html` | Template editor + composer + queue/log |
| `supabase/functions/send-sms/index.ts` | Provider-agnostic dispatch |
| `supabase/schema.sql` | `sms_logs.recipient_mobile` |
| `supabase/seed.sql` | Six Bangla templates (BR5) |
| `supabase/rls.sql` | sms_templates + sms_logs policies |

## API / data contracts
- Queue convention (producers): insert `sms_logs` with `status='pending'` and a fully-resolved
  `message_body` — the function never re-renders templates.
- `POST functions/v1/send-sms` `{ log_id }` → `{ ok, status, sent_to }` | `{ error }` (503 when
  no provider configured; the row stays pending).

## Known issues
- No provider contracted — deliveries return 503 and stay queued (backlog #14 deploy runbook).
- Mobile OTP login remains out of scope until a provider exists.
