---
type: requirement
spec_version: 1
title: "Notices & Meetings — requirement"
feature: notices
phase: 2
tags: [notices, requirement]
last_review: 2026-08-13
---

# Notices & Meetings — requirement

> Pure business. Continues AC numbering from Phase 01 (AC1–AC2).

## Goal
Let admins publish notices and meeting announcements, each with a reference number, and optionally notify members by SMS.

## User stories
- US3: As an admin, I can create, edit, publish and archive notices, so that members stay informed.
- US4: As an admin, I can post a meeting notice with date, time and venue, so that members know when and where.
- US5: As an authorized executive, I can send the notice by SMS after reviewing it, so that members are alerted.

## Business rules
- BR3: Each notice gets an automatic reference number, e.g. SOT-NOT-202608-0001.
- BR4: Meeting notices include date, time and venue.
- BR5: The associated SMS can be edited before sending, and only an authorized executive may send it.

### AC3: Create & publish with reference number
- **Trace**: US3, BR3
- **Given**: an admin with notice permission
- **When**: they create and publish a notice
- **Then**: it is published with an auto-generated SOT-NOT-YYYYMM-0001 reference, and can later be edited or archived.

### AC4: Meeting notice fields
- **Trace**: US4, BR4
- **Given**: a meeting notice
- **When**: it is created
- **Then**: it records date, time and venue.

### AC5: Send notice SMS after review
- **Trace**: US5, BR5
- **Given**: an authorized executive and a notice
- **When**: they choose to send its SMS
- **Then**: they can edit the message before it is sent.

## Out of scope (not asked for)
- The running-notice banner on the homepage (already covered by notices AC2, Phase 01).
