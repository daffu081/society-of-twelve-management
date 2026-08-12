#!/usr/bin/env bash
# Stop hook — runs after every Claude response.
# Now does these checks:
#   1. Spec drift detection (original behavior: feature registration, AC parity, ADR registry)
#   2. Spec-to-code drift detection (source changed without spec update)
#   3. Spec freeze check — refuses to let frozen files change while .spec-frozen-at-* markers exist
#   4. Error-codes cross-check — .md and .yml symmetry
#   5. Frozen-file modification guard — rejects edits to frozen:true files
#   6. Requirement<->task<->spec parity (spec-parity.py) — drift, AC id collisions, coverage gaps
#
# Exits non-zero (2) on any drift, frozen violation, error-codes asymmetry, or parity failure.

set -euo pipefail

REPO="$(cd "$(dirname "$0")/../.." && pwd)"
FEATURES_DIR="$REPO/context/05-features"
IMPLEMENT_CMD="$REPO/.claude/commands/implement-task.md"
INDEX_YML="$REPO/context/05-features/INDEX.yml"
ADR_DIR="$REPO/context/04-architecture/decisions"
DRIFT_SCRIPT="$REPO/scripts/check-spec-drift.sh"
AUTO_UPDATE_SCRIPT="$REPO/scripts/auto-update-spec.sh"
DRIFT_STATE="$REPO/.claude/drift-state.json"

errors=()
add_error() { errors+=("$1"); }

# ---------------------------------------------------------------------------
# 1. Spec drift detection
# ---------------------------------------------------------------------------

features=()
while IFS= read -r feature; do
  features+=("$feature")
done < <(
  find "$FEATURES_DIR" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; \
    | grep -v '^_template$' \
    | sort
)

for name in "${features[@]}"; do
  # feature must appear in INDEX.yml
  if [ -f "$INDEX_YML" ] && ! grep -q "^  $name:" "$INDEX_YML" 2>/dev/null; then
    add_error "context/05-features/INDEX.yml is missing feature: $name"
  fi
done

if [ -f "$IMPLEMENT_CMD" ] && grep -q "Valid feature names: \`" "$IMPLEMENT_CMD" 2>/dev/null; then
  add_error ".claude/commands/implement-task.md hardcodes feature names; it must discover context/05-features dynamically"
fi

# AC count parity (per-feature business-context vs INDEX.yml)
if [ -f "$INDEX_YML" ]; then
  for name in "${features[@]}"; do
    bc="$FEATURES_DIR/$name/business-context.md"
    if [ -f "$bc" ]; then
      count="$(grep -c '^### AC[0-9]' "$bc" 2>/dev/null || true)"
      yml_count="$(grep -A 8 "^  $name:" "$INDEX_YML" | grep -Eo 'ac_count: [0-9]+' | head -n 1 | grep -Eo '[0-9]+' || true)"
      if [ -n "$yml_count" ] && [ "$yml_count" -ne "$count" ]; then
        add_error "INDEX.yml ac_count for $name=$yml_count but business-context has $count ACs"
      fi
    fi
  done
fi

# ADR registry consistency: every decisions/ADR-NNN.md must appear in decisions/INDEX.yml
if [ -d "$ADR_DIR" ] && [ -f "$ADR_DIR/INDEX.yml" ]; then
  while IFS= read -r adr_file; do
    base="$(basename "$adr_file" .md)"
    if ! grep -q "$base" "$ADR_DIR/INDEX.yml"; then
      add_error "04-architecture/decisions/INDEX.yml missing entry for: $base"
    fi
  done < <(find "$ADR_DIR" -maxdepth 1 -name 'ADR-[0-9]*.md' -type f)
fi

# Frontmatter validator — every file under context/ (except _template, decisions log) must have YAML frontmatter
missing_frontmatter=()
while IFS= read -r f; do
  head -1 "$f" | grep -q '^---$' || missing_frontmatter+=("$f")
