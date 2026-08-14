---
type: test-context
spec_version: 1
feature: _cross-cutting
file_type: test-context
contract_version: 1
status: done
depends_on: []
last_review: 2026-08-15
frozen: false
tags: [_cross-cutting, test-context]
---

# Cross-cutting — test context

> No automated runner yet — manual checks (AC2–AC3 need a live Supabase with rls.sql applied;
> AC4 needs the buckets created per supabase/storage.md).

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| AC1 no secrets in client | ✅ verified (inspection) | — |
| AC2 enforced access control | 🟢 manual | — |
| AC3 public exposure safe-only | 🟢 manual | — |
| AC4 storage split | 🟢 manual | — |

## Manual checks
- AC2: with only the anon key (no login), attempt to select every table → members/payments/
  finance/etc. return nothing; as a logged-in member, select `members`/`payments` → only own rows
  (via the *_self views), never another member's. Every table reports RLS enabled.
- AC3: run each public query (`members_public`, published notices/projects/mahfils, visible
  committee/founding/awards, published rules) → no NID/Birth-Reg/Passport, no payment/finance
  column is present in any result.
- AC4: upload a photo to `public-media` → reachable by public URL; upload an identity doc to
  `private-docs` → no public URL, and an anon fetch is denied; only an admin gets a signed URL.

## Rules for writing new tests
- Prove enforcement by querying directly with the anon key, not through the UI.
