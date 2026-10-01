#!/usr/bin/env bash
# dispose-project.sh — 회사 프로젝트 하나를 이 기기에서 지운다 (소각).
#
# 지우는 것:
#   1. projects/<이름>/              문서·원자료·자료 카드·git 기록 전체
#   2. Claude Code 대화 기록         ~/.claude/projects/ 안의 그 폴더 기록
#   3. 그 대화의 세션 데이터          file-history, session-env, tasks, todos, debug 안의 같은 세션 ID
#   4. 그 폴더의 임시 작업 폴더       ${TMPDIR:-/tmp}/claude-*/<그 폴더>
#
# 지우지 못하는 것 (직접 확인):
#   - Anthropic 서버에 남은 대화 (계정의 개인정보 설정과 보관 기간을 따름)
#   - 백업·동기화 사본 (OneDrive, iCloud, Time Machine, 회사 백업 등)
#   - WorkforMe 루트에서 연 대화 (회사 이야기가 섞였을 수 있음 — 목록만 보여 줌)
#
# 사용법:
#   scripts/dispose-project.sh <프로젝트-이름>            지울 목록만 보여 줌 (아무것도 지우지 않음)
#   scripts/dispose-project.sh <프로젝트-이름> --delete   목록을 보여 주고, 이름을 다시 입력하면 지움
#
# 지우기 전에 그 프로젝트를 연 Claude Code 창을 모두 닫으세요. 열려 있으면 기록을 다시 씁니다.
set -euo pipefail

usage() {
  sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'
  exit "${1:-0}"
}

[ "$#" -ge 1 ] || usage 1
case "$1" in -h|--help) usage 0 ;; esac
NAME="$1"
MODE="${2:-}"
case "$MODE" in ""|--delete) ;; *) echo "알 수 없는 옵션: $MODE" >&2; usage 1 ;; esac

# 이름 검사: 폴더 이름 하나만 받는다 (경로·숨김·README 금지)
case "$NAME" in
  ""|.|..|*/*|*\\*|.*|README.md)
    echo "프로젝트 이름이 올바르지 않아요: '$NAME' (projects/ 안의 폴더 이름 하나만 쓰세요)" >&2
    exit 1 ;;
esac

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECTS="$ROOT/projects"
PROJECT="$PROJECTS/$NAME"
if [ ! -d "$PROJECT" ]; then
  echo "프로젝트 폴더가 없어요: $PROJECT" >&2
  echo "있는 프로젝트:" >&2
  for d in "$PROJECTS"/*/; do [ -d "$d" ] && echo "  $(basename "$d")" >&2; done
  exit 1
fi

CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

# Claude Code가 폴더 경로를 기록 폴더 이름으로 바꾸는 방식:
# 절대 경로의 영문·숫자가 아닌 글자를 모두 '-'로 바꾼다.
# Windows(Git Bash)에서는 C:/Users/... 형태의 경로를 쓴다.
native_path() {
  if command -v cygpath >/dev/null 2>&1; then cygpath -m "$1"; else printf '%s' "$1"; fi
}
encode() { printf '%s' "$1" | sed 's/[^A-Za-z0-9]/-/g'; }

ENC_PROJECT="$(encode "$(native_path "$PROJECT")")"
ENC_ROOT="$(encode "$(native_path "$ROOT")")"

# 이름이 이 프로젝트로 시작하는 다른 프로젝트(예: A 와 A-b)의 기록은 빼기 위한 목록
OTHER_PREFIXES=()
while IFS= read -r other; do
  [ "$other" = "$PROJECT" ] && continue
  enc_other="$(encode "$(native_path "$other")")"
  if [ "$enc_other" = "$ENC_PROJECT" ]; then
    # 영문·숫자가 아닌 글자(한글 등)는 모두 '-'가 되어, 두 프로젝트의 기록을 구분할 수 없음
    echo "'$NAME'과 '$(basename "$other")'의 대화 기록 폴더 이름이 같아요. 구분할 수 없어서 멈춰요." >&2
    echo "한쪽 폴더 이름을 영문으로 바꾼 뒤 다시 실행하거나, 직접 확인해서 지우세요." >&2
    exit 1
  fi
  case "$enc_other" in "$ENC_PROJECT"-*) OTHER_PREFIXES+=("$enc_other") ;; esac
