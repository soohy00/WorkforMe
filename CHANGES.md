# dryforge 원본 대비 변경 기록

`dryforge/` 폴더는 [Dryforge](https://github.com/prekuter/dryforge) **v1.3.7**(커밋 `904f257`)을
git subtree로 가져온 것이에요. 가져온 커밋에서는 아무것도 바꾸지 않았어요.
그 뒤의 변경은 **한 번에 하나씩** 커밋하고, 여기에 무엇을·왜 바꾸었는지 적어요.

- 원본과 비교하기: `git diff <가져온 커밋> HEAD -- dryforge/`
- 변경 하나만 보기: `git log --grep "CH-01"`처럼 번호로 커밋을 찾아 `git show`로 봐요.
- 원본 새 버전 받기: `git subtree pull --prefix=dryforge https://github.com/prekuter/dryforge <태그> --squash`

## 사용자가 정한 것 (변경의 근거)

| 번호 | 질문 | 정한 답 |
|---|---|---|
| U1 | dryforge를 어떻게 가져오나 | 원본 그대로 + 기록 연결 (git subtree) |
| U2 | 처음 만든 docforge는 | 지우고 원본부터 다시 쌓음 |
| U3 | 회사 문서는 어디에 | 같은 저장소의 `projects/<회사>/`, 문서는 내 PC에만 (GitHub에 올리지 않음) |
| U4 | 보안 등급 | 4단계: 공개 / 사내한정 / 대외비 / 극비. 회사 규정이 있으면 회사 규정이 이김 |
| U5 | 문서용으로 바꾸는 방식 | 원본 스킬(ready · go · migration)을 직접 고침 |
| U6 | 지침 언어 | 영어 유지, 변경 기록은 한국어 |
| U7 | 다른 에이전트용 패키지 | Claude만 만듦 |
| U8 | 결과물 도구(HTML·PDF 템플릿, 숫자 확인 스크립트) | 나중에. 이번 결과물은 md |
| U9 | 이 도구의 성격 | 한 서비스에 묶이지 않는 작성 도구. 회사 하나 = 프로젝트 하나 |
| U10 | 주요 독자 | 협업하는 디자이너·개발자, 보고를 받는 상사·대표, 성과 보고를 받는 투자사 |
| U11 | 결과물 채널 | 메일 PDF, 노션, HTML, md |
| U12 | PPT · 브랜드 | 필요할 때 요청 / 방향이 잡힌 뒤 |

## 변경 목록

| 번호 | 무엇을 바꾸었나 | 왜 | 근거 |
|---|---|---|---|
| CH-01 | 빌드를 Claude 패키지만 만들도록 줄임. Codex·Grok·Agent Plugin·Antigravity 패키지와 그 입력 폴더, 마켓플레이스 파일을 지움. `verify.py`의 다른 패키지 검사는 같은 강도의 Claude 검사(`validate_claude_package`)로 바꿈 | 쓰는 도구가 Claude Code뿐이에요. 원본은 변경 하나가 패키지 6곳에 복사되어 diff에 6번 보여요. 한 곳만 남기면 "무엇을 바꾸었나"가 한 번만 보여요 | U7 |
| CH-02 | 플러그인 이름을 `dryforge` → `dryforge-docs`로, 마켓플레이스 이름을 `workforme`로 바꿈. WorkforMe 루트에 마켓플레이스(`.claude-plugin/marketplace.json` → `./dryforge/claude`)를 둠. 루트 `NOTICE` 추가 | 원본 dryforge를 따로 설치해도 이름이 겹치지 않게 해요. 루트 마켓플레이스가 있어야 `/plugin marketplace add soohy00/WorkforMe`로 바로 설치돼요. Apache-2.0은 바꾼 파일에 "바꾸었다"는 표시를 요구해요 | U1, U7 |
| CH-03 | WorkforMe 루트에 CI(`.github/workflows/dryforge-ci.yml`)를 추가. `dryforge/`에서 원본의 검사(`shellcheck`, `ci/verify.py`)를 돌리고, 루트 마켓플레이스가 빌드된 패키지를 가리키는지 확인 | 원본 CI는 `dryforge/.github/` 안에 있어서 하위 폴더에서는 돌지 않아요. 원본의 강점(빌드 안전장치, 다시 빌드해도 같은 결과인지 검사)을 PR마다 살려요 | U1 |
