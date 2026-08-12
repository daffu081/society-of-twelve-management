---
type: requirement
spec_version: 1
title: "Members — requirement"
feature: members
phase: 1
tags: [members, requirement]
last_review: 2026-08-13
---

# Members — requirement

> **Pure business.** Bootstrap-seeded from the existing codebase to match `05-features/members/business-context.md`.
> Ongoing changes go through `/gather-requirement`. AC ids are permanent and append-only.

## Goal
Maintain the society's member records — identity, contact, fee category and monthly fee — and let
each member choose whether to appear in the public directory.

## User stories
- US1: As an admin, I can add and edit a member's profile.
- US2: As an admin, I can see and search the member list.
- US3: As a member (via an admin), I can opt in/out of the public directory.

## Business rules
- BR1: Every member has a unique `member_id` and a name and mobile.
- BR2: Private fields (NID, birth-registration, passport) are never public.
- BR3: A member appears publicly only if `show_on_public_directory = true`.

## Acceptance criteria

### AC1: Create / edit member
- **Trace**: US1, BR1
- **Given**: the members admin page
- **When**: an admin saves a valid member (name, mobile, member_id)
- **Then**: the member is stored and appears in the list

### AC2: Public-directory consent
- **Trace**: US3, BR2, BR3
- **Given**: a member profile
- **When**: an admin toggles "Show on public directory"
- **Then**: only that member's public-safe fields become publicly visible

### AC3: List & search members
- **Trace**: US2
- **Given**: members exist
- **When**: an admin opens the list
- **Then**: members are listed and can be filtered by name/member_id

## Out of scope (not asked for)
- Member self-service editing without an admin.
