---
type: requirement
spec_version: 1
title: "Admin Dashboard — requirement"
feature: dashboard
phase: 2
tags: [dashboard, requirement]
last_review: 2026-08-13
---

# Admin Dashboard — requirement

> Pure business. New feature.

## Goal
Give admins an at-a-glance overview of the organization's health with key numbers and charts.

## User stories
- US1: As an admin, I can see key membership and money figures on one screen, so that I understand status quickly.
- US2: As an admin, I can see useful charts, so that I can spot trends.

## Business rules
- BR1: Each figure respects the viewer's permissions (e.g. finance figures only for finance-permitted admins).

### AC1: Summary figures
- **Trace**: US1, BR1
- **Given**: an admin on the dashboard
- **When**: it loads
- **Then**: it shows total members, active members, due members, monthly collection, total income, total expense, current balance, today's collection, recent payments, upcoming birthdays, recent notices and a project/activity summary.

### AC2: Charts
- **Trace**: US2
- **Given**: available data
- **When**: the dashboard loads
- **Then**: it shows useful charts for collection, income vs expense, professions and payment methods.

## Out of scope (not asked for)
- The underlying records (owned by their own features).
