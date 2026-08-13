---
type: requirement
spec_version: 1
title: "Public Member Directory — requirement"
feature: public-directory
phase: 2
tags: [public-directory, requirement]
last_review: 2026-08-13
---

# Public Member Directory — requirement

> Pure business. New feature. Privacy-safe public exposure of members.

## Goal
Let the public see a safe directory of members who have opted in, while guaranteeing private information is never exposed.

## User stories
- US1: As a member, I can turn "show me on the public directory" on or off, so that I control my public presence.
- US2: As a public visitor, I can browse opted-in members' safe details, so that I can find community members.

## Business rules
- BR1: The public directory shows only safe fields — profile photo, name, profession and approved short bio.
- BR2: Only members who have enabled "Show on Public Directory" appear.
- BR3: Sensitive identity, contact, payment and finance fields are never public, under any query or page.

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

## Out of scope (not asked for)
- Editing profile content (covered by member-profile).
