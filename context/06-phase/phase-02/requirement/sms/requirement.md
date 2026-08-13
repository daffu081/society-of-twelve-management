---
type: requirement
spec_version: 1
title: "SMS — requirement"
feature: sms
phase: 2
tags: [sms, requirement]
last_review: 2026-08-13
---

# SMS — requirement

> Pure business. Continues AC numbering from Phase 01 (AC1–AC3).

## Goal
Send members Bangla SMS from editable templates through a replaceable provider, with full logging and permission control.

## User stories
- US4: As an admin, I can edit any SMS message template, so that wording stays current.
- US5: As an authorized admin/executive, I can send an SMS, so that members are informed.
- US6: As an admin, I can review a log of sent messages, so that I have a record.

## Business rules
- BR4: All SMS bodies are editable from the admin interface and stored as templates.
- BR5: Initial Bangla templates: Payment Success, Due Payment Reminder, Meeting Notice, Birthday Wish, General Notice, Payment Thank You.
- BR6: Templates use dynamic placeholders such as {member_name}, {amount}, {receipt_no}, {due_amount}, {date}, {time}, {venue}, {notice_text}, replaced with real values before sending.
- BR7: Only users with the SMS permission can send.
- BR8: The provider is configurable/replaceable without rewriting the app; provider secrets are never in the browser.
- BR9: Where supported, the sender ID/header is "Society of Twelve".
- BR10: Every send is logged with recipient, message/template, timestamp, delivery status, trigger and sending user.

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

## Out of scope (not asked for)
- Birthday scheduling logic (covered by birthday).
