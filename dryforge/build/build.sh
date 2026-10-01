#!/usr/bin/env bash
# build.sh — regenerate every platform package from the canonical skill source.
#
#   src/skills/        canonical, platform-neutral skills (single source of truth)
#   platform/claude/   claude-only frontmatter values + plugin.json + LICENSE
#   README.md          repo-root README (+ README_{ko,zh,ja}.md) — GitHub landing only, NOT bundled into plugins
#   claude/            generated Claude plugin   (committed; Claude installs this)
#
# WorkforMe fork: only the Claude package is built (the Codex / Grok / Agent Plugin /
# Antigravity targets were removed — see CHANGES.md CH-01 at the WorkforMe repo root).
#
# Root marketplace manifests are committed repo files, not build outputs.
#
# Build-time guards:
#   ① shared references byte-identical (5 pairs; the classification pairs are WorkforMe CH-07)
#   ② frontmatter injection post-verified (a silent perl no-op must not ship)
#   ③ skill list discovered dynamically from src/skills/*/ (a 4th skill without
#     its claude_tools mapping fails the build)
#   ④ all plugin.json versions non-empty + identical + match CHANGELOG top

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/src/skills"
PLAT="$ROOT/platform"
BUILD_TMP="$(mktemp -d "$ROOT/.build.XXXXXX")"
OUT="$BUILD_TMP/output"
mkdir -p "$OUT"
trap 'rm -rf "$BUILD_TMP"' EXIT

# ── guard ①: shared references byte-identical (pair list = the contract) ────
for pair in \
  "migration/references/harness-format.md:go/references/harness-format.md" \
  "migration/references/harness-review.md:go/references/harness-review.md" \
  "ready/references/foundation-format.md:go/references/foundation-format.md" \
  "ready/references/classification.md:go/references/classification.md" \
  "ready/references/classification.md:migration/references/classification.md"; do
  a="$SRC/${pair%%:*}"; b="$SRC/${pair##*:}"
  if ! diff -q "$a" "$b" >/dev/null 2>&1; then
    echo "FAILED: shared reference drift: ${pair%%:*} != ${pair##*:}" >&2
    diff "$a" "$b" >&2 || true
    exit 1
  fi
done
echo "✓ shared references byte-identical (5 pairs)"

# ── guard ③: skills discovered dynamically from src ─────────────────────────
SKILLS=""
for d in "$SRC"/*/; do [ -d "$d" ] && SKILLS="$SKILLS $(basename "$d")"; done
[ -n "$SKILLS" ] || { echo "FAILED: src/skills is empty" >&2; exit 1; }

# Per-skill allowed-tools for the Claude build. All three add Agent: ready dispatches the
# intent-completeness + 3-doc-gate subagents, go dispatches implementers/reviewers, and migration
# dispatches the final independent harness REVIEW subagent. bash 3.2 — no assoc arrays.
claude_tools() {
  case "$1" in
    migration|ready|go) echo "Read, Edit, Write, Bash, Grep, Glob, Agent, AskUserQuestion" ;;
  esac
}

# ── Claude → ./claude ───────────────────────────────────────────────────────
echo "=== build: claude ==="
mkdir -p "$OUT/claude/.claude-plugin"
cp -R "$SRC" "$OUT/claude/skills"
for s in $SKILLS; do
  TOOLS="$(claude_tools "$s")"
  [ -n "$TOOLS" ] || { echo "FAILED: missing Claude tool mapping for skill: $s" >&2; exit 1; }
  INJECT=$'disable-model-invocation: true\nallowed-tools: '"$TOOLS" \
    perl -0777 -i -pe 'BEGIN{$j=$ENV{INJECT}} s/\A(---\n.*?\n)---\n/$1$j\n---\n/s' \
    "$OUT/claude/skills/$s/SKILL.md"
done
# guard ②: assert the injection actually landed (perl substitution can no-op silently)
for s in $SKILLS; do
  f="$OUT/claude/skills/$s/SKILL.md"
  if [ "$(grep -c '^disable-model-invocation: true$' "$f")" -ne 1 ] || [ "$(grep -c '^allowed-tools: ' "$f")" -ne 1 ]; then
    echo "FAILED: Claude frontmatter injection failed for skill: $s" >&2
    exit 1
  fi
done
cp "$PLAT/claude/plugin.json" "$OUT/claude/.claude-plugin/plugin.json"
cp "$PLAT/claude/LICENSE" "$OUT/claude/"

find "$OUT/claude" -name ".DS_Store" -delete 2>/dev/null || true

# ── guard ④: version consistency ────────────────────────────────────────────
# Both plugin.json (platform input + generated) carry the same non-empty
# version AND it matches the CHANGELOG top entry. Catches manual-edit skew at build time instead of leaving it for a
# human (or another agent) to spot. Release tags are validated separately so
# the build remains independent of Git state.
pj_ver() { perl -ne 'if(/"version"\s*:\s*"([^"]+)"/){print $1; last}' "$1"; }
VERS=""
for pj in "$PLAT/claude/plugin.json" "$OUT/claude/.claude-plugin/plugin.json"; do
  v="$(pj_ver "$pj")"
  [ -n "$v" ] || { echo "FAILED: empty version: $pj" >&2; exit 1; }
  VERS="$VERS$v"$'\n'
done
UNIQ="$(printf '%s' "$VERS" | sort -u)"
if [ "$(printf '%s\n' "$UNIQ" | grep -c .)" -ne 1 ]; then
  echo "✗ version mismatch across plugin.json:" >&2
  printf '%s' "$VERS" >&2
  exit 1
fi
CL_VER="$(perl -ne 'if(/^##\s+v([0-9][^\s(]*)/){print $1; last}' "$ROOT/CHANGELOG.md")"
if [ "$UNIQ" != "$CL_VER" ]; then
  echo "✗ plugin.json=v$UNIQ but CHANGELOG top=v$CL_VER" >&2
  exit 1
fi
echo "✓ version OK: v$UNIQ (2 manifests + CHANGELOG)"

# Publish only after every generated package and guard has succeeded. The existing output is
# retained inside BUILD_TMP until the swap completes, so a failed move can be rolled back.
# (WorkforMe fork: one target, so the upstream per-target loops are a single swap — CH-01.)
BACKUP="$BUILD_TMP/previous"
mkdir -p "$BACKUP"
HAD_OLD=""
if [ -e "$ROOT/claude" ]; then
  if ! mv "$ROOT/claude" "$BACKUP/claude"; then
    echo "FAILED: could not stage existing output: claude" >&2
    exit 1
  fi
  HAD_OLD=1
fi
if ! mv "$OUT/claude" "$ROOT/claude"; then
  if [ -n "$HAD_OLD" ]; then
    mv "$BACKUP/claude" "$ROOT/claude"
  fi
  echo "FAILED: could not publish generated output: claude" >&2
  exit 1
fi

echo "=== done → ./claude ==="
