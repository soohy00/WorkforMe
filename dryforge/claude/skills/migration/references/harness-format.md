# harness-format.md — the project harness spec (force-load)

The operational spec for a **project harness**: the durable documentation layer dryforge writes
for a project (created by `migration`, created/updated by `go`). This file is the **runtime
authority** — what each file is, what it must contain, the bar its content must clear, and how it
is created and updated. It carries the rules, not the design rationale.

The harness is the project-lifetime layer, distinct from the per-task 3-doc. It occupies the
platform harness paths (`CLAUDE.md` / `AGENTS.md`), so every agent working the project — dryforge
or not — operates inside it. It is a **durable project constraint** (the project's discipline and
memory), not ground truth: an active task's spec works *within* the harness, never overrides it
silently — a conflict is escalated to the user (see "Conflict" below).

**The harness is the sole durable store for project knowledge.** Anything you learn about *this
project* that is worth keeping — a trap, a non-obvious mechanism, a decision and its reason, a run
procedure — goes into the harness (working-notes / operations / decisions / the matching doc),
**never into the agent's own host memory or any external / per-agent memory store**. Host memory is
private to one agent on one platform and invisible to the next agent and to other agents' entry
points; project knowledge parked there is lost to everyone else and to the next cycle. The
harness is portable, shared, and committed with the project — it is the one place durable project
knowledge belongs.

## Language

**Language-agnostic.** Write the **entire harness in the language the user communicates in**, natively
(as a fluent speaker of that language would, never translationese). The *method* is fixed; the
*specific language* is discovered at runtime, never assumed — exactly as company specifics are. The
language this spec is written in does not constrain the harness.

## Structure

The project is one **company project** — a folder kept as its own local git repository (the documents
of IT planning and business operations are its deliverables). Every file has a fixed slot. A missing
file that the project needs is a defect. An *empty* file is correct only when its category genuinely
does not apply to this project; an empty file for a category that *does* apply is a hollow shell — a
defect.

```
project-root/
├── CLAUDE.md                     ← Claude Code entry point
├── AGENTS.md                     ← agent entry point (identical content to CLAUDE.md)
├── docs/
│   ├── stakeholders.md           ← organization: people, roles, who decides what, how work flows
│   ├── business-rules.md         ← the service and its business domain
│   ├── security.md               ← classification policy and sensitive information
│   ├── standards.md              ← rules (hard gates for writing and delivery)
│   ├── working-notes.md          ← knowledge (traps, non-obvious mechanisms, checklists)
│   ├── operations.md             ← how documents are produced, reviewed, delivered, stored
│   ├── audiences.md              ← what each recurring reader expects from a document
│   └── tracking/
│       ├── status.md             ← current position vs full scope, and the document index
│       ├── decisions/
│       │   ├── index.md          ← ADR index
│       │   └── NNNN-<slug>.md     ← individual decisions
│       └── findings.md           ← unresolved problems
└── outputs/
    ├── <YYYY-MM-DD>-<slug>/      ← one finished document (its parts and the assembled file)
    └── <series>/
        ├── AGENTS.md             ← per-series scope, reader, invariants (recurring documents)
        └── <YYYY-MM-DD>-<slug>/  ← one issue of the series
```

`.dryforge/` (the 3-doc, `NNN/` archives, `backup/`, the local `status.json` marker) is the
per-task workspace, **not** part of the harness — the harness never references it (see
self-containment). `outputs/` holds the deliverables; the harness describes the project, not the
content of each deliverable.

## Content quality — the bar every file must clear

A harness whose structure is filled but whose content is hollow is **worse than none**: the next
agent sees "docs exist," assumes it is informed, and works uninformed. The single purpose of every
file is that the next agent reads it and can work the project without going off the rails. Do not
satisfy this with structural box-filling — drive content density in prose.

**Five principles — does this sentence earn its place?** (apply to every file)

1. **Non-derivability** — if reading the project's material or finished documents reveals it,
   don't write it. The harness exists for what they cannot express: intent, constraints, the reason
   behind a decision, domain knowledge, who decides, non-obvious mechanisms.
