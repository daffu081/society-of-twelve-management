---
type: requirement
spec_version: 1
title: "Birthday automation — requirement"
feature: birthday
phase: 1
tags: [birthday, requirement]
last_review: 2026-08-13
---

# Birthday automation — requirement

> **Pure business.** Bootstrap-seeded from the existing codebase to match `05-features/birthday/business-context.md`.
> Ongoing changes go through `/gather-requirement`. AC ids are permanent and append-only.

## Goal
Automatically send a birthday greeting to each member on their birthday, once per year.

## User stories
- US1: As the society, members receive a birthday greeting automatically.

## Business rules
- BR1: A member gets at most one birthday greeting per year (`birthday_logs` unique on member+year).
- BR2: Greetings go out via the `sms` feature.

## Acceptance criteria

### AC1: Detect today's birthdays
- **Trace**: US1
- **Given**: members with `dob`
- **When**: the daily job runs
- **Then**: members whose birthday is today (and not yet greeted this year) are selected

### AC2: Send greeting once per year
- **Trace**: US1, BR1, BR2
- **Given**: a member due a greeting
- **When**: the job sends via `sms`
- **Then**: a `birthday_logs` row (member, year, sms_log) prevents a duplicate send

## Out of scope (not asked for)
- Email birthday greetings (email receipts are a separate later item).
