# harness-review.md — verifying a generated/updated harness (force-load)

The verification criteria for a project harness. Used by **migration's REVIEW phase** and by
**`go`'s final-review lenses 3–4** — one source of truth, so both judge the harness the same way.
The spec being verified against is `harness-format.md`.

This is an **adversarial pass**: the reviewer's job is to find holes, not to bless the work
(self-judgment is the weak move). The four dimensions below are *what to
check*, applied with judgment — not a box-ticking checklist that earns a pass by being walked.

## Dimension 1 — content (does each file substantively meet its spec?)

For each file, check it against `harness-format.md`'s spec for that file, then against the
cross-cutting quality bar:

- **Meets its own spec** — has the *kinds* of information harness-format requires for that file, at
  that file's altitude, and clears that file's quality floor (e.g. business-rules: every rule
  verifiable, every metric defined with a source; security: every level states who may receive it and
  what it forbids; stakeholders: every decision type has one owner; standards: every rule has a
  violation criterion).
- **Five principles** — non-derivability (nothing the material already reveals), work-changing (would
  change the next agent's work), density (every sentence carries a fact), project-specificity (no
  universal truths), consequence-of-absence (removing it would break something).
- **Four techniques** — verifiable statements, counter-cases stated, mechanism described (not just
  outcome), edge cases concrete (no "handled appropriately").
- **Language** — the harness is written natively in the **language the user communicates in**
  (language-agnostic; the specific language is discovered, not assumed). A harness that doesn't match
  the user's language is a defect. (The reviewer is told the user's language by the orchestrator at
  dispatch — in both migration and go the finished work is verified by an independent dispatched
  reviewer, never self-reviewed.)
- **Harness describes the project only (blocking)** — flag any file that describes itself (its state,
  thinness, lifecycle, or *its own purpose / how to read it* — e.g. "read this instead of the old documents"),
  its origin (that it was generated / migrated / is a first-cycle artifact; status.md listing the
  documentation layer itself as a delivered capability), or that uses the **generating tool's name or
  dryforge's coined vocabulary to label the doc system** ("dryforge" anywhere; calling the docs "the
  harness"/"하네스", a section "Harness navigation", or naming "3-doc"/"delta"/"wave"). Section titles
  use the project's plain terms. It describes the project, not the document. ("dryforge" is a reliable
  sweep; for "harness" use judgment — a project's own *test* harness is legitimate, labeling the doc
  layer a harness is not.)
- **Entry-point navigation is one whole-harness tree** — CLAUDE.md/AGENTS.md show the navigation as a
  single project-root directory tree (`├──`/`└──`) covering the entry files + `docs/` + `outputs/` +
  series `AGENTS.md` at their dirs; flag a table, a flat list, or a docs-only tree with series tacked on.
- **No baked scope-freeze in any doc** — flag *any* doc that writes planned-but-not-yet-done scope
  (a status.md "remaining" item) as a permanent constraint: a hard gate or standards rule saying
  "don't write X yet", a business-rule calling a planned capability impossible, or a "keep shape Y"
  gate where a remaining item will change shape Y. Planned scope is a *status*,
  not a permanent invariant — it falsely conflicts with the cycle that builds it. Describe the current
  state, not a permanent ban; hard gates and domain laws are permanent only.

The failure mode to hunt: a **hollow shell** — structurally present, substantively empty. A file
that reads as generic boilerplate, restates what the material shows, or fills a section with modifiers
("clear," "effective," "appropriate") fails this dimension even though the section "exists."

## Dimension 2 — format (self-containment)

- **No cross-references between `docs/` files** — no "see stakeholders.md"; each file states what it
  needs at its own altitude.
- **Each file at one altitude** — no upper-altitude detail replicated below, no lower-altitude
  implementation mentioned above. The same topic appearing in two files is fine *only* if each
  treats it at its own altitude.
- **No 3-doc references** — nothing points at `.dryforge/` (the 3-doc is archived after the task;
  the pointer would dangle).
- **No constraint-ID labels (blocking).** Flag any constraint-ID carried into the harness — the
  3-doc's `INV-N` / `T-N`, or any `XXX-N` scheme — and any reference to another doc's invariant/rule
  *by label*. These dangle once the 3-doc is archived and violate self-containment; invariants must be
  stated **by content**. A sweep for `\b[A-Z]{2,}-[0-9]+\b` across the harness catches most; also sweep for the 3-doc's
working ids (`\b[FQVT][0-9]+\b` — fact, question, visual, task), which must never appear in the
harness or in a delivered document.
- **Series AGENTS.md** references no other series AGENTS.md and no `docs/` file.

## Dimension 3 — completeness (required files present)

- All `docs/` files exist (the 7 core — stakeholders, business-rules, security, standards,
  working-notes, operations, audiences — + tracking: status.md, decisions/index.md, findings.md).
- CLAUDE.md and AGENTS.md both exist, with **identical content**.
- An AGENTS.md exists for every identified document series (series-identification heuristic in
  harness-format.md). A missing series AGENTS.md for a real series is a defect.
- An empty file is correct only when its category genuinely doesn't apply; an empty file for an
  applicable category is a defect (hollow shell), caught by Dimension 1.

## Dimension 4 — against the source (omission vs hallucination)

Cross-check the harness against its sources — the project's material, the finished documents in
`outputs/`, and the decisions the user confirmed (passed in by the orchestrator) — **both
directions**:

- **Omission** — an intent / constraint / decision that the material **cannot show on its own** (who
  decides, what may go to whom, what a reader needs) was settled with the user but is missing from the
  docs. This is the real omission. *Facts the material already shows being absent is not an
  omission* — by the non-derivability principle, the harness deliberately omits them.
- **Hallucination** — the docs assert something no source supports (a person, a rule, a metric, a
  reader preference nobody stated). Flag it — **except** content that legitimately derives from
  **future scope**: status.md's "remaining" items and other forward-looking content sourced from the
  Foundation/design. Distinguish "the doc describes a planned future state" (correct) from "the doc
  describes a present state the sources contradict" (a real hallucination).

## Findings → disposition

Each finding is one of:
- **Internally resolvable** (a hollow section you can deepen from sources already in hand, a
  cross-reference to inline, an altitude violation to move) → fix it directly.
- **Needs user intent** (a gap only the user can fill — a domain rule, a policy decision, a
  rationale not on the record) → do not invent it; raise it to the user (migration: ask in the user
  gate; go: surface as a blocking finding the orchestrator escalates).

In `go`'s final review, harness findings carry the same blocking/advisory split as document findings.

## Universality guard

Stack- and company-agnostic. The criteria judge information *kind*, density, and altitude — never
conformance to a particular organization. What counts as a series, a reader, or a rule is whatever the
project actually is, discovered at runtime.
