---
type: requirement
spec_version: 1
title: "Cross-cutting (security, privacy, storage) — requirement"
feature: _cross-cutting
phase: 2
tags: [_cross-cutting, requirement]
last_review: 2026-08-13
---

# Cross-cutting (security, privacy, storage) — requirement

> Pure business. Continues AC numbering from Phase 01 (AC1 = no secrets in frontend).

## Goal
Guarantee that access control, member privacy and file storage are enforced securely across the whole system — not just hidden in the interface.

## User stories
- US1: As the organization, private data is protected everywhere, so that it can never leak through a page, link or query.
- US2: As the organization, file storage keeps private documents out of public reach, so that identity documents are never exposed.

## Business rules
- BR2: Access control is enforced at the secure server layer; hiding menus or frontend checks alone is never sufficient.
- BR3: Each member can access only their own permitted records; members cannot see other members' private information.
- BR4: Public access uses only explicitly safe views; payment, finance and NID/Birth-ID/Passport data are never public.
- BR5: Security enforcement is never disabled as a shortcut to make a feature work.
- BR6: Private identity documents are never stored in a publicly accessible location; public files (photos, event images) use appropriate public storage.

### AC2: Enforced access control
- **Trace**: US1, BR2, BR3, BR5
- **Given**: any user (public, member, executive, super admin)
- **When**: they attempt to read or change data directly, bypassing the interface
- **Then**: they can only access what their role permits, and privileged data stays protected.

### AC3: Public exposure is safe-only
- **Trace**: US1, BR4
- **Given**: any public page or public query
- **When**: it runs
- **Then**: it returns only safe fields — never payment, finance or NID/Birth-ID/Passport data.

### AC4: Storage separates public and private files
- **Trace**: US2, BR6
- **Given**: uploaded files (profile/committee/project/mahfil/award images and private identity documents)
- **When**: they are stored
- **Then**: private identity documents are kept in non-public storage while public images use public storage.

## Out of scope (not asked for)
- Frontend secret handling (already covered by _cross-cutting AC1, Phase 01).
