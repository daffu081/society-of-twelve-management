---
type: requirement
spec_version: 1
title: "Members (admin management) — requirement"
feature: members
phase: 2
tags: [members, requirement]
last_review: 2026-08-13
---

# Members (admin management) — requirement

> Pure business. Continues AC numbering from Phase 01 (AC1–AC3).

## Goal
Let admins manage the full membership roster — create, edit, activate/deactivate, list and search members.

## User stories
- US4: As an admin, I can create and edit any member record, so that the roster stays accurate.
- US5: As an admin, I can activate or deactivate a member, so that lapsed members are marked without losing history.
- US6: As an admin, I can search and filter the member list, so that I can find a member quickly.

## Business rules
- BR5: Deactivating a member never deletes their records or history.
- BR6: A member's payment and receipt history is preserved regardless of profile changes.

### AC4: Manage the roster
- **Trace**: US4, US5, BR5
- **Given**: an admin with member permission
- **When**: they create, edit, or set a member active/inactive
- **Then**: the change is saved and the member's past records remain intact.

### AC5: List, search and filter
- **Trace**: US6
- **Given**: the member list
- **When**: an admin searches by name/ID/mobile or filters by status/profession
- **Then**: the matching members are shown.

## Out of scope (not asked for)
- Member-facing profile editing (covered by member-profile).
- Deleting members (members are deactivated, not deleted).
