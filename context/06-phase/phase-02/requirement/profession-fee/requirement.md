---
type: requirement
spec_version: 1
title: "Profession & Fee Management — requirement"
feature: profession-fee
phase: 2
tags: [profession-fee, requirement]
last_review: 2026-08-13
---

# Profession & Fee Management — requirement

> Pure business. New feature.

## Goal
Let admins define profession categories and their monthly fees so member dues are driven by configuration, not hard-coded.

## User stories
- US1: As an admin, I can define profession categories and their monthly fee, so that dues are calculated correctly.
- US2: As an admin, I can set a custom/special fee for a member, so that exceptions are handled.

## Business rules
- BR1: Initial categories and fees: Business BDT 200, Jobholder BDT 100, Student BDT 50, High Ranking Officer (admin-configurable), Special Fee (any custom amount).
- BR2: Profession/category values and their fees are admin-editable.
- BR3: A special/custom fee may be any arbitrary amount.
- BR4: Changing a current fee must never alter historical payment records.

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

## Out of scope (not asked for)
- Recording payments (covered by payments).
