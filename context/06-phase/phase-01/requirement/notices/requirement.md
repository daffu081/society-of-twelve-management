---
type: requirement
spec_version: 1
title: "Notices — requirement"
feature: notices
phase: 1
tags: [notices, requirement]
last_review: 2026-08-13
---

# Notices — requirement

> **Pure business.** Bootstrap-seeded from the existing codebase to match `05-features/notices/business-context.md`.
> Ongoing changes go through `/gather-requirement`. AC ids are permanent and append-only.

## Goal
Publish society notices, with the current "running" notice highlighted on the public homepage.

## User stories
- US1: As an admin, I can create and publish a notice.
- US2: As a visitor, I see running notices on the homepage.

## Business rules
- BR1: Every notice has a unique `ref_no`, title and body.
- BR2: Only published notices are public; a notice may be flagged "running".

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

## Out of scope (not asked for)
- Per-member targeted notices (that would be SMS).
