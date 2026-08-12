---
description: Implement a task from the active phase — reads the task, loads its feature spec, implements AC-by-AC (test first), updates the technical/test context, then marks the task done and opens a PR. Usage `/implement-task "phase-3" "T03"`.
argument-hint: "<phase-id>" "<task-id>"
---

You are implementing a task from the [PROJECT NAME] phase roadmap. Arguments: **$ARGUMENTS**

This is the **only** command that writes code, and the **only** command that writes the
`05-features/` spec. As work lands, it settles the gathered requirement into the feature's spec:
authoring `business-context.md` from the phase's `requirement/<feature>/requirement.md`, and
filling the "how" (`technical-context.md`) and the "proof" (`test-context.md`). No other command
touches `05-features/`, and it is never hand-edited. If a client wants the scope changed, that's a
new requirement — stop and tell the user to run `/gather-requirement`.

---

## Step 0 — Parse arguments
- **PHASE_ID** — first quoted token (e.g. `phase-3`).
- **TASK_ID** — second token (`T03`, `t03`, or `3` → normalise to `T<NN>`).
Missing either → print usage and stop.

## Step 1 — Locate and read the task

```bash
ls context/06-phase/<PHASE_ID>/task-<TASK_ID>-*.md 2>/dev/null
```
Not found → list available tasks and stop. Read the task file in full: extract `feature`,
`status`, the ACs it delivers, and its "Files to read first" list. If `status: done`, warn and
wait for confirmation before re-implementing.

Confirm the phase is the active one (`context/06-phase/ACTIVE.md`). Refuse to implement a task in
a locked or non-active phase.

## Step 2 — Branch setup

Working tree must be clean (else stop). Branch `feat/<PHASE_ID>-<TASK_ID>-<slug>` off `main`
(follow `context/02-shared/git-conventions.md` — no `git add -A`, no `--no-verify`, no force-push).

## Step 3 — Load context (Tier A + the requirement + the task's feature)

1. `context/architecture-map.md`
2. `context/agent-rules.md`
3. `context/02-shared/anti-patterns.md`
4. `context/06-phase/<PHASE_ID>/requirement/<feature>/requirement.md` — the pure-business ACs to build
5. `context/05-features/<feature>/business-context.md`, `technical-context.md`, `test-context.md`
   — **only if the feature already exists** (built in an earlier phase). First time building this
   feature, this folder doesn't exist yet — you'll create it in Step 6 from the requirement.

Cross-feature reads: only the `## Public surface` section of another feature's
`technical-context.md` — never its full context.

## Step 4 — Implement AC by AC (test first)

For each AC the task delivers, in order:
1. **Write the test first** at the tier named in `test-context.md`. Confirm it fails for the right reason.
2. Write the **minimum** code to pass it. Stay in the files listed in `technical-context.md`'s
   "Code file mapping" (add a row first if a new file is needed). Follow `patterns.md`.
3. Re-run the test → green.
4. Commit one AC per commit: `feat(<feature>): AC<n> — <title>` with What/Why body.

## Step 5 — Verify no regressions

Run the feature's tests and `<lint-cmd>`. Fix any newly-red test before continuing.

## Step 6 — Write the `05-features/` spec (this is the only command that does)

- **First time building this feature** — create its spec folder from the template and settle the
  requirement into it:
  ```bash
  cp -R context/05-features/_template context/05-features/<feature>
  ```
  Author `business-context.md` from `requirement/<feature>/requirement.md` (Goal, user stories,
  business rules, the `### AC` headings) — the settled, as-built business record. **Copy each AC's
  id and text verbatim** from the requirement — never renumber or reword. Only bring across the ACs
  this task actually built; later tasks append theirs. The result must stay a **subset** of the
  feature's gathered requirement ACs (the parity hook enforces this). Register the feature in
  `05-features/INDEX.yml` (`status`, `ac_count`, `contract_version: 1`, `depends_on`).
- `technical-context.md`: flip completed capabilities to **Done** in the status table; update the
  "Code file mapping". **If the public interface changed**, edit the `## Public surface` section,
  bump `contract_version` (in `technical-context.md` frontmatter + `INDEX.yml`), and update every
  consumer's `depends_on` pin. This is the only place the contract moves.
- `test-context.md`: mark each delivered AC's row green in the "Coverage status" table.
- `05-features/INDEX.yml`: set `status: done` (or `in_progress`) for the feature; keep `ac_count`
  in sync with the `### AC` headings.
- The task file: flip AC rows to ✅, set `status: done`.
- `context/06-phase/<PHASE_ID>/phase.md`: flip the task row to ✅, bump `ac_green`. Mirror the
  `ac_green` bump into this phase's block in `context/06-phase/index.yml`.
- If a genuine architectural decision was made: add an ADR under `04-architecture/decisions/`
  (and its `INDEX.yml` block) — the ADR is the decision record.

## Step 7 — Push and open PR

Push the branch and open a PR summarising the task and its ACs (skip if one already exists).
Reference the delivered AC IDs in the body.

## Step 8 — Confirm

```
✅ Task <TASK_ID> complete — <title>   (feature <feature>, <n>/<n> ACs green)
Next: /implement-task "<PHASE_ID>" "<next-task-id>"
```

---

## Hard rules

- **Write the test before the implementation** — always. One commit per AC.
- **Never load another feature's full context** — only its `## Public surface` section.
- **Business intent comes from the requirement** — settle it into `business-context.md` as-built,
  copying AC ids/text verbatim; never invent new scope or renumber an AC here. A client-driven scope
  change is a new `/gather-requirement`.
- **Never mark a task done** unless every AC row is ✅ with a passing test.
- **Never `--no-verify`**; if the hook blocks, fix the underlying issue.
