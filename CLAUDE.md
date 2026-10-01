# WorkforMe

문서 작성 도구(dryforge-docs)와 회사별 문서 프로젝트(`projects/`)가 있는 저장소예요.

## 디자인

@DESIGN.md

- 문서·페이지(HTML, PDF, 노션 템플릿, 시각화)의 색, 글꼴, 간격은 `DESIGN.md`(Mintlify 기반)를 따른다.
- **한글 글꼴은 Paperlogy(페이퍼로지)를 쓴다.** `DESIGN.md`의 글꼴 지정보다 우선한다.
  영문·숫자는 `DESIGN.md`의 글꼴(Inter, 코드는 Geist Mono)을 쓴다.
  - 파일: `brand/fonts/paperlogy/` (OFL 1.1). 굵기 100–900의 9개. 굵기 값은 그 폴더의 README 표를 따른다.
- `DESIGN.md`는 웹사이트 분석에서 온 파일이라 마케팅 화면(히어로, 버튼 등) 내용이 많다.
  문서에 맞게 다듬은 규칙이 생기면 이 파일에 적고, 그 규칙이 `DESIGN.md`보다 우선한다.

## 문서용 규칙 (DESIGN.md보다 우선)

문서(HTML·PDF)는 `brand/document.css`를 쓴다. 견본: `brand/samples/decision-request.html`.
PDF 만들기: `NODE_PATH=$(npm root -g) node brand/tools/render.js <입력.html> <출력.pdf> [미리보기.png]`

- **종이**: A4, 여백 18mm(아래 20mm), 쪽 번호는 오른쪽 아래. 등급은 쪽마다 오른쪽 위(문서마다 `@page`에 적음).
- **글꼴**: Paperlogy 하나로 한글·영문·숫자를 쓴다(코드만 Geist Mono). 본문은 화면 15px, 인쇄 10.5pt,
  줄 간격 1.75. 한글은 단어 사이에서만 줄을 바꾼다(`word-break: keep-all`).
  Paperlogy 숫자는 모두 같은 폭이라 "11"처럼 1이 겹치면 간격이 넓어 보인다(글꼴 설계, 고칠 수 없음).
- **굵기**: 본문 400, 강조·표 머리글 600, 제목 700. 800·900은 표지·큰 숫자에만.
- **색**: 강조색은 하나(`--accent`). 회사 브랜드 색으로 바꿀 때는 `--accent`, `--accent-text`, `--accent-soft`
  세 개만 바꾼다. 글자색은 흰 바탕 대비 4.5:1 이상 — Mintlify 초록(`#00d4a4`)과 `#888888`은 글자에 쓰지 않는다.
- **첫 화면**: 핵심 메시지와 요청은 `.lead` 상자(왼쪽 강조선)에 둔다.
- **표**: 줄 선만 쓰고 세로선·줄무늬는 쓰지 않는다. 숫자 칸은 오른쪽 정렬(`.num`).
  여러 안을 나란히 비교하는 표(`.compare`)는 칸 폭을 같게 하고, 어느 한 안도 색·굵기로 돋보이게 하지 않는다.
- **알림 상자**: `.callout`에 `note`(초록), `info`(파랑), `warn`(주의), `danger`(위험). 제목 한 줄 + 본문.
- **등급 표시**: 맨 위 `.marking` 줄에 배지 — `public`(공개), `internal`(사내한정), `confidential`(대외비),
  `secret`(극비). 잠정이면 배지 글에 "(잠정)"을 붙인다.
- **추천·의견**: 맨 끝에 꾸밈 없이 둔다(`.opinion`). 색 상자나 강조를 쓰지 않는다.
- **움직임**: 문서에는 쓰지 않는다.
