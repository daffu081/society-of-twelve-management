---
type: requirement
spec_version: 1
title: "Admin access — requirement"
feature: admin-access
phase: 3
tags: [admin-access, requirement]
last_review: 2026-08-15
---

# Admin access — requirement

> **Pure business. Written for a non-technical client.** What they want and why — never how.

## Goal
Keep the admin sign-in screen honest: it only offers the login method that actually works
(a login link), so nobody is confused by a password box that does nothing.

## User stories
- US5: As an admin, I see only the login-link option on the sign-in screen, so that I'm not asked for a
  password the system never checks.

## Business rules
- BR5: The admin sign-in screen shows no password field while login is link-based.

## Acceptance criteria

### AC5: Sign-in screen shows only the working login method
- **Trace**: US5, BR5
- **Given**: an admin opens the sign-in screen
- **When**: the screen loads
- **Then**: they see only the login-link option and no unused password field, and they can still sign in
  successfully with the login link.

## Out of scope (not asked for)
- Adding password login (still not requested; login stays link-based).