2. **Work-changing** — an agent that reads the sentence and one that doesn't must produce different
   work. If the work is identical, the sentence is decoration, not information.
3. **Density** — every sentence carries a core fact. Information density, not word count, sets a
   document's value.
4. **Project-specificity** — a fact true of any project is not worth writing. Only this project's
   decisions, constraints, and mechanisms.
5. **Consequence-of-absence** — "if this sentence were missing, what breaks?" No answer → cut it.
   An answer → that consequence is the sentence's weight.

**Four techniques — how to state what survived the principles:**

1. **Verifiable statements** — every rule/constraint written so "was this honored?" is decidable.
2. **State the counter-case** — pair each "must" with its "must not."
3. **Describe the mechanism** — not just the outcome: input → processing → output.
4. **Make edge cases concrete** — never "handle other cases appropriately"; give each edge a
   specific disposition.

**The harness describes the *project* only — not itself, its origin, or the tooling.** Never write:
- **The document talking about itself** — its state, thinness, completeness, lifecycle, maturity, or
  *why it exists / how to read it* (e.g. "read this instead of the old documents", "written so you
  can brief a new writer"). State the project fact directly; don't narrate the doc's role.
- **Its origin or creation** — that it was generated, migrated, or a first-cycle artifact; and never
  list the documentation layer itself as a deliverable (status.md must not record "created the docs/
  layer" as done — docs are not a shipped project capability).
- **The generating tool or dryforge's coined vocabulary** — "dryforge" never appears in a generated
  project, nor do its internal coinages used to label the doc system ("harness", "3-doc", "delta",
  "migration"/"wave" as process names). Name sections in the project's own plain terms ("Project
  structure", not "Harness navigation").

(Current *project* state — "the launch proposal was approved on 10-02" in status.md — is fine; commentary about a
*document's* own maturity, purpose, or origin is not.)

## Entry point — CLAUDE.md / AGENTS.md

Two files, **identical content**, different platform. Write both together, byte-for-byte the same.

Must contain:
- **Project overview** — the company and its service, the user's role in it, and what documents
  this project produces for whom, in 2–3 lines. Lets an agent register the project's scope before
  working. This is where drift-prevention pays off most: an agent that doesn't know the project's
  character will write for the wrong reader, at the wrong level of formality, or with the wrong
  level of disclosure.
- **Navigation tree** — show the **whole harness** as a single project-root directory tree:
  `CLAUDE.md` / `AGENTS.md`, the `docs/` subtree, `outputs/`, **and the series `AGENTS.md` at their
  actual directories** — each path annotated with an arrow + a one-line role. A **tree** (`├──` /
  `└──`), **never** a table, a flat list, or just the `docs/` subtree with series tacked on flat below — one
  coherent tree so structure + purpose register at a glance.
- **Hard gates** — a **curated highlight** of the project's top non-negotiables (3–5, for at-a-glance
  before reading docs/). This is a highlight, **not** the full normative set: `standards.md` holds
  the authoritative complete rules (the navigation tree points there). Don't restate the full
  standards / verify-gate list here — surface only the headline non-negotiables.
  The classification rule is always among them.
  **Hard gates are permanent project invariants, not this-cycle scope boundaries.** "Don't write
  document X yet" is **not** a hard gate — unbuilt-but-planned scope lives in `status.md`'s "remaining"
  (it's a *status*, not an invariant; a later cycle will build it, and a permanent don't-build gate
  would falsely conflict with that cycle — a cycle's scope-freeze belongs in its 3-doc, not the
  harness). **Forward-compat is not a hard gate either.** "Keep it compatible with planned scope" is
  not a permanent invariant: a genuinely structural rule (e.g. "every investor update uses the same
  metric definitions") is a rule → `standards.md`; anything that *preserves a current shape so future
  work can attach* is maintain-guidance → `status.md`'s remaining or `working-notes.md`. Never write a "keep shape Y" gate — especially when a remaining-scope item
  will change shape Y (that is a scope-freeze wearing a forward-compat label).
- **Pre-work checklist** — the baseline reads (`docs/standards.md`, `docs/working-notes.md`, the
  relevant series' `AGENTS.md`) **plus project-specific targeted reads**: before a given kind of
  risky work, which section to read first (e.g. before anything going outside the company, the
  classification policy and that reader's entry in audiences; before quoting a metric, its definition
  in business-rules).
  A generic "read these three files" alone is low-value — make it project-specific.
- **Problem-routing** — name the project's **specific critical-failure conditions** (what is critical
  for *this* project — e.g. Confidential content about to reach an outside recipient, a figure that
  contradicts one already sent to investors, a commitment made that nobody approved) → report to the
  user immediately; everything else → record in `docs/tracking/findings.md`. Not generic
  boilerplate.

Handling an existing entry file (CLAUDE.md / AGENTS.md): (1) back up each one that exists to
`.dryforge/backup/`; (2) review the old content **critically** — do not transcribe it. Decide which
dryforge document each piece belongs in, drop what the new `docs/` already covers, and
improve/re-state what is worth keeping; (3) present the review to the user (what went where, what
was dropped and why) and get approval; (4) rewrite into the dryforge structure (approved content
only).

## docs/ file specs

Each file is **self-contained** and written at **one altitude**. "What to include" defines a *kind*
of information, not a company or industry — if the project has none of that kind, the item may be
empty.

### stakeholders.md — the organization around the project
- **Purpose**: who is involved, what each person or team is responsible for, and how decisions and
  work move between them.
- **Altitude**: organization level (roles and relationships, not personalities).
- **Include**: the roles involved (by role, with names only where the user supplied them and the
  classification allows); the reporting line and who approves what (scope, budget, dates, release,
  external communication); the collaboration map (which team hands what to whom — planning → design →
  development → operations); the channels each relationship uses (meeting, chat, workspace page,
  email); external parties (partners, vendors, investors) and who owns each relationship.
- **Exclude**: what each reader expects from a document (→ audiences); classification of what they
  may receive (→ security); the service's rules (→ business-rules).
- **Quality floor**: every decision type named has exactly one owner role ("release date: the team
  lead approves, the CEO is informed"), not "management decides"; every hand-off states what is handed
  over and when; external parties state who may speak to them.

### business-rules.md — the service and its domain
- **Purpose**: the canonical source for what the company's service is and the business rules the
  documents must state correctly — the definition of the domain, not how any document presents it.
- **Altitude**: domain level (the service's entities, rules, states, and terms).
- **Include**: what the service does and for whom; its main entities and their relationships; the
  business rules and policies (pricing logic, eligibility, limits, lifecycle and state transitions —
  the possible and the impossible ones); the key metrics and **how each is defined** (what is counted,
  over which period); domain-term definitions (where the same word means different things to
  different teams, distinguish them).
- **Exclude**: who decides (→ stakeholders); how documents are written (→ standards); a single
  document's claims (they live in that document).
- **Planned scope is not a permanent rule.** A capability that is planned but not yet launched must
  not be written as a permanent impossibility — describe the *current* state.
- **Quality floor**: every rule is verifiable — a reader could check a document's statement against
  it; every "must" has its paired "must not"; every metric has a definition and a source; no
  "handled appropriately" — each edge case gets a concrete disposition.

### security.md — classification and sensitive information
- **Purpose**: what may go to whom. The project's classification policy.
- **Altitude**: policy level (levels, recipients, handling).
- **Include**: the classification scheme in force (the company's own, or the default four levels —
  Public / Internal / Confidential / Strictly confidential — confirmed for this project); which
  recurring recipients may receive which level; the sensitive content of *this* project and its
  minimum level (revenue, contract terms, personal data, unreleased plans, fundraising, ...); the
  allowed channels per level (which tools may hold which level; public links); personal-data rules
  (what is collected into documents, and what never is); where documents may and may not be stored or
  backed up.
- **Exclude**: people and roles (→ stakeholders); writing rules (→ standards).
- **Quality floor**: every level states who may receive it and what it forbids; every sensitive item
  names its level; states what is *explicitly not allowed* (a public link for an Internal document,
  a revenue figure to an external recipient); not "handle sensitive data carefully" — this project's
  own rules. A rule about the document's content or marking is decidable by reading the document and
  names its source (the company's policy, the user) — `go`'s rule check runs it.

### standards.md — rules
- **Purpose**: what breaks when violated. The project's hard gates for writing and delivery.
- **Altitude**: normative level (MUST / MUST NOT).
- **Include**: classification marking and recipient rules as applied to every document; sourcing
  rules (every figure, date, name, quotation traceable; an unconfirmed fact is shown as unconfirmed);
  terminology rules (the official terms and the forbidden ones); number, date, currency, and name
  formats; file naming and output layout; versioning and status marking (draft / in review / final);
  the verification a document must pass before it is sent (reader check, fact trace, classification, rule check,
  any named sign-off).
- **Exclude**: traps and practical knowledge (→ working-notes); domain rules (→ business-rules);
  what a particular reader likes (→ audiences).
- **Bar**: only what leads to a wrong, leaked, or rejected document when violated. Preferences ("it'd
  be nice if...") are not rules.
- **Not a standards rule: the current cycle's scope-freeze.** "Don't write document X yet" is a
  *status* (→ status.md's "remaining"), not a permanent MUST/MUST-NOT.
- **Quality floor**: every rule has a clear violation criterion — decidable by reading the document
  (pass or fail), because `go`'s rule check runs every recorded rule that applies; record only rules
  actually in force, each with its source (the company's guide, the user); add a reason only when the
  rule is surprising. A company rule the user adds later is recorded the same way. Not "write clearly" — "every figure shows its period
  and source; a figure without both is not sent."

### working-notes.md — knowledge
- **Purpose**: what traps you if you don't know it. Practical knowledge distilled from experience in
  this project.
- **Altitude**: practitioner level (symptom → cause → response).
- **Include**: traps found in practice (observed symptom, root cause, response — e.g. a document
  bounced, a meeting that did not decide, a figure that disagreed with another team's number);
  non-obvious mechanisms (why a metric differs between two dashboards; which approval is really
  required); distilled checklists for repeated work (including how to verify).
- **Exclude**: rules (→ standards); domain rules (→ business-rules); a reader's standing expectations
  (→ audiences).
- **Trait** (author guidance — do **not** write this into the doc): may be thin in the first cycle;
  it thickens each cycle. The file contains only knowledge items — never a note about its own
  thinness or lifecycle.
- **Quality floor**: each item is symptom → cause → response; checklists don't end at "do X" but
  include "verify with Y"; never state what the material already makes obvious.

### operations.md — how documents are produced and delivered
- **Purpose**: everything needed to take a document from request to delivered and stored.
- **Altitude**: procedure level (follow it in order and it works).
- **Include**: where requests come from and how they are confirmed; the review and approval route
  per document kind (who reviews, who signs off, in what order); the delivery procedure per channel
  (pasting into a workspace page, attaching to an email, presenting in a meeting) including what to
  check before sending; storage and backup (where finished documents live, what may be backed up
  where — within the classification policy); recurring schedules (weekly reports, monthly updates).
- **Exclude**: writing rules (→ standards); organization (→ stakeholders).
- **Quality floor**: every procedure starts from its trigger and ends at "delivered and stored";
  each step's ordering dependency is clear; not "get it reviewed" — who reviews, by when, and what
  happens on rejection.

### audiences.md — what each recurring reader expects
- **Purpose**: the contract with each recurring reader — what they need from a document to act on it.
  Promises from the reader's point of view.
- **Altitude**: reader level (expectations, not personalities).
- **Include**: per recurring reader or reader group (designers, developers, the manager, the CEO,
  investors, partners, ...): what they decide or do with documents; what they already know and what
  they don't; the form that works for them (length, first-screen content, detail level, terms to use
  or avoid, visuals that help); cadence if recurring; how they give feedback. State a convention
  shared by all readers once.
- **Exclude**: who they are in the organization (→ stakeholders); which level they may receive
  (→ security).
- **Quality floor**: every reader entry states what they act on and what they need to act; a writer
  could shape a document for that reader from this file alone; drawn from what the user said or
  observed feedback, never from stereotypes.

### tracking/status.md — the dashboard
- **Purpose**: the current position against the project's full scope. The other `docs/` describe the
  project; status.md shows "where are we now" and which documents exist.
- **Include**: what is done (documents delivered, with date, kind, reader, level, and state — draft /
  sent / approved); what remains (documents or milestones still to come, in priority order); blockers
  (if any).
- **Update**: every cycle.
- **Quality floor**: a "delivered" or "approved" claim reflects the *actual* state the user confirmed
  — "written" is not "sent", and "sent" is not "approved". "Remaining" is a concrete item, never a
  vague "needs improvement."

### tracking/decisions/ — decision records (ADR)
- **Structure**: a folder. `index.md` (the index) + individual `NNNN-<slug>.md`.
- **Criterion**: only decisions with a real trade-off. Test: "could another team in the same
  situation have chosen differently?" — if so, it's a record (a document convention chosen over an
  alternative, a disclosure decision, a channel choice).
- **Each decision**: context (why the decision was needed); decision (what was chosen); alternatives
  (what was not chosen, and why — the reason **as it stands on the record**); consequences (the
  constraints this imposes on future documents, including what it made impossible).
- **Quality floor**: context states the concrete situation; every reason is **on the record** — the
  user's own words, the material, or the design's recorded reasoning; consequences include what is now
  impossible. When the user chose without giving a reason, write that no reason was given (in the
  user's language, e.g. "이유는 밝히지 않음") — **never supply one**. An honest "no reason given"
  meets this floor; an invented reason, or a reader preference nobody stated, fails it (a
  hallucination, blocking).

### tracking/findings.md — unresolved problems
- **Criterion**: only problems not resolved on the spot — a figure two sources disagree on, a policy
  question nobody has answered, an approval route that is unclear.
- **Duty before listing**: try to solve it first. **findings is the place for "cannot be solved in
  the current session," not "too tedious to investigate."** On listing, always state *why it can't be
  solved now* (waiting on a person, needs a higher-level decision, out of scope, ...).
- **Each problem**: what is wrong (reproducibly); why it matters (which documents or readers it
  affects); why it can't be solved now; a possible approach (if any).
- **Quality floor**: each problem is "under condition C, symptom S is observed," not "X is wrong";
  an item with no "why not now" is unfinished work, not a finding.

## Series AGENTS.md

One per **recurring document series or workstream** (a weekly report, a monthly investor update, the
documents of one feature's alignment) — only when such a series exists.

- **Include**: scope (what this series covers and what it does not); the primary reader and the
  outcome of each issue; invariants (what every issue must contain and keep consistent — metric
  definitions, section order the reader relies on); how an issue is produced and checked.
- **Altitude**: series level (maps directly to the documents in the folder).
- **Location**: the series folder under `outputs/`.
- **Series identification** — discovered at runtime from the documents and the user: a set of
  documents with the same reader and a recurring cadence or shared purpose. Exclude one-off documents.
- **Quality floor**: scope states what is *not* this series' job; invariants are verifiable ("every
  issue compares against the previous issue's figures, with the same definitions").

## Self-containment rules

1. **No cross-references between `docs/` files.** Not "see the other doc" — state what is needed, at
   this file's altitude, inside this file.
2. **The same topic may appear in several files — but each describes it only at its own altitude.**
   Altitude assignment test: "who consumes this information?" Someone orienting in the organization →
   stakeholders; someone stating the service's rules → business-rules; the writer of the next issue in
   a series → that series' AGENTS.md. Don't replicate an upper
   altitude's detail at a lower one, or mention a lower altitude's implementation at an upper one.
3. **The harness never references the 3-doc.** The 3-doc is archived after a task completes, so a
   pointer to it would dangle.
4. **A series AGENTS.md references no other series AGENTS.md and no `docs/` file.**
5. **No constraint-ID label scheme; restate, don't reference.** The harness carries **no**
   cross-referenceable constraint IDs — not the 3-doc's `INV-N` / task `T-N`, nor any `XXX-N` scheme of
   its own. Invariants and rules are stated **by content** (the content-name is the stable handle —
   e.g. "the no-revenue-to-outsiders rule"), and **every doc restates the slice of a constraint it needs
   at its own altitude** instead of pointing — to another `docs/` file or to the archived 3-doc — by
   label. Restating is required even though a label reference (`(INV-1)`) is shorter: the harness must
   be self-contained and the 3-doc is ephemeral (archived after the task), so any such label becomes a
   dangling pointer. (The 3-doc itself may use `INV-N` while active — this rule is harness-scoped.)

## Conflict (task vs harness)

When a task must contradict an existing harness decision (e.g. a reader now receives a higher
level, a metric is redefined): detect the
conflict, sort out which part is a trade-off and which is a defect, and report to the user. The user
decides; the decision flows into the spec, and `go`'s delta updates the harness. The spec does not
override the harness — **the user's decision changes both at once.** Domain conflicts don't
self-resolve; the user always decides.

## Update rules

### First creation (the first `go` cycle's wrap-up, or `migration`)
- Generate the whole `docs/` structure (all files).
- Generate CLAUDE.md / AGENTS.md.
- Generate series AGENTS.md (per identified series).
- If a CLAUDE.md or AGENTS.md exists, back it up and rewrite (see entry-point handling).

### Delta update (`go`, second cycle onward)
- **Read the current `docs/` first and treat it as the existing project constraint** — no separate
  tracking mechanism.
- Update only the area matching this cycle's task scope + output diff (scope-limited delta).
- Don't touch existing content outside the change scope — whether hand-edited or written by a prior
  dryforge run.
- Where this cycle must change something that already has different content in scope: **escalate to
  the user.**
- New series started → create its AGENTS.md (and update the entry point's navigation tree).
- status.md: every cycle (the delivered document and its state). working-notes.md: add non-obvious
  facts found while writing.
  decisions/: add this cycle's trade-off decisions (only if they meet the criterion). findings.md:
  update on find/resolve.

### Which file to touch (delta)
Identify the relevant files from the 3-doc's task scope + the actual output diff:
- stakeholders.md — only when a role, an owner of a decision, or a hand-off changes.
- business-rules.md — only when a service rule, a metric definition, or a term is added/changed.
- security.md — only when the classification policy, a recipient's level, or a sensitive item changes.
- standards.md — only when a new writing or delivery rule is introduced.
- audiences.md — only when a reader's expectations are learned or change (from the user or feedback).
- operations.md — only when the review, approval, delivery, or storage procedure changes.

**Delta is bidirectional.** A delta update is not only "add new content." Verify that this cycle's
change has not invalidated an existing statement elsewhere. Updating stale content matters as much
as adding new content.

## Execution discipline (when authoring the harness)

- **Explore sources before writing.** Explore every available source (the project's material and
  finished documents, the 3-doc, the user conversation, existing notes) enough to fully understand
  the project *before* writing. Don't start writing from partial understanding.
- **Don't write off what you don't know.** Where uncertain, read more material and generalize to a
  substantive project-specific fact. No guessing, no generalities. What the material can't settle,
  ask the user.
- **Verify against the source.** After writing, cross-check both ways: what the material and the
  dialogue established but the doc lacks (omission), and what the doc has but no source supports
  (hallucination — except content that derives from future scope, which is correct, see
  harness-review.md).
- **A discovered contradiction is not propagated.** When sources conflict — two received documents,
  an old document vs what the user said, or a claim you can't confirm (e.g. a deck stating one user
  count while the latest report states another) — do not copy both sides into the harness. Reconcile
  from the authoritative source (the latest dated source of record for *what currently is*; for
  *what should be*, the user decides) and write the single reconciled fact. If it can't be resolved
  from a source, record it in `findings.md` (with the conflict and why) or escalate — never leave
  two statements that can't both be true.
- **Filling files is not the goal.** The goal is the next agent working this project without going
  off the rails. A sentence that doesn't serve that goal is not written, however accurate.

## Universality guard

Stack- and company-agnostic throughout. Every concrete example named above is an *illustration* of
a kind of information, never a required organization or industry — the actual shapes are discovered
in the project at runtime. If you cannot generalize something, ask the user; never hardcode a
company.
