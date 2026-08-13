---
type: requirement
spec_version: 1
title: "Rules & Regulations — requirement"
feature: rules
phase: 2
tags: [rules, requirement]
last_review: 2026-08-13
---

# Rules & Regulations — requirement

> Pure business. New feature.

## Goal
Give the organization a dedicated Rules & Regulations section that the Super Admin maintains.

## User stories
- US1: As a Super Admin, I can create, edit, publish and archive rules, so that members always see current regulations.

## Business rules
- BR1: There is a dedicated Rules & Regulations section.
- BR2: Only the Super Admin can create, edit, publish and archive rules.
- BR3: Version/history is supported where practical.

### AC1: Manage rules
- **Trace**: US1, BR1, BR2
- **Given**: a Super Admin
- **When**: they create, edit, publish or archive a rule
- **Then**: the change is saved and published rules are visible to members/public.

### AC2: Version history
- **Trace**: BR3
- **Given**: a rule that has changed
- **When**: it is edited
- **Then**: prior versions/history are retained where practical.

## Out of scope (not asked for)
- The public rules page layout (covered by public-site).
