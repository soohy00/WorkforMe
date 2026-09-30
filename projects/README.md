# projects — 회사별 문서 프로젝트

회사 하나 = 프로젝트 하나 = 이 폴더 안의 폴더 하나예요.

```text
projects/
├── README.md            ← 이 파일 (GitHub에 올라가는 유일한 파일)
└── <회사-프로젝트>/      ← 내 PC에만 있음. 자기만의 로컬 git 저장소
    ├── CLAUDE.md / AGENTS.md   프로젝트 입구 (dryforge-docs가 만듦)
    ├── docs/                   프로젝트 기억: 조직·독자·규칙·보안 등급·결정 기록
    ├── outputs/                만든 문서
    └── .dryforge/              작업 중인 설계서 (git에 넣지 않음)
```

## 왜 이렇게 두나요

- **회사 문서는 GitHub에 올리지 않아요.** 많은 회사가 회사 문서를 개인 저장소에 두는 것을 금지해요.
  WorkforMe의 `.gitignore`가 `projects/` 안의 회사 폴더를 모두 막아요.
- **그래도 기록은 남아요.** 회사 폴더마다 `git init`을 해서 **원격 없는 로컬 저장소**로 써요.
  dryforge-docs는 git으로 작업을 기록하고 되돌려요. 원격이 없으면 "푸시 안 된 커밋" 검사도 통과해요.
- **회사끼리 섞이지 않아요.** 회사를 옮기면 새 폴더를 만들어요. 이전 회사 폴더는 회사 규정에 따라
  넘기거나 지워요.

## 새 회사 프로젝트 시작하기

```bash
mkdir projects/<회사-프로젝트> && cd projects/<회사-프로젝트>
git init && git commit --allow-empty -m "start"
```

그다음 이 폴더에서 Claude Code를 열고:

- 회사 자료(온보딩 문서, 위키, 기획서)가 있으면 → `/migration`
- 자료 없이 첫 문서부터 시작하면 → `/ready <필요한 문서 설명>`

## 백업

로컬에만 있으므로 백업은 **회사가 허락한 곳**(회사 드라이브, 회사 git 등)에 따로 해요.
회사 git에 올려도 되면, 그 폴더에서 `git remote add`로 회사 저장소를 연결해요.
