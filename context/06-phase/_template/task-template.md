---
spec_version: 1
file_type: task
phase: <N>
task_id: T<NN>
feature: <feature-slug>
status: todo
---

# T<NN> — <Task Title>

## Description
<!-- 3–5 sentences. What this builds, which spec section it satisfies, why it's in this phase,
     what it depends on and what depends on it. Give enough context to start without re-reading the spec. -->

## Delivers these ACs
<!-- Pull from requirement/<feature>/requirement.md — reference by ID, don't restate rules. -->
| AC | Title | Done? |
|----|-------|-------|
| AC1 | <title from requirement> | ⬜ |

## Implementation approach
<!-- Ordered steps: how to build it. Data layer → server/auth → admin UI → public/member UI → automation.
     Business-aware but not a full design; /implement-task fills in specifics. -->
1. …
2. …

## Files to create / modify
<!-- Best-known target files. Action = Create | Update. /implement-task may adjust. -->
| Action | File | Why |
|--------|------|-----|
| Create | `<path>` | <what goes here> |
| Update | `<path>` | <what changes> |

## Files to read first
| File | Why |
|------|-----|
| `context/06-phase/<PHASE>/requirement/<feature>/requirement.md` | the ACs (pure business) this task delivers |
| `context/05-features/<feature>/technical-context.md` | current state, public surface, file mapping — only if it already exists |
| `context/05-features/<feature>/test-context.md` | coverage table — only if it already exists |
| `context/04-architecture/patterns.md` | patterns to follow |

## Definition of done
- [ ] Every AC above is ✅ with a passing test
- [ ] lint clean, tests green
- [ ] `technical-context.md` + `test-context.md` updated (done by `/implement-task`)
- [ ] This task's `status: done`; phase row flipped to ✅
