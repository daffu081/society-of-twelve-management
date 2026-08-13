---
type: technical-context
spec_version: 1
feature: _cross-cutting
file_type: technical-context
contract_version: 1
status: done
depends_on: []
last_review: 2026-08-13
frozen: false
tags: [_cross-cutting, technical-context]
---

# Cross-cutting — technical context

## Public surface
**Depends on:** none
**Exposed to:** every page loads `config.js`
**Exposes:** `window.SOT_CONFIG = { SUPABASE_URL, SUPABASE_ANON_KEY }` — public values only.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| No secret credentials in client code | AC1 | Done | `config.js` holds only URL + anon-key placeholders, with an explicit "never the service-role key" comment |

## Logic
- `config.js` is the only committed config the browser reads. It carries the project URL and the **anon** (public) key only. Data protection is Postgres RLS, not secrecy of the anon key.

## Code file mapping
| File | Purpose |
|---|---|
| `config.js` | `window.SOT_CONFIG` — anon key only; documented ban on service-role key |

## Known issues
- No automated guard yet prevents a future edit from pasting a secret into `config.js` — relies on the file comment + review.