done < <(find "$PROJECTS" -mindepth 1 -maxdepth 1 -type d)

belongs_here() {  # $1 = 기록 폴더 이름. 이 프로젝트(또는 그 하위 폴더)의 것이면 참
  local n="$1" p
  case "$n" in "$ENC_PROJECT"|"$ENC_PROJECT"-*) ;; *) return 1 ;; esac
  for p in "${OTHER_PREFIXES[@]+"${OTHER_PREFIXES[@]}"}"; do
    case "$n" in "$p"|"$p"-*) return 1 ;; esac
  done
  return 0
}

TARGETS=()
add() { TARGETS+=("$1"); }

# 1. 프로젝트 폴더
add "$PROJECT"

# 2. 대화 기록 폴더 + 3. 세션 ID 수집
SESSIONS=()
if [ -d "$CLAUDE_DIR/projects" ]; then
  while IFS= read -r dir; do
    base="$(basename "$dir")"
    belongs_here "$base" || continue
    add "$dir"
    while IFS= read -r f; do
      SESSIONS+=("$(basename "$f" .jsonl)")
    done < <(find "$dir" -maxdepth 1 -type f -name '*.jsonl')
  done < <(find "$CLAUDE_DIR/projects" -mindepth 1 -maxdepth 1 -type d)
fi

for id in "${SESSIONS[@]+"${SESSIONS[@]}"}"; do
  # 세션 ID는 UUID 형태일 때만 쓴다 (다른 파일을 잘못 지우지 않도록)
  [[ "$id" =~ ^[0-9a-fA-F-]{36}$ ]] || continue
  for sub in file-history session-env tasks todos debug; do
    [ -d "$CLAUDE_DIR/$sub" ] || continue
    while IFS= read -r hit; do add "$hit"; done \
      < <(find "$CLAUDE_DIR/$sub" -mindepth 1 -maxdepth 1 -name "$id*")
  done
done

# 4. 임시 작업 폴더
TMP_BASE="${TMPDIR:-/tmp}"
while IFS= read -r dir; do
  belongs_here "$(basename "$dir")" && add "$dir"
done < <(find "$TMP_BASE" -mindepth 2 -maxdepth 2 -type d -path "$TMP_BASE/claude-*/*" 2>/dev/null)

# 루트에서 연 대화 (지우지 않고 알려만 줌)
ROOT_LOGS=""
[ -d "$CLAUDE_DIR/projects/$ENC_ROOT" ] && ROOT_LOGS="$CLAUDE_DIR/projects/$ENC_ROOT"

echo "== 지울 것 (프로젝트: $NAME) =="
for t in "${TARGETS[@]}"; do
  size="$(du -sh "$t" 2>/dev/null | cut -f1 || true)"
  printf '  %-6s %s\n' "${size:-?}" "$t"
done
echo
echo "== 지우지 않음 — 직접 확인하세요 =="
[ -n "$ROOT_LOGS" ] && echo "  WorkforMe 루트에서 연 대화 기록: $ROOT_LOGS (회사 이야기를 했다면 직접 지우세요)"
echo "  Anthropic 서버의 대화: 계정 개인정보 설정과 보관 기간을 확인하세요"
echo "  백업·동기화 사본: OneDrive, iCloud, Time Machine, 회사 백업 등"
echo

if [ "$MODE" != "--delete" ]; then
  echo "목록만 보여 주었어요. 지우려면: $0 $NAME --delete"
  exit 0
fi

echo "지운 것은 되돌릴 수 없어요. 그 프로젝트를 연 Claude Code 창을 모두 닫았는지 확인하세요."
printf '지우려면 프로젝트 이름을 다시 입력하세요 (%s): ' "$NAME"
read -r answer
if [ "$answer" != "$NAME" ]; then
  echo "이름이 달라서 아무것도 지우지 않았어요."
  exit 1
fi

for t in "${TARGETS[@]}"; do
  rm -rf -- "$t"
done

left=0
for t in "${TARGETS[@]}"; do
  if [ -e "$t" ]; then echo "  남음: $t" >&2; left=1; fi
done
if [ "$left" -eq 0 ]; then
  echo "다 지웠어요 (${#TARGETS[@]}곳)."
else
  echo "일부를 지우지 못했어요. 위 경로를 직접 확인하세요." >&2
  exit 1
fi
