---
type: technical-context
spec_version: 1
feature: technical-team
file_type: technical-context
contract_version: 1
status: done
depends_on: []
last_review: 2026-08-14
frozen: false
tags: [technical-team, technical-context]
---

# Technical Team — technical context

## Public surface
**Depends on:** none.
**Exposed to:** public-site (footer credit links here).

**Exposes:**
```
technical-team.html   -- static public page; no data model, no Supabase
```
**Callers MUST NOT:** add a data model or admin surface without a new requirement.

## Implementation status
| Capability | AC | Status | Notes |
|---|---|---|---|
| Developer credit page | AC1 | ✅ built | static; verifiable by opening the file |

## Logic
- `technical-team.html`: static card showing "Sabbir Ahmed Sakib — Developer"; homepage footer
  credit links to it.

## Code file mapping
| File | Purpose |
|---|---|
| `technical-team.html` | Static public credit page |
| `index.html` | Footer credit links here |

## API / data contracts
- None — static content by design (spec §26).

## Known issues
- None.
