# 문서 종류별 레이아웃

문서 종류마다 **순서(섹션)**와 **쓰는 부품**을 정해 둔 표예요. 종류는 dryforge-docs의
`doc-types.md`와 같아요. 시각화 문서는 디자인 시스템이 정해진 뒤에 따로 만들어요.

모든 문서의 공통 틀:

1. `.marking` — 등급 배지 + 받는 사람 (맨 위 한 줄)
2. `h1` 제목 (+ 필요하면 `.badge.draft`로 "초안" 등) · `.meta` 또는 `dl.kv`로 작성·날짜·버전
3. `.lead` — 첫 화면: 핵심 메시지와 요청. 첫 화면만 읽어도 무엇을 해야 하는지 알게 함
4. 본문 섹션 (`h2`)
5. `.doc-foot` — 필요할 때만

인쇄: 문서마다 `<style>`에 `@page { @top-right { content: "<등급>"; ... } }`를 적어 쪽마다 등급을 찍어요.
표지가 있는 문서는 `@page :first`에서 등급·쪽 번호를 지워요.

| 종류 | 견본 | 섹션 순서 | 핵심 부품 |
|---|---|---|---|
| 상사·대표 보고 (결정 요청, 상황 보고) | `samples/decision-request.html` | 결정 요청 → 상황 → 두 안 비교 → 여쭐 것 → 작성자 의견 | `.lead`, `table.compare`, `.callout.note`, `.opinion` |
| 제안서 | `samples/proposal.html` | **표지** → 승인 요청 → 문제와 이유 → 방법 → 범위 → 기대 효과(추정 표시) → 비용·일정·사람 → 위험과 대응 → 다른 방법(아무것도 안 함 포함) | `.cover`, `dl.kv`, `ol.steps`, `.cols`, `.pill.neutral`(추정), `.callout.warn`, `table.compare` |
| 협업 정렬 문서 (디자이너·개발자) | `samples/alignment.html` | 한 줄 요약 → 왜 하나요 → 정해진 것·열린 것·정할 것(담당·기한) → 범위(지금/지금 아님) → 화면 상태 → 완료 기준 → 질문 창구 | `.pill.settled/open/decide`, `.cols`, `ul.checklist`, `.callout.info` |
| 투자사 보고 | `samples/investor-update.html` | **표지** → 요약 → 핵심 숫자(지난 기간·목표 대비, 정의) → 지난번 약속과 결과 → 잘 안 된 것과 대응 → 다음 목표 → 부탁 | `.cover`, `.stats` + `.stat`(`.delta`, `.bar`, `.def`), `.pill.settled/missed/open`, `.callout.warn` |
| 회의 자료 (사전 자료) | `samples/meeting-preread.html` | 일시·진행 → 이 회의가 끝나면(결정/확인) → 이미 정해진 것 → 안건(시간, 끝나는 모양) → 결정할 안건 비교 → 회의 뒤 할 일(빈 표) | `dl.kv`, `table.agenda`(`.ends`), `table.compare` |
| 운영 문서 (정책·절차·회고) | `samples/operations.html` | 시행일·담당·범위 → 한 줄 요약 → 절차 → 누가 무엇을 → 예외와 승인자 → 개정 이력 | `dl.kv`, `ol.steps`, `.callout.danger`(예외), 개정 이력 표 |

## 부품을 쓰는 규칙

- **숫자 카드(`.stat`)**: 숫자마다 비교 기준(지난 기간)과 목표, 정의(무엇을 셌나, 언제 기준, 어디서)를 함께 써요.
  정의가 없는 숫자는 카드에 넣지 않아요. 막대(`.bar`)는 목표 대비 정도예요.
- **상태(`.pill`)**: `settled` 정해짐 · `open` 열림 · `decide` 정할 것 · `missed` 미달 · `neutral` 추정·안내.
  열림·정할 것에는 담당과 기한을 같은 줄에 써요.
- **비교 표(`table.compare`)**: 칸 폭을 같게 하고, 어느 한 안도 색·굵기로 돋보이게 하지 않아요.
- **추천**: 결정 요청은 맨 끝 `.opinion`에만. 회의 자료처럼 추천이 없으면 "추천 없음"이라고 적어요.
- **추정**: 추정한 숫자나 날짜에는 `.pill.neutral`로 "추정"을 붙이거나 글에 "(추정)"을 적어요.
- **절차(`ol.steps`)**: 단계 제목에 "무엇 — 누가, 언제까지"를 넣어요. 끝난 단계는 `li.done`.
- **완료 기준(`ul.checklist`)**: 한 줄에 하나, "~하면 ~됨"처럼 맞았는지 판단할 수 있게 써요. 끝난 것은 `li.done`.

## PDF 만들기

```bash
NODE_PATH=$(npm root -g) node brand/tools/render.js <문서.html> <문서.pdf> [미리보기.png]
```
