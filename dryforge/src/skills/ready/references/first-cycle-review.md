# first-cycle-review.md — the foundation-sufficiency rubric (shared)

The rubric for one question: *is the spec + Project Foundation deep enough to be the foundation of the
whole project?* Adversarial stance — find the holes, don't bless the work. Used **only in the first
cycle**, in **two places** that share this one rubric:

- **ELICIT (generative)** — the first-cycle loop (`elicitation.md`) presses against this floor *during
  dialogue*, while the user is present to fill a gap.
- **3-doc-gate (independent)** — the foundation-sufficiency pass (`3-doc-gate.md`) judges the
  *written* Foundation against this same rubric, from a fresh session that never saw the dialogue
  (the A=A backstop).

Both use the failure modes and floor below; they differ only in *when* and *with what session access*.

**Floor, not ceiling.** The failure modes and floor are the floor; how hard you press each is
risk-proportional judgment.

## Failure modes to hunt

- **Model too shallow** — entity or role *names* present, but rules / metric definitions / decision
  owners / edge-case dispositions missing. A concept without its four facts (what it is / does /
  cannot do / how it ends) is a name, not a model.
- **Model too narrow** — a core feature, person, or recurring reader is missing — the trace of
  closing without asking the user "are there others?" (the breadth guard was skipped).
- **Working decision left open** — a "decide later" / "TBD" survives. An open load-bearing working
  question is a gap (the writer will fill it arbitrarily).
- **Classification generality** — "confidential stuff is handled carefully" with no project-specific
  scheme, recipient levels, or sensitive items.
- **Scoping mismatch** — the design is heavier or lighter than the project's confirmed character.
- **Vague modifiers remain** — "appropriately," "if needed," "as suitable" still present.

## Floor

- Every model concept meets `project-design-domain.md`'s depth floor.
- Every working decision is closed by user confirmation (no open question).
- **Zero** vague modifiers.
- Design depth is consistent with the CALIBRATE character profile.

## On a miss — reopen the foundation gap, don't self-fill

A finding here is one of two kinds:
- **Internally resolvable** (a vague modifier you can concretize from what's already on the record, an
  altitude slip) → fix it.
- **A gap only the user can fill** (a missing business rule, an unknown decision owner, an unsettled
  working decision, a classification policy) → **do not auto-fill it.** Auto-filling a foundation gap bakes a guess into the whole
  project.
  - If found by ELICIT (during dialogue): **reopen the foundation gap in the loop** — add it to the
    open-set and ask, in its mode (model = extract, working decisions = present).
  - If found by the 3-doc-gate (after the docs are written): the orchestrator relays it to the user
    and reopens ELICIT for that gap only → updates SPEC/Foundation (`3-doc-gate.md`).

## Universality guard

Stack- and company-agnostic. The rubric checks depth, breadth, and decision-closure — never
conformance to an organization. What counts as a rule or a working decision is whatever this project
is, judged at runtime.
