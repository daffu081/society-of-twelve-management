---
type: requirement
spec_version: 1
title: "Finance — requirement"
feature: finance
phase: 2
tags: [finance, requirement]
last_review: 2026-08-13
---

# Finance — requirement

> Pure business. Continues AC numbering from Phase 01 (AC1–AC3).

## Goal
Give admins full control of the organization's income and expenses with a running balance, kept strictly private.

## User stories
- US4: As an admin, I can record income from defined sources, so that all money in is tracked.
- US5: As an admin, I can record expenses with details, so that all money out is tracked.
- US6: As an admin, I can see cumulative income, expense and balance, so that I know the organization's position.

## Business rules
- BR4: Income sources: Monthly Subscription, Project Donation, Mahfil Donation, Special Donation, Other Income, Historical/Offline Collection.
- BR5: An expense record contains category, amount, date, description and recorded-by.
- BR6: Finance data is never public.
- BR7: Executive access to finance requires explicit permission.

### AC4: Record income by source
- **Trace**: US4, BR4
- **Given**: an admin with finance permission
- **When**: they record income
- **Then**: it is saved against one of the defined income sources.

### AC5: Record expense
- **Trace**: US5, BR5
- **Given**: an admin with finance permission
- **When**: they record an expense
- **Then**: category, amount, date, description and recorded-by are saved.

### AC6: Finance dashboard totals
- **Trace**: US6, BR6, BR7
- **Given**: recorded income and expenses
- **When**: an authorized admin opens finance
- **Then**: cumulative income, cumulative expense and balance are shown, and no finance data is ever exposed publicly or to executives without permission.

## Out of scope (not asked for)
- Exported finance reports (covered by reports).
