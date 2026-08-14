---
type: business-context
spec_version: 1
feature: technical-team
file_type: business-context
contract_version: 1
status: done
depends_on: []
last_review: 2026-08-14
frozen: false
tags: [technical-team, business-context]
---

# Technical Team — business context

## Goal
Show the developer/technical-team credit publicly.

## User stories
- US1: As a visitor, I can see the technical team credit, so that I know who built the site.

## Business rules
- BR1: The technical team page displays the developer credit: "Sabbir Ahmed Sakib — Developer".

## What this feature owns
- The public technical-team credit page.

## What this feature does NOT own
- The footer developer credit (public-site, Phase 01).

## Out of scope (not planned)
- Footer developer credit (already covered by public-site AC3, Phase 01).

## Acceptance criteria

### AC1: Technical team credit shown
- **Trace**: US1, BR1
- **Given**: the public technical-team page
- **When**: a visitor opens it
- **Then**: it shows "Sabbir Ahmed Sakib — Developer".
