---
type: technical-context
spec_version: 1
feature: receipts
file_type: technical-context
contract_version: 1
status: done
depends_on: [payments, member-profile]
last_review: 2026-08-14
frozen: false
tags: [receipts, technical-context]
---

# Receipts — technical context

## Public surface
**Depends on:** payments (`payments` table, `receipt_no`), member-profile/members (member fields on
the receipt), admin-access (`checkAdminAccess()` on the admin side).
**Exposed to:** payments (admin + member pages link `receipt.html?no=<receipt_no>`).

**Exposes:**
```
receipt.html?no=<receipt_no>     -- the receipt page; viewer must be an active admin or the owner
public.receipt_self              -- view: receipt fields + member name/ID/house + recorded-by,
                                 -- rows visible to active admins or the owning member (email match)
send-receipt-email (edge fn)     -- POST { receipt_no }; admin-only; emails the branded receipt
```
**Callers MUST NOT:** route receipts/PDFs over SMS (BR5); read `payments` directly from public pages.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Branded print-friendly receipt + PDF download | AC1 | ✅ built | native print-to-PDF, no PDF lib |
| Reachable from profile & history | AC2 | ✅ built | profile → payments → receipt links |
| Email a receipt | AC3 | ✅ built | needs `supabase functions deploy` + RESEND_API_KEY |

## Logic
- `receipt.html`: reads `?no=`, queries `receipt_self` (server-side authorization), renders the
  branded sheet; `@media print` hides the actions so the browser's print-to-PDF is the download.
- `receipt_self` (in `rls.sql`): joins payments → members (→ admins for recorded-by); WHERE clause
  admits active admins or the owning member only.
- `send-receipt-email` edge function: verifies the caller's JWT is an active admin, loads the
  payment + member email with the service role, sends branded HTML via the Resend API. Email-only —
  no SMS path exists.
- `admin/payments.html`: per-row receipt link + "Email receipt" button invoking the function.

## Code file mapping
| File | Purpose |
|---|---|
| `receipt.html` | Branded receipt page (print/PDF) |
| `supabase/rls.sql` | `receipt_self` view |
| `supabase/functions/send-receipt-email/index.ts` | Admin-only email delivery (Resend) |
| `admin/payments.html` | Receipt link + email action per payment |
| `member/payments.html` | Receipt link per own payment |
| `member/profile.html` | "My payments" link (profile → history → receipt) |

## API / data contracts
- `select * from receipt_self where receipt_no = ?` (authenticated; row-limited server-side).
- `POST functions/v1/send-receipt-email` `{ receipt_no }` → `{ ok, sent_to }` | `{ error }`.

## Known issues
- Email is the rendered HTML receipt, not a PDF attachment — the member can print-to-PDF from the
  receipt page; attach a generated PDF later only if the client asks.
- The edge function requires deployment + the `RESEND_API_KEY` secret; the from-address domain
  must be verified in Resend.
