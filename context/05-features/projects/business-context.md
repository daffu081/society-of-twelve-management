---
type: business-context
spec_version: 1
feature: projects
file_type: business-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [projects, business-context]
---

# Projects — business context

## Goal
Showcase the society's running and previous projects on the public site.

## User stories
- US1: As an admin, I can add a project with a status (running/previous).
- US2: As a visitor, I see running and previous projects.
- US3: As an admin, I can record a project with details, images and financial information, so that it's documented.
- US4: As an admin, I can delete a project safely, so that mistakes can be recovered.

## Business rules
- BR1: A project has a title and a status (default running).
- BR3: A project has title, description, images, start/end dates, status and financial information.
- BR4: Projects use soft deletion — deleted projects move to Bin/Trash.
- BR5: Only a Super Admin can restore or permanently delete a project.

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

### AC3: Manage project with details & finance
- **Trace**: US3, BR3
- **Given**: an admin with project permission
- **When**: they create or edit a project
- **Then**: title, description, images, start/end dates, status and financial information are saved.

### AC4: Soft-delete and restore
- **Trace**: US4, BR4, BR5
- **Given**: a project
- **When**: an admin deletes it
- **Then**: it moves to Bin/Trash, and only a Super Admin can restore or permanently delete it.

### Edge & error cases
- Empty state shows nothing under Project.
