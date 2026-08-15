---
type: business-context
spec_version: 1
feature: member-profile
file_type: business-context
contract_version: 1
status: done
depends_on: [admin-access]
last_review: 2026-08-15
frozen: false
tags: [member-profile, business-context]
---

# Member profile — business context

## Goal
Give every member a complete, structured profile — starting with blood group (Phase 01) and
extended to the full identity/contact/fee/status field set with private identity documents and
member self-service (Phase 02) — so the society has full member records and members can maintain
their own details.

## User stories
- US1: As an admin registering a member, I can record the member's blood group on the registration form, so that the society keeps it on file.
- US2: As someone viewing a member's profile, I can see that member's blood group.
- US3: As an admin, I can record a member's full details, so that the organization has complete records.
- US4: As a member, I can view and edit the fields I'm permitted to, so that my information stays current.
- US5: As an admin, I can store a member's private identity documents securely, so that they're on file but never exposed.

## Business rules
- BR1: The blood group is captured on the member registration form.
- BR2: The blood group is chosen from the standard blood groups (A+, A−, B+, B−, AB+, AB−, O+, O−).
- BR3: A member's saved blood group is shown on their member profile.
- BR4: Each member gets an automatically generated member ID in the format SOT0001, SOT0002, … — never reused, never editable.
- BR5: Email is optional; mobile number is required.
- BR6: NID number, Birth Registration ID and Passport number are strictly private organization-only fields.
- BR7: A member may only edit the fields they are permitted to; identity, fee and status fields are admin-only.

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
