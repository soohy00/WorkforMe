# project-design-technical.md — first-cycle foundation design (working decisions)

Establish the project's **working decisions** with the user — how documents are classified, delivered,
written, reviewed, and stored in this project. This is the **present** mode (the knowledge of the
options lives with *you*; the user speaks in generalities — translate them into concrete options +
trade-offs, the user decides). The floor below is what the ELICIT loop must close on the working axis;
depth follows the CALIBRATE character. Order is gap-driven, not a fixed phase — working decisions
interleave with the business and stakeholder model and lean on it (a stakeholder fact triggers a
working question and vice versa, `elicitation.md`).

It is the opposite of model design. The model *draws out* what the user knows; working decisions
*present* what the user may not have framed, as options the user chooses among. The user says a
generality ("keep it confidential") → you translate it into concrete choices ("Confidential with named
recipients, or Internal with the revenue figures generalized — the first limits forwarding, the
second lets the whole team read it") → the user decides → their language narrows → repeat.

**Floor, not ceiling.** You know how to present working options. This file blocks the failure modes
and lays the floor; which options to present, in what order, is your judgment.

## Failure modes and guardrails

- **Silent decision (the core one).** Never settle a working direction without user approval.
  Translate the generality into concrete options with trade-offs and let the user pick — don't quietly
  choose the default and move on.
- **Over-engineering.** When a process is heavier than the CALIBRATE character warrants (a four-step
  approval route for a two-person team), detect it and surface it with your reasoning. Don't shrink it
  unilaterally — the user decides.
- **Tool-locking.** Don't presuppose a specific workspace, mail, or office tool. Offer the *kinds* of
  channel and their trade-offs; the company's actual tools are discovered from the user.
- **Classification generalities.** Don't stop at "handle it carefully." Concretize until this
  project's classification scheme, the level each recurring reader may receive, and the project's
  sensitive items are settled by user confirmation (`classification.md`). A company scheme, if one
  exists, overrides the default.
- **No conventions established.** Entering `go` with no conventions lets the writer invent them
  arbitrarily. Establish at least the minimal standards (terminology source, number and date format,
  tone per reader, file naming) with the user.

## What to cover (proportional to CALIBRATE depth)

The areas a typical project's technical floor touches — **common, not a fixed catalog.** A given project
may add others (templates the company requires, translation, recurring schedules, ...) or legitimately have almost nothing in one.
Cover what *this* project's character implies, not all four by rote.

- **Classification** — the scheme, recipients per level, sensitive items (`classification.md`).
- **Channels and formats** — where each kind of document goes (a workspace page, an email attachment,
  a shared screen) and in what form.
- **Writing conventions** — the terminology source, number/date/currency formats, tone per reader,
  file naming and versioning.
- **Review and storage** — who reviews and approves which kind of document; where finished documents
  are stored and what may be backed up where.

Scale to the character: a short internship is "adopt the default + a one-beat confirm" per area; a
long engagement with outside readers is "design each area deeply." The depth comes from the
character, not a fixed amount of ceremony.

## Depth floor

- Every working decision is **settled by user confirmation** — no solo agent decision.
- Every decision that has a trade-off was presented as **options + each trade-off**.
- The classification policy is this project's **specific** policy, not a generality.
- **No open working question remains.**

The ceiling is open.

## What this produces

The confirmed working decisions, recorded in the handoff's Project Foundation
(`foundation-format.md`, "working decisions" section) — only decisions the user confirmed. `go` uses
them as context while writing, and later turns them into `security.md` + `standards.md` +
`operations.md`.

## Universality guard

Stack- and company-agnostic. Options are presented as kinds-of-approach with trade-offs; the
concrete tools and rules are the user's decision at runtime, never assumed or named as a rule here.
