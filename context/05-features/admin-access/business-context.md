---
type: business-context
spec_version: 1
feature: admin-access
file_type: business-context
contract_version: 1
status: done
depends_on: []
last_review: 2026-08-15
frozen: false
tags: [admin-access, business-context]
---

# Admin access — business context

## Goal
Only vetted committee members may enter the admin area. Access is by email (a login link),
and being able to log in is not enough — the person must be a currently-active admin.

## User stories
- US1: As an admin, I can request a login link by email so I don't manage a password.
- US2: As the society, I can be sure only active admins reach the dashboard.
- US3: As an admin, I can log out.

## Business rules
- BR1: A person reaches the dashboard only if they are an active admin.
- BR2: Removing someone's access must not require deleting their login — deactivating them is enough.
- BR3: An admin sees whether they are Super Admin or Executive Admin.

## What this feature owns
- The login flow, the "are you an active admin?" gate, and logout.

## What this feature does NOT own
- Creating/editing admin rows or their permissions (that is `executive-admins`).

## Out of scope (not planned)
- Passwords, social login, self-service signup.

## Acceptance criteria

### AC1: Request login link
- **Trace**: US1, BR1
- **Given**: the login page
- **When**: an admin enters their email and submits
- **Then**: a magic login link is emailed and a confirmation message shows

### AC2: Active admin gets in
- **Trace**: US2, BR1, BR3
- **Given**: a logged-in user who is an active admin
- **When**: they open the dashboard
- **Then**: their name and role (Super/Executive Admin) are shown

### AC3: Non-admin is rejected
- **Trace**: US2, BR1
- **Given**: a logged-in user with no active admin row
- **When**: they open the dashboard
- **Then**: they are signed out and returned to login with a "no access" message

### AC4: Logout
- **Trace**: US3
- **Given**: a logged-in admin
- **When**: they click Logout
- **Then**: the session is cleared and they return to login

### Edge & error cases
- Sending the link fails → show "Unable to send login link."
- Not logged in at all → redirect straight to login.
