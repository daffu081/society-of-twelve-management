---
type: business-context
spec_version: 1
feature: _cross-cutting
file_type: business-context
contract_version: 1
status: done
depends_on: []
last_review: 2026-08-15
frozen: false
tags: [_cross-cutting, business-context]
---

# Cross-cutting — business context

## Goal
Keep the organization's secret credentials out of anything a visitor can see, so the system can't be broken into through the public website.

## User stories
- US1: As the organization, I want no secret/service credentials to be reachable from the public website, so that no one can misuse them to access our data.
- US2: As the organization, private data is protected everywhere, so that it can never leak through a page, link or query.
- US3: As the organization, file storage keeps private documents out of public reach, so that identity documents are never exposed.

## Business rules
- BR1: Secret or service-level credentials must never be present in the public website code that visitors' browsers can read.
- BR2: Access control is enforced at the secure server layer; hiding menus or frontend checks alone is never sufficient.
- BR3: Each member can access only their own permitted records; members cannot see other members' private information.
- BR4: Public access uses only explicitly safe views; payment, finance and NID/Birth-ID/Passport data are never public.
- BR5: Security enforcement is never disabled as a shortcut to make a feature work.
- BR6: Private identity documents are never stored in a publicly accessible location; public files (photos, event images) use appropriate public storage.

## Out of scope (not planned)
- Frontend secret handling beyond AC1 (already covered).

## Acceptance criteria

### AC1: No secret credentials in the public website
- **Trace**: US1, BR1
- **Given**: the public website as delivered to a visitor's browser
- **When**: its contents are inspected
- **Then**: no secret or service-level credentials are present — only the safe, public-facing configuration

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
