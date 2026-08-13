---
type: requirement
spec_version: 1
title: "Receipts — requirement"
feature: receipts
phase: 2
tags: [receipts, requirement]
last_review: 2026-08-13
---

# Receipts — requirement

> Pure business. New feature.

## Goal
Produce a professional, branded receipt for every payment, viewable, printable and emailable.

## User stories
- US1: As a member, I can view and print a branded receipt for my payment, so that I have proof.
- US2: As an admin, I can email a receipt to a member, so that they get a copy.

## Business rules
- BR1: A receipt includes organization logo, member name, member ID, house name, amount, purpose, payment method, receipt number, date and authorized/recorded-by information.
- BR2: Receipts are accessible from both the member profile and payment history.
- BR3: The receipt must be print-friendly and downloadable as a PDF.
- BR4: Email delivery of the receipt/PDF is supported.
- BR5: PDF files are never sent through SMS.

### AC1: Branded receipt generated
- **Trace**: US1, BR1, BR3
- **Given**: a recorded payment
- **When**: a member or admin opens its receipt
- **Then**: a branded, print-friendly receipt shows all required fields and can be downloaded as a PDF.

### AC2: Receipt reachable from profile & history
- **Trace**: BR2
- **Given**: a member with payments
- **When**: they view their profile or payment history
- **Then**: each payment's receipt is accessible.

### AC3: Email a receipt
- **Trace**: US2, BR4, BR5
- **Given**: an admin viewing a payment
- **When**: they email the receipt
- **Then**: the receipt/PDF is emailed to the member, and no PDF is ever sent by SMS.

## Out of scope (not asked for)
- Recording the payment itself (covered by payments).
