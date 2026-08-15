---
type: requirement
spec_version: 1
title: "Payments — requirement"
feature: payments
phase: 3
tags: [payments, requirement]
last_review: 2026-08-15
---

# Payments — requirement

> **Pure business. Written for a non-technical client.** What they want and why — never how.
> Gathered by `/gather-requirement`. `/create-task` turns the ACs below into tasks;
> `/implement-task` later builds it and records the technical spec in `05-features/`.

## Goal
Let the organization prepare its bank / QR collection details ahead of time, so members can
be given a way to pay directly once the organization opens a bank account — without forcing the
feature to be live before then.

## User stories
- US6: As an admin, I can enter and save the organization's bank / QR payment details, so that they are
  ready to show to members when we start accepting direct transfers.
- US7: As an admin, I can keep those bank / QR details switched off, so that nothing incomplete is shown
  to members until we have a confirmed bank account.

## Business rules
- BR6: Bank / QR payment details are optional and start switched off.
- BR7: While switched off, the bank / QR option is not offered to members anywhere.
- BR8: Saving or changing bank / QR details never alters any existing payment record.

## Acceptance criteria

### AC6: Configure bank / QR collection details (may stay inactive)
- **Trace**: US6, US7, BR6, BR7, BR8
- **Given**: an admin is managing payment settings and the organization has no confirmed bank account yet
- **When**: the admin enters the bank / QR details and leaves the option switched off
- **Then**: the details are saved for later, members are shown no bank / QR payment option, and no
  existing payment record is changed; when the admin later switches it on, the saved details become
  available to members.

## Out of scope (not asked for)
- Live online payment processing / gateways (still not requested — v2 only asks for the details to
  exist and stay inactive until a bank account is confirmed).
- Automatic reconciliation of bank transfers against member dues.
