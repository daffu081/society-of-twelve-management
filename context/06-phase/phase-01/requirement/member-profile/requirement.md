---
type: requirement
spec_version: 1
title: "Member profile — requirement"
feature: member-profile
phase: 1
tags: [member-profile, requirement]
last_review: 2026-08-13
---

# Member profile — requirement

> **Pure business. Written for a non-technical client.** What they want and why — never how.

## Goal
Capture each member's blood group when they register and show it on their member profile, so the society has it on record.

## User stories
- US1: As an admin registering a member, I can record the member's blood group on the registration form, so that the society keeps it on file.
- US2: As someone viewing a member's profile, I can see that member's blood group.

## Business rules
- BR1: The blood group is captured on the member registration form.
- BR2: The blood group is chosen from the standard blood groups (A+, A−, B+, B−, AB+, AB−, O+, O−).
- BR3: A member's saved blood group is shown on their member profile.

## Acceptance criteria

### AC1: Blood group captured at registration
- **Trace**: US1, BR1, BR2
- **Given**: the member registration form
- **When**: an admin fills it in and saves a new member
- **Then**: they can select the member's blood group from the standard blood groups and it is saved with the member.

### AC2: Blood group shown on the member profile
- **Trace**: US2, BR3
- **Given**: a member who has a saved blood group
- **When**: their member profile is viewed
- **Then**: the member's blood group is displayed.

## Out of scope (not asked for)
- Showing blood group in the public member directory (not requested here).
- Other member registration fields (name, mobile, fee, etc.) — this requirement only adds blood group.
- Making blood group mandatory / blocking registration when it is left blank (not requested).
