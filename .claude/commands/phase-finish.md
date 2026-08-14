---
description: Seal a phase as permanently locked. Verifies all work is complete, stamps the phase file as a read-only historical record, and updates the roadmap index. Once locked, no new tasks can be added and no work can be started in that phase. Usage `/phase-finish phase-1`.
argument-hint: <phase-id>
---

You are locking a phase in the [PROJECT NAME] roadmap.

Arguments received: **$ARGUMENTS**

The phase folder lives at `context/06-phase/`. The index is `context/06-phase/README.md`.

---

## Step 1 — Parse and validate the phase ID

Extract the phase ID from `$ARGUMENTS` (e.g. `phase-1`, `phase-2`).

If no argument is given, stop and print:
```
Usage: /phase-finish <phase-id>
Example: /phase-finish phase-1
```

Check the phase file exists:
```bash
ls context/06-phase/$ARGUMENTS/phase.md 2>/dev/null && echo "exists" || echo "missing"
```

If the file does not exist, stop:
```
context/06-phase/<phase-id>/phase.md does not exist.
Use `ls context/06-phase/` to list valid phases.
```

---

## Step 2 — Read the phase file

Read only the frontmatter + feature table (first 40 lines is enough):
```bash
head -40 context/06-phase/<phase-id>/phase.md
```

Extract:
- `status` — current status from frontmatter
- `ac_total` and `ac_green` — AC counts
- The list of feature rows from the feature table

---

## Step 3 — Check if already locked

Read the `status` field from the frontmatter.

If `status: locked`, stop immediately:
```
🔒 Phase <phase-id> is already locked.
It was sealed on <locked_at date> and cannot be modified.
```

---

## Step 4 — Check readiness: are all tasks complete?

### Step 4a — Check phase table rows

Scan the feature table rows for any that still show `⬜ todo` or `🔄 partial`.

### Step 4b — Verify ACs are actually green (not just marked ✅)

**Check at TASK granularity, not feature granularity.** A phase task delivers only a *subset* of
its feature's ACs (e.g. task T05 builds payments AC3–AC5 while AC1–AC2 belong to a later phase), so
a feature can be legitimately `in_progress` in `INDEX.yml` while every task this phase committed to
is done. Checking the feature's overall `INDEX.yml` status here produces false "MISMATCH" alarms —
do **not** do that.

Instead, for each `✅`-marked row in the phase table, open the task file
`context/06-phase/<phase-id>/task-<Tnn>-*.md` and verify:
1. its frontmatter `status: done`, **and**
2. every AC row in its "Delivers these ACs" table is `✅`, **and**
3. each of those AC ids is marked green/built in that feature's
   `context/05-features/<feature>/test-context.md` coverage table (the authoritative as-built proof).

If a task file's `status` is not `done`, or any of its delivered ACs is not green in the feature's
test-context, treat that row as incomplete and flag it. (This is the settle-drift guard: a task row
marked ✅ in the phase table whose ACs were never settled green is exactly the bug this step exists
to catch.)

Print a summary (task-granular):
```
Task verification:
  T01 member-profile  → task: done, AC3–AC5 green ✅
  T05 payments        → task: done, AC3–AC5 green ✅
  T09 executive-admins→ task: in_progress ⚠️  (phase table shows ✅ — MISMATCH)
```

If all verified done:
→ Proceed to Step 4c.

**If all rows show ✅ done (and Step 4b confirms):**
→ Proceed to Step 4c.

### Step 4c — Prove it's actually green (locking is permanent — no self-reported ✅)

A locked phase is immutable history, so "marked done" is not enough. Run the real checks:

```bash
<test-cmd>                                   # the project's full test suite
bash .claude/hooks/check-spec-cache.sh       # parity / drift / contract checks
```

Two different kinds of result:

- **Corruption — hard stop, no override.** Failing tests, or `check-spec-cache.sh` exiting non-zero
  (requirement↔spec drift, AC-id collision, stale contract pin). Stop:
  `❌ Cannot lock <phase-id>: tests red / spec parity broken — fix, then re-run.` A phase that
  lies must never be sealed.
- **Coverage advisories — treat as unfinished work.** `check-spec-cache.sh` prints
  `advisory: coverage gap …` lines (gathered ACs with no task) but still exits 0. These are not
  corruption — they're scope you gathered but didn't build. Fold each into the incomplete-work list
  in Step 4 and require the same explicit `LOCK` confirmation to abandon them.

