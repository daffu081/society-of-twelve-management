---
type: business-context
spec_version: 1
feature: members
file_type: business-context
contract_version: 1
status: planned
depends_on: [admin-access]
last_review: 2026-08-13
frozen: false
tags: [members, business-context]
---

# Members — business context

## Goal
Maintain the society's member records — identity, contact, fee category and monthly fee — and let
each member choose whether to appear in the public directory.

## User stories
- US1: As an admin, I can add and edit a member's profile.
- US2: As an admin, I can see and search the member list.
- US3: As a member (via an admin), I can opt in/out of the public directory.
- US4: As an admin, I can create and edit any member record, so that the roster stays accurate.
- US5: As an admin, I can activate or deactivate a member, so that lapsed members are marked without losing history.
- US6: As an admin, I can search and filter the member list, so that I can find a member quickly.

## Business rules
- BR1: Every member has a unique `member_id` and a name and mobile.
- BR2: Private fields (NID, birth-registration, passport) are never public.
- BR3: A member appears publicly only if `show_on_public_directory = true`.
- BR5: Deactivating a member never deletes their records or history.
- BR6: A member's payment and receipt history is preserved regardless of profile changes.

## What this feature owns
- The `members` table and member CRUD.

## What this feature does NOT own
- Payments (feature `payments`), SMS (feature `sms`).

## Out of scope (not planned)
- Member self-service editing without an admin.

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

### Edge & error cases
- Duplicate `member_id` is rejected.
- Empty list shows an empty state.
