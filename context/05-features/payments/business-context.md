---
type: business-context
spec_version: 1
feature: payments
file_type: business-context
contract_version: 1
status: planned
depends_on: [admin-access, members]
last_review: 2026-08-13
frozen: false
tags: [payments, business-context]
---

# Payments — business context

## Goal
Record fee and other payments against members, each with a unique receipt number.

## User stories
- US1: As an admin, I can record a payment for a member.
- US2: As an admin, I can see a member's payment history.

## Business rules
- BR1: Every payment has a unique `receipt_no`, an amount, a purpose, a method and a date.
- BR2: Amounts are exact money (no rounding drift).
- BR3: A payment references an existing member.

## What this feature owns
- The `payments` table and payment recording.

## What this feature does NOT own
- Overall income/expense totals (feature `finance`).

## Out of scope (not planned)
- Online payment processing / gateways.

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

### Edge & error cases
- Duplicate `receipt_no` is rejected.
- Non-existent member cannot be paid against.
