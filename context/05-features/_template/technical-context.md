---
type: technical-context
spec_version: 1
feature: [feature]
file_type: technical-context
contract_version: 1
status: planned
depends_on: []
last_review: YYYY-MM-DD
frozen: false
tags: [[feature], technical-context]
---

# [Feature name] — technical context

> **Empty until development starts.** The developer fills this in *while building* — it's the
> "how" for `business-context.md`'s "what". Keep it in sync with the code, not aspirational.

## Public surface
<!-- THE ONLY section other features may read. Keep it small — interface, not internals.
     Written by `/implement-task`; changing it bumps `contract_version` and updates consumers. -->

**Depends on:** <!-- other-feature or none -->
**Exposed to:** <!-- other-feature or none -->

**Exposes:**
```
<!-- the entities / functions / endpoints callers may use — signatures only -->
```
**Callers MUST NOT:** <!-- forbidden access patterns -->

## Implementation status
| Capability | Status | Notes |
|---|---|---|
| <!-- capability --> | Not started | — |

## Logic
<!-- One short line per meaningful piece of logic / component: what it does. -->
- <!-- e.g. "Validates note text is non-empty before save" -->

## Code file mapping
| File | Purpose |
|---|---|
| `<path/to/entity>` | Domain entity |
| `<path/to/repository>` | Data access |
| `<path/to/screen>` | UI entry point |

## API / data contracts
<!-- Endpoints, queries, or events this feature consumes/exposes. -->
- [METHOD] /[path] — request/response, errors (codes from `02-shared/error-codes.md`)

## Known issues
- None
