---
type: business-context
spec_version: 1
feature: projects
file_type: business-context
contract_version: 1
status: planned
depends_on: [admin-access]
last_review: 2026-08-13
frozen: false
tags: [projects, business-context]
---

# Projects — business context

## Goal
Showcase the society's running and previous projects on the public site.

## User stories
- US1: As an admin, I can add a project with a status (running/previous).
- US2: As a visitor, I see running and previous projects.

## Business rules
- BR1: A project has a title and a status (default running).

## What this feature owns
- The `projects` table and project CRUD.

## What this feature does NOT own
- Public rendering (feature `public-site`).

## Out of scope (not planned)
- Project budgets/finance linkage.

## Acceptance criteria

### AC1: Create project with status
- **Trace**: US1, BR1
- **Given**: the projects admin page
- **When**: an admin adds a project
- **Then**: it is stored with its status

### AC2: Shown on public site
- **Trace**: US2
- **Given**: projects exist
- **When**: a visitor opens the site
- **Then**: running and previous projects are listed

### Edge & error cases
- Empty state shows nothing under Project.
