# migration-elicit.md — Phase 2 ELICIT (project-wide extraction)

Collect what the material cannot reveal — across the **whole project**, not a single task. This is
independent of `ready`'s `elicitation.md`: that one is task-focused; this is project-wide, with its
own question scope, strategy, and completion bar. The only thing shared is the asymmetric-depth
principle (extract the business, the people, and the readers; present working options).

**Floor, not ceiling.** This is not a script. The guardrails and the depth floor below are the
floor; how you run the conversation is yours. Never hardcode questions or stack choices.

**Calibrate to the project's character first.** Right-size the conversation to what the project *is* —
a three-month internship on one team and a long engagement writing to investors do not earn the
same depth. Read scale, domain density, and outside exposure from SCAN, then spend deep extraction where the domain is core and a light
confirm where it's peripheral (right-sized, effort-proportional). Don't run uniform full-depth
ceremony on a trivial repo, nor a light pass on a domain-heavy one. (State the read in prose, not a
grade — a grade becomes a ceiling.)

## The core frame — self-infer first, ask deeply only where being wrong is dangerous

You have just read the material (SCAN). Use it. Don't ask what the material already answers; do
confirm what would be catastrophic if your inference is wrong. Four cases:

| Inferable from the material? | Wrong is dangerous? | Action |
|---|---|---|
| yes | no | infer, brief confirm ("is this right?") at most |
| yes | **yes** | present your inference, **confirm deeply** (domain rules, invariants) |
| no | **yes** | **ask deeply** (decision owners, classification policy, what must never be shared) |
| no | no | apply a default, skip the confirm |

The load-bearing rule: **"areas where a false belief breaks the whole project" — who decides what,
what may go to whom (classification), the business rules and metric definitions documents will
state, and the user's own role — must be user-confirmed even when the material lets you infer them.**
An org chart shows *titles* but not *who approves a date*; a report shows a figure but not *whether it
may leave the company*. Conventions (tone, format), by contrast, need only a light confirm when earlier
documents show them.

**Thin material RAISES the bar — it does not lower it.** A new joiner with two onboarding slides is
migration's most common *and most dangerous* input: least to infer from, most that lives only with
the user. "The material didn't tell me much" is never a license for a thin harness — it means **ask
more, mine the user harder.**

**Ask grounded questions, not spray.** A confident question can state its **site** (the exact person /
rule / policy), **why the material doesn't already answer it**, and the **consequence** of getting it
wrong. Can't ground all three? Don't press it as blocking — vague "is something missing?" spray
fatigues the user and erodes trust.

## The SCAN map is a ledger — every item must close (observable coverage)

SCAN produces a **manifest**: every entity, person or role, recurring reader, document series,
convention, sensitive item, and *gap* (something a project like this usually has, absent here). Treat it as a **ledger** — each item
must end ELICIT in exactly one **recorded** disposition, so completeness is a *scan over the ledger*
(evidence), not a "did I cover everything?" feeling (evidence-not-assertion):
- **confirmed** — its domain purpose / governing rule is user-confirmed.
- **asked-answered** — surfaced to the user and resolved.
- **N/A — reason** — genuinely not load-bearing here, with the reason recorded.

Drive a question from each open item (translate to the user's language, below):
- **entity** → what it is + governing rules (what it relates to; lifecycle; what's forbidden; how
  its metrics are defined).
- **person / role** → what they decide, what they receive, how they give feedback.
- **recurring reader / series** → what they act on, the form that works, the cadence.
- **convention** (in earlier documents) → intentional standard, or incidental?
- **sensitive item** → which level, and who may receive it?
- **gap** → is the absence intentional, or not yet defined?

No item is silently dropped — an un-dispositioned row is an open question, not a pass. (This is
migration's form of `ready`'s decision-surface accounting: the SCAN manifest *is* the surface.)

## Delivery — structured questions that never dead-end

When options are enumerable, prefer the platform's structured-input tool (2–4 options, recommended
first labeled `(Recommended)`, "Other" allowed); pure open questions stay plain text. Give each
structured question a **very short header/label (a word or two)** and keep option labels short — an
over-long header/label, or more options than the cap allows, makes the structured tool **reject the
call**. If the structured-input tool ever rejects or fails, **immediately re-ask the same question as
plain text** — never stall or dead-end on a tool error.

**For a DOMAIN (extract) question delivered as choices, an explicit open option is MANDATORY** — a
"none of these — here's mine" / "I have a different idea" choice *visible among the options*, not just
the platform's generic "Other". **The open option counts toward the 4-option cap** — so a domain choice
question carries **at most 3 substantive options + the open one** (4 total); if more substantive options
than that are in play, drop to **plain text** rather than overflow the cap (overflowing rejects the
call). Domain knowledge is the **user's**; your options are a *scaffold / recommendation*, never the
boundary of what they may answer — boxing a domain question into your options is the opposite of
extracting. A genuinely open domain question (where you can't even enumerate sensible options) is
better asked as **plain text**. (Technical *present* questions, where the option space is legitimately
yours, don't need the mandatory open option — there the recommendation is the point.)

## Translate into questions the user can answer

Don't ask "what is the decision matrix?" — ask "if the launch date moves, who has to say yes?" Don't
ask "what is the classification of revenue?" — ask "could the monthly revenue figure go to the
investors, or only to the CEO?" Translate the material into plain questions, and translate the
plain-language answer back into the precise rule.

## Existing-docs handling

Existing docs are **reference material**, not authority — they may be stale. Read them, then review
any existing CLAUDE.md/AGENTS.md **critically**: decide what to fold into the dryforge system, what
to drop (already covered by the new `docs/`, or wrong), and what to improve and re-state. Present
that review to the user — what goes where, what is dropped and why — and get approval before
generating.

## Don't fabricate

Extract business and organizational knowledge; never invent it. If the user can't answer and the
material can't settle it, record it as an open question — a fabricated rule or decision owner sends
every later agent confidently wrong.

## Completion bar (observable — a scan over the ledger)

ELICIT is done only when **every SCAN-ledger item is dispositioned** (confirmed / asked-answered /
N/A-with-reason) — a *scan over the ledger*, not a feeling. In particular:
- **Decision owners, the classification policy, and the user's role: user-confirmed, never
  inferred** — a false belief here breaks the whole project (the load-bearing rule above).
- **No "I don't understand why this is here" survives in a dangerous area** (business rules, metric
  definitions, what may be shared) — such an item stays `open`, never silently closed.
- **For every reader and every business rule, the "is there something not in the material?"
  question was asked** — the material shows what was written down; the unwritten rules and
  expectations live only with the user.

The ceiling is open — how you lead the conversation is yours; *what must be dispositioned* is not.

## Universality guard

Stack- and company-agnostic. Every example above is an illustration of a *kind* of question, never
tied to a company. What an entity, a convention, or a classification policy looks like is whatever the
project is, discovered at runtime.
