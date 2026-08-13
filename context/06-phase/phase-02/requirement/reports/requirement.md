---
type: requirement
spec_version: 1
title: "Reports & Exports — requirement"
feature: reports
phase: 2
tags: [reports, requirement]
last_review: 2026-08-13
---

# Reports & Exports — requirement

> Pure business. New feature.

## Goal
Let authorized admins view and export the organization's key reports.

## User stories
- US1: As an authorized admin, I can view and export reports, so that I can share and archive them.

## Business rules
- BR1: Available reports: member list, payment history, monthly collection, due member report, income report, expense report, project finance report, SMS log and birthday delivery log.
- BR2: Exports are available as CSV/Excel/PDF where appropriate.
- BR3: Reports and exports are permission-controlled — a user sees only what their permissions allow.

### AC1: View reports
- **Trace**: US1, BR1, BR3
- **Given**: an authorized admin
- **When**: they open a report (member list, payment history, monthly collection, dues, income, expense, project finance, SMS log or birthday log)
- **Then**: the report is shown, limited to what their permissions allow.

### AC2: Export reports
- **Trace**: US1, BR2, BR3
- **Given**: a report the admin may view
- **When**: they export it
- **Then**: they get a CSV/Excel/PDF as appropriate, respecting their permissions.

## Out of scope (not asked for)
- Dashboard charts (covered by dashboard).
