---
type: requirement
spec_version: 1
title: "Birthday Automation — requirement"
feature: birthday
phase: 2
tags: [birthday, requirement]
last_review: 2026-08-13
---

# Birthday Automation — requirement

> Pure business. Continues AC numbering from Phase 01 (AC1–AC2).

## Goal
Automatically wish members a happy birthday by SMS, once per year, without manual effort.

## User stories
- US3: As an admin, I can see a birthday calendar/list, so that I know whose birthday is coming.
- US4: As the organization, birthday greetings go out automatically, so that no one is missed.

## Business rules
- BR3: A scheduled daily job checks members whose birthday matches the current date and sends the greeting automatically — never relying on manual execution.
- BR4: The greeting includes the actual member's name.
- BR5: A yearly birthday delivery log prevents duplicate messages to the same member in the same year.
- BR6: The birthday message content stays editable by admins.

### AC3: Admin birthday calendar
- **Trace**: US3
- **Given**: members with dates of birth
- **When**: an admin opens the birthday calendar/list
- **Then**: upcoming birthdays are shown.

### AC4: Automatic, once-per-year greeting
- **Trace**: US4, BR3, BR4, BR5
- **Given**: today matches a member's birthday
- **When**: the daily job runs
- **Then**: a birthday SMS with the member's real name is sent automatically, and the yearly log prevents a duplicate for that member that year.

## Out of scope (not asked for)
- Editing the message body (covered by sms templates).
