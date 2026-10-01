# 회사 기기에서 쓰기 — 시작부터 소각까지

회사(예: A회사, 폴더 이름 `acme`)의 업무용 기기에서 이 도구를 쓰는 순서예요.
회사 정보는 그 기기 안에만 두고, 회사를 떠날 때 지워요.

## 0. 시작 전에 확인할 것

- [ ] **회사의 AI 사용 규정.** 회사 정보를 외부 AI에 넣어도 되는지, 어느 계정을 써야 하는지 확인해요.
      내 기기에서 실행해도 **대화 내용은 Anthropic 서버로 가요.** 기기에만 남는 것은 파일이에요.
- [ ] **계정.** 회사가 정한 Claude 계정이 있으면 그 계정을 써요. 개인 계정을 쓴다면 claude.ai의
      개인정보 설정(대화를 모델 학습에 쓰는지)을 확인해요.
- [ ] **설치 허가.** Claude Code와 git을 설치해도 되는지 IT 규정을 확인해요.
- [ ] **동기화 폴더 피하기.** OneDrive, iCloud, Dropbox가 동기화하는 폴더(바탕화면, 문서 등)에 두지 마세요.
      사본이 다른 곳에 생기고, 소각할 때 지우기 어려워요. 예: `C:\work\WorkforMe`, `~/work/WorkforMe`.

## 1. 설치

1. **git**을 설치해요. Windows는 Git for Windows를 설치해요(Claude Code가 Git Bash를 써요).
2. **Claude Code**를 설치하고 로그인해요. 설치 방법은 Claude Code 공식 문서를 따라요.

## 2. 이 저장소 가져오기

둘 중 하나를 골라요.

- **방법 A — git clone** (회사 기기에서 개인 GitHub에 로그인해도 될 때)
  ```bash
  git clone https://github.com/soohy00/WorkforMe.git ~/work/WorkforMe
  ```
- **방법 B — ZIP** (개인 GitHub 로그인이 안 될 때)
  GitHub에서 ZIP으로 받아 `~/work/WorkforMe`에 풀어요. git 기록이 없어도 도구는 동작해요.

**회사 기기에서는 이 저장소로 push하지 마세요.** 회사 폴더는 git이 무시하지만, push를 아예 하지 않는 것이 가장 안전해요.
방법 A로 받았다면 실수를 막기 위해 push 주소를 막아 둘 수 있어요:

```bash
cd ~/work/WorkforMe
git remote set-url --push origin no-push
```

## 3. 플러그인 설치

`~/work/WorkforMe` 폴더에서 Claude Code를 열고 입력해요:

```text
/plugin marketplace add ./
/plugin install dryforge-docs@workforme
```

설치한 뒤 `/`를 입력해 스킬 이름을 확인해요. `/ready` 또는 `/dryforge-docs:ready`처럼 보여요.
이름이 헷갈리면 "ready 스킬로 시작해 줘"라고 말해도 돼요.

## 4. 회사 프로젝트 만들기

```bash
cd ~/work/WorkforMe
mkdir projects/acme && cd projects/acme
git init && echo "material/raw/" > .gitignore
git add .gitignore && git commit -m "start"
```

- 폴더 이름은 **영문·숫자**로 지어요(예: `acme`). Claude Code는 대화 기록 폴더 이름에서 한글을 `-`로 바꿔서,
  한글 이름 프로젝트끼리 기록이 구분되지 않을 수 있어요.
- 원격(remote)을 추가하지 마세요. 이 폴더는 기기 안에만 있어요.
- 회사가 백업을 허락한 곳(회사 git 등)이 있으면 그때만 연결해요.

## 5. 문서 쓰기

`projects/acme` 폴더에서 Claude Code를 열고 시작해요.

- 회사 자료(공유해도 되는 것)가 있으면 → `migration`
- 없으면 → `ready <필요한 문서 설명>`
- 문서 설계가 끝나면 → `go`

정보를 주는 방법(말, 원자료, 자료 카드)은 [projects/README.md](projects/README.md)를 보세요.
원자료는 `material/raw/`에 넣어요. 이 폴더는 git에 기록되지 않아요.

## 6. 도구 업데이트

```bash
cd ~/work/WorkforMe && git pull        # 방법 B는 ZIP을 다시 받아 덮어써요 (projects/는 건드리지 않음)
```

그다음 Claude Code에서 `/plugin marketplace update workforme`를 입력해요.

## 7. 대화 기록을 짧게 남기기 (선택)

Claude Code는 대화 기록을 기기에 남겨요(`~/.claude/projects/`). 읽은 파일 내용도 들어 있어요.
오래된 기록을 자동으로 지우려면 `~/.claude/settings.json`에 넣어요:

```json
{ "cleanupPeriodDays": 14 }
```

## 8. 소각 (회사를 떠날 때)

1. 그 프로젝트를 연 **Claude Code 창을 모두 닫아요.**
2. 지울 목록을 먼저 봐요 (아무것도 지우지 않아요):
   ```bash
   cd ~/work/WorkforMe
   bash scripts/dispose-project.sh acme
   ```
3. 목록이 맞으면 지워요. 프로젝트 이름을 한 번 더 입력해야 지워져요:
   ```bash
   bash scripts/dispose-project.sh acme --delete
   ```

스크립트가 지우는 것:

| 무엇 | 어디 |
|---|---|
| 문서·원자료·자료 카드·git 기록 | `projects/acme/` |
| 그 폴더에서 연 대화 기록 | `~/.claude/projects/` 안의 그 폴더 기록 |
| 그 대화의 세션 데이터 | `~/.claude/` 안의 file-history, session-env, tasks, todos, debug (같은 세션 ID만) |
| 임시 작업 폴더 | `/tmp/claude-*/` 안의 그 폴더 것 |

스크립트가 지우지 **못하는** 것 — 직접 확인해요:

- [ ] **WorkforMe 루트에서 연 대화.** 회사 이야기를 했다면 스크립트가 보여 주는 경로를 직접 지워요.
- [ ] **Anthropic 서버의 대화.** 계정의 보관 기간과 설정을 따라요.
- [ ] **백업·동기화 사본.** OneDrive, iCloud, Time Machine, 회사 백업 등.
- [ ] **회사에 남길 것.** 회사 규정이 문서를 넘기라고 하면, 지우기 전에 회사가 정한 곳에 넘겨요.

이 도구(WorkforMe 폴더와 플러그인)는 회사 정보가 없으므로 남겨도 돼요. 기기를 반납한다면 같이 지워요.