Only when tests pass and no corruption remains → proceed (via the Step-4 `LOCK` gate if any
coverage advisories or incomplete tasks remain) to Step 5.

**If any rows show ⬜ todo or 🔄 partial:**
→ Print a warning listing the incomplete items:

```
⚠️  The following tasks are not yet complete:

  ⬜  security      (15 ACs — not started)
  ⬜  sync          (16 ACs — not started)
  ⬜  bugfix: dashboard empty-state CTA

Locking a phase with unfinished work means those tasks are
permanently abandoned — they will NOT carry over to the next phase.

To carry them forward instead:
  1. Create the next phase with /create-phase, then add tasks with /create-task
  2. Then run /phase-finish <phase-id> again

Type LOCK to confirm you want to seal this phase anyway, or anything else to cancel.
```

Wait for the user's reply.
- If the user types `LOCK` (case-insensitive): proceed to Step 5.
- Otherwise: stop with `Cancelled — phase remains unlocked.`

---

## Step 5 — Write the lock to the phase file

Make the following edits to `context/06-phase/<phase-id>/phase.md`:

### 5a — Update frontmatter

Change:
```yaml
status: <old_status>
started_at: <value>
```
To:
```yaml
status: locked
locked_at: <today's date YYYY-MM-DD>
```

### 5b — Replace the status banner

Find the line:
```
> **Status: <anything> — <N> / <M> ACs green**
```
Replace it with:
```
> 🔒 **LOCKED — sealed on <today's date YYYY-MM-DD>**
> This phase is a permanent historical record. No further changes are allowed.
```

### 5c — Add a lock notice block at the top of the file (after frontmatter, before the title)

Insert this block immediately after the `---` closing of the frontmatter:

```markdown
> [!NOTE]
> **This phase is locked.** It was sealed on <today's date YYYY-MM-DD> and serves as a read-only historical record.
> To continue work, see the next phase or run ``ls context/06-phase/``.
```

### 5d — Append a final entry to the Completion log

Find the `## Completion log` section and append a new row:

```
| <today's date> | 🔒 Phase locked | — | Sealed by /phase-finish. No further changes allowed. |
```

---

## Step 6 — Update `context/06-phase/README.md`

Find the row for this phase in the phase overview table and update its Status column:

Change:
```
| ✅ **COMPLETE** (<N> / <M>) |   or   | ⬜ **NOT STARTED** ...  |   or   | 🔄 **IN PROGRESS** ...  |
```
To:
```
| 🔒 **LOCKED** (<N> / <M>) |
```

---

## Step 6b — Clear the active-phase pointer

Edit `context/06-phase/ACTIVE.md`. Replace the active-phase table row with the
"none" row so no phase is active until a new one is created:

```
| _none_ | — | — |
```

Also update `context/06-phase/index.yml`: set this phase's `status: locked` and `active: null`.

This is what enforces "one phase at a time": with no active phase, `/create-phase`
is now free to start the next one.

---

## Step 7 — Print confirmation

```
🔒 Phase <phase-id> is now LOCKED.

  Sealed on: <today's date>
  Features:  <count> features / tasks
  ACs:       <ac_green> / <ac_total> green

This phase is now a permanent historical record.
No new tasks can be added and no work can be started in this phase.

Next: `ls context/06-phase/`   — see what's open in other phases
```

---

## Hard rules

- NEVER unlock a phase. There is no `/phaseunlock` command. Locked means permanently locked.
- NEVER lock a phase whose tests are red or whose parity/contract checks fail (corruption) — hard
  stops, no override (Step 4c). Coverage advisories and incomplete-but-passing tasks CAN be
  abandoned, but only via explicit `LOCK` confirmation.
- NEVER delete any ✅ rows when locking.
- NEVER edit the Completion log except to append the final lock entry.
- If any incomplete tasks exist, always warn the user and require explicit `LOCK` confirmation before sealing.
- Only edit `context/06-phase/<phase-id>/phase.md`, `context/06-phase/README.md`, and `context/06-phase/ACTIVE.md` — nothing else.
- Always clear `ACTIVE.md` to `_none_` when locking — a stale active pointer would block the next phase from starting.
