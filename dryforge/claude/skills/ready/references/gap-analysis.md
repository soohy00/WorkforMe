# gap-analysis.md — ELICIT's generation & detection layer (depth probe + gap probes)

The generation & detection half of ELICIT (`elicitation.md`): how to *measure* where the accumulated
intent falls short of the floor, and how to *generate* the "unsaid" candidates the input never named.
It runs **right after the floor is set** (to fill the initial question set) and **after every
integration** (to refresh it). The probes deliberately raise more than survives — every candidate
they produce clears `grounds-gate.md` before it becomes a confident question.

This is *detection*, not disposition: it surfaces gaps and candidates; ELICIT decides what to ask
(`elicitation.md`), and conflicts/traces handled elsewhere are not re-done here (structural grounding
is ORIENT's, spec↔plan trace is PLAN's trace gate, source conflicts are DECOMPOSE's flags).

## Depth probe — coverage vs floor, per axis

After CALIBRATE has set the floor, measure each axis (reader, claim, classification, alignment, ...) for **depth
proportional to the project's character**: are the rules and claims checkable (a reader could verify
each against its source), or do they stay at generalities? The gap is `floor − coverage`, where *coverage* is the
**measured depth**, not the mere presence of content: DECOMPOSE supplies a **presence map** (what landed
per axis + a **form marker** — bare mention vs. full treatment), and a *touched* axis is **not**
automatically a *covered* one — the form marker is what keeps a thin mention from reading as coverage.

- **Reader depth** — is the primary reader named with what they know, worry about, and decide, or
  only "the team" / "management"?
- **Claim depth** — does every claim carry evidence with a source, or is it asserted? Are commitments
  bounded (what is *not* promised), or open-ended?
- **Classification depth** — are the level and the recipients concrete, or "internal, probably"?
- **Alignment depth** (coordinating documents) — do open items carry an owner and a due date, do
  states and edge cases carry a disposition, or are they "to be discussed"?

Output per axis: a **sufficient / insufficient** read + a concrete pointer to what is thin. An
insufficient axis feeds ELICIT's open question set. Unlike a structural fix, this does **not** auto-fill —
depth is added through dialogue, never invented.

## Three gap probes — generate the "unsaid"

Beyond measuring stated content, three probes catch what the dialogue has been *silent* on. They are
deliberately **liberal** — they raise more than survives — so every candidate clears `grounds-gate.md`.

- **Kind-silence probe** — does the accumulated intent stay SILENT on a standard *kind* of content
  this **document's kind** implies (`doc-types.md`)? For a proposal — the alternatives and the cost of
  doing nothing; for an alignment doc — states, exceptions, acceptance criteria, owners; for an
  escalation — the decision needed and by when; for an investor report — progress against what was
  promised last time, and the bad news; for meeting material — what gets decided today. If silent on
  a kind its document implies, do **not** invent the content (no fabrication) — surface the silence
  as a candidate.
- **Completeness sweep** — when a requirement is cross-cutting (every figure has a source, every open
  item has an owner, every screen has its error state, every recipient is allowed the level),
  enumerate **every** site it must apply to and flag any missing site.
- **Consistency-coupling probe** — when the document **restates something that lives elsewhere** (a
  figure also in last month's report, a date already sent to the designer, a scope already approved,
  a term the project defines), check the project's earlier documents and rules for the **existing
  value**. A document that silently disagrees with what the reader already received breaks trust —
  flag each such site so the spec either matches it or states the change explicitly ("was X, now Y,
  because Z").

These three are **concrete slot-finders that populate `elicitation.md`'s decision-surface lenses** (the
OUTCOME kind-sweep and the CLAIM colliding-pair walk) — the lenses say *what kinds* of
obligation to enumerate; these probes mechanically surface the candidates. Cross-stack testing showed roughly half of what they raise are false positives,
which is exactly why they are paired with the grounds gate: never escalate a candidate you can't
ground.

## When a summary isn't enough

If the in-session context can't settle whether an axis is thin (you need to see a specific earlier
document or received file), read the narrow, specific path inline — ELICIT is inline (no subagent dispatch — those belong to the
two independent checks, intent-completeness and the 3-doc-gate). This is a pinpoint follow-up, kept small.

## Universality guard

Stack-agnostic. The axes, the silence kinds, and the collection cardinalities are whatever this
project actually is — discovered at runtime; no stack assumed, no fixed property checklist imposed.
