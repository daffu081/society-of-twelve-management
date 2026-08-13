---
type: requirement
spec_version: 1
title: "Awards & Achievements — requirement"
feature: awards
phase: 2
tags: [awards, requirement]
last_review: 2026-08-13
---

# Awards & Achievements — requirement

> Pure business. New feature.

## Goal
Let admins record awards and achievements, optionally linked to a member, and control their public visibility.

## User stories
- US1: As an admin, I can record an award with details and control whether it's public, so that achievements are recognized.

## Business rules
- BR1: An award has title, recipient/member, description, date, image/document and visibility.
- BR2: Publication is admin-controlled.
- BR3: Linking an award to a member is optional.

### AC1: Record an award
- **Trace**: US1, BR1, BR3
- **Given**: an admin with awards permission
- **When**: they create or edit an award
- **Then**: title, recipient/member (optional), description, date, image/document and visibility are saved.

### AC2: Control public visibility
- **Trace**: US1, BR2
- **Given**: an award
- **When**: an admin sets it public or not
- **Then**: it appears on the public awards page only when made public.

## Out of scope (not asked for)
- The public awards page layout (covered by public-site).