done < <(
  find "$REPO/context" -type f -name '*.md' \
    -not -name 'README.md' \
    -not -path '*/_template/*' \
    -not -path '*/08-c4-diagram/*' \
    -not -path '*/03-business/*' \
    -not -path '*/05-features/*/business-context.md' \
    -not -path '*/05-features/*/technical-context.md' \
    -not -path '*/05-features/*/test-context.md' \
    -not -path '*/06-phase/*'
)
if [ ${#missing_frontmatter[@]} -gt 0 ]; then
  for f in "${missing_frontmatter[@]}"; do
    add_error "missing frontmatter: $f"
  done
fi

# ---------------------------------------------------------------------------
# 2. Spec-to-code drift detection + auto-update
#    Opt-in: inactive until you add context/.source-map.yml + scripts/check-spec-drift.sh.
#    The boilerplate ships neither, so this block is a no-op until you wire it up.
# ---------------------------------------------------------------------------

if [ -f "$DRIFT_SCRIPT" ] && [ -f "$REPO/context/.source-map.yml" ]; then
  if ! "$DRIFT_SCRIPT" 2>/dev/null; then
    # Drift detected — try mechanical auto-update first
    if [ -f "$AUTO_UPDATE_SCRIPT" ]; then
      if "$AUTO_UPDATE_SCRIPT" 2>/dev/null; then
        :  # Mechanical updates resolved all drift — silent success
      else
        # Drift remains after mechanical fixes — capture detailed state
        if [ -f "$DRIFT_STATE" ]; then
          add_error "spec-to-code drift remains (the 05-features spec is written by /implement-task; re-run it or reconcile):"
          while IFS= read -r line; do
            add_error "  $line"
          done < <("$DRIFT_SCRIPT" 2>&1 || true)
        fi
      fi
    else
      # No auto-update script — report raw drift
      drift_output="$("$DRIFT_SCRIPT" 2>&1 || true)"
      add_error "spec-to-code drift detected:\n$drift_output"
    fi
  else
    # No drift — clean up stale state file if present
    [ -f "$DRIFT_STATE" ] && rm -f "$DRIFT_STATE"
  fi
fi

# ---------------------------------------------------------------------------
# 3. Spec freeze guard — if .spec-frozen-at-* markers exist, the named feature's tier-A/B files
#    must not have changed since the SHA snapshot inside the marker
# ---------------------------------------------------------------------------

shopt -s nullglob
for marker in "$REPO"/.spec-frozen-at-*; do
  feature="$(basename "$marker" | sed 's/^.spec-frozen-at-//')"
  while IFS= read -r line; do
    path="${line%% *}"
    expected="${line##* }"
    if [ -f "$REPO/$path" ]; then
      actual="$(shasum -a 256 "$REPO/$path" | awk '{print $1}')"
      if [ "$actual" != "$expected" ]; then
        add_error "SPEC FREEZE VIOLATION ($feature): $path changed after /implement-task started. Either revert or run scripts/unfreeze.sh $feature."
      fi
    fi
  done < "$marker"
done
shopt -u nullglob

# ---------------------------------------------------------------------------
# 4. Error-codes cross-check — every code in error-codes.yml must appear in
#    error-codes.md and vice versa. The two files are kept in sync.
#    Opt-in: the boilerplate ships only error-codes.md, so this is a no-op
#    until you add a machine-readable error-codes.yml alongside it.
# ---------------------------------------------------------------------------

ERR_YML="$REPO/context/02-shared/error-codes.yml"
ERR_MD="$REPO/context/02-shared/error-codes.md"
if [ -f "$ERR_YML" ] && [ -f "$ERR_MD" ]; then
  yml_codes="$(awk '
    /^codes:/ { in_codes = 1; next }
    in_codes && /^  [A-Z][A-Z_]+:/ {
      sub(/:.*/, "")
      sub(/^[[:space:]]+/, "")
      print
    }
  ' "$ERR_YML" | sort -u)"
  md_codes="$(grep -Eo '`[A-Z][A-Z_]+`' "$ERR_MD" | tr -d '`' | sort -u)"

  missing_in_md="$(comm -23 <(echo "$yml_codes") <(echo "$md_codes") || true)"
  missing_in_yml="$(comm -13 <(echo "$yml_codes") <(echo "$md_codes") || true)"

  if [ -n "$missing_in_md" ]; then
    for c in $missing_in_md; do
      add_error "error-codes.yml has $c but error-codes.md does not"
    done
  fi
  if [ -n "$missing_in_yml" ]; then
    for c in $missing_in_yml; do
      add_error "error-codes.md has $c but error-codes.yml does not"
    done
  fi
fi

# ---------------------------------------------------------------------------
# 5. Frozen-file modification guard — any file whose frontmatter has
#    `frozen: true` AND whose mtime is newer than 5 minutes ago is an error.
#    To legitimately edit a frozen file, flip frontmatter to `frozen: false`
#    first (which itself is a deliberate, reviewable change).
# ---------------------------------------------------------------------------

while IFS= read -r f; do
  if head -20 "$f" 2>/dev/null | grep -qE '^frozen:[[:space:]]*true[[:space:]]*$'; then
    add_error "FROZEN FILE MODIFIED: $f — flip 'frozen: true' to 'frozen: false' first if the edit is intentional"
  fi
done < <(
  find "$REPO/context" "$REPO/.claude" "$REPO/scripts" -type f \( -name '*.md' -o -name '*.yml' -o -name '*.sh' \) -newermt '5 minutes ago' 2>/dev/null
)

# ---------------------------------------------------------------------------
# 6. Requirement <-> task <-> spec parity (see spec-parity.py):
#    requirement/spec drift, AC id collisions across phases, uncovered ACs.
# ---------------------------------------------------------------------------

PARITY="$(dirname "$0")/spec-parity.py"
if [ -f "$PARITY" ] && command -v python3 >/dev/null 2>&1; then
  while IFS= read -r line; do
    [ -z "$line" ] && continue
    case "$line" in
      *"[warn]"*) echo "advisory: ${line##*spec-parity\[warn\]: }" >&2 ;;  # coverage — non-fatal
      *)          add_error "${line#spec-parity: }" ;;                      # corruption — blocks
    esac
  done < <(python3 "$PARITY" 2>&1 1>/dev/null || true)
fi

# ---------------------------------------------------------------------------
# Exit
# ---------------------------------------------------------------------------

if [ ${#errors[@]} -gt 0 ]; then
  echo "Spec drift / freeze violation detected:" >&2
  for err in "${errors[@]}"; do
    printf ' - %b\n' "$err" >&2
  done
  exit 2
fi

exit 0
