---
type: business-context
spec_version: 1
feature: sms
file_type: business-context
contract_version: 1
status: in_progress
depends_on: [admin-access, members]
last_review: 2026-08-14
frozen: false
tags: [sms, business-context]
---

# SMS — business context

> **Provider still not contracted.** The full layer (templates, queue, send path, log) is built;
> actual delivery starts once SMS_PROVIDER_URL/SMS_API_KEY are configured — no code change needed.

## Goal
Manage reusable SMS templates and send/log messages to members (fee reminders, greetings),
via an external provider.

## User stories
- US1: As an admin, I can manage SMS templates.
- US2: As an admin, I can send a message to a member and see it logged.
- US3: As the society, delivery goes through a chosen provider.
- US4: As an admin, I can edit any SMS message template, so that wording stays current.
- US5: As an authorized admin/executive, I can send an SMS, so that members are informed.
- US6: As an admin, I can review a log of sent messages, so that I have a record.

## Business rules
- BR1: Every template has a unique `template_key`.
- BR2: Every send is logged with status and (when available) a provider message id.
- BR4: All SMS bodies are editable from the admin interface and stored as templates.
- BR5: Initial Bangla templates: Payment Success, Due Payment Reminder, Meeting Notice, Birthday Wish, General Notice, Payment Thank You.
- BR6: Templates use dynamic placeholders such as {member_name}, {amount}, {receipt_no}, {due_amount}, {date}, {time}, {venue}, {notice_text}, replaced with real values before sending.
- BR7: Only users with the SMS permission can send.
- BR8: The provider is configurable/replaceable without rewriting the app; provider secrets are never in the browser.
- BR9: Where supported, the sender ID/header is "Society of Twelve".
- BR10: Every send is logged with recipient, message/template, timestamp, delivery status, trigger and sending user.

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

### AC4: Edit templates
- **Trace**: US4, BR4, BR5, BR6
- **Given**: an admin with template-edit permission
- **When**: they edit a template
- **Then**: the new wording (with placeholders) is saved and used for future sends.

### AC5: Send and log
- **Trace**: US5, US6, BR7, BR9, BR10
- **Given**: an authorized sender
- **When**: they send an SMS
- **Then**: placeholders resolve to the correct member's values, the message goes out under the Society of Twelve sender ID where supported, and a log entry records recipient, template, timestamp, status, trigger and sender.

### AC6: Provider is replaceable and secret-safe
- **Trace**: BR8
- **Given**: the SMS provider must change
- **When**: configuration is updated
- **Then**: sending continues to work without app changes, and no provider secret is ever present in browser code.

### Edge & error cases
- No provider configured → send is blocked/queued, clearly indicated.
