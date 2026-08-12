---
type: requirement
spec_version: 1
title: "SMS — requirement"
feature: sms
phase: 1
tags: [sms, requirement]
last_review: 2026-08-13
---

# SMS — requirement

> **Pure business.** Bootstrap-seeded from the existing codebase to match `05-features/sms/business-context.md`.
> Ongoing changes go through `/gather-requirement`. AC ids are permanent and append-only.

## Goal
Manage reusable SMS templates and send/log messages to members (fee reminders, greetings),
via an external provider.

## User stories
- US1: As an admin, I can manage SMS templates.
- US2: As an admin, I can send a message to a member and see it logged.
- US3: As the society, delivery goes through a chosen provider.

## Business rules
- BR1: Every template has a unique `template_key`.
- BR2: Every send is logged with status and (when available) a provider message id.

## Acceptance criteria

### AC1: Manage templates
- **Trace**: US1, BR1
- **Given**: the SMS admin page
- **When**: an admin creates/edits a template
- **Then**: it is stored with a unique template_key

### AC2: Send & log a message
- **Trace**: US2, BR2
- **Given**: a member and a template
- **When**: an admin sends
- **Then**: an `sms_logs` row records body + status

### AC3: Provider integration
- **Trace**: US3
- **Given**: provider credentials are configured
- **When**: a message is sent
- **Then**: it is dispatched and the provider message id is stored

## Out of scope (not asked for)
- (see business-context)
