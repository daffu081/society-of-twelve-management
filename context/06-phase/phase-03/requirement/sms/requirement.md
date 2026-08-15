---
type: requirement
spec_version: 1
title: "SMS — requirement"
feature: sms
phase: 3
tags: [sms, requirement]
last_review: 2026-08-15
---

# SMS — requirement

> **Pure business. Written for a non-technical client.** What they want and why — never how.
> Gathered by `/gather-requirement`. `/create-task` turns the ACs below into tasks;
> `/implement-task` later builds it and records the technical spec in `05-features/`.

## Goal
Make sure the organization starts with a ready-to-use set of standard Bangla messages, so admins can
send common notifications immediately and still edit the wording whenever they want.

## User stories
- US7: As an admin, I want the six standard Bangla messages to already exist when the system starts, so
  that I can send them right away without writing them from scratch.

## Business rules
- BR7: Six default Bangla templates ship pre-populated: payment success, due payment reminder, meeting
  notice, birthday wish, general notice, and payment thank-you.
- BR8: Each default template stays fully editable by an admin, exactly like any other template.
- BR9: Each template keeps its fill-in placeholders (such as the member's name, amount, receipt number,
  due amount, date, time, venue and notice text) so the right details appear when a message is sent.

## Acceptance criteria

### AC7: Six default Bangla templates ship ready to use
- **Trace**: US7, BR7, BR8, BR9
- **Given**: a freshly set-up system
- **When**: an admin opens the SMS templates
- **Then**: the six standard Bangla templates are already present with their placeholders, ready to send,
  and each one can be edited and saved.

## Out of scope (not asked for)
- Adding new template types beyond the six defaults (admins can still create their own separately).
- Actually sending messages, which is covered by the existing send-and-log criteria.
