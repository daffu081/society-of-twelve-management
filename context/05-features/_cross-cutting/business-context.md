---
type: business-context
spec_version: 1
feature: _cross-cutting
file_type: business-context
contract_version: 1
status: done
depends_on: []
last_review: 2026-08-13
frozen: false
tags: [_cross-cutting, business-context]
---

# Cross-cutting — business context

## Goal
Keep the organization's secret credentials out of anything a visitor can see, so the system can't be broken into through the public website.

## User stories
- US1: As the organization, I want no secret/service credentials to be reachable from the public website, so that no one can misuse them to access our data.

## Business rules
- BR1: Secret or service-level credentials must never be present in the public website code that visitors' browsers can read.

## Out of scope (not planned)
- Row-level data access rules for members/admins beyond the existing admin gate (future phases).
- Audit logging of admin actions (future phase).

## Acceptance criteria

### AC1: No secret credentials in the public website
- **Trace**: US1, BR1
- **Given**: the public website as delivered to a visitor's browser
- **When**: its contents are inspected
- **Then**: no secret or service-level credentials are present — only the safe, public-facing configuration
