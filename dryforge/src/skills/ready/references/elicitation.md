# elicitation.md — ELICIT (realize the user's intent)

The heart of the front door: a real conversation whose **one job is to realize the user's intent** —
to understand the user deeply enough that the spec written from it is *their* design, not a stranger's.
It replaces a human design partner, so it *actively asks*, but never asks just anything.

## The one rule (everything below serves this)

> **Realize the user's intent. Ask well. Never pass over the unknown.**

The discipline underneath every decision is **understand vs. guess.** For each load-bearing decision
you face, exactly one of two things is true:
- **You understand the user's intent on it** — they said it, or it follows from what they said + the
  project material + their established goal/values. Then *realize it* — that is their intent, even though
  your hand wrote it.
- **You do not** — you'd be a stranger picking a "reasonable default." That is a **guess**, and a
  guess on a load-bearing decision is **forbidden**. Close the gap by the right method (below): the
  decision is not yours to default.

There is **no third option** ("pick a sensible default and move on"). "Move on from a load-bearing
unknown" is the failure that detonates later — the agent decides what the user would have decided
differently, and it surfaces as rework, a document that argues for the wrong thing, a commitment the
user never agreed to, a wrong number in front of a CEO or an investor, or "who decided this?" in the
meeting. *A reasonable default by someone who hasn't understood this user is still a guess.*

**Floor, not ceiling.** This is guidance, not a script — never hardcode question lists or stack
choices; specifics are discovered at runtime. Floor-not-ceiling lifts the *ceiling* on how well you
elicit; it never lowers the *floor* of "no guess survives on a load-bearing decision."

## The two methods — by where the knowledge sits (both serve the one goal)

You reach understanding by one of two methods, chosen per decision by **who holds the knowledge.**
Both converge on the same thing — the user's intent.

| The decision is... | knowledge sits with | method | how |
|---|---|---|---|
| **content** — what the document says: claims, facts and figures, commitments, scope, priorities, what is asked of whom, the reader's situation, what is sensitive | the **user** | **EXTRACT** | draw it out ("when the reader asks X, what is our answer?"). The user knows; you must not invent. Mine to the end. |
| **form** — how the document says it: kind, structure and order, which parts become visuals, length allocation, tone mechanics, channel mechanics | the **agent** | **PRESENT** | translate the user's generality, *grounded in the content you've extracted*, into concrete options + trade-offs, recommendation first; the user chooses. |

These are not two phases that take turns — they are two *ways to not-guess*, interleaved as the
dialogue needs. Crucially, **PRESENT depends on EXTRACT**: you cannot present the right structure or
visual until you understand the reader and the content they must serve. So content understanding
leads, and form decisions are presented *against* it.

**Spend questions asymmetrically — but the asymmetry is about *method*, not *permission to skip*.**
Content intent: extract deeply (only the user holds it). Load-bearing form: present (default +
trade-off, the user decides in one beat — *never* silently defaulted; a silent form default traps the
user who didn't know to object — e.g. a one-page summary chosen for a reader who needed the full
reasoning). Genuinely trivial (changing it costs the user
nothing and has no downstream weight): decide it — *that is not a guess*, it's understood-as-not-caring.
What is "load-bearing" is a runtime judgment (would changing it force rewriting downstream, or would
the user plausibly have a preference?), never a fixed list.

## Build a model of the user (this is how you *understand* rather than guess)

Understanding is not a feeling — it is a **model of the user you build and maintain as you talk**:
- their **goal** (what they are really trying to achieve with this document — often not the literal
  request: not "a report" but "get the CEO to approve two more weeks"),
- their **values / priorities** (what they keep returning to — e.g. a word repeated three times is a
  core value, not filler),
- their **constraints** (a deadline, a length, the channel, their position — an intern writing to a
  CEO is not a director writing to a board, what must not be shared),
- the **domain facts** they've given (and where each came from),
- the **reader model** — for each reader: what they already know, what they don't, what they worry
  about, what they decide, the words they use.

