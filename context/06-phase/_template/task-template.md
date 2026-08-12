---
spec_version: 1
title: "T<NN> — <Task Title>"
last_review: YYYY-MM-DD
file_type: task
type: phase-task
tags: [phase-<N>, task, <feature-slug>]
phase: <N>
task_id: T<NN>
feature: <feature-slug>
status: todo
ac_count: 0
---

# T<NN> — <Task Title>

## Description
<!-- 2–4 sentences. What this builds, why it's in this phase, what problem it solves. -->

## Goal
<!-- One sentence: the concrete end state. "User can do X." -->

## Acceptance Criteria
| AC | Title | Tier | Done? |
|---|---|---|---|
| AC1 | … | Unit | ⬜ |
| AC2 | … | Integration | ⬜ |

## Agent Instructions
### What to implement
1. …
2. …

### Files to read first
| File | Why |
|---|---|
| `context/05-features/<feature>/business-context.md` | ACs, BRs |
| `context/05-features/<feature>/technical-context.md` | current state |
| `context/04-architecture/patterns.md` | patterns to copy |

### Key files to create / modify
| Action | File |
|---|---|
| Create | `<source path>` |
| Update | `context/05-features/<feature>/technical-context.md` |

### Definition of done
- [ ] All ACs ✅
- [ ] Lint / analyze clean
- [ ] Tests pass
- [ ] `technical-context.md` updated
- [ ] Phase task row flipped to ✅
