---
type: technical-context
spec_version: 1
feature: admin-access
file_type: technical-context
contract_version: 1
status: done
depends_on: []
last_review: 2026-08-15
frozen: false
tags: [admin-access, technical-context]
---

# Admin access — technical context

## Public surface
**Depends on:** none
**Exposed to:** every admin feature (all admin pages guard with it)

**Exposes:** (from `admin/admin.js`, loaded globally)
```
supabaseClient                          // shared Supabase client
async checkAdminAccess() -> { user, admin } | null   // null after redirecting to login
async logoutAdmin() -> void
```
**Callers MUST NOT:** create a second Supabase client; render any admin data before `checkAdminAccess()` resolves truthy.

## Implementation status
| Capability | Status | Notes |
|---|---|---|
| Magic-link login | Done | `signInWithOtp`, redirects to `admin/dashboard.html` |
| Active-admin gate | Done | queries `admins` by `auth_user_id`, `active=true` |
| Role display | Done | dashboard shows super/executive label |
| Logout | Done | `signOut()` + `sessionStorage.clear()` |

## Logic
- On login submit: disable button, `signInWithOtp({ email, emailRedirectTo: origin + "/admin/dashboard.html" })`, show success/error.
- `checkAdminAccess()`: `getUser()`; if none → `login.html`; else fetch matching active `admins` row; if none → `signOut()` + alert + `login.html`.

## Code file mapping
| File | Purpose |
|---|---|
| `admin/login.html` | Passwordless login form (email only → "Send Login Link") |
| `admin/admin.js` | Client, login handler, `checkAdminAccess`, `logoutAdmin` |
| `admin/dashboard.html` | Calls `checkAdminAccess`, renders name/role |
| `admins` (table) | `auth_user_id`, `role`, `active`, `permissions` |

## API / data contracts
- `supabaseClient.auth.signInWithOtp(...)`
- `supabaseClient.from("admins").select("*").eq("auth_user_id", user.id).eq("active", true).single()`

## Known issues
- No Postgres RLS: the `admins` gate is client-side only and bypassable via the anon API — see ADR-001 / db-conventions D6.

## Resolved
- (T01) `login.html` password field removed — the form is now magic-link only, matching `admin.js`. (AC1)
