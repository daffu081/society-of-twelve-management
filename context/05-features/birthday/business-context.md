---
type: business-context
spec_version: 1
feature: birthday
file_type: business-context
contract_version: 1
status: planned
depends_on: [sms, members]
last_review: 2026-08-13
frozen: false
tags: [birthday, business-context]
---

# Birthday automation — business context

> **Blocked:** depends on the `sms` feature (and therefore an SMS provider).

## Goal
Automatically send a birthday greeting to each member on their birthday, once per year.

## User stories
- US1: As the society, members receive a birthday greeting automatically.

## Business rules
- BR1: A member gets at most one birthday greeting per year (`birthday_logs` unique on member+year).
- BR2: Greetings go out via the `sms` feature.

## What this feature owns
- Birthday detection and the `birthday_logs` idempotency record.

## What this feature does NOT own
- Actual SMS delivery (feature `sms`) or member data (feature `members`).

## Out of scope (not planned)
- Email birthday greetings (email receipts are a separate later item).

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

### Edge & error cases
- Member without `dob` is skipped.
- SMS provider unavailable → no `birthday_logs` row, so it retries next run.
