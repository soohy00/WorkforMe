# WorkforMe

회사 일에서 쓰는 **문서를 만드는 개인 도구**예요. 한 회사, 한 서비스에 묶이지 않아요.
회사를 옮기면 프로젝트를 새로 만들어요.

도구의 뼈대는 [Dryforge](https://github.com/prekuter/dryforge) v1.3.7이에요.
원본을 **그대로 가져온 뒤**, 코드 대신 **문서**를 만들도록 한 번에 하나씩 고쳤어요.
무엇을 왜 고쳤는지는 [CHANGES.md](CHANGES.md)에 있어요.

## 무엇을 만드나

| 문서 | 주로 읽는 사람 |
|---|---|
| 협업 정렬 문서 (기능 기획서, 디자인 브리프, 요구·정책 정의) | 디자이너, 개발자 |
| 보고·에스컬레이션 (현황 보고, 문제 보고, 결정 요청) | 상사, 대표 |
| 성과 보고 | 투자사 |
| 제안서, 회의 자료, 시각화 문서(흐름도·상태도·로드맵), 운영 문서 | 상황에 따라 |

지금 결과물은 **Markdown(md)**이에요. 노션에 붙이거나 메일에 넣어요.
HTML·PDF 템플릿과 브랜드는 나중에 더해요.

## 흐름

```text
/migration   회사 자료로 프로젝트 시작 (한 번)      ─┐
                                                     ├─ 프로젝트 기억(docs/)이 쌓임
/ready       무엇을 누구에게 왜 쓰는지 잡기 → 승인   │
/go          쓰기 → 독립 독자 확인 → 결과 보고      ─┘  문서마다 반복
```

- **ready** — 요청, 메모, 파일을 읽어요. 사용자만 정할 수 있는 것(주요 독자, 읽고 할 일, 핵심 메시지,
  숫자, 약속, 보안 등급)만 선택지를 주고 물어요. 그다음 설계서를 보여 주고 승인을 받아요.
- **go** — 설계서대로 써요. 끝나면 세 가지를 확인해요.
  1. 모든 숫자·날짜·이름에 출처가 있나 (없으면 문서에 "미확인"으로 보여요)
  2. 대화를 모르는 **다른 에이전트**가 문서만 읽고 약속한 질문에 답하나
  3. 보안 등급과 받는 사람이 맞나
- **migration** — 온보딩 문서, 위키, 조직도, 이전 기획서를 읽어요. 자료가 말해 주지 않는 것
  (누가 무엇을 결정하나, 무엇을 누구에게 줘도 되나)만 물어요.

보안 등급은 4단계예요: **공개 / 사내한정 / 대외비 / 극비**. 회사에 규정이 있으면 회사 규정을 따라요.

## 설치 (Claude Code)

```text
/plugin marketplace add soohy00/WorkforMe
/plugin install dryforge-docs@workforme
```

비공개 저장소 인증이 안 되면, 먼저 clone하고 로컬 경로로 추가해요.

```text
/plugin marketplace add ~/WorkforMe
/plugin install dryforge-docs@workforme
```

## 메시지 다듬기

`/message`(또는 `/dryforge-docs:message`)에 거친 초안을 주면 "푸른 스타일" 업무 메시지로 바꿔 줘요.
첫 줄에 `[후배]`, `[동료]`, `[윗사람]`을 붙여 말투를 정해요. 붙이지 않으면 바꾸기 전에 셋 중 누구인지 먼저 물어요(추천 포함).
모르는 칸은 `[ ? ]`로 남겨요.

## 회사 프로젝트 시작하기

회사 문서는 **GitHub에 올리지 않아요**. [projects/README.md](projects/README.md)를 보세요.

```bash
mkdir projects/<회사-프로젝트> && cd projects/<회사-프로젝트>
git init -b main && echo "material/raw/" > .gitignore
git add .gitignore && git commit -m "start"
```

그 폴더에서 Claude Code를 열고 `/migration`(자료가 있을 때) 또는 `/ready <필요한 문서>`로 시작해요.

**회사 업무용 기기에서 쓸 때**(설치, 정보 주기, 소각)는 [COMPANY-DEVICE.md](COMPANY-DEVICE.md)를 보세요.
회사를 떠날 때는 `bash scripts/dispose-project.sh <회사-프로젝트>`로 그 프로젝트를 기기에서 지워요.

## 저장소 구조

```text
WorkforMe/
├── README.md                   ← 이 파일
├── CHANGES.md                  ← dryforge 원본 대비 변경 기록 (무엇을, 왜)
├── NOTICE                      ← 원본 저작권·라이선스 표시
├── .claude-plugin/             ← 마켓플레이스 (workforme → dryforge/claude)
├── .github/workflows/          ← dryforge 검사를 PR마다 실행
├── COMPANY-DEVICE.md           ← 회사 기기에서 쓰기: 설치부터 소각까지
├── scripts/dispose-project.sh  ← 회사 프로젝트 소각 스크립트
├── projects/                   ← 회사 프로젝트 (내 PC에만, README만 올라감)
└── dryforge/                   ← dryforge 원본 + 변경
    ├── src/skills/             ← 스킬 원본 (여기를 고침)
    ├── claude/                 ← 빌드 결과 (직접 고치지 않음)
    ├── build/build.sh          ← src → claude 빌드
    └── ci/verify.py            ← 검사
```

## 고칠 때

1. `dryforge/src/skills/`를 고쳐요.
2. `bash dryforge/build/build.sh`로 빌드해요.
3. 커밋한 뒤 `python3 dryforge/ci/verify.py`로 검사해요.
4. `CHANGES.md`에 번호, 무엇을, 왜를 적어요.

원본 새 버전 받기:

```bash
git subtree pull --prefix=dryforge https://github.com/prekuter/dryforge <태그> --squash
```

## 라이선스

`dryforge/`는 Apache-2.0이에요 ([dryforge/LICENSE](dryforge/LICENSE), [NOTICE](NOTICE)).
