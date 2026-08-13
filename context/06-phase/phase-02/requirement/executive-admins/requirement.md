---
type: requirement
spec_version: 1
title: "Executive Admins & Permissions — requirement"
feature: executive-admins
phase: 2
tags: [executive-admins, requirement]
last_review: 2026-08-13
---

# Executive Admins & Permissions — requirement

> Pure business. Continues AC numbering from Phase 01 (AC1–AC3).

## Goal
Let the Super Admin grant executive admins granular, enforced permissions across every area of the system.

## User stories
- US4: As a Super Admin, I can assign granular permissions to an executive using a checkbox matrix, so that access is controlled per area.
- US5: As a Super Admin, I can manage Super Admin assignment safely, so that the organization is never locked out.

## Business rules
- BR4: Permission keys include read/write (and where noted, extra actions) for: members, payments, finance, notices (+publish), projects, mahfil, sms (+send, +template_edit), birthday (+manage), awards, rules, reports (+export), committee, settings.
- BR5: Permission restrictions must be enforced by secure server-side authorization, not only by hiding menus.
- BR6: The system must protect against removing the last active Super Admin.
- BR7: A future mechanism must allow authorized Super Admin management/change.

### AC4: Assign granular permissions
- **Trace**: US4, BR4, BR5
- **Given**: a Super Admin on the Executive Management screen
- **When**: they check/uncheck permission keys for an executive
- **Then**: the executive can perform only the allowed actions, and denied actions are blocked even if attempted directly.

### AC5: Protect the last Super Admin
- **Trace**: US5, BR6
- **Given**: only one active Super Admin remains
- **When**: an attempt is made to remove or deactivate them
- **Then**: the system prevents it.

## Out of scope (not asked for)
- Executive login itself (covered by admin-access).
