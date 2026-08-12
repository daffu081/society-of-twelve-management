---
type: business-context
spec_version: 1
feature: notices
file_type: business-context
contract_version: 1
status: planned
depends_on: [admin-access]
last_review: 2026-08-13
frozen: false
tags: [notices, business-context]
---

# Notices — business context

## Goal
Publish society notices, with the current "running" notice highlighted on the public homepage.

## User stories
- US1: As an admin, I can create and publish a notice.
- US2: As a visitor, I see running notices on the homepage.

## Business rules
- BR1: Every notice has a unique `ref_no`, title and body.
- BR2: Only published notices are public; a notice may be flagged "running".

## What this feature owns
- The `notices` table and notice CRUD/publishing.

## What this feature does NOT own
- The homepage layout (feature `public-site` renders the running notice).

## Out of scope (not planned)
- Per-member targeted notices (that would be SMS).

## Acceptance criteria

### AC1: Create & publish notice
- **Trace**: US1, BR1, BR2
- **Given**: the notices admin page
- **When**: an admin creates a notice and marks it published
- **Then**: it is stored with a unique ref_no and visible publicly

### AC2: Running notice on homepage
- **Trace**: US2, BR2
- **Given**: a published notice flagged running
- **When**: a visitor opens the homepage
- **Then**: that notice is highlighted

### Edge & error cases
- Duplicate `ref_no` rejected; unpublished notices stay private.
