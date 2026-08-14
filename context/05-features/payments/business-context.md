---
type: business-context
spec_version: 1
feature: payments
file_type: business-context
contract_version: 1
status: in_progress
depends_on: [admin-access, members]
last_review: 2026-08-14
frozen: false
tags: [payments, business-context]
---

# Payments — business context

## Goal
Record fee and other payments against members, each with a unique receipt number.

## User stories
- US1: As an admin, I can record a payment for a member.
- US2: As an admin, I can see a member's payment history.
- US3: As an admin, I can record a payment with full details, so that collections are tracked.
- US4: As a member, I can see my own payment history, so that I know what I've paid.

## Business rules
- BR1: Every payment has a unique `receipt_no`, an amount, a purpose, a method and a date.
- BR2: Amounts are exact money (no rounding drift).
- BR3: Payment methods include Online, Cash, Bank, bKash, Nagad and future methods.
- BR4: A payment record contains member, amount, purpose, method, timestamp, receipt number, recorded-by user and notes.
- BR5: Receipt number format is SOT-YYYYMM-0001.
- BR6: Recorded payment amounts are immutable — never changed by later fee edits.
- BR7: Bank/QR configuration may stay inactive until the organization has a confirmed bank account.

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

### Edge & error cases
- Duplicate `receipt_no` is rejected.
- Non-existent member cannot be paid against.
