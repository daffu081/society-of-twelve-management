---
type: technical-context
spec_version: 1
feature: sms
file_type: technical-context
contract_version: 1
status: planned
depends_on: [admin-access, members]
last_review: 2026-08-13
frozen: false
tags: [sms, technical-context]
---

# sms — technical context

> Not built yet. Intended shape; sync to code once work starts.

## Public surface
**Depends on:** admin-access, members
**Exposed to:** <!-- filled when consumers appear -->

**Exposes:**
```
<!-- signatures added by /implement-task as the feature is built -->
```
**Callers MUST NOT:** bypass `checkAdminAccess()`; hard-delete rows; use floats for money.

## Implementation status
| Capability | Status | Notes |
|---|---|---|
| (all) | Not started | Blocked on external SMS provider selection; no send integration exists. |

## Code file mapping (intended)
| File | Purpose |
|---|---|
| `admin/sms.html` | Admin page (to create) |
| `admin/sms.js` | Page logic (to create) |
| `sms_templates`, `sms_logs` | Backing table(s) in `supabase/schema.sql` |

## API / data contracts
- Supabase selects/inserts on `sms_templates`, `sms_logs`, guarded by `checkAdminAccess()`.

## Known issues
- Not started. **Blocked** on choosing/contracting an SMS provider; `config.js` has no provider creds.
