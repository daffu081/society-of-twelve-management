---
type: requirement
spec_version: 1
title: "Cross-cutting — requirement"
feature: _cross-cutting
phase: 1
tags: [_cross-cutting, requirement]
last_review: 2026-08-13
---

# Cross-cutting — requirement

> **Pure business. Written for a non-technical client.** What they want and why — never how.

## Goal
Keep the organization's secret credentials out of anything a visitor can see, so the system can't be broken into through the public website.

## User stories
- US1: As the organization, I want no secret/service credentials to be reachable from the public website, so that no one can misuse them to access our data.

## Business rules
- BR1: Secret or service-level credentials must never be present in the public website code that visitors' browsers can read.

## Acceptance criteria

### AC1: No secret credentials in the public website
- **Trace**: US1, BR1
- **Given**: the public website as delivered to a visitor's browser
- **When**: its contents are inspected
- **Then**: no secret or service-level credentials are present — only the safe, public-facing configuration

## Out of scope (not asked for)
- Row-level data access rules for members and admins beyond the existing admin gate (future phases).
- Audit logging of admin actions (future phase).
