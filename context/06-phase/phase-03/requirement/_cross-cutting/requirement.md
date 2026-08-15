---
type: requirement
spec_version: 1
title: "Cross-cutting — requirement"
feature: _cross-cutting
phase: 3
tags: [_cross-cutting, requirement]
last_review: 2026-08-15
---

# Cross-cutting — requirement

> **Pure business. Written for a non-technical client.** What they want and why — never how.

## Goal
Get the system safely into real production use: lock down the last data tables, deploy the release
correctly, and confirm every feature actually works against the live setup before it's trusted.

## User stories
- US5: As the organization, I want every sensitive data table protected, so that nobody holding a public
  key can read or change our message logs, birthday logs, templates or counters.
- US6: As the organization, I want the release applied to production in the correct order with the right
  access granted, so that admins and executives can actually use the system after go-live.
- US7: As the organization, I want every feature checked against the live system, so that we don't
  discover broken behaviour only after members rely on it.

## Business rules
- BR5: Sensitive data tables are readable/writable only through allowed access — never by anyone simply
  holding the public key.
- BR6: The production release is applied as a defined, repeatable sequence, and executives gain their area
  access only after their permission keys are granted.
- BR7: A feature is not considered live-verified until its checks pass against the real production setup.

## Acceptance criteria

### AC5: Deployment brings the system live in the correct order
- **Trace**: US6, BR6
- **Given**: a production environment with the release ready to apply
- **When**: the deployment steps are carried out in the defined order and executive permission keys are
  granted
- **Then**: the system is live, super admins have access, and each executive has exactly the area access
  their granted keys allow.

### AC6: Every feature is verified against the live setup
- **Trace**: US7, BR7
- **Given**: the system is deployed with real credentials in place
- **When**: each feature's checks are run against the live production setup
- **Then**: every feature behaves as specified, and any failure is recorded rather than assumed to work.

### AC7: Remaining sensitive tables are protected
- **Trace**: US5, BR5
- **Given**: the message logs, birthday logs, message templates and counters
- **When**: someone holding only the public key tries to read or change them
- **Then**: they are refused, and only allowed roles can access those tables.

## Out of scope (not asked for)
- Frontend secret handling beyond what AC1 already covers.
