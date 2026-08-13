---
type: requirement
spec_version: 1
title: "Member Profile — requirement"
feature: member-profile
phase: 2
tags: [member-profile, requirement]
last_review: 2026-08-13
---

# Member Profile — requirement

> Pure business. Continues AC numbering from Phase 01 (AC1–AC2 = blood group).

## Goal
Give every member a complete, structured profile so the organization has full member records and members can maintain their own details.

## User stories
- US1: As an admin, I can record a member's full details, so that the organization has complete records.
- US2: As a member, I can view and edit the fields I'm permitted to, so that my information stays current.
- US3: As an admin, I can store a member's private identity documents securely, so that they're on file but never exposed.

## Business rules
- BR1: Each member gets an automatically generated member ID in the format SOT0001, SOT0002, … — never reused, never editable.
- BR2: Email is optional; mobile number is required.
- BR3: NID number, Birth Registration ID and Passport number are strictly private organization-only fields.
- BR4: A member may only edit the fields they are permitted to; identity, fee and status fields are admin-only.

### AC3: Full profile captured
- **Trace**: US1, BR1, BR2
- **Given**: an admin is registering or editing a member
- **When**: they fill the profile
- **Then**: the system stores full name, father's name, house name, village, mobile, optional email, date of birth, blood group, profession, monthly fee, join date, active/inactive status, profile photo, and optional education, skills, interests and short bio — with an auto-generated SOT member ID.

### AC4: Private identity fields stored but hidden
- **Trace**: US3, BR3
- **Given**: a member has NID, Birth Registration ID or Passport recorded
- **When**: any non-admin view, public page or public query is used
- **Then**: those three fields are never shown or returned.

### AC5: Member self-service edit
- **Trace**: US2, BR4
- **Given**: a logged-in member on their own profile
- **When**: they change a permitted field (e.g. skills, bio, interests)
- **Then**: the change is saved, and they cannot alter identity, fee, member ID or status fields.

## Out of scope (not asked for)
- Public exposure of any profile field (covered by public-directory).
- Fee tier definitions (covered by profession-fee).
