# Changelog

## v1.3.7-docs.9 (2026-10-01)

Fixes from an end-to-end ready → go run with the writing guide:
- `writing-style.md`: one verb for the ask (승인 when the reader decides, never mixed with 검토); a next
  step for each outcome (approved, other option, held, no reply); the author's commitments in 합니다체;
  table cells without 님; dated table only for 3+ dated events; a new section on which rule wins
  (company rules → the user's recorded choice → this guide; an earlier document is not a rule); notes that
  hand the decision back are explained once, then a recorded user choice is followed
- Reviewer and writer prompts carry the same rules; a choice the spec records as the user's is not a finding
- `ready` checks the `main` branch name in ORIENT instead of interrupting `go`
- `go` step 9: an independent harness check before the final review; `harness-format.md`: never call
  the author by a word the project uses as a domain term (e.g. 사용자)

## v1.3.7-docs.8 (2026-10-01)

- Removed the `message` skill: the user's "푸른 스타일" was meant as a source for report writing, not
  as a message converter
- `writing-style.md` adapts it for reports: a habit → report-form table (배경, 목적, 결정 사항,
  향후 계획, 잠정 표시), the document register (개조식 facts, 합니다체 requests), what never appears in
  a document ("!", "~", emoticons, chat openers, thanks or apologies), and a notes → report example

## v1.3.7-docs.7 (2026-10-01)

- `message`: a draft with no recipient tag is no longer read as [동료]; the skill asks first, with
  the three options and a recommendation from the draft's hints

## v1.3.7-docs.6 (2026-10-01)

- Added the shared `writing-style.md` (ready, go): the author owns a position and asks for approval,
  upward documents follow the Korean report frame (두괄식, 건의, 향후 계획, 관련 문서), readability
  rules (cause → effect, where each fact connects), and register by reader; a decision handed back to
  the reader is blocking in the final review
- Added the `message` skill: turns a rough draft into a work message in the user's "푸른 스타일"

## v1.3.7-docs.5 (2026-10-01)

- ready asks only what the document needs: a purpose line, follow-ups checked against it, off-purpose
  topics parked and shown at the user gate; every question carries a recommendation
- Classification: an unclear level is asked with options and a recommendation; a provisional level
  is marked "(잠정)" and confirmed by the person who decides
- The main branch is always `main`; new repositories use `git init -b main`
- go adds a rule check to the verify set: every recorded company rule is checked against the
  document, and a rule/spec conflict is asked before writing
- Independent review fixes: rule-check results (pass, fail, not applicable, exception, undecidable —
  user), first-cycle rule sources, the rule check in bounded re-checks and at the user gate, and the
  foundation questions kept on purpose in a first cycle

## v1.3.7-docs.4 (2026-10-01)

- Added the shared `material-intake.md` (ready, go, migration): shareable documents in `material/`,
  raw datasets in the git-ignored `material/raw/` with a committed data card (source, as-of,
  definitions, classification, masking, figures used), spoken facts as user-stated with as-of,
  where seen, and what is counted
- New projects get a `.gitignore` holding `material/raw/`; go stops if a raw file is not ignored
- Fact-ledger sources point at the data card, never at the raw file alone

## v1.3.7-docs.3 (2026-10-01)

- Decision records state only reasons on the record; when the user gave none they say so, and an
  invented reason is a blocking hallucination
- The user's answers reach later subagents verbatim (question, options, answer), never summarized
- Writers receive the whole fact ledger with their rows marked, not a hand-picked subset

## v1.3.7-docs.2 (2026-09-30)

- go: bounded re-checks. The reader check separates blocking findings (conflicting facts, unsourced
  figures, a wrong expected answer) from the reader's open questions, which go to the user gate
  instead of starting another round; at most two re-checks, then the user decides. Advisories are
  triaged once, and a re-review after a fix judges blocking findings only
- go: completion-gate fixes use the same lightweight/fix-dispatch triage; text the user dictated is
  applied directly; a mid-run content change by the user updates the spec before re-verifying

## v1.3.7-docs.1 (2026-09-30)

- WorkforMe fork: ready, go and migration produce IT planning and business-operations documents
  instead of code; see CHANGES.md at the WorkforMe repository root for every change and its reason
- Added the shared classification reference, document kinds, the fact ledger and reader-check
  questions, and the independent reader check
- Build and verification cover the Claude package only

## v1.3.7 (2026-09-27)

- Added Chinese and Japanese READMEs

## v1.3.6 (2026-09-26)

- Replaced typographic ellipses and circled numerals in skill text with plain ASCII so plugin security scanners no longer misread them; no change to skill behavior

## v1.3.5 (2026-09-25)

- Relicensed under Apache-2.0
- migration and go now back up and review an existing AGENTS.md before rewriting it, as they do for CLAUDE.md
- Rewrote the skill descriptions, fixed the README install and update steps, and added contribution guidelines

## v1.3.1 (2026-09-24)

- Rewrote the README in English and Korean, with light and dark graphics and per-agent install and update instructions
- No changes to skills

## v1.3.0 (2026-09-24)

- Added Antigravity CLI support with its official plugin manifest and plugin rules
- Added the Antigravity CLI install guide to the README

## v1.2.0 (2026-09-23)

- Added Grok Build support, based in part on @williamjeong2’s contribution in #3
- Added GitHub Copilot CLI support through Agent Plugins 1.0 packaging

## v1.1.2 (2026-09-23)

- Refined plugin marketplace metadata

## v1.1.1 (2026-06-12)

- Brought the skill instructions in line with each other
- Added update instructions to the README

## v1.1.0 (2026-06-09)

- Merged set into ready, reducing the skills from four to three
- Reworked how ready finds the decisions that are yours to make
- go and migration now finish only on evidence from checks that ran

## v1.0.2 (2026-06-08)

- Streamlined the set skill and refined how go runs tasks

## v1.0.1 (2026-06-07)

- Added the project documentation layout to the README

## v1.0.0 (2026-06-07)

- First stable release
- Added migration for bringing existing projects in
- ready and go now create and keep project documentation that the next cycle starts from

## v0.5.1 (2026-06-06)

- Refined how go runs tasks

## v0.5.0 (2026-06-03)

- Added Codex support, with Claude Code and Codex built from one skill source
- Made go's task execution more efficient

## v0.2.5 (2026-06-02)

- Made go's task execution more efficient

## v0.2.0 (2026-06-01)

- Reworked ready and go for leaner runs

## v0.1.2 (2026-06-01)

- Made task execution more efficient

## v0.1.1 (2026-06-01)

- Fixed output files colliding with paths in your project
