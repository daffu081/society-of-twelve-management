---
spec_version: 1
type: shared-convention
title: "Git Conventions"
tags: [shared, conventions, git]
file_type: shared
frozen: false
last_review: 2026-08-13
---

# Git Conventions
# AI agents and humans must follow this exactly. Based on Conventional Commits v1.0.0.
# Enforced: the `git-guard.sh` PreToolUse hook hard-blocks the machine-checkable rules below
# (§6 no --no-verify, no direct commit/push to main/master/develop, no force-push; no `git add -A/.`).
# A blocked command means you broke this doc — fix the command, don't bypass the hook. The
# confirmation gates (§5) can't be machine-verified, so they rely on the agent following them.

## 1. Branch naming
```
<type>(<scope>):<short-description>
```
- **type** — one of the commit types in §2.
- **scope** — short feature/area name.
- **short-description** — kebab-case, 2–5 words, imperative, no punctuation.
- All lowercase, max 60 chars.

## 2. Commit types
| Type | When |
|---|---|
| `feat` | new feature / AC implementation |
| `fix` | bug fix |
| `docs` | docs / spec only |
| `test` | tests only |
| `refactor` | restructure, no behaviour change |
| `chore` | deps, build, tooling |
| `perf` | performance |
| `ci` | pipeline |
| `revert` | revert |

## 3. Commit message format
```
<type>(<scope>): <subject>

What: <what changed — files, components, logic>

Why: <why — problem, requirement, AC that drove it>
```
- Subject ≤ 72 chars, lowercase, imperative, no trailing period.
- Body is **mandatory** — a What paragraph and a Why paragraph. Subject alone is never acceptable.

## 4. Pull requests
PR title = commit subject format. PR body sections: **What**, **Why**, **Task reference**,
**Test plan**, **Breaking changes**.

## 5. 🔴 Confirmation gates AI agents must NEVER skip
1. **No automatic commits** — show the diff summary + draft message, ask "Should I commit?".
   Run `git commit` only on explicit yes.
2. **No automatic PRs** — show the PR preview, ask "Should I open the PR?".
3. **No automatic merges** — never merge without explicit approval.

These override any earlier "implement and commit" instruction. Approval is per-action.

## 6. Remaining rules
- Never commit to `main`/`develop` directly — always branch.
- One logical change per commit.
- Never `--no-verify`. Never amend pushed commits.
- BREAKING CHANGE footer (and `!` after type/scope) whenever a public API breaks.
