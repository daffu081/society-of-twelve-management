---
type: business-context
spec_version: 1
feature: member-profile
file_type: business-context
contract_version: 1
status: in_progress
depends_on: [admin-access]
last_review: 2026-08-13
frozen: false
tags: [member-profile, business-context]
---

# Member profile — business context

## Goal
Capture each member's blood group when they register and show it on their member profile, so the society has it on record.

## User stories
- US1: As an admin registering a member, I can record the member's blood group on the registration form, so that the society keeps it on file.
- US2: As someone viewing a member's profile, I can see that member's blood group.

## Business rules
- BR1: The blood group is captured on the member registration form.
- BR2: The blood group is chosen from the standard blood groups (A+, A−, B+, B−, AB+, AB−, O+, O−).
- BR3: A member's saved blood group is shown on their member profile.

## What this feature owns
- The blood-group field on the member registration form and its display in the members list/profile.

## What this feature does NOT own
- The full member record and public directory (that is the `members` feature, not yet built).

## Out of scope (not planned)
- Showing blood group in the public member directory.
- Making blood group mandatory.

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
