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
