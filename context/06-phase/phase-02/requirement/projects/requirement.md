---
type: requirement
spec_version: 1
title: "Projects — requirement"
feature: projects
phase: 2
tags: [projects, requirement]
last_review: 2026-08-13
---

# Projects — requirement

> Pure business. Continues AC numbering from Phase 01 (AC1–AC2).

## Goal
Let admins manage organization projects with full details and financials, using recoverable deletion.

## User stories
- US3: As an admin, I can record a project with details, images and financial information, so that it's documented.
- US4: As an admin, I can delete a project safely, so that mistakes can be recovered.

## Business rules
- BR3: A project has title, description, images, start/end dates, status and financial information.
- BR4: Projects use soft deletion — deleted projects move to Bin/Trash.
- BR5: Only a Super Admin can restore or permanently delete a project.

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

## Out of scope (not asked for)
- The Bin retention/cleanup mechanics (covered by bin).
