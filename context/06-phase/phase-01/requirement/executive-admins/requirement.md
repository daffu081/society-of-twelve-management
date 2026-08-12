---
type: requirement
spec_version: 1
title: "Executive admins — requirement"
feature: executive-admins
phase: 1
tags: [executive-admins, requirement]
last_review: 2026-08-13
---

# Executive admins — requirement

> **Pure business.** Bootstrap-seeded from the existing codebase to match `05-features/executive-admins/business-context.md`.
> Ongoing changes go through `/gather-requirement`. AC ids are permanent and append-only.

## Goal
Let the Super Admin create executive admins and grant each one only the capabilities they need
(checkbox permissions), and deactivate them without deleting.

## User stories
- US1: As a Super Admin, I can add an executive admin.
- US2: As a Super Admin, I can set which capabilities an executive admin has.
- US3: As a Super Admin, I can deactivate an admin.

## Business rules
- BR1: Only a Super Admin manages admins.
- BR2: Executive admins have exactly the capabilities checked in their `permissions`.
- BR3: Deactivating (not deleting) revokes access.

## Acceptance criteria

### AC1: Create executive admin
- **Trace**: US1, BR1
- **Given**: a Super Admin
- **When**: they add an admin (name, email)
- **Then**: an `executive_admin` row is created, active

### AC2: Set checkbox permissions
- **Trace**: US2, BR2
- **Given**: an executive admin
- **When**: the Super Admin checks/unchecks capabilities
- **Then**: the `permissions` jsonb reflects exactly those capabilities

### AC3: Deactivate admin
- **Trace**: US3, BR3
- **Given**: an active admin
- **When**: the Super Admin deactivates them
- **Then**: `active=false` and they can no longer reach the dashboard

## Out of scope (not asked for)
- Custom roles beyond super/executive.
