---
description: Create a new phase and make it the single active phase. Usage `/create-phase phase-3 "Phase 3: Charts"`. One phase is active at a time — finish the current one with `/phase-finish` first.
argument-hint: <phase-id> ["Phase Title"]
---

You are creating a new phase in the [PROJECT NAME] roadmap. Arguments: **$ARGUMENTS**

The phase folder lives at `context/06-phase/`. The index is `context/06-phase/README.md`.

---

## Step 1 — Refuse if a phase is already active

```bash
cat context/06-phase/ACTIVE.md
```
If `ACTIVE.md` names a live phase (not `_none_`), **stop**:
```
❌ <active-phase> is still active. Finish it first: /phase-finish <active-phase>
```
Only one phase may be active at a time.

## Step 2 — Determine the phase number and title

- Parse `phase-N` from the first argument. If none given, auto-detect the highest existing
  `context/06-phase/phase-*` and use N+1.
- If `phase-N/` already exists, stop and say so.
- Title: use the quoted title if given, else prompt "What should Phase N be called?"

## Step 3 — Write the phase file

Create `context/06-phase/phase-N/phase.md`:

```markdown
---
title: "Phase N — <Title>"
status: not_started
started_at: null
ac_total: 0
ac_green: 0
---

# Phase N — <Title>

> **Status: ⬜ NOT STARTED — 0 / 0 ACs green**

## What this phase delivers

_Describe what the app can do after this phase is complete that it can't do before._

---

## Feature table

| # | Feature | ACs | Status | What it does | Spec |
|---|---------|-----|--------|--------------|------|
| — | _No tasks added yet_ | — | — | — | — |

**Total: 0 ACs**

---

## Completion log

_Filled in as tasks complete. Never edit existing entries._

| Date | Task | ACs | Notes |
|------|------|-----|-------|
| — | — | — | Phase N not yet started |
```

Also create the phase's requirement folder — where `/gather-requirement` writes the client's
pure-business asks, feature by feature:

```bash
mkdir -p context/06-phase/phase-N/requirement
```

## Step 4 — Make it the active phase and register it

- Edit `context/06-phase/ACTIVE.md` — replace the `_none_` row with:
  `| **phase-N** | `context/06-phase/phase-N/` | <today's date> |`
- Append a row to the Phase overview table in `context/06-phase/README.md`:
  `| [Phase N](phase-N/phase.md) | <Title> | ⬜ **NOT STARTED** (0 / 0) | 0 | _TBD_ |`
- Update `context/06-phase/index.yml` (the machine registry): set `active: phase-N` and append
  ```yaml
    phase-N:
      title: "Phase N — <Title>"
      status: not_started
      ac_total: 0
      ac_green: 0
  ```

## Step 5 — Confirm

```
✅ Created context/06-phase/phase-N/ — "<Title>" (now the active phase)

Next: gather the client's asks  →  /gather-requirement "<what the client wants>"
      then split into tasks       →  /create-task "phase-N" "<what to do>"
```

---

## Hard rules

- Never create a phase while another is active — `/phase-finish` the current one first.
- Never skip a phase number.
- This command only touches `context/06-phase/` — never `context/05-features/`.
