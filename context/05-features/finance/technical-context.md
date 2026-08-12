---
type: technical-context
spec_version: 1
feature: finance
file_type: technical-context
contract_version: 1
status: planned
depends_on: [admin-access, payments]
last_review: 2026-08-13
frozen: false
tags: [finance, technical-context]
---

# finance — technical context

> Not built yet. This is the intended shape; keep it in sync with code once work starts.

## Public surface
**Depends on:** admin-access, payments
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
| `admin/finance.html` | Admin page (to create) |
| `admin/finance.js` | Page logic (to create) |
| `income`, `expenses` | Backing table(s) in `supabase/schema.sql` |

## API / data contracts
- Supabase selects/inserts on `income`, `expenses`, guarded by `checkAdminAccess()`.

## Known issues
- Not started.
