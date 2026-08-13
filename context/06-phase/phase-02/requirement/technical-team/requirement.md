---
type: requirement
spec_version: 1
title: "Technical Team — requirement"
feature: technical-team
phase: 2
tags: [technical-team, requirement]
last_review: 2026-08-13
---

# Technical Team — requirement

> Pure business. New feature.

## Goal
Show the developer/technical-team credit publicly.

## User stories
- US1: As a visitor, I can see the technical team credit, so that I know who built the site.

## Business rules
- BR1: The technical team page displays the developer credit: "Sabbir Ahmed Sakib — Developer".

### AC1: Technical team credit shown
- **Trace**: US1, BR1
- **Given**: the public technical-team page
- **When**: a visitor opens it
- **Then**: it shows "Sabbir Ahmed Sakib — Developer".

## Out of scope (not asked for)
- Footer developer credit (already covered by public-site AC3, Phase 01).