Every load-bearing decision is tested against this model: **does the model *ground* this decision?**
- Grounded → realize it (understood — derived from the user, even if they didn't say it literally).
  *This is how you avoid asking the derivable (don't re-ask what the model already settles).*
- Model is **silent** here → this is exactly the gap. You don't get to fill a model-silence with a
  default — you close it (extract or present). Model-silence on a load-bearing point **is** the guess.

This makes "understand vs. guess" *operational and checkable*: a decision you can trace to the model
is the user's; a decision the model can't ground is a stranger's. The richer your model, the more you
can realize without asking — and the fewer guesses hide as "reasonable defaults."

## Scope by cycle — first establishes the foundation, delta works within it; **both equally rigorous**

The cycle changes *what you must understand*, never *how rigorously you avoid guessing.* Delta is
**not** "lighter" — the intent for this task must be just as fully realized as in a first cycle.

- **First cycle (no harness): a forced foundation design.** You must establish the project's
  foundation — its domain model and its technical decisions — from scratch, because nothing holds it
  yet. Force-load `project-scoping.md` (CALIBRATE: character → depth), then run the **domain extraction**
  (`project-design-domain.md`) and the **technical presentation** (`project-design-technical.md`).
  **Their floors are non-negotiable, not loop-optional:** the domain **breadth guard** (you may not
  close without asking "are there other major entities/features/rules?"), the domain **depth floor**
  (every concept has its four facts; every rule is testable), and the technical **no-silent-decision**
  rule (every load-bearing technical decision settled by the user, presented as options). These are
  the structures that *force* understanding over guessing while the foundation is being laid — do not
  dilute them into a light pass. Scope = project foundation + this task.
- **Delta (harness exists): task intent within the foundation — with the same rigor.** Do **not**
  re-run foundation design (the harness holds the organization, the readers, the service domain, the
  writing and classification rules — read the floor from it, don't re-ask what it answers). But the
  document's load-bearing intent must be realized with the **full** "no guess survives" discipline:
  extract its content, present its form, run the same generation and the same exit check. Scope =
  this document only; rigor = full.

## Account the decision surface — enumerate the obligations, don't wait to be told

The user names a fraction of what's load-bearing; you must surface the rest (the decisive difference
from tools that only tidy what was said). But **naming is where this fails silently** — you don't
sweep what you never named (a real failure: an agent wrote one document "for the team" without ever
surfacing *who the primary reader is* as a decision, and the designer and the CEO each found it
written for someone else). An implicit "did I cover enough?" feeling is the weakest move
(self-judgment). So **make the surface explicit: enumerate the load-bearing decisions this document is
*obligated to answer*, then account for each.**

**1. Name the entities first (a manifest).** List every reader and stakeholder, and every thing the
document talks about — features, screens, metrics, money, dates, teams, vendors, earlier decisions,
other documents it must agree with — you cannot enumerate a decision for an entity you never named,
so this bounds the surface. (The breadth guard, materialized: before closing, also ask "is there one
we haven't named?")

**2. Walk five lenses over each entity and each colliding pair to surface obligation-slots** — a slot
is *a question the document must answer or it isn't a design*:
- **READER** — who the **primary** reader is (one — a document written for everyone is written for no
  one) and who else reads it; per reader: what they already know, what they don't, what they worry
  about, what they have authority to decide, the words they use (a CEO reads money · risk · time; a
  designer reads users · flows · states; a developer reads rules · exceptions · data · boundaries; an
  investor reads progress against what was promised). The lens whose absence lets a one-size document
  through; never skip it.
- **OUTCOME** — the **one** action the primary reader takes after reading (approve / choose / start
  building / give feedback / only understand), by when, and what counts as the document having
  worked. **Name the kind first** — an approval, an escalation, an alignment, and a results report
  need different things.
- **CLAIM** — the key message in one sentence; each claim's evidence and its source; what the
  document commits to and what it explicitly does not (scope); risks and their handling; the
  objections this reader will raise. The *combination* of two concepts creates unsaid edges ("the
  deadline moved earlier" + "the scope is unchanged" → "who absorbs the cost?"; "an investor reader" +
  "an internal estimate" → "shown as an estimate, or left out?"): walk the colliding pairs.
- **FORM** — document kind, channel, length, the parts that text alone would leave open to different
  readings (a flow, a state change, a structure, a comparison, a timeline — each a visual candidate),
  tone and formality, and the **classification level and recipients**.
- **ALIGNMENT** — for a document that coordinates people: what is settled / open / to be decided now,
  and per open item its owner and due date; for designers — flows, screens, and every state (empty,
  loading, error, no permission) and edge case; for developers — rules and exceptions, data,
  integrations, permissions, and acceptance criteria written so "was this met?" is decidable.

These lenses are **accelerators for spotting, not an exhaustive catalog**: if a load-bearing slot fits
none, your lenses are incomplete for *this* domain — name the new one, don't force-fit. (The floor is
"no slot left a silent guess," which is lens-independent; the lenses only lift the ceiling.)

**3. Enumerate ≠ ask — the over-asking firewall.** Enumerating is cheap, internal, and exhaustive;
*asking* is expensive, user-facing, and minimal. Resolve each slot in this **fixed order** before it
may become a question:
1. **The user-model grounds it** (said / derived from the model / a chosen option)? → realize it,
   **don't ask** (the derivable — see "Build a model of the user").
2. **A tuning value inside an already-settled mechanism** (conventional default / tuned-later, no user
   preference)? → record a sensible default **marked tunable**, **don't ask**.
3. **Survives both = `assumed`** (load-bearing, model-silent — you'd pick it as a stranger). This is
   the guess. → **ask** it (content = extract, form = present).

So the surface is enumerated *exhaustively* (completeness) while questions stay *minimal*:
only `assumed` slots become questions. **An `assumed` slot may not survive into the spec** — that is
the exit bar, now *observable* (below) rather than a feeling.

The three probes in `gap-analysis.md` (kind-silence, completeness-sweep, consistency-coupling) are
concrete slot-finders that populate the lenses; the risk-proportional lenses in `intent-review.md`
press the high-stakes slots harder. The accounting is **ephemeral working memory** — it drives the
exit scan and feeds the independent backstop, then evaporates; it is **never** written into the spec
as provenance tags (`output-format.md`).

## Ask well — so the user can actually answer

A generated candidate is not yet a question. Throw only what survives:

1. **grounds-gate** (`grounds-gate.md`) — a confident question can state its site, why it isn't already
   covered, and the consequence. This filters noise so the dialogue isn't "have you considered
   concurrency?" spray. (It does **not** let you drop a *load-bearing* candidate by under-arguing —
   `grounds-gate.md`.)
2. **Lead with a recommendation / default.** Never throw a question empty-handed. For content, lead with
   a concrete conception the user adjusts; for form, lead with the recommended option + trade-off.
   A concrete proposal is faster to answer than a blank slate. (This is *how you present*, not a
   license to default — the user still decides.) For content, a proposed key message the user edits
   ("Shall the key message be 'the pilot cut support time by 30% in three months'?") beats "what is
   your key message?".
3. **Right-sized rhythm.** Highest-leverage first; batch a few related questions when it serves the
   user (platform limit: at most 4 questions / 4 options per structured prompt). Don't pad with
   low-value questions to look thorough — but "don't pad" bans *trivia*, it **never** excuses skipping a
   load-bearing one. When unsure if something is load-bearing, surface it: one question costs a beat; an
   un-surfaced load-bearing decision costs a wrong-direction build.

**Delivery.** When options are enumerable, prefer the platform's structured-input tool (2–4 options,
recommended first labeled `(Recommended)`, "Other" allowed); pure open questions stay plain text.
Give each structured question a **very short header/label (a word or two)** and keep option labels
short — an over-long header/label, or more options than the cap allows, makes the structured tool
**reject the call**. If the structured-input tool ever rejects or fails, **immediately re-ask the same
question as plain text** — never stall or dead-end on a tool error.

**For a CONTENT (extract) question delivered as choices, an explicit open option is MANDATORY** — a
"none of these — here's mine" / "I have a different idea" choice *visible among the options*, not just
the platform's generic "Other". **The open option counts toward the 4-option cap** — so a content choice
question carries **at most 3 substantive options + the open one** (4 total); if more substantive options
than that are in play, drop to **plain text** rather than overflow the cap (overflowing rejects the
call). Content knowledge is the **user's**; your options are a *scaffold / recommendation*, never the
boundary of what they may answer — boxing a content question into your 3 options is the opposite of
extracting (you'd cap the user's own model with yours). A genuinely open content question (where you
can't even enumerate sensible options) is better asked as **plain text**. (Form *present*
questions, where the option space is legitimately yours, don't need the mandatory open option — there
the recommendation is the point.)

## Mandatory: the load-bearing document shape is surfaced

A spec needs a target document shape, and the request rarely states it. So before leaving you MUST
have **settled** the load-bearing shape — the **primary reader**, the **outcome** (the one action
after reading), the **document kind and channel**, the **classification level and recipients**, and
**which parts become visuals** (or that none do, and why). **The kind alone does not satisfy this** —
"a proposal" does not settle who approves it or what they are asked to approve. Reader and outcome are
content (extract); kind, channel, and visuals are form (present = options + trade-offs + a beat to
decide; never silent). If the project's rules or an earlier document in the same series already fixed
the shape, **confirm** rather than re-ask.

## Exit — you may write the spec only when no guess survives on a load-bearing decision

Stop and proceed to SPEC **only when all hold** (not merely when the user says "that's enough"):

1. **The decision surface is accounted** — entities named (manifest), the four lenses walked over each
   entity and each colliding pair, and **every load-bearing slot is `grounded`, `deferred-tunable`, or
   was asked-and-answered. No slot is left `assumed` (a silent guess).** This is observable — a scan
   over the enumerated surface — not a feeling.
2. **Every load-bearing decision is grounded in the user** — traceable to what they said, to the model
   you built (derived + the user wouldn't object), or to a presented option they chose. **No
   load-bearing decision is a default you couldn't ground.** The load-bearing unit is the
   **decision / mechanism / policy the user has intent on**, *plus* any **value the user would
   genuinely have a preference on** (which side wins a contested case; how strict or lenient a policy
   is; a direction). Surfacing a yes/no for a mechanism does not settle these preference-values — they
   are grounded too.
   - It does **NOT** include **tuning values** — a detail *within an already-settled form* that is a
     *conventional default* or is *tuned later by feel*, on which the user has no preference (heading
     wording, the order of points inside a settled section, table styling, spacing). That is the **executor's inference** (derivability — the produce/execute boundary):
     record a sensible default *marked tunable* and move on. **Do not force-surface tuning values, and
     do not treat a defaulted one as an un-grounded guess** — forcing each into the dialogue is
     over-asking and breeds false "ungrounded" findings.
   - **The test per value:** *does the user genuinely have a preference on it, or is it a conventional
     default / something they'd tune later?* Preference → ground; default/tunable → the executor infers.
     (What is a "mechanism" vs a "tuning value" is judged per project at runtime — never a fixed list.)
3. **Load-bearing document shape settled** (reader, outcome, kind and channel, classification,
   visuals), the floor of the document's kind met (`doc-types.md`), and — first cycle — the
   foundation floors met (breadth guard, depth floor, no open working decision).
4. **No material gap remains** — only trivia the user need not decide.

A clean record of this is simply the spec itself: every load-bearing decision appears as a settled
rule, and the **non-derivable ones carry their reason in the thinking-base** (`output-format.md`) — in
the user's own terms, as prose, *not* machine tags. If a decision is load-bearing and you cannot write
its rule from understanding (only from a guess), the exit bar is **not** met — close it.

**A thin input raises the bar — it does not lower it.** Few signals, big gaps → ask *more*, mine
*harder*. Producing a thin result from a thin input is the exact failure this front door exists to
prevent. A self-assessed "low-blast" call scopes *dialogue length*, never the generation's coverage —
every entity the goal touches is named and swept regardless.

## The gate is insurance, not your safety net

There is a downstream independent check, but **elicit as if it does not exist.** A load-bearing guess
that reaches it is an **ELICIT failure** — you closed while a decision was still a stranger's. Told a
check exists, an LLM drifts to "do the minimum it'll pass" — that is **reward-hacking**, laziness in
the costume of "the backstop will handle it." Your objective is *this dialogue realizing the user's
intent*, never "a doc that passes." Independent checking exists because you (A=A) cannot fully see your
own guesses — so one **independent** check audits your decision surface before the spec freezes
(confirming each `grounded`/`deferred` disposition is real, and hunting any obligation-slot you never
enumerated) and routes its findings back to the user (`intent-completeness.md`). It is a backstop on a
*small* residual, never a substitute for the work.

**Don't churn clean input.** A part already well-grounded has nothing to convert — there the value is
*verify + promote* (confirm an assumption against the project material, promote it to a fact, escalate on
conflict). Don't hand a resolvable uncertainty downstream as a hedge.

## Terminology

- **spec = the contract** (binding WHAT; ground truth; authority). **plan = a provisional blueprint**
  realizing it. A task's content is a **content contract** (the section's job for the reader, its
  claims and facts, what to verify), not premature prose; don't call the plan "the contract."

## Universality guard

No concrete stack, framework, library, or tool name — and no company, service, or industry name —
appears in this file or the skill. All guidance is stack-, company-, and language-agnostic; the actual
organization, readers, and the user's language are discovered at runtime from the material and the
dialogue — never assumed.
