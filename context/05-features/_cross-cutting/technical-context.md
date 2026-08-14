---
type: technical-context
spec_version: 1
feature: _cross-cutting
file_type: technical-context
contract_version: 1
status: done
depends_on: []
last_review: 2026-08-15
frozen: false
tags: [_cross-cutting, technical-context]
---

# Cross-cutting — technical context

## Public surface
**Depends on:** admin-access (`is_active_admin`, `is_super_admin`, `has_permission`).
**Exposed to:** every feature — this is the enforcement substrate.
**Exposes:**
```
window.SOT_CONFIG = { SUPABASE_URL, SUPABASE_ANON_KEY, PUBLIC_BUCKET } -- public values only
storage buckets: public-media (public) / private-docs (private)       -- see supabase/storage.md
RLS coverage: every public.* table has row level security enabled
safe public views: members_public + published/visible-row policies    -- no private column
```
**Callers MUST NOT:** disable RLS to make a feature work (BR5); put a secret in `config.js`;
store identity documents in `public-media`; expose a private column through a public view.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| No secrets in client code | AC1 | Done | `config.js` anon key only (Phase 01) |
| Enforced access control (RLS everywhere) | AC2 | ✅ built | all tables RLS'd; members reach only own rows |
| Public exposure safe-only | AC3 | ✅ built | safe views expose no private/payment/finance field |
| Storage public/private split | AC4 | ✅ built | policy in `supabase/storage.md`; buckets set in dashboard |

## Logic
- RLS sweep (in `rls.sql`): every `public.*` table has RLS enabled. Domain tables use
  permission-keyed or ownership policies; counter tables have RLS on with no client policy
  (function-only); `birthday_logs` is sms_read-gated. The file ends with a coverage summary.
- Member isolation: `members_self` / `payments_self` / `receipt_self` return only the caller's
  own rows (email match) and omit NID/Birth-Reg/Passport.
- Public safety: anon reads hit only safe views/policies (`members_public`, published/visible
  rows) — no payment, finance or identity column is present.
- Storage: `public-media` (world-read, admin-write) for images; `private-docs` (admin-only, no
  public URL, signed-URL access) for identity documents — see `supabase/storage.md`.

## Code file mapping
| File | Purpose |
|---|---|
| `config.js` | `window.SOT_CONFIG` — anon key + public bucket only |
| `supabase/rls.sql` | RLS on every table + coverage summary |
| `supabase/storage.md` | public vs private bucket policy |

## Known issues
- No automated guard prevents a future edit pasting a secret into `config.js` — relies on the
  file comment + review (Phase-01 known issue, unchanged).
- Storage buckets/policies are applied in the Supabase dashboard (no migration framework — D5);
  `storage.md` is the source of truth to replay them.
