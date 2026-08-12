---
type: test-context
spec_version: 1
feature: [feature]
file_type: test-context
contract_version: 1
status: planned
depends_on: []
last_review: YYYY-MM-DD
frozen: false
tags: [[feature], test-context]
---

# [Feature name] — test context

> **Empty until development starts.** The developer fills this in *while building* — one row
> per acceptance criterion in `business-context.md`, mapped to the test that proves it.

## Coverage status
| AC / scenario | Status | Test file |
|---|---|---|
| Happy path | Not tested | — |
| Error / failure | Not tested | — |

## Test gate — feature is not Done until every required tier is green
### Unit
- <!-- domain logic / validators — every business rule -->
- <!-- data access, view-model state transitions -->

### Component / Widget
- <!-- each UI state renders; one happy-path interaction -->

### Integration (real in-memory persistence, mocked remote)
- <!-- one file per cross-feature flow -->

### E2E
- <!-- the critical user journey -->

## Test helpers and factories
```
// <path>/fixtures/[feature] — minimal entity factories
```

## Rules for writing new tests
- T1: mock the layer below — never hit real network.
- T2: fresh in-memory store per test.
- T3: do not test capabilities marked "Not started".
- T4: inject the clock; never call "now" directly.
