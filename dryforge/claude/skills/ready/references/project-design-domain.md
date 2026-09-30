# project-design-domain.md — first-cycle foundation design (business and stakeholder model)

Extract the project's **business and stakeholder model** from the user: (1) the **service domain** —
what the company's service is, its entities, rules, states, metrics and how each is defined, and its
terms; (2) the **stakeholder model** — the roles around the project, who decides what, how work is
handed over, and the recurring readers with what each needs from a document. Documents fail at both:
a wrong rule stated to a developer, a date promised by someone who could not approve it. This is the **extraction** mode (knowledge
lives with the user; you must draw it out — never invent it), and the thickest first-cycle
reference, because domain knowledge is the hardest to extract systematically and the most damaging
to get wrong. The domain floor below is what the ELICIT loop must close on the domain axis once
CALIBRATE has confirmed the project's character; depth follows that character. Order is gap-driven,
not a fixed phase after technical — but domain naturally leads early in a first cycle, since the
technical decisions depend on it (`elicitation.md`).

**Floor, not ceiling.** You already know how to hold a domain conversation. This file does **not**
script it — it blocks the failure modes you fall into and lays the depth/breadth floor. The ceiling
is open: how you lead, in what order, is your judgment.

## Asymmetric depth — but domain is always deep

Spend depth where the domain is core; go light on the peripheral (don't fatigue the user). **But:**
even when CALIBRATE judged the project "small," do **not** compromise the *accuracy* of a domain rule.
A small project has *fewer* rules, not *shallower* ones — each rule still meets the depth floor below.

## Failure modes and guardrails

- **Surface-skimming.** Receiving a feature's name or a person's title is the *start*, not the end.
  Dig until the feature's rules are at a verifiable level and the person's decisions are named —
  keep pressing past the label.
- **Guessing who decides.** Never infer decision ownership from a job title ("the PM probably
  approves scope"). Who approves scope, dates, budget, release, and external communication is asked,
  never assumed.
- **Metric without a definition.** A metric name is not a fact. Pin what is counted, over which
  period, from which source — two teams' "active users" are rarely the same number.
- **Missing implicit rules.** Don't capture only what the user said aloud. For *every* identified
  concept, confirm its **lifecycle** (created → changes → destroyed) and its **exceptions** (what
  happens off the normal path). The unspoken rules live in those two places.
- **Accepting vagueness.** No vague modifiers ("appropriate," "suitable," "as needed") survive into
  the spec. Dig until each is concrete.
- **Document bleed.** Use no document-layout terms in model design. Not "which section says it" but
  "what is true." The model is the business and the people, not the page.
- **Rule fabrication.** Every rule must come from the user's words, or be one you derived and the
  user confirmed. Never bake in a rule no one stated.
- **Domain-term confusion.** Where the same word means different things in different contexts,
  distinguish and pin each meaning explicitly.

## Depth floor

- Every identified concept has all four: **what it is / what it does / what it cannot do / what
  happens when it ends.**
- Every rule is checkable (state it so a reader could check a document's statement against it).
- Every metric has a definition, a period, and a source.
- Every decision type the project touches has exactly one owner role; every recurring reader has
  what they act on and what they need to act.
- No vague modifier ("appropriately," "if needed") remains in the spec.
- Mechanism, not just outcome: "when condition A and condition B hold simultaneously, transition to
  state X," not "becomes state X." Each "must" paired with its "must not."

## Breadth guard (against laziness / premature closure)

Depth and breadth are independent — meeting the depth floor on the concepts you found does **not**
mean you found them all.

- Before ending model design, **explicitly ask the user "are there other major features / rules /
  people / readers?"** Do not close without this confirmation.
- A satisfied depth floor with no breadth confirmation is **not** a valid close.

## Cross-validation (interactions between concepts)

Per-concept lifecycle checks don't surface the edges where two concepts *meet*. Check the
interactions and dependencies between identified concepts: when concept A changes, what is its
effect on concept B — and who must be told? (A price change touches the investor report's revenue
line and the support team's scripts.) The edge cases that bite live at those junctions — a lifecycle pass on each
concept in isolation will miss them.

## What this produces

A business and stakeholder model captured at the depth/breadth floor above: the service's entities
and their relationships, state transitions (possible and forbidden), metric definitions, explicit
edge-case dispositions, and term definitions; the roles, decision owners, hand-offs, and recurring
readers. This is recorded in the handoff's Project Foundation (`foundation-format.md`) as the **whole
project's** model — non-executable context. *This document's* WHAT lives in `spec.md` (what `go`
writes); the Foundation is read as context. `go` later turns the model into `business-rules.md`,
`stakeholders.md`, and `audiences.md`.

## Universality guard

Stack- and company-agnostic. "Entity," "state," "rule," "role" are model concepts; the actual
business and organization are whatever the user describes, drawn out at runtime. No company,
industry, or tool is assumed.
