---
type: requirement
spec_version: 1
title: "Founding Members — requirement"
feature: founding-members
phase: 2
tags: [founding-members, requirement]
last_review: 2026-08-13
---

# Founding Members — requirement

> Pure business. New feature.

## Goal
Let admins maintain founding-member records shown publicly with their historical role.

## User stories
- US1: As an admin, I can maintain founding-member records, so that the organization's founders are recognized publicly.

## Business rules
- BR1: A founding-member record has photo, name, historical role and short biography.

### AC1: Manage founding members
- **Trace**: US1, BR1
- **Given**: an admin
- **When**: they add or edit a founding member
- **Then**: photo, name, historical role and short biography are saved and shown on the public founding-members page.

## Out of scope (not asked for)
- Executive committee (separate feature).
