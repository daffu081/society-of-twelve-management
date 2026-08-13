---
type: requirement
spec_version: 1
title: "Mahfil — requirement"
feature: mahfil
phase: 2
tags: [mahfil, requirement]
last_review: 2026-08-13
---

# Mahfil — requirement

> Pure business. Continues AC numbering from Phase 01 (AC1–AC2).

## Goal
Let admins manage mahfil events with full details and a public page.

## User stories
- US3: As an admin, I can record a mahfil with full details and control its publication, so that it's documented and optionally shown publicly.

## Business rules
- BR3: A mahfil has title, date, time, venue, description, image and publication status.
- BR4: Mahfil is managed by admins or authorized executives.
- BR5: A public mahfil page shows published mahfils.

### AC3: Manage mahfil with full details
- **Trace**: US3, BR3, BR4
- **Given**: an admin or authorized executive
- **When**: they create or edit a mahfil
- **Then**: title, date, time, venue, description, image and publication status are saved.

### AC4: Public mahfil page
- **Trace**: US3, BR5
- **Given**: a published mahfil
- **When**: a visitor opens the public mahfil page
- **Then**: the published mahfil is shown.

## Out of scope (not asked for)
- Mahfil donations (covered by finance income sources).
