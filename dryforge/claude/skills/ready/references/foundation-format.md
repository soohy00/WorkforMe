# foundation-format.md — the Project Foundation section (handoff, first cycle only)

The format contract for the **Project Foundation** section of the handoff: the authoring form when
`ready` writes it, and the reading rules when `go` consumes it. Used **only in the first cycle** (no
harness exists yet). Shared byte-identical between `ready` and `go`.

**When it is written.** `ready` writes the Foundation into `handoff.md`'s Foundation section **at the
SPEC step — together with `spec.md`, not deferred to HANDOFF** — so the inline fidelity review can
verify a *written* Foundation (the rest of the handoff's governing parts still wait for the plan and
are filled at HANDOFF). In a first cycle the Foundation is **always produced**; `go` relies on that as
an invariant (see "First-cycle precondition" below).

## Purpose

The first cycle's CALIBRATE and the first-cycle foundation design in ELICIT produce project-wide
foundation knowledge that does *not* belong in spec.md. spec.md carries only **this task's**
execution contract; the **project-wide** foundation — the company and the user's role, the service's
domain, the stakeholders and readers, the working decisions (classification, channels, writing
conventions, review route), future scope — goes in the handoff's Project Foundation. This split keeps
`go` from over-writing (it writes the document the spec describes, not everything about the company)
while giving it project context to write *within*.

## Structure — four fixed sections

Structure the Foundation as **four sections**. Do **not** organize it by `docs/` filename — naming
sections after harness files invites box-filling (reward-hacking) when `go` later builds the harness;
keep the Foundation about the *project*, and let `go` map it to files.

- **Section 1 — Project identity.** The company and its service, the user's role and position, what
  documents the project produces for whom, at what scale, under what constraints (the CALIBRATE
  result).
- **Section 2 — Business and stakeholder model.** The service's entities, rules, states, metrics and
  their definitions, and terms; the stakeholders — roles, who decides what, how work is handed over —
  and the recurring readers with what each needs (the domain-design result). The **whole project's**
  model, as context. The thickest section.
  (Do **not** label individual entities `[implementation target]` / `[project context]` — those
  per-entity tags are clutter, and the distinction is already carried where it belongs: `spec.md` holds
  *this task's WHAT* (what `go` implements), and the Foundation as a whole is non-executable context.
  `go` builds the spec, reads the Foundation as context — no per-entity tag needed.)
- **Section 3 — Working decisions.** Classification policy, channels and formats, writing
  conventions, the review and approval route, storage (the working-setup result). **Only decisions
  the user confirmed.**
- **Section 4 — Future scope.** Documents and milestones planned for the project but out of this
  task's scope. `go` does **not** write them — it is the context for keeping the current document
  consistent with what comes next.

## Labeling rule — separate from the handoff's governing role

Begin the Foundation with an explicit label: *"Non-executable project context — `go` reads this
section as context + harness source, not as an implementation target."* The handoff's existing
governing parts (Document Roles, Hard Gates, conflict resolution, ...) stay clearly separated from the
Foundation, so `go` never confuses a governing instruction / hard gate with project context. The
Foundation is a **conditional expansion inside the handoff's "supplement" role**, not a new authority.

## How `go` uses it (dual use)

- **At execution.** `go` reads the Foundation when it first reads the handoff → it writes the
  spec's document *with* project context. (E.g. a Foundation that records "the CEO approves every
  date that reaches a customer" makes `go` word a delivery date in an alignment doc as proposed, not
  promised.)
- **At harness creation.** Each Foundation area maps to `docs/` files per `go`'s `harness-format.md`:
  business and stakeholder model → business-rules.md + stakeholders.md + audiences.md; working
  decisions → security.md + standards.md + operations.md; identity → the entry-point overview; future scope → status.md's
  "remaining."

## Lifetime

Created in the first cycle only. After `go` creates the harness, the 3-doc (handoff included, with
its Foundation) is archived to `.dryforge/NNN/`. From the next cycle on, the harness takes over the
project-context role, so no Foundation is written.

## First-cycle precondition (Foundation is always present — no degrade)

The Foundation is a **required first-cycle artifact**, not optional: `ready` always produces it
through its first-cycle ELICIT loop. So `go` treats its presence as an **invariant**, not something to
work around. If `go` runs a first cycle (no `status.json`) and the handoff carries **no Foundation
section**, that is a **precondition violation, not a degrade path** — `go` does **not** guess a
Foundation from spec + material. It **stops and asks the user to regenerate the 3-doc via `ready`**
(escalate-don't-guess). (This is a fail-fast check, not a fallback mode — the operational rule lives
in `go`'s `harness-lifecycle.md`.)

## Content quality

The same content-quality bar that governs the harness (non-derivability, work-changing, density,
project-specificity, consequence-of-absence) applies to the Foundation too. A thick Foundation is
normal, but every sentence must carry a core fact — not padding.

## Universality guard

Stack- and company-agnostic. The four sections hold project-specific identity, model, decisions, and
scope in the project's own terms — no company assumed, discovered at runtime.
