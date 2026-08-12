---
description: Create a Jira-style task ticket inside a phase folder, deriving its scope from a gathered requirement. Usage `/create-task "phase-3" "Add dark mode toggle to settings"`.
argument-hint: "<phase-id>" "<what to do>"
---

You are creating a task ticket for the [PROJECT NAME] phase roadmap. Arguments: **$ARGUMENTS**

A task points at work that has **already been gathered as a requirement** — in the phase's
`requirement/<feature>/requirement.md`. It does not invent scope — if the feature or its ACs
haven't been gathered yet, tell the user to run `/gather-requirement` first.

---

## Step 0 — Parse arguments

- **PHASE_ID** — first quoted token (e.g. `phase-3`).
- **DESCRIPTION** — the rest, unquoted.

Missing either → print usage and stop.

## Step 1 — Validate the phase

```bash
ls context/06-phase/<PHASE_ID>/ 2>/dev/null || echo "MISSING"
```
- No folder → `❌ <PHASE_ID> does not exist. Create it: /create-phase <PHASE_ID> "Title"`.
- If the phase's `phase.md` frontmatter is `status: locked` → stop, it can't accept tasks.

## Step 2 — Next task ID

Count `context/06-phase/<PHASE_ID>/task-T*.md`; next id = count+1, zero-padded (`T01`, `T02`…).

## Step 3 — Bind the task to a gathered requirement

Match DESCRIPTION to one feature the requirement was gathered under, in this phase:
```bash
ls -1 context/06-phase/<PHASE_ID>/requirement/ 2>/dev/null
```
- Pick the best match. Shared work that isn't one feature (auth, logging, migrations) belongs to
  the reserved `_cross-cutting` feature — which must still be **gathered** first, like any other.
  There is no un-gathered task bucket; if the ACs aren't in a requirement, stop.
- Read that feature's `requirement/<feature>/requirement.md` and pull the **exact AC IDs** this task
  will deliver (reference them verbatim — `AC3`, not a fresh number). If the requirement or the ACs
  it needs don't exist yet, stop: `❌ That isn't gathered yet — run /gather-requirement first.`
- Every gathered AC must end up in some task. The parity hook flags any requirement AC in the
  active phase with no task — so split the requirement so nothing is left uncovered.

## Step 4 — Write the task file

Create `context/06-phase/<PHASE_ID>/task-<TASK_ID>-<slug>.md` (slug = kebab-case of DESCRIPTION, ≤40 chars):

```markdown
---
spec_version: 1
file_type: task
phase: <N>
task_id: <TASK_ID>
feature: <feature>
status: todo
---

# <TASK_ID> — <Title>

## Description
<2–3 sentences: what is being built and why it belongs in this phase.>

## Delivers these ACs
<Pull from the phase's requirement/<feature>/requirement.md — reference by ID, don't restate rules.>
| AC | Title | Done? |
|----|-------|-------|
| AC1 | <title from requirement> | ⬜ |
| AC2 | <title from requirement> | ⬜ |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/<PHASE_ID>/requirement/<feature>/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/<feature>/technical-context.md` | current state, public surface, file mapping — **only if the feature already exists from earlier work** |
| `context/05-features/<feature>/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] `<lint-cmd>` clean, `<test-cmd>` green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
```

## Step 5 — Register in the phase

In `context/06-phase/<PHASE_ID>/phase.md`, append a row to the Feature table and bump `ac_total`
in frontmatter by this task's AC count. Update the `**Total: N ACs**` line. Mirror the same
`ac_total` bump into this phase's block in `context/06-phase/index.yml`.

## Step 6 — Confirm

```
✅ Created task <TASK_ID> — <Title>  (phase <PHASE_ID>, feature <feature>, <n> ACs)

Implement it:  /implement-task "<PHASE_ID>" "<TASK_ID>"
```

---

## Hard rules

- Never create a task in a locked phase.
- Never invent scope — a task only references ACs that already exist in the phase's `requirement/`.
- This command only writes under `context/06-phase/` — never touches `context/05-features/`.
- Task file name is always `task-<TASK_ID>-<slug>.md`; ids are `T01`, `T02`, … zero-padded.
