---
type: business-context
spec_version: 1
feature: executive-admins
file_type: business-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-14
frozen: false
tags: [executive-admins, business-context]
---

# Executive admins — business context

## Goal
Let the Super Admin create executive admins and grant each one only the capabilities they need
(checkbox permissions), and deactivate them without deleting.

## User stories
- US1: As a Super Admin, I can add an executive admin.
- US2: As a Super Admin, I can set which capabilities an executive admin has.
- US3: As a Super Admin, I can deactivate an admin.
- US4: As a Super Admin, I can assign granular permissions to an executive using a checkbox matrix, so that access is controlled per area.
- US5: As a Super Admin, I can manage Super Admin assignment safely, so that the organization is never locked out.

## Business rules
- BR1: Only a Super Admin manages admins.
- BR2: Executive admins have exactly the capabilities checked in their `permissions`.
- BR3: Deactivating (not deleting) revokes access.
- BR4: Permission keys include read/write (and where noted, extra actions) for: members, payments, finance, notices (+publish), projects, mahfil, sms (+send, +template_edit), birthday (+manage), awards, rules, reports (+export), committee, settings.
- BR5: Permission restrictions must be enforced by secure server-side authorization, not only by hiding menus.
- BR6: The system must protect against removing the last active Super Admin.
- BR7: A future mechanism must allow authorized Super Admin management/change.

## What this feature owns
- Admin rows management and the `permissions` model.

## What this feature does NOT own
- The login/gate flow itself (feature `admin-access`).

## Out of scope (not planned)
- Custom roles beyond super/executive.

## Acceptance criteria

### AC1: Create executive admin
- **Trace**: US1, BR1
- **Given**: a Super Admin
- **When**: they add an admin (name, email)
- **Then**: an `executive_admin` row is created, active

### AC2: Set checkbox permissions
- **Trace**: US2, BR2
- **Given**: an executive admin
- **When**: the Super Admin checks/unchecks capabilities
- **Then**: the `permissions` jsonb reflects exactly those capabilities

### AC3: Deactivate admin
- **Trace**: US3, BR3
- **Given**: an active admin
- **When**: the Super Admin deactivates them
- **Then**: `active=false` and they can no longer reach the dashboard

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

### Edge & error cases
- A non-Super admin cannot open this feature.
