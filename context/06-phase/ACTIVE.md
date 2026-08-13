---
type: active-phase-pointer
title: "Active Phase"
last_review: 2026-08-13
---

# Active phase

> **There is exactly one active phase at a time.** This file names it. It is the ONLY phase
> folder an agent may load. Every other phase is either locked (finished, read-only) or not
> yet started. Never load them.

| Active phase | Folder | Started |
|---|---|---|
| **phase-02** | `context/06-phase/phase-02/` | 2026-08-13 |

## The rule for agents
1. Read this file to learn the active phase.
2. Load only that phase's `phase.md` (and the specific `task-T*.md` you were told to work on).
3. Never open a locked phase folder.
4. Idea outside the active phase? Add it to [BACKLOG.md](BACKLOG.md) and move on.

## The invariant
- Only one phase active. A new phase can't start until the current one is sealed.
