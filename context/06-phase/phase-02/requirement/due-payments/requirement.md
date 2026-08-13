---
type: requirement
spec_version: 1
title: "Due Payment Management — requirement"
feature: due-payments
phase: 2
tags: [due-payments, requirement]
last_review: 2026-08-13
---

# Due Payment Management — requirement

> Pure business. New feature.

## Goal
Show who owes what and let admins send due reminders.

## User stories
- US1: As an admin, I can see which members are due and how much, so that I can follow up.
- US2: As an admin, I can send an editable due reminder, so that members are prompted to pay.

## Business rules
- BR1: Monthly dues are calculated from each member's fee configuration and their payment history.
- BR2: The dashboard shows due members and due amounts, plus each member's last payment information.
- BR3: Only an authorized admin/executive can send due reminders.
- BR4: The due reminder text is editable before sending.

### AC1: Due calculation
- **Trace**: US1, BR1, BR2
- **Given**: members with configured fees and payment history
- **When**: an admin views the due list
- **Then**: each due member is shown with the amount owed and their last payment info.

### AC2: Send editable due reminder
- **Trace**: US2, BR3, BR4
- **Given**: an authorized admin/executive
- **When**: they send a due reminder
- **Then**: they can edit the reminder text before it is sent to the member.

## Out of scope (not asked for)
- SMS provider integration (covered by sms).
