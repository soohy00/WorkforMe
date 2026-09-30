# dependency-calc.md — the Execution Graph

The **last** step of PLAN: after the spec is frozen and the plan prose is written, compute the
machine-readable scheduling skeleton. The schema is in `output-format.md`; this file is *how*
to fill it. Compute it once here — go follows it and never re-judges dependencies.

## The skeleton is not a task

The document skeleton (the output folder, the part files, the classification header, the title
block, the heading outline) is **not a plan task**. `go` creates it inline before dispatching writers.
Do not create a skeleton task in the Execution Graph. Exception: if setting up the skeleton itself
needs investigation (collecting many received files into the project, rebuilding an existing
document's structure), it may appear as a task, but this is rare.

## Encode two things; leave the rest

The graph encodes only:

- **`depends`** — per task, the task ids that must finish first. The only encoded judgment.
- **`regen_barriers`** — cross-cutting steps between waves (`after: [ids]`, `run: "<cmd>"`).

Do **not** encode produces / consumes / shared_write / waves:
- produces/consumes are the *reasoning you use to derive `depends`*, not graph fields.
- **waves** are derived by go (topological sort of `depends`, then ≤8-concurrent batches).
- **shared_write** is a prose hint (below), with a runtime safety net.

## Deriving `depends`

For each task ask: does it **consume** something another task **produces** — a figure or term a
part defines, a visual a section explains, a conclusion a summary restates? If so, it depends on that
task. The **first screen** (title, key message, summary, request) consumes every part it summarizes,
so it depends on them — write it last, even though it is read first.

- **Complete *and* minimal** — go topologically sorts `depends` into waves, so
  accuracy cuts both ways:
  - **Miss a real edge** → a consumer runs before its producer exists → it breaks at
    integration (the summary promises what the section never says; two parts define the same term
    differently).
  - **Add a spurious edge** → work that could run in parallel gets serialized → lost parallelism.
- Encode every genuine producer→consumer need and nothing else. Tasks with no real edge share a
  wave (run in parallel).

**Beyond artifact consumption.** Are any tasks ordered by something other than content — a part
that needs a figure the user will only confirm later, a part updated in an outside tool? If so,
declare an explicit `depends` even with no file consumed. And for **external shared state** — tasks
writing the same outside page or workspace with no local file collision — declare a serialization
point (a writer task the others `depends` on); otherwise record the safe-parallel assumption in the
handoff. ORIENT surfaces these project-specific constraints.

## Task risk tier (optional)

Per task, optionally classify the content risk. It sizes the writer's **per-part verification
ceremony** and, for a single-task wave, go's execution mode; it does not set review topology. The
field shape is `risk: RISKY | MECHANICAL | NONE`. It is **optional**. If omitted, the task is
unclassified: go leans toward stronger verification, and the implementer still judges test ceremony
at build time (no break). When present it is visible in the 3-doc the user reviews before go runs.

Derivation heuristic (a **floor, not a checklist** — judged per task):

- **RISKY** if the part carries figures, commitments, a request or decision, classification-sensitive
  content, rules and edge cases a builder will follow, or is the first screen.
- **NONE** if the part is metadata with no new claim (a revision table, a distribution list already
  fixed by the spec). Assembly itself is never a task — `go` does it after every wave.
- **MECHANICAL** otherwise (explanation or background that restates settled, sourced content).

This sizes the writer's per-part verification ceremony — it never changes whether a part is
verified or reviewed, and never touches gate topology. (go may also read the tier to choose a
single-task wave's execution mode — a consumer-side use; the producer only derives and emits it.)

## regen barriers

A step that must run **between** waves because one task changes an input others regenerate
from: a figure index or numbering rebuilt after the visuals land, a table of contents, a glossary
collected from the parts. Encode `{ after: [ids], run: "<command or step>" }`. **The step is
discovered while reading the project** — never hardcode one. Most documents need none. Note for the executor: if the regen *output* is
consumed by a later task, it must be **committed** to the base (and not gitignored), or it
won't reach the fresh worktree of a downstream wave — same propagation rule as the deferred-wiring
commit.

## shared-write (prose hint, not graph)

When several tasks would write the **same** file (the assembled document, a shared glossary, a
figure index), prevent collision with a **single deferred writer**:

- In the plan prose, give each part its own file and tell it *not* to touch the shared file; add one
  assembly step at the **end of the wave** that joins the parts in order.
- This is best-effort. go still backstops it at runtime (changed-file overlap
  detection + merge-conflict). A missed hint becomes a *handled conflict*, not corruption.
- **Shared scaffolding counts too.** The classification header, the title block, and the folder
  every part sits in are needed by **every** parallel task, so they are an implicit shared-write: if
  each task creates them, they collide or disagree. Assign them to the **skeleton step** (go's inline
  setup, so they exist before the parallel wave) — don't leave each part to create them.

## When uncertain, escalate

If you can't confidently determine a dependency, a regen step, or whether a file is
shared-written, **ask the user — don't guess.** A wrong edge breaks waves or kills parallelism.
(escalate-don't-guess.)

## Method fixed, specifics discovered

The *method* (produces/consumes → `depends`; mark regen points; defer shared writes) is
stack-agnostic and fixed. *What* is a regen barrier or a shared file is discovered per project while
reading the material — never assumed.
