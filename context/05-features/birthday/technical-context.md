---
type: technical-context
spec_version: 1
feature: birthday
file_type: technical-context
contract_version: 1
status: planned
depends_on: [sms, members]
last_review: 2026-08-13
frozen: false
tags: [birthday, technical-context]
---

# birthday — technical context

> Not built yet. Intended shape; sync to code once work starts.

## Public surface
**Depends on:** sms, members
**Exposed to:** <!-- filled when consumers appear -->

**Exposes:**
```
<!-- signatures added by /implement-task as the feature is built -->
```
**Callers MUST NOT:** bypass `checkAdminAccess()`; hard-delete rows; use floats for money.

## Implementation status
| Capability | Status | Notes |
|---|---|---|
| (all) | Not started | Blocked on the sms feature / provider; scheduling mechanism (cron/edge function) not chosen. |

## Code file mapping (intended)
| File | Purpose |
|---|---|
| `admin/birthday.html` | Admin page (to create) |
| `admin/birthday.js` | Page logic (to create) |
| `birthday_logs` | Backing table(s) in `supabase/schema.sql` |

## API / data contracts
- Supabase selects/inserts on `birthday_logs`, guarded by `checkAdminAccess()`.

## Known issues
- Not started.
