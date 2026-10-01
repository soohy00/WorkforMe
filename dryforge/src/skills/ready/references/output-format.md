# output-format.md — the 3-doc contract

Defines what **`ready`** (the producer) outputs and **`go` consumes**. This is the contract between
`ready` and `go`.

**Core principle:** exactly THREE parts are rigid, machine-read schemas — the **Execution
Graph** (plan), the **fact ledger** and the **reader-check questions** (spec). `go` schedules from the
first and verifies against the other two. Everything else in the three documents is a *content
requirement*: the agent designs the structure per project (intent fixed, structure flexible). All
content is stack- and company-agnostic — project specifics are discovered while reading the project,
never hardcoded.

**The deliverable is a document** (see `ready`'s SKILL.md). Its output lives at a project-root-relative folder,
by default `outputs/<YYYY-MM-DD>-<slug>/` (a document in a recurring series:
`outputs/<series>/<YYYY-MM-DD>-<slug>/`), as Markdown (the channel the spec names — a Notion page,
an email, a shared screen — is where the Markdown goes; converting to other file formats is not part
of this cycle).

## The three documents (handoff governs)

### handoff — governing doc + intent injection
Must convey (structure is the agent's to design — 3 hard gates or 30):
- **Document Roles** table + conflict resolution: spec defines *what the document says and for
  whom*; plan defines *its parts, their order, and work targets*.
- File locations (as project-root-relative paths, e.g. `.dryforge/spec.md` — never
  machine-absolute, so the 3-doc stays portable and survives archiving) + the big
  picture (execution shape).
- **Hard gates**: non-negotiable constraints the executing agent cannot derive from the material
  alone (things the document must never say or promise, fixed dates and wording) —
  always including the classification requirements of the spec's level (`classification.md`, "Hard
  gates").
- Intent decided while authoring but not captured in spec/plan.
- **First cycle only (no project harness yet):** the handoff **carries** a **Project Foundation**
  section — the project-wide foundation (business and stakeholder model, working decisions, future scope) that
  seeds the harness `go` creates at the end. `ready` produces it through its first-cycle ELICIT loop
  and writes it at the SPEC step (`foundation-format.md`). It is **required** in a first cycle — there
  is no degrade path; `go` treats a missing Foundation in a first cycle as a precondition violation and
  stops (`foundation-format.md`, "First-cycle precondition"). Omit it in later cycles (the harness has
  taken over the project-context role).

### spec — what to write (ground truth)
Must convey: the **classification level and named recipients** (`classification.md`); the **readers**
(the one primary reader, the others, and per reader what they know · worry about · decide); the
**outcome** (the one action after reading, by when, and what counts as success); the **key message**
in one sentence; the **content** — each claim with its evidence (fact-ledger ids), what is committed
and what is explicitly not (scope), risks and their handling, the objections to answer; the
**requests** (what, how much, from whom, by when; options and recommendation where a decision is
asked); for a coordinating document, what is **settled / open / to decide** with owners and dates,
states and edge cases as explicit rules, acceptance criteria; the **form** — kind, channel, length,
tone, output location, and the **visual list** (each visual with the question it answers); key design
rationale / thinking-base (decision + why, where not derivable from the material — see below); the
**fact ledger**; the **reader-check questions** (the required verification).
spec is ground truth — on conflict spec wins; spec errors are fixed only with user
approval.

**Fact ledger (fixed format).** Every figure, date, proper name, and quotation that may appear in the
document, one row each — `go` traces the finished document against it:

```
## Fact ledger
| id | fact | source | status |
|---|---|---|---|
| F1 | Monthly active users 120,000 (2026-09) | Q3 report.pdf p.4 | sourced |
| F2 | Launch target 2026-11-20 | user, in dialogue | user-stated |
| F3 | Competitor A monthly price | — | unconfirmed |
```

`source` is a committed file path (for raw data: its data card in `material/`, never the raw file
alone — it may be deleted), or `user, in dialogue (YYYY-MM-DD)` for a spoken fact
(`material-intake.md`). `status` is exactly one of `sourced` / `user-stated` / `unconfirmed` (write the labels in the user's
language if the document is in it; keep the three meanings). An `unconfirmed` fact is shown in the
document **marked as unconfirmed**, never smoothed into a confident statement — and the user was told
about it in ELICIT. The ids (`F1`, and the `Q1` / `V1` / `T1` ids below) are working labels for the
3-doc and `go`'s checks — they never appear in the delivered document.

**Reader-check questions (fixed format).** The document's acceptance test: an independent reader who
never saw the dialogue must answer each from the finished document alone:

```
## Reader-check questions
| id | question | expected answer (gist) | answered in |
|---|---|---|---|
| Q1 | What exactly am I asked to approve? | a 3-month pilot, 40M KRW | first screen, section 1 |
| Q2 | When payment fails, where does the user go? | retry screen; after 3 failures, support | section 3, V2 |
```

5–10 questions. They must cover the outcome, the key message, every request, and the part most easily
misread. The expected answer is for `go`'s comparison only — it is **never** shown to the reader.

**The spec transcribes the settled decision surface — it does not make or defer decisions.** ELICIT
already settled every load-bearing decision, *including what the reader acts on* (`intent-review.md`:
the exact request, each figure with unit · date · source, the committed scope and what is out, owners
and dates of open items, acceptance criteria). Pin each of those **here, the first time — as precisely
as if no downstream gate existed.** Do **not** ship
a half-pinned contract for the 3-doc-gate to tighten over rounds: a gate catching a precision gap is an
*upstream failure*, not the gate's job, and leaning on it is the reward-hack
`elicitation.md` forbids. (A genuine tuning default with no user preference is *pinned* as a default
**marked tunable** — which is settling it, not deferring it.)

**The spec is pure content — no provenance/attribution tags.** Every load-bearing decision appears as
a settled rule, written from understanding the user's intent (`elicitation.md`). Do **not** annotate
decisions with who-decided markers (`[user-decided]` / `[agent-default]`) or target/context labels —
those are internal tokens, they clutter the user-facing document, and the artifact does not need them.
That a decision is the user's intent (not an agent guess) is ensured *upstream* — by ELICIT's
"no-guess-survives" exit and the independent intent-completeness check (`intent-completeness.md`) — not
by a tag in the doc. The only annotation a decision carries is its **reason in the thinking-base** when
non-derivable (below), written in the user's terms as prose.

### plan — what to do (tasks + the machine graph)
A task is one **part of the document** — a section, a visual, an appendix, the first screen (title,
summary, request). Must convey: per-task **content contract** (the part's job for the reader, the
claims and fact-ledger ids it uses, what it must not say, **work targets** — files | state | external
resource — and verification gate: the reader-check questions it answers + the facts it must trace);
**thinking-base** (decision + reason where not derivable from the material); shared-write guidance
(prose, below); a narrative of how the reader moves through the document; and the **Execution Graph**
(below). The verification gate matches the deliverable type: a file diff for a written part, captured
external evidence for work outside the tree (e.g. a page updated in an outside tool). Target shape
and gate are discovered from the project, not assumed.

## The Execution Graph — the scheduling schema

A fenced `yaml` block inside the plan. go parses it for scheduling:

```yaml
tasks:
  - id: T5
    depends: [T2, T3]      # task ids that must finish first
    risk: RISKY            # OPTIONAL: RISKY | MECHANICAL | NONE
regen_barriers:
  - { after: [T3], run: "<regen step — discovered while reading the project>" }
```

- `depends` is the **only encoded judgment** (which task needs which). the producer
  computes it; go follows.
- `risk: RISKY | MECHANICAL | NONE` is an **optional** per-task atom alongside `depends`.
  It sizes the writer's per-part verification ceremony — it never changes whether a part is
  verified or reviewed, and never touches gate topology. (go may also read it to choose a single-task
  wave's execution mode, but that is a consumer-side use; the producer just derives the tier.) Derive
  it per task (see
  `references/dependency-calc.md`): RISKY if the part introduces figures or commitments the reader
  acts on, a request or decision, rules and edge cases a builder will follow, classification-sensitive
  content, or is the first screen (restating an already-sourced figure as background is MECHANICAL); NONE if it is metadata with no new
  claim; otherwise MECHANICAL. (Assembly is never a task — `go` regenerates the assembled document
  after every wave.) This is a derivation heuristic
  judged per task, not a fixed checklist. If a producer omits it, the task is unclassified: go leans
  toward stronger verification, and the writer still judges verification ceremony while writing — no
  break.
- go derives waves by topological sort of `depends`, then dispatches in
  batches of **≤8 concurrent**.
- `regen_barriers` = cross-cutting steps between waves (timing: after task X). The
  command is discovered per project while reading the project, not hardcoded. Documents rarely need
  one; when a part must be regenerated after others land (a numbered figure index, a table of
  contents), that is the barrier.
- Do **not** encode produces / consumes / shared_write / waves here — they are prose,
  runtime-derived (git diff), or computed.
- `id`s match the prose plan; the graph is the scheduling skeleton only.

## Shared-write handling — two layers (hint + safety net)

Parallel tasks must not collide on shared files (the assembled document, a shared glossary, a
figure index, ...). Each part is written to its **own file**; one assembly step writes the shared
document. Two layers, not a strict prediction:

1. **Hint** (prose in plan, best-effort, may be incomplete): per task, e.g. *"Write only
   `parts/03-payment-failure.md`; do not edit `document.md` — the assembly step joins all parts at
   the end of the wave."* Proactively avoids known collisions. Not authoritative.
2. **Guarantee** (runtime, go): before merging a wave, detect changed-file
   overlaps across task branches (`git diff`). Declared-shared files are already
   deferred; an **undeclared** overlap degrades safely (serialize / ad-hoc defer /
   escalate); a git merge conflict is the final backstop. A missed hint becomes a
   *handled conflict*, never silent corruption.

## Authoring rules (for the prose bodies)
- **Match the user's language (language-agnostic)**: author the three docs in the language the user
  communicates in, natively — discovered at runtime, never assumed, exactly like stack specifics. Not
  translationese; the language this contract is written in does not constrain the 3-doc.
- Replace premature prose with **content contracts** (the part's job, its claims and facts,
  what it must not say, which reader-check questions it answers — not the wording).
- **Stack-agnostic**: no project-specific assumption as a rule; specifics (build
  targets, regen commands, conventions) are discovered from the project.
- The three docs' section layout is the agent's to design; only the content above is
  required.

## thinking-base (decision + reason) — the derivability test

Record a reason only where a fresh agent, reading the project material, could **not** reach the
designer's decision on its own. Test in order:

1. **Derivable from the material?** → **Yes**: no reason needed (the material says it).
2. **Unsure if it's derivable?** → include it (gray-zone default: an over-included reason is cheap; a
   missing one derails the executing agent).
3. **Not derivable (a reason is needed)** → is it **actually on the record** — settled in the
   dialogue / material?
   - **Yes** → record *decision + reason*.
   - **No — you'd have to invent it** → **do NOT write a reason. Ask the user.** A fabricated reason is
     worse than none: it sends the executing agent confidently the wrong way. (Never attribute a
     reason to something that was not actually decided.)

**Tuning values are recorded as defaults, not grounded decisions.** A configurable value within an
already-settled mechanism that is a *conventional default* or is *tuned later by feel* — one the user
has no preference on — is a tuning value, *not* a user-grounded decision (`elicitation.md`, "exit bar
item 2"). Record a sensible default and **mark it tunable**, so the executor knows it is adjustable,
not a hard requirement. This is **not** a thinking-base reason (it is derivable / a default), and it
must **not** be forced through the user — that is over-asking. The *mechanism* it sits in is
the load-bearing decision; the *value* is the tunable. (Mechanism vs tuning value is judged per
project, never a fixed list.)

Frequent categories (accelerators for spotting candidates, **not** an exhaustive list): trade-off /
external constraint / scope boundary / convention exception / domain invariant / reader-driven
choice (why this reader gets this order, this length, this level of detail) / sensitivity (why a
figure is generalized or left out) / rejected alternative (an option the designer considered and
discarded — record it, and why, so a downstream agent doesn't "improve" the design back into the
rejected choice).

## A complete worked example

See `references/example-3doc.md` for one full `handoff` + `spec` + `plan` (an alignment document for
designers and developers) — read it once to anchor the shape and altitude. It is **illustrative, not a template**:
its role names are deliberately generic because a real 3-doc is stack-agnostic and written against
the project discovered at runtime. Copy the structure, not the words.
