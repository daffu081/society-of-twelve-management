---
type: business-context
spec_version: 1
feature: notices
file_type: business-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [notices, business-context]
---

# Notices — business context

## Goal
Publish society notices, with the current "running" notice highlighted on the public homepage.

## User stories
- US1: As an admin, I can create and publish a notice.
- US2: As a visitor, I see running notices on the homepage.
- US3: As an admin, I can create, edit, publish and archive notices, so that members stay informed.
- US4: As an admin, I can post a meeting notice with date, time and venue, so that members know when and where.
- US5: As an authorized executive, I can send the notice by SMS after reviewing it, so that members are alerted.

## Business rules
- BR1: Every notice has a unique `ref_no`, title and body.
- BR2: Only published notices are public; a notice may be flagged "running".
- BR3: Each notice gets an automatic reference number, e.g. SOT-NOT-202608-0001.
- BR4: Meeting notices include date, time and venue.
- BR5: The associated SMS can be edited before sending, and only an authorized executive may send it.

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

### AC3: Create & publish with reference number
- **Trace**: US3, BR3
- **Given**: an admin with notice permission
- **When**: they create and publish a notice
- **Then**: it is published with an auto-generated SOT-NOT-YYYYMM-0001 reference, and can later be edited or archived.

### AC4: Meeting notice fields
- **Trace**: US4, BR4
- **Given**: a meeting notice
- **When**: it is created
- **Then**: it records date, time and venue.

### AC5: Send notice SMS after review
- **Trace**: US5, BR5
- **Given**: an authorized executive and a notice
- **When**: they choose to send its SMS
- **Then**: they can edit the message before it is sent.

### Edge & error cases
- Duplicate `ref_no` rejected; unpublished notices stay private.
