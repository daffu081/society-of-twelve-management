---
type: business-context
spec_version: 1
feature: sms
file_type: business-context
contract_version: 1
status: planned
depends_on: [admin-access, members]
last_review: 2026-08-13
frozen: false
tags: [sms, business-context]
---

# SMS — business context

> **Blocked:** requires the society to contract an external SMS provider. Until then this is
> planned only (see BACKLOG / phase notes).

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

## What this feature owns
- The `sms_templates` and `sms_logs` tables and sending.

## What this feature does NOT own
- Birthday scheduling (feature `birthday` triggers sends).

## Out of scope (not planned until provider chosen)
- Mobile OTP login (listed in the implementation plan, inactive without a provider).

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

### Edge & error cases
- No provider configured → send is blocked/queued, clearly indicated.
