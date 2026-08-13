---
type: requirement
spec_version: 1
title: "Payments — requirement"
feature: payments
phase: 2
tags: [payments, requirement]
last_review: 2026-08-13
---

# Payments — requirement

> Pure business. Continues AC numbering from Phase 01 (AC1–AC2).

## Goal
Record member payments completely and reliably, with a proper receipt number and history members can see.

## User stories
- US3: As an admin, I can record a payment with full details, so that collections are tracked.
- US4: As a member, I can see my own payment history, so that I know what I've paid.

## Business rules
- BR3: Payment methods include Online, Cash, Bank, bKash, Nagad and future methods.
- BR4: A payment record contains member, amount, purpose, method, timestamp, receipt number, recorded-by user and notes.
- BR5: Receipt number format is SOT-YYYYMM-0001.
- BR6: Recorded payment amounts are immutable — never changed by later fee edits.
- BR7: Bank/QR configuration may stay inactive until the organization has a confirmed bank account.

### AC3: Record a full payment
- **Trace**: US3, BR3, BR4, BR5
- **Given**: an admin with payment permission
- **When**: they record a payment
- **Then**: the system saves member, amount, purpose, method, timestamp, recorded-by and notes with an auto-generated SOT-YYYYMM-0001 receipt number.

### AC4: Payment triggers receipt & notification
- **Trace**: US3
- **Given**: a payment has been successfully recorded
- **When**: it is saved
- **Then**: a receipt is generated and the notification workflow is started.

### AC5: Member views own history
- **Trace**: US4
- **Given**: a logged-in member
- **When**: they open their payment history
- **Then**: they see their own payments and can open each receipt, and cannot see other members' payments.

## Out of scope (not asked for)
- Receipt document/PDF layout (covered by receipts).
- Due calculation and reminders (covered by due-payments).
