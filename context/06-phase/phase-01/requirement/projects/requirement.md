---
type: requirement
spec_version: 1
title: "Projects — requirement"
feature: projects
phase: 1
tags: [projects, requirement]
last_review: 2026-08-13
---

# Projects — requirement

> **Pure business.** Bootstrap-seeded from the existing codebase to match `05-features/projects/business-context.md`.
> Ongoing changes go through `/gather-requirement`. AC ids are permanent and append-only.

## Goal
Showcase the society's running and previous projects on the public site.

## User stories
- US1: As an admin, I can add a project with a status (running/previous).
- US2: As a visitor, I see running and previous projects.

## Business rules
- BR1: A project has a title and a status (default running).

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

## Out of scope (not asked for)
- Project budgets/finance linkage.
