---
type: business-context
spec_version: 1
feature: profession-fee
file_type: business-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [profession-fee, business-context]
---

# Profession & Fee Management — business context

## Goal
Let admins define profession categories and their monthly fees so member dues are driven by
configuration, not hard-coded.

## User stories
- US1: As an admin, I can define profession categories and their monthly fee, so that dues are calculated correctly.
- US2: As an admin, I can set a custom/special fee for a member, so that exceptions are handled.

## Business rules
- BR1: Initial categories and fees: Business BDT 200, Jobholder BDT 100, Student BDT 50, High Ranking Officer (admin-configurable), Special Fee (any custom amount).
- BR2: Profession/category values and their fees are admin-editable.
- BR3: A special/custom fee may be any arbitrary amount.
- BR4: Changing a current fee must never alter historical payment records.

## What this feature owns
- The fee-category configuration and the per-member custom fee meaning.

## What this feature does NOT own
- Recording payments (payments feature); due calculation (due-payments feature).

## Out of scope (not planned)
- Recording payments (covered by payments).

## Acceptance criteria

### AC1: Configure profession fees
- **Trace**: US1, BR1, BR2
- **Given**: an admin with settings permission
- **When**: they add or edit a profession category and its monthly fee
- **Then**: the new fee applies to future dues for members in that category.

### AC2: Custom fee per member
- **Trace**: US2, BR3
- **Given**: a member needing an exception
- **When**: an admin assigns a special/custom fee amount
- **Then**: that member's monthly due uses the custom amount.

### AC3: Fee change doesn't rewrite history
- **Trace**: BR4
- **Given**: past payments recorded at an old fee
- **When**: an admin changes the current fee
- **Then**: previously recorded payment amounts are unchanged.

### Edge & error cases
- Duplicate category name is rejected (unique constraint).
- Empty category list points the admin at the seed file.
