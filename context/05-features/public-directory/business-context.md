---
type: business-context
spec_version: 1
feature: public-directory
file_type: business-context
contract_version: 1
status: done
depends_on: [members, member-profile]
last_review: 2026-08-14
frozen: false
tags: [public-directory, business-context]
---

# Public Member Directory — business context

## Goal
Let the public see a safe directory of members who have opted in, while guaranteeing private
information is never exposed.

## User stories
- US1: As a member, I can turn "show me on the public directory" on or off, so that I control my public presence.
- US2: As a public visitor, I can browse opted-in members' safe details, so that I can find community members.

## Business rules
- BR1: The public directory shows only safe fields — profile photo, name, profession and approved short bio.
- BR2: Only members who have enabled "Show on Public Directory" appear.
- BR3: Sensitive identity, contact, payment and finance fields are never public, under any query or page.

## What this feature owns
- The opt-in flag's public meaning, the safe public view, and the public directory page.

## What this feature does NOT own
- Editing profile content (member-profile), the member roster (members).

## Out of scope (not planned)
- Editing profile content (covered by member-profile).
- A separate bio-approval workflow (short bio is shown as entered).

## Acceptance criteria

### AC1: Member controls public visibility
- **Trace**: US1, BR2
- **Given**: a logged-in member
- **When**: they toggle "Show on Public Directory"
- **Then**: their safe profile appears or disappears from the public directory accordingly.

### AC2: Directory exposes only safe fields
- **Trace**: US2, BR1, BR3
- **Given**: a public visitor viewing the directory
- **When**: they open any listed member
- **Then**: only photo, name, profession and approved short bio are shown, and no private field is retrievable.

### Edge & error cases
- No opted-in members → the directory shows an empty state.
- A member without a photo → a name-initial avatar is shown.
