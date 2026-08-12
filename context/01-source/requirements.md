---
type: source
title: "Requirements"
last_review: 2026-08-13
---

# Requirements

## Functional
- R1: Admins authenticate (magic-link email) and are authorized only if active in the `admins` table.
- R2: Two admin tiers — Super Admin and Executive Admin (the latter with per-capability checkbox permissions).
- R3: Manage members (profile, fee category, monthly fee) and let a member opt into the public directory.
- R4: Record payments with a unique receipt number, purpose, method and date.
- R5: Track finance as income and expenses; derive totals.
- R6: Publish notices (with a "running" flag surfaced on the public homepage), projects and mahfil.
- R7: Soft-delete: deleted rows move to a `bin` with a 30-day restore window.
- R8 (planned): SMS templates + logs via an external provider; mobile-OTP; birthday-greeting automation.

## Non-functional
- NFR1 (performance): static frontend, no build step; loads over plain HTTP hosting.
- NFR2 (security): all writes gated by Supabase auth + `admins` check; Postgres RLS to be added (currently absent — known gap).
- NFR3 (availability): backend availability = Supabase cloud SLA; frontend is static and cache-friendly.

<!-- TODO(user): confirm RLS requirement and any data-residency needs. -->
