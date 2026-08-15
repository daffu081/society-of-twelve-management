---
spec_version: 1
type: agent-rules
title: "Agent Rules"
tags: [rules, agent, guardrails]
file_type: spec
frozen: false
last_review: 2026-08-13
---

# Agent rules
# These rules apply on EVERY task. No exceptions.

## 🔒 The context is command-only — this rule overrides everything

**Nothing under `05-features/` or `06-phase/` is ever edited freehand. It changes ONLY through the
slash commands below.** Never "just quickly update" an AC, a business rule, a status, a contract,
or a phase/task by editing the markdown directly.

Two things are kept strictly apart:
- **Requirements** — what the client wants, in pure business language — live in the active phase's
  `06-phase/<phase>/requirement/` folder. This is the ONE place business intent is written, and
  only `/gather-requirement` writes it.
- **The `05-features/` spec** — the as-built technical/business/test record — is **derived**. It is
  **never hand-edited** and is written ONLY by `/implement-task`, as the work actually lands.

| To change… | Run |
|---|---|
| Business intent — what the client wants (goals, user stories, business rules, acceptance criteria) — gathered into the active phase's `requirement/` folder, pure business, no tech | `/gather-requirement "<what the client wants>"` |
| Create a phase | `/create-phase <phase-id> "<title>"` |
| Split a requirement into a task on the active phase | `/create-task "<phase-id>" "<what>"` |
| Build a task — the ONLY command that writes code AND the ONLY command that writes the `05-features/` spec (from the requirement, as work lands) | `/implement-task "<phase-id>" "<task-id>"` |
| Lock a finished phase | `/phase-finish <phase-id>` |

These five commands are the entire surface. There is no other way to mutate requirements or the
spec. If asked to edit either without one, invoke the correct command or tell the user which to run.
(Reading is always fine — this rule is about *writing*.)

## Before writing any code

1. Read `/context/architecture-map.md` FIRST — it is the loading policy. Follow it strictly.
2. State which files you are about to load and why (one line each).
3. Load ONLY the files the map allows for your task type.
4. For cross-feature info, read that feature's `## Public surface` section (in its `technical-context.md`) and **nothing else** from it.
5. State the current implementation status from `technical-context.md`.
6. If a known bug exists in the area — mention it before any code.
7. If status is "Not started" — confirm intent before building from scratch.
8. For phase/task work, read `/context/06-phase/ACTIVE.md` and load ONLY the phase it names.

## Output format

- Start with 1–2 sentences: what you are doing and why.
- Show ONLY changed files — never repeat unchanged files.
- Implementation status is updated by `/implement-task` as it lands the work — not hand-edited.
- Use only error codes from `/context/02-shared/error-codes.md`.
- Follow patterns from `/context/04-architecture/patterns.md`.
- Follow naming from `/context/04-architecture/guidelines.md`.

## Never do these things

- Do not scan source files to understand the project — read spec files. (Exception: an
  explicit drift/audit task may compare specs against source as a read-only check.)
- Do not load another feature's `business-context.md`, full `technical-context.md`, or `test-context.md` — read only its `## Public surface` section.
- Do not load the whole `decisions/` directory — jump to the named ADR file.
- Do not preemptively read shared docs — load on demand (architecture-map Tier D).
- Do not re-explain the architecture back to the developer.
- Do not ask clarifying questions if spec files already answer it.
- Do not touch files outside the current feature unless explicitly asked.
- Do not load or work on any phase except the one named in `06-phase/ACTIVE.md`.
- Do not start a new phase while one is active — finish (lock) the current one first.
- Do not start work that isn't in the active phase — park it in `BACKLOG.md`.
- Do not suggest a different architecture than what is in the ADRs.
- Do not invent new error codes — use `error-codes.md`.
- Do not invent new patterns — use `patterns.md`.
- Never add a framework, bundler, or npm dependency — this is a deliberately build-free static site (needs an ADR to change).
- Never trust the auth session for authorization — re-check the `admins` table (`active=true`) via `checkAdminAccess()` (ADR-001).
- Never hard-`DELETE` a domain row — soft-delete into `bin` with a snapshot + 30-day expiry (ADR-003).
- Never do money math in JS floats — money is Postgres `numeric(12,2)` (ADR-002).
- Never put the Supabase service-role key in client code, or hardcode creds — read `window.SOT_CONFIG`.
- Never expose a member's private fields publicly unless `show_on_public_directory = true`.

## Git — mandatory on every branch / commit / PR

Read `/context/02-shared/git-conventions.md` before any git operation. Non-negotiables:

- **Never commit to `main`/`develop` directly** — always branch first.
- **Every commit has a body** — a "What" paragraph and a "Why" paragraph.
- **🔴 No automatic commits** — show the diff + draft message, ask before `git commit`.
- **🔴 No automatic PRs** — show the PR preview, ask before `gh pr create`.
- **🔴 No automatic merges** — never merge without explicit approval.
- **Never add AI attribution** — no `Co-Authored-By: Claude` trailer and no "Generated with Claude Code" line in any commit message or PR body.
- **Never leave work uncommitted** — end every task with a clean working tree. Commit finished
  changes on a feature branch (through the approval gate above) or discard them; never leave dangling
  edits behind for the next session to trip over.

These confirmation gates override everything, including earlier "implement X and commit"
instructions. Approval is per-action: commit approval is NOT push/PR/merge approval.

## When you finish a task

All of these happen **through commands**, never by hand-editing requirements or the spec:

- Capability done / bug found / file mapping / contract / AC settled → `/implement-task` records it
  in the feature's `05-features/` spec as part of landing the work.
- The client wants the scope changed (new/edited business intent) → stop and run
  `/gather-requirement` to update the requirement, then `/create-task` + `/implement-task`.
- A genuine architectural decision was made → `/implement-task` adds the ADR + decision-log entry.
