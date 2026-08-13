---
type: requirement
spec_version: 1
title: "Audit Logging — requirement"
feature: audit
phase: 2
tags: [audit, requirement]
last_review: 2026-08-13
---

# Audit Logging — requirement

> Pure business. New feature.

## Goal
Keep a trustworthy record of important administrative actions for accountability.

## User stories
- US1: As a Super Admin, I can review a log of important actions, so that I can audit who did what.

## Business rules
- BR1: Important administrative actions are logged.
- BR2: Each entry stores actor, action, timestamp, affected record and relevant old/new values where practical.
- BR3: At minimum, log permission changes, sensitive member changes, payments, finance, SMS sending, deletions and restorations.

### AC1: Actions are logged
- **Trace**: US1, BR1, BR2, BR3
- **Given**: an admin performs a logged action (permission change, sensitive member change, payment, finance entry, SMS send, deletion or restoration)
- **When**: the action completes
- **Then**: an audit entry records actor, action, timestamp, affected record and old/new values where practical.

## Out of scope (not asked for)
- Exporting the audit log (may be covered by reports later).
