---
title: "Phase 01 — Foundation (auth + scaffold)"
type: phase-summary
tags: [phase-01, phase-summary]
last_review: 2026-08-13
status: locked
locked_at: 2026-08-13
ac_total: 10
ac_green: 10
---

> [!NOTE]
> **This phase is locked.** It was sealed on 2026-08-13 and serves as a read-only historical record.
> To continue work, see the next phase or run `ls context/06-phase/`.

# Phase 01 — Foundation (auth + scaffold)

> 🔒 **LOCKED — sealed on 2026-08-13**
> This phase is a permanent historical record. No further changes are allowed.

## What this phase delivers
The foundation the rest of the roadmap builds on: authentication/authorization for admins, the
full Postgres schema (`supabase/schema.sql`), and the public Bengali homepage. Feature CRUD
(members, payments, finance, notices, projects, mahfil, executive-admins) is scaffolded as
dashboard cards but **not wired** — those are future phases.

## Feature table
| # | Feature | ACs | Status | What it does | Task |
|---|---|---|---|---|---|
| 1 | **admin-access** | 4 | ✅ done | Magic-link login + active-admin gate + logout | T01 |
| 2 | **public-site** | 3 | ✅ done | Static Bengali homepage + footer year + developer credit/branding | T02 |
| 3 | **_cross-cutting** | 1 | ✅ done | No secret credentials in the public website | T03 |
| 4 | **member-profile** | 2 | ✅ done | Capture blood group at registration + show on profile | T04 |

**Total: 10 ACs (4 + 3 + 1 + 2)**

## Not in this phase (scaffolded only — see BACKLOG)
members, payments, finance, notices, projects, mahfil, executive-admins (dashboard cards, no logic);
sms + birthday (blocked on an SMS provider).

## Completion log
_Filled in as features complete. Never edit existing entries._

| Date | Feature | ACs | Notes |
|---|---|---|---|
| 2026-08-13 | admin-access, public-site, _cross-cutting, member-profile | 10 | T01–T04 verified by user; 10/10 ACs green. |
| 2026-08-13 | 🔒 Phase locked | — | Sealed by /phase-finish. No further changes allowed. Un-tasked requirements (members, payments, finance, notices, projects, mahfil, executive-admins, sms, birthday) abandoned per user confirmation. |
