---
type: requirement
spec_version: 1
title: "Executive Committee — requirement"
feature: committee
phase: 2
tags: [committee, requirement]
last_review: 2026-08-13
---

# Executive Committee — requirement

> Pure business. New feature.

## Goal
Let admins maintain the executive committee roster shown publicly in a chosen order.

## User stories
- US1: As an admin, I can maintain committee members with their details and order, so that the public sees the current committee.

## Business rules
- BR1: A committee entry has photo, name, position, year, short biography, display order and public visibility.

### AC1: Manage committee entries
- **Trace**: US1, BR1
- **Given**: an admin with committee permission
- **When**: they add or edit a committee member
- **Then**: photo, name, position, year, short biography, display order and public visibility are saved.

### AC2: Public committee display in order
- **Trace**: US1, BR1
- **Given**: committee entries marked public
- **When**: a visitor views the committee page
- **Then**: public entries are shown in the configured display order.

## Out of scope (not asked for)
- Founding members (separate feature).
