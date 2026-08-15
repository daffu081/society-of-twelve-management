---
type: requirement
spec_version: 1
title: "Member profile — requirement"
feature: member-profile
phase: 3
tags: [member-profile, requirement]
last_review: 2026-08-15
---

# Member profile — requirement

> **Pure business. Written for a non-technical client.** What they want and why — never how.
> Gathered by `/gather-requirement`. `/create-task` turns the ACs below into tasks;
> `/implement-task` later builds it and records the technical spec in `05-features/`.

## Goal
Give each member their own way to sign in to the member portal, so they can reach their profile,
payment history and receipts without an admin doing it for them — and, once the organization has an
SMS provider, let them sign in with a one-time code sent to their mobile.

## User stories
- US6: As a member, I can log in to my own member portal, so that I can view and manage the parts of my
  profile I'm allowed to and see my payment history and receipts.
- US7: As a member, I can log in with a one-time code sent to my mobile, so that I can sign in easily
  without needing a link or password.

## Business rules
- BR6: A member can only ever see and manage their own information after logging in — never anyone else's.
- BR7: Logging in by mobile one-time code is only offered once an SMS provider is connected; until then a
  login-link method is used.
- BR8: A one-time code is valid only for a short time and only for the member it was sent to.

## Acceptance criteria

### AC6: Member logs in to their own portal
- **Trace**: US6, BR6, BR7
- **Given**: a registered member who is not signed in
- **When**: the member logs in with their own credentials
- **Then**: they reach their own member portal — their profile, payment history and receipts — and can
  see nothing belonging to any other member.

### AC7: Member logs in with a mobile one-time code
- **Trace**: US7, BR6, BR7, BR8
- **Given**: a registered member with a mobile number, and an SMS provider is connected
- **When**: the member requests a one-time code and enters the code they receive
- **Then**: they are signed in to their own portal; an expired, already-used or wrong code does not sign
  them in, and no code grants access to anyone else's information.

## Out of scope (not asked for)
- Public self-service signup — accounts are still created through the admin roster.
- One-time-code login while no SMS provider is connected (AC7 activates once a provider is set up).
