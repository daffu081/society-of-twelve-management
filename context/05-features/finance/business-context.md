---
type: business-context
spec_version: 1
feature: finance
file_type: business-context
contract_version: 1
status: in_progress
depends_on: [admin-access, payments]
last_review: 2026-08-14
frozen: false
tags: [finance, business-context]
---

# Finance — business context

## Goal
Track the society's income and expenses and show the current balance, so the committee can
answer "what's our balance?" at any time.

## User stories
- US1: As an admin, I can record an income entry (optionally from a payment).
- US2: As an admin, I can record an expense entry.
- US3: As an admin, I can see totals and current balance.
- US4: As an admin, I can record income from defined sources, so that all money in is tracked.
- US5: As an admin, I can record expenses with details, so that all money out is tracked.
- US6: As an admin, I can see cumulative income, expense and balance, so that I know the organization's position.

## Business rules
- BR1: All amounts are exact money.
- BR2: Balance = total income − total expenses.
- BR3: Income may link to a payment for traceability.
- BR4: Income sources: Monthly Subscription, Project Donation, Mahfil Donation, Special Donation, Other Income, Historical/Offline Collection.
- BR5: An expense record contains category, amount, date, description and recorded-by.
- BR6: Finance data is never public.
- BR7: Executive access to finance requires explicit permission.

## What this feature owns
- The `income` and `expenses` tables and finance reporting.

## What this feature does NOT own
- Recording member payments (feature `payments`).

## Out of scope (not planned)
- Full double-entry accounting.

## Acceptance criteria

### AC1: Record income
- **Trace**: US1, BR1, BR3
- **Given**: the finance page
- **When**: an admin adds an income entry (source, amount, optional payment link)
- **Then**: it is stored and included in the income total

### AC2: Record expense
- **Trace**: US2, BR1
- **Given**: the finance page
- **When**: an admin adds an expense (category, amount)
- **Then**: it is stored and included in the expense total

### AC3: See balance
- **Trace**: US3, BR2
- **Given**: income and expenses exist
- **When**: an admin views finance
- **Then**: total income, total expenses, and balance are shown exactly

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

### Edge & error cases
- Empty state shows zero balance.
