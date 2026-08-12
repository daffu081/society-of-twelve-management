---
type: requirement
spec_version: 1
title: "Public site — requirement"
feature: public-site
phase: 1
tags: [public-site, requirement]
last_review: 2026-08-13
---

# Public site — requirement

> **Pure business.** Bootstrap-seeded from the existing codebase to match `05-features/public-site/business-context.md`.
> Ongoing changes go through `/gather-requirement`. AC ids are permanent and append-only.

## Goal
Give the community a public Bengali homepage introducing the Society of Twelve and (eventually)
surfacing running notices, projects, mahfil and the consenting-members directory.

## User stories
- US1: As a visitor, I can read about the society, its projects, mahfil, notices, rules and contact.
- US2: As the society, I want running notices and activity to appear publicly (planned).

## Business rules
- BR1: Content is Bengali-first.
- BR2: Only members who opted in (`show_on_public_directory`) appear publicly.
- BR3: The footer shows the developer credit "Developed By Sabbir Ahmed Sakib".
- BR4: The Society of Twelve logo/branding is used consistently across the public site.

## Acceptance criteria

### AC1: Homepage renders
- **Trace**: US1
- **Given**: a visitor opens `/`
- **When**: the page loads
- **Then**: header, hero, and About/Project/Mahfil/Notice/Members/Rules/Contact sections show

### AC2: Footer year is current
- **Trace**: US1
- **Given**: the homepage
- **When**: it loads
- **Then**: the footer copyright year is the current year

### AC3: Footer shows developer credit and consistent branding
- **Trace**: US1, BR3, BR4
- **Given**: any public page showing the footer
- **When**: the visitor views it
- **Then**: the footer shows "Developed By Sabbir Ahmed Sakib" and the page uses the Society of Twelve logo/branding

## Out of scope (not asked for)
- Public login or member self-service on the public site.
