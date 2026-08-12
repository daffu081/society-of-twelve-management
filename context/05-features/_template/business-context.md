---
type: business-context
spec_version: 1
feature: [feature]
file_type: business-context
contract_version: 1
status: planned
depends_on: []
last_review: YYYY-MM-DD
frozen: false
tags: [[feature], business-context]
---

# [Feature name] — business context

> **Written first, before any code — by whoever knows the business need (product/client).**
> Pure business language. No file names, no classes, no tech. If a non-technical person
> can't read it, it's in the wrong file — put that in `technical-context.md`.

## Goal
<!-- One paragraph: what this feature achieves and why the business wants it. -->

## User stories
- US1: As a [actor], I can [action] so that [outcome]
- US2:

## Business rules
- BR1: <!-- a concrete rule the business requires, in plain language -->
- BR2:

## What this feature owns
- <!-- the responsibilities that belong to this feature -->

## What this feature does NOT own
- <!-- things that belong to other features -->

## Out of scope (not planned)
- <!-- explicitly not doing -->

## Acceptance criteria

> When is the client satisfied? Each AC is one observable outcome, in business terms, that
> traces back to a user story or business rule. No test files or tiers here — those live in
> `test-context.md`.
> Format: Given (starting situation) → When (what the user does) → Then (what they see).

### AC1: <short title>
- **Trace**: US1, BR1
- **Given**: <starting situation>
- **When**: <the action>
- **Then**: <the outcome the client can observe>

### AC2: <…>

### Edge & error cases
<!-- Empty state, each rejection the business cares about, undo/restore, etc. -->
