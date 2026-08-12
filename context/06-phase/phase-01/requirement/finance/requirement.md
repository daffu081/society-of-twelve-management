---
type: requirement
spec_version: 1
title: "Finance — requirement"
feature: finance
phase: 1
tags: [finance, requirement]
last_review: 2026-08-13
---

# Finance — requirement

> **Pure business.** Bootstrap-seeded from the existing codebase to match `05-features/finance/business-context.md`.
> Ongoing changes go through `/gather-requirement`. AC ids are permanent and append-only.

## Goal
Track the society's income and expenses and show the current balance, so the committee can
answer "what's our balance?" at any time.

## User stories
- US1: As an admin, I can record an income entry (optionally from a payment).
- US2: As an admin, I can record an expense entry.
- US3: As an admin, I can see totals and current balance.

## Business rules
- BR1: All amounts are exact money.
- BR2: Balance = total income − total expenses.
- BR3: Income may link to a payment for traceability.

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

## Out of scope (not asked for)
- Full double-entry accounting.
