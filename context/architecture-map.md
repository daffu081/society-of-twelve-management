---
spec_version: 1
type: loading-policy
title: "Architecture Map"
tags: [policy, loading, agent, navigation]
file_type: spec
frozen: false
last_review: 2026-08-13
---

# Architecture Map
# **READ THIS FIRST on every task. Do not load other spec files unless this map tells you to.**
# This map is the loading policy. It exists to prevent token waste and cross-feature hallucination.

---

## The Iron Rule

> Load only what your current task requires. The default is to load NOTHING beyond the rules below.

When you work on feature **X**, you may load files inside `/context/05-features/X/`. You may **not**
load files inside `/context/05-features/Y/` — except the `## Public surface` section of Y's
`technical-context.md`.

---

## Loading tiers — exactly what to read per task type

### Tier A — Always (tiny; load once at task start)
1. `/context/architecture-map.md` ← this file
2. `/context/agent-rules.md`
3. `/context/02-shared/anti-patterns.md`

### Tier B — One feature's full context (when implementing or fixing that feature)
Pick exactly one feature. Load all three of its files. Do not load Tier B for any other feature.

### Tier C — Cross-feature surface (only when you call another feature)
Read **only** the `## Public surface` section of `/context/05-features/<Y>/technical-context.md`.

### Tier D — Concern-specific shared docs (load on demand by topic)
| Reading | Load |
|---|---|
| Touching Supabase tables / schema | `/context/02-shared/db-conventions.md` |
| Writing tests | `/context/02-shared/testing-conventions.md` |
| Emitting or catching errors | `/context/02-shared/error-codes.md` |
| Disambiguating a term | `/context/02-shared/glossary.md` |
| Adding a dependency | `/context/02-shared/tech-stack.md` |
| Branching, committing, opening a PR | `/context/02-shared/git-conventions.md` |
| Setting up / running locally | `/context/02-shared/dev-setup.md` |
| Why a decision was made | the specific `/context/04-architecture/decisions/ADR-NNN.md` |
| Original product scope | `/context/01-source/` |
| Any UI / theme work | `/context/07-design-guideline/design-system.md` |
| System boundaries / components | `/context/08-c4-diagram/` — only the level you need |

### Tier E — Architecture references (load by ADR number, never the whole dir)
- `/context/04-architecture/patterns.md` — copy-paste patterns
- `/context/04-architecture/guidelines.md` — folder placement + naming
- `/context/04-architecture/decisions/` — load ONLY the specific ADR file you need

### Tier F — Phase work (load the active phase ONLY, never a locked one)
1. Read `/context/06-phase/ACTIVE.md` — it names the single active phase.
2. Load **only** that phase's `phase.md`, plus the specific `task-T*.md` you were told to work on.
3. Never open a locked phase folder.

---

## Project directory (one-line tour)
```
index.html              # public landing page (Bengali)
config.js               # window.SOT_CONFIG = { SUPABASE_URL, SUPABASE_ANON_KEY }
assets/css, assets/js   # public site styles + behaviour
admin/                  # login.html, dashboard.html, admin.js (shared client + auth helpers)
supabase/schema.sql     # all Postgres tables (idempotent)
context/                # YOU ARE HERE — the specification
```
No build step, no package manager. Browser talks to Supabase directly. See `04-architecture/guidelines.md`.

## Feature index & routing (one-line each — do NOT load these to learn the feature)
Match a task to ONE feature by its trigger keywords, then load that feature per Tier B.

| Feature | Folder | Trigger keywords | Role |
|---|---|---|---|
| admin-access | `/context/05-features/admin-access/` | login, magic link, auth, admin gate, logout, session | Admin authN + authZ (BUILT) |
| public-site | `/context/05-features/public-site/` | homepage, landing, public, about, contact | Public Bengali site (BUILT) |
| members | `/context/05-features/members/` | member, profile, directory, fee category, consent | Member records + public directory |
| payments | `/context/05-features/payments/` | payment, receipt, fee, collect | Fee payments + receipts |
| finance | `/context/05-features/finance/` | income, expense, balance, finance | Income/expense ledger |
| notices | `/context/05-features/notices/` | notice, announcement, running notice | Notices (public + running flag) |
| projects | `/context/05-features/projects/` | project, running project, previous project | Projects showcase |
| mahfil | `/context/05-features/mahfil/` | mahfil, event, gathering | Mahfil events |
| executive-admins | `/context/05-features/executive-admins/` | admin, permission, checkbox, role, executive | Admin management + permissions |
| sms | `/context/05-features/sms/` | sms, template, provider, message log, otp | SMS templates/logs (PLANNED, blocked on provider) |
| birthday | `/context/05-features/birthday/` | birthday, greeting, automation | Birthday-greeting automation (PLANNED, blocked on sms) |

### Cross-feature dependencies
Keep in sync with each feature's `depends_on` in `05-features/INDEX.yml`.

| Feature | Depends on | Why |
|---|---|---|
| public-site | members, notices, projects, mahfil | Surfaces public directory + running items |
| members | admin-access | Managed from the admin area |
| payments | admin-access, members | A payment belongs to a member |
| finance | admin-access, payments | Income can link to a payment |
| notices | admin-access | Managed from the admin area |
| projects | admin-access | Managed from the admin area |
| mahfil | admin-access | Managed from the admin area |
| executive-admins | admin-access | Manages admin rows + permissions |
| sms | admin-access, members | Sends to members |
| birthday | sms, members | Birthday greeting is an SMS to a member |

## ADR index — which ADR answers which question
| Question | ADR |
|---|---|
| How do we decide who is allowed into the admin area? | ADR-001 |
| How is money stored / why not floats? | ADR-002 |
| How do we delete things without losing them? | ADR-003 |

## What you must NEVER do (loading-wise)
- Never grep across the spec to "find things." Use this map.
- Never load all features' contexts to "be safe." Load one.
- Never read another feature's `business-context.md` or full `technical-context.md` — read only its `## Public surface` section.
- Never read the whole `decisions/` directory. Jump to the ADR you need.
- Never open a locked phase folder. Only the phase named in `06-phase/ACTIVE.md` may be loaded.

## Pre-flight self-check (run before reading anything else)
1. **What feature am I working on?** → Tier B for that feature
2. **What concerns does this task touch?** → relevant Tier D
3. **Do I need to call another feature?** → only that feature's `## Public surface` section (Tier C)
If any answer is uncertain, ask the user before reading.
