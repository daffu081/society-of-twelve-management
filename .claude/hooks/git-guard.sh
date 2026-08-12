#!/usr/bin/env bash
# PreToolUse(Bash) hook — hard-enforces context/02-shared/git-conventions.md.
# Blocks the deterministic "NEVER" rules so the agent cannot skip them, no matter
# what an earlier instruction said. Exit 2 = block the tool call; the stderr
# message is fed back to the agent so it can correct itself.
#
# The confirmation gates (§5: "ask before commit/PR/merge") are NOT enforced here
# — a hook can't tell whether the agent asked. Those stay in settings.json
# custom_instructions. This hook covers the rules that ARE machine-checkable.
#
# Self-test: bash git-guard.sh --selftest

set -euo pipefail

selftest() {
  local pass=0 fail=0
  check() { # <expected: block|allow> <branch> <command>
    local want="$1" branch="$2" cmd="$3" got
    got="$(GIT_GUARD_BRANCH_OVERRIDE="$branch" run_checks "$cmd" && echo allow || echo block)"
    if [ "$got" = "$want" ]; then pass=$((pass+1)); else
      fail=$((fail+1)); echo "FAIL: want=$want got=$got  [$branch] $cmd" >&2
    fi
  }
  check block  feature/x "git commit --no-verify -m x"
  check block  feature/x "git add -A"
  check block  feature/x "git add ."
  check block  feature/x "git add --all"
  check block  main      "git commit -m x"
  check block  master    "git push"
  check block  develop   "git commit -m x"
  check block  feature/x "git push --force origin feature/x"
  check block  feature/x "git push -f"
  check allow  feature/x "git push --force-with-lease origin feature/x"
  check allow  feature/x "git commit -m x"
  check allow  feature/x "git add src/foo.py src/bar.py"
  check allow  main      "git status"
  check allow  feature/x "npm test"
  echo "git-guard selftest: $pass passed, $fail failed" >&2
  [ "$fail" -eq 0 ]
}

# Pure check logic (no stdin) so the selftest can drive it.
# Returns 0 = allow, 2 = block (with reason on stderr).
run_checks() {
  local cmd="$1"
  case "$cmd" in *git*) ;; *) return 0 ;; esac

  block() { echo "BLOCKED by git-conventions.md — $1" >&2; return 2; }

  # §6 — never bypass hooks
  printf '%s' "$cmd" | grep -qE -- '--no-verify' \
    && { block "never use --no-verify (§6)."; return 2; }

  # implement.md — never blanket-stage; stage named files only
  printf '%s' "$cmd" | grep -qE 'git add ([[:space:]]*)(-A|--all|\.)([[:space:]]|$)' \
    && { block "never 'git add -A/--all/.' — stage the specific files you changed."; return 2; }

  # §6 — never commit/push directly to a protected branch
  local branch="${GIT_GUARD_BRANCH_OVERRIDE-}"
  [ -z "$branch" ] && branch="$(git branch --show-current 2>/dev/null || true)"
  case "$branch" in
    main|master|develop)
      printf '%s' "$cmd" | grep -qE 'git[[:space:]]+(commit|push)' \
        && { block "never commit/push directly to '$branch' — create a feature branch first (§6)."; return 2; }
      ;;
  esac

  # §6 — never force-push (allow the safe --force-with-lease)
  if printf '%s' "$cmd" | grep -qE 'git[[:space:]]+push' \
     && printf '%s' "$cmd" | grep -qE -- '(--force([[:space:]]|$)|[[:space:]]-f([[:space:]]|$))' \
     && ! printf '%s' "$cmd" | grep -qE -- '--force-with-lease'; then
    block "never force-push — use --force-with-lease on your own branch if you truly must (§6)."
    return 2
  fi

  return 0
}

[ "${1-}" = "--selftest" ] && { selftest; exit $?; }

# Normal PreToolUse invocation: command arrives as JSON on stdin.
input="$(cat)"
cmd="$(printf '%s' "$input" | { python3 -c 'import sys,json;print(json.load(sys.stdin).get("tool_input",{}).get("command",""))' 2>/dev/null || jq -r '.tool_input.command // empty' 2>/dev/null; } || true)"

run_checks "$cmd"
exit $?
