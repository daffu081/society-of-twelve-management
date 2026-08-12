---
title: "Phase 01 — Foundation (auth + scaffold)"
type: phase-summary
tags: [phase-01, phase-summary]
last_review: 2026-08-13
status: in_progress
started_at: "2026-08-13"
ac_total: 10
ac_green: 0
---

# Phase 01 — Foundation (auth + scaffold)

> **Status: 🔄 IN PROGRESS**
> This phase captures what already exists in the repo: admin magic-link auth + gate, the DB
> schema for all entities, and the public site shell. No ACs are formally verified yet
> (there is no test runner), so `ac_green` = 0 until each is confirmed.

## What this phase delivers
The foundation the rest of the roadmap builds on: authentication/authorization for admins, the
full Postgres schema (`supabase/schema.sql`), and the public Bengali homepage. Feature CRUD
(members, payments, finance, notices, projects, mahfil, executive-admins) is scaffolded as
dashboard cards but **not wired** — those are future phases.

## Feature table
| # | Feature | ACs | Status | What it does | Task |
|---|---|---|---|---|---|
| 1 | **admin-access** | 4 | 🔄 built, unverified | Magic-link login + active-admin gate + logout | T01 |
| 2 | **public-site** | 3 | 🔄 built, unverified | Static Bengali homepage + footer year + developer credit/branding | T02 |
| 3 | **_cross-cutting** | 1 | 🔄 todo | No secret credentials in the public website | T03 |
| 4 | **member-profile** | 2 | 🔄 todo | Capture blood group at registration + show on profile | T04 |

**Total: 10 ACs (4 + 3 + 1 + 2)**

## Not in this phase (scaffolded only — see BACKLOG)
members, payments, finance, notices, projects, mahfil, executive-admins (dashboard cards, no logic);
sms + birthday (blocked on an SMS provider).

## Completion log
_Filled in as features complete. Never edit existing entries._

| Date | Feature | ACs | Notes |
|---|---|---|---|
| — | — | — | — |
