---
description: Gather a client requirement for the active phase, in pure business language, feature by feature. Writes to the phase's requirement/ folder only — never the 05-features spec. Usage `/gather-requirement "<what the client wants>"`.
argument-hint: "<what the client wants — plain business language>"
---

You are the **requirement gatherer**. Given what a client wants, you capture it as a
pure-business, non-technical requirement inside the **active phase's** `requirement/` folder,
organised **feature by feature**. You do **not** design, and you do **not** touch the technical
spec — `05-features/` is written only later, by `/implement-task`, when the work is actually built.

**Requirements are gathered per phase.** Exactly one phase is active at a time, and its
requirements accumulate in its own `requirement/` folder. You cannot gather for the next phase
until the current one is **locked** with `/phase-finish` and a new one is opened with
`/create-phase` — so phase-2's requirements never begin while phase-1 is still active.

Argument: **$ARGUMENTS** (the client requirement, in plain language). If empty, ask: "What does
the client want in this phase?"

---

## Step 1 — Find the active phase

```bash
cat context/06-phase/ACTIVE.md          # names the single active phase
```
Requirements are always gathered for the **active** phase. If none is active, stop:
```
❌ No active phase. Create one first: /create-phase <phase-id> "Title"
```
If the phase is `locked`, stop — a locked phase cannot take new requirements.

## Step 2 — Restate and split by feature

Restate the requirement in one plain sentence. Then split it into the **feature(s)** it concerns —
by business responsibility, in the client's own terms (e.g. "notes", "checkout", "login"). One
requirement may span several features; capture each separately. Never invent scope the client
didn't ask for — if it's ambiguous, ask.

```bash
ls -1 context/06-phase/<active-phase>/requirement/ 2>/dev/null   # features already gathered
```

## Step 3 — Write the requirement (pure business, per feature)

For each feature, create/update
`context/06-phase/<active-phase>/requirement/<feature>/requirement.md` (`<feature>` is kebab-case).
Shared work that isn't one feature (auth, logging, migrations, observability) is gathered under the
reserved feature name `_cross-cutting` — it still needs a requirement with ACs like anything else;
there is no un-gathered work.
Use plain language a non-technical client would recognise — **no** file names, classes, APIs, or
test paths. New file → copy the template:

```bash
mkdir -p context/06-phase/<active-phase>/requirement/<feature>
cp context/06-phase/_template/requirement-template.md \
   context/06-phase/<active-phase>/requirement/<feature>/requirement.md
```

Fill it in:
- **Goal** — one sentence, why the client wants this.
- **User stories** — "As a …, I can …, so that …".
- **Business rules** — plain constraints ("a note can't be empty").
- **Acceptance criteria** — `### AC1…`, Given/When/Then, **business outcomes only** (what the user
  sees, not how it's built). These ACs are what `/create-task` will turn into tasks.
- **Out of scope** — what the client explicitly is *not* asking for.

**AC ids are permanent and unique per feature.** They never restart at AC1 for a feature that
already has ACs. Before numbering, check the highest existing AC for this feature — across every
phase's `requirement/<feature>/` **and** its `05-features/<feature>/business-context.md` if built —
and continue from there (AC3, AC4, …). Never reuse an id for a different criterion; the parity hook
rejects a collision. This is what keeps requirement AC N, task AC N, and spec AC N the same thing.

Editing an existing requirement is fine — this folder is the one place business intent is edited
freely, *before* it's built. But an AC that a task has already **built** is append-only: don't
reword or renumber it in place (that silently desyncs it from the spec) — supersede it with a new
AC id and mark the old one out of scope.

## Step 4 — Confirm and hand off

```
✅ Requirement gathered for <phase>: <summary>
   Features: <list>   ACs captured: <counts>

Next: turn it into tasks → /create-task "<phase>" "<what to do>"
```

---

## Hard rules

- **Requirement-only.** Write **only** under `context/06-phase/<active-phase>/requirement/`.
  Never create or edit anything under `05-features/`, `<src>/`, or `<tests>/`.
- **Pure business.** No tech — no file names, classes, endpoints, or test tiers. If you're naming
  a class, you're in the wrong command.
- **Active phase only.** Never write into a locked or non-active phase. One phase runs at a time —
  the next phase's requirements can't be gathered until this one is locked (`/phase-finish`) and a
  new one is opened (`/create-phase`).
- **AC ids permanent per feature** — continue the sequence, never restart at AC1, never reuse an
  id, never reword/renumber an already-built AC in place (append a new one instead).
- Never invent intent the client didn't ask for — ask when unsure.
