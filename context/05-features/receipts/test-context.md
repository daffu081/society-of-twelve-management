---
type: test-context
spec_version: 1
feature: receipts
file_type: test-context
contract_version: 1
status: done
depends_on: [payments, member-profile]
last_review: 2026-08-14
frozen: false
tags: [receipts, test-context]
---

# Receipts — test context

> No automated runner yet — manual checks (needs live Supabase; AC3 also needs the edge function
> deployed with RESEND_API_KEY).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 branded receipt + PDF | 🟢 manual | — |
| AC2 reachable from profile & history | 🟢 manual | — |
| AC3 email a receipt | 🟢 manual | — |
| Not-owner / unknown receipt | 🟢 manual | — |

## Manual checks
- AC1: open `receipt.html?no=<a real receipt>` as the owner or an admin → all spec §10 fields
  render; "Print / Save as PDF" produces a clean PDF (actions hidden in print).
- AC2: from `member/profile.html` → "My payments" → click a receipt → it opens; same from the
  admin payments list.
- AC3: click "Email receipt" on a payment → success message names the member's email; the inbox
  receives the branded receipt. A member with no email shows "Member has no email on file".
- Isolation: member B opening member A's receipt URL sees "not found / not allowed"; anon sees the
  sign-in message.
