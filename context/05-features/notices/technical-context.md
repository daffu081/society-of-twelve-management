---
type: technical-context
spec_version: 1
feature: notices
file_type: technical-context
contract_version: 1
status: planned
depends_on: [admin-access]
last_review: 2026-08-13
frozen: false
tags: [notices, technical-context]
---

# notices — technical context

> Not built yet. Intended shape; sync to code once work starts.

## Public surface
**Depends on:** admin-access
**Exposed to:** <!-- filled when consumers appear -->

**Exposes:**
```
<!-- signatures added by /implement-task as the feature is built -->
```
**Callers MUST NOT:** bypass `checkAdminAccess()`; hard-delete rows; use floats for money.

## Implementation status
| Capability | Status | Notes |
|---|---|---|
| (all) | Not started | dashboard card only; no page/script wired |

## Code file mapping (intended)
| File | Purpose |
|---|---|
| `admin/notices.html` | Admin page (to create) |
| `admin/notices.js` | Page logic (to create) |
| `notices` | Backing table(s) in `supabase/schema.sql` |

## API / data contracts
- Supabase selects/inserts on `notices`, guarded by `checkAdminAccess()`.

## Known issues
- Not started.
