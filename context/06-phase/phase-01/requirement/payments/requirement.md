---
type: requirement
spec_version: 1
title: "Payments — requirement"
feature: payments
phase: 1
tags: [payments, requirement]
last_review: 2026-08-13
---

# Payments — requirement

> **Pure business.** Bootstrap-seeded from the existing codebase to match `05-features/payments/business-context.md`.
> Ongoing changes go through `/gather-requirement`. AC ids are permanent and append-only.

## Goal
Record fee and other payments against members, each with a unique receipt number.

## User stories
- US1: As an admin, I can record a payment for a member.
- US2: As an admin, I can see a member's payment history.

## Business rules
- BR1: Every payment has a unique `receipt_no`, an amount, a purpose, a method and a date.
- BR2: Amounts are exact money (no rounding drift).
- BR3: A payment references an existing member.

## Acceptance criteria

### AC1: Record a payment
- **Trace**: US1, BR1, BR2, BR3
- **Given**: a member exists
- **When**: an admin records amount + purpose + method
- **Then**: a payment with a unique receipt number is stored and shown

### AC2: View member payment history
- **Trace**: US2
- **Given**: a member with payments
- **When**: an admin opens that member
- **Then**: their payments are listed with receipt numbers

## Out of scope (not asked for)
- Online payment processing / gateways.
