---
type: technical-context
spec_version: 1
feature: executive-admins
file_type: technical-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [executive-admins, technical-context]
---

# executive-admins — technical context

## Public surface
**Depends on:** admin-access (`checkAdminAccess()`, the `admins` table shape).
**Exposed to:** every permission-gated feature (members, payments, finance, …).

**Exposes:**
```
public.has_permission(cap text)  -- capability check: super_admin, or permissions->>cap = true
public.is_super_admin()          -- true when caller is an active Super Admin
permission-key catalog           -- <area>_read / <area>_write for members, payments, finance,
                                 -- notices, projects, mahfil, sms, birthday, awards, rules,
                                 -- reports, committee, settings; plus notices_publish, sms_send,
                                 -- sms_template_edit, birthday_manage, reports_export
                                 -- (single source: CATALOG in admin/executives.html)
```
**Callers MUST NOT:** gate features by hiding menus only (BR5) — every feature's RLS must check
`has_permission()`; invent keys outside the catalog.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Add executive admin | AC1 | ✅ built | insert with empty permissions |
| Checkbox permission matrix | AC2, AC4 | ✅ built | full BR4 catalog; RLS-enforced keys |
| Deactivate admin | AC3 | ✅ built | status select in the matrix panel |
| Last-Super-Admin guard | AC5 | ✅ built | DB trigger on update + delete |

## Logic
- `admin/executives.html`: Super-Admin-only (client gate + `admins_super_all` RLS). Lists admins,
  adds executives, and per admin shows the checkbox matrix built from `CATALOG`; save writes the
  checked keys as `admins.permissions` jsonb, plus role/active.
- `supabase/rls.sql`: `is_super_admin()`; admins RLS (self-read for the login gate, super manage);
  `admins_protect_last_super` trigger raises on removing/demoting/deactivating the final active
  Super Admin; members/payments/finance/fee_categories policies keyed to the catalog.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/executives.html` | Admin list + add-executive + permission matrix (the key catalog) |
| `supabase/rls.sql` | `is_super_admin()`, admins RLS, last-super trigger, keyed policies |
| `admin/dashboard.html` | Executive Admins card links here |

## API / data contracts
- Select/insert/update on `admins` (Super Admin via RLS); permissions stored as flat jsonb
  `{ "<key>": true }` — absent = denied.

## Known issues
- Feature areas not yet built (notices, sms, …) have catalog keys but no RLS policies yet — each
  T1x task adds its own keyed policies as its tables gain RLS.
- BR7 (future Super-Admin transfer mechanism) is satisfied by role reassignment on this screen;
  a formal handover flow is not built.
