# Society of Twelve Management System

Admin + member management portal for the Society of Twelve community organization (members, payments, finance, notices, projects/mahfil, SMS), built on Supabase with a static HTML/CSS/JS frontend.

---

## STEP 1 — always

**Read `context/architecture-map.md` first.** It is the loading policy. It tells you which
files to load for your task type, which to load on demand, and which to never load. Follow
it strictly. After the map, load only what the map directs you to.

---

## Where things live

| You need… | Look in |
|---|---|
| The loading policy (READ FIRST) | `context/architecture-map.md` |
| Hard rules (always load, tiny) | `context/agent-rules.md`, `context/02-shared/anti-patterns.md` |
| A feature's full context | `context/05-features/<feature>/` — its 3 files |
| What another feature exposes (cross-feature only) | the `## Public surface` section of `context/05-features/<other>/technical-context.md` — nothing else from it |
| An architectural decision (by number) | `context/04-architecture/decisions/` — the specific ADR; never the whole dir |
| Code patterns to copy | `context/04-architecture/patterns.md` |
| Folder structure / naming | `context/04-architecture/guidelines.md` |
| Test helpers + coverage thresholds | `context/02-shared/testing-conventions.md` |
| Error codes table | `context/02-shared/error-codes.md` |
| Glossary of domain terms | `context/02-shared/glossary.md` |
| Dependencies | `context/02-shared/tech-stack.md` |
| Day-to-day commands | `.claude/commands/` |

---

## Non-negotiables

- Money is stored as `numeric(12,2)` in Postgres — never floats in app code — ADR-002
- All admin access is gated through the `admins` table (`active = true`) after Supabase auth — never trust the auth session alone — ADR-001
- Deletes are soft: rows move to the `bin` table with a 30-day `expires_at` snapshot — never hard-delete domain rows — ADR-003

If anything you remember conflicts with the spec, the **spec wins**. Ask the user before
acting on the conflict.

---

## Common entry points

**Requirements and the spec change ONLY through these commands — never hand-edit files under `05-features/` or `06-phase/`.**

- Capture what the client wants (pure business, into the active phase's `requirement/`) → `/gather-requirement "<what the client wants>"`
- Start a phase → `/create-phase <phase-id> "<title>"`
- Split a requirement into a task on the active phase → `/create-task "<phase-id>" "<what>"`
- Build a task (writes code + settles the requirement into the `05-features/` spec) → `/implement-task "<phase-id>" "<task-id>"`
- Lock a finished phase → `/phase-finish <phase-id>`

Run Claude Code from this project root so the `context/...` paths resolve correctly.
