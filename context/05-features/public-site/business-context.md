---
type: business-context
spec_version: 1
feature: public-site
file_type: business-context
contract_version: 1
status: in_progress
depends_on: []
last_review: 2026-08-13
frozen: false
tags: [public-site, business-context]
---

# Public site — business context

## Goal
Give the community a public Bengali homepage introducing the Society of Twelve and (eventually)
surfacing running notices, projects, mahfil and the consenting-members directory.

## User stories
- US1: As a visitor, I can read about the society, its projects, mahfil, notices, rules and contact.
- US2: As the society, I want running notices and activity to appear publicly (planned).

## Business rules
- BR1: Content is Bengali-first.
- BR2: Only members who opted in (`show_on_public_directory`) appear publicly.

## What this feature owns
- The public landing page and its static sections.

## What this feature does NOT own
- The data behind notices/projects/mahfil/members (those features own it); this feature only displays it.

## Out of scope (not planned)
- Public login or member self-service on the public site.

## Acceptance criteria

### AC1: Homepage renders
- **Trace**: US1
- **Given**: a visitor opens `/`
- **When**: the page loads
- **Then**: header, hero, and About/Project/Mahfil/Notice/Members/Rules/Contact sections show

### AC2: Footer year is current
- **Trace**: US1
- **Given**: the homepage
- **When**: it loads
- **Then**: the footer copyright year is the current year

### Edge & error cases
- Dynamic content (running notices/projects, public directory) is **not yet wired** — currently placeholder copy.
