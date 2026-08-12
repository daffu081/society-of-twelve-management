---
spec_version: 1
type: shared-convention
title: "Testing Conventions"
tags: [shared, conventions, testing]
file_type: shared
frozen: false
last_review: 2026-08-13
---

# Testing conventions
# Read before writing any test.

> **Current state: there is no test runner in this project.** No framework is installed and no
> tests exist. The tiers below are the target once testing is introduced; until then, "tested"
> means a documented manual check (see each feature's `test-context.md`). Introducing a runner
> (e.g. Vitest/Playwright) is an architectural change — add an ADR + a `package.json` first.

## Test tiers (the gate — a feature is Done only when all required tiers are green)
| Tier | Roughly | What it covers |
|---|---|---|
| Unit | ~60% | pure JS logic (validators, receipt-number generation, fee/finance math) |
| Component | ~20% | a rendered admin view shows the right state |
| Integration | ~15% | a flow against a real (test) Supabase project or a stubbed client |
| E2E | ~5% | admin login → do an action → see it persisted |

## Manual test log (until automation exists)
Each feature's `test-context.md` lists its ACs with a manual verification step and pass/fail.

## Naming (once a runner exists)
- Test file: `<source>.test.js` mirroring the source path.
- Test name: starts with a verb — "returns error when member inactive".

## Rules
- T1: Never hit a real production Supabase project from a test — use a throwaway project or stub the client.
- T2: Fresh test data per run; clean up (or use the `bin`) — never leave test rows in shared data.
- T3: Do not write tests for capabilities marked "Not started".
- T4: Money assertions compare exact decimal strings, never floats.
