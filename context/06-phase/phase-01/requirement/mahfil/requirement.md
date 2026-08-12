---
type: requirement
spec_version: 1
title: "Mahfil — requirement"
feature: mahfil
phase: 1
tags: [mahfil, requirement]
last_review: 2026-08-13
---

# Mahfil — requirement

> **Pure business.** Bootstrap-seeded from the existing codebase to match `05-features/mahfil/business-context.md`.
> Ongoing changes go through `/gather-requirement`. AC ids are permanent and append-only.

## Goal
Manage and showcase mahfil (community/religious gathering) events, running and previous.

## User stories
- US1: As an admin, I can add a mahfil with a status.
- US2: As a visitor, I see running and previous mahfil.

## Business rules
- BR1: A mahfil has a title and a status (default running).

## Acceptance criteria

### AC1: Create mahfil with status
- **Trace**: US1, BR1
- **Given**: the mahfil admin page
- **When**: an admin adds a mahfil
- **Then**: it is stored with its status

### AC2: Shown on public site
- **Trace**: US2
- **Given**: mahfil exist
- **When**: a visitor opens the site
- **Then**: running and previous mahfil are listed

## Out of scope (not asked for)
- Ticketing / attendance.
