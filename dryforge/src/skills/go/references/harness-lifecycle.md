# harness-lifecycle.md — go's harness create / update / archive (force-load)

The operational rules for go's harness step: detecting first-vs-delta, generating or updating the
harness, and archiving the 3-doc. Runs **after the completion gate, before the final review**.
Load alongside `harness-format.md` (the harness spec) — this file is the *process*, that one is the
*spec*.

## First-cycle vs delta — the `status.json` marker

`.dryforge/status.json` is a **local-only marker** (it lives inside the gitignored `.dryforge/`, so
it is not committed — local is by design). Its content is one fact: `{ "initialized": true }`. It is
written at the **successful finish** of a first cycle (after the user approves the harness — see
"Archiving" below) or by `migration` on completion.

- **Marker present (`initialized: true`)** → the harness already exists → this cycle is a **delta**.
- **Marker absent** → this cycle is **first-cycle** (create the harness).

This is the whole detection rule — simple on purpose. Consequences:

- **Pre-finish failure → first-cycle on retry.** If a first cycle fails *before* the marker is
  written (during harness generation, final review, the user gate, or archiving), the marker is
  absent, so a retry re-enters **first-cycle** and regenerates. The in-progress harness files from
  the failed run are unapproved, so overwriting them is correct. The 3-doc stays active (not yet
  archived), so the retry has its sources.
- **Safety guard against clobbering.** If first-cycle is detected (no marker) **but** a harness
  structure already exists on disk (an entry file (CLAUDE.md or AGENTS.md) with the harness
  navigation structure + a populated `docs/`) — e.g. a fresh clone where the committed harness is
  present but the local marker isn't — do **not** blindly overwrite it. Stop and ask the user
  whether to treat it as an existing harness (delta) or regenerate. (escalate-don't-guess; never
  destroy a harness you didn't just generate.)

## 3-doc re-read (mandatory, both modes)

Before generating/updating, **re-read `.dryforge/{handoff,spec,plan}.md`.** By this point the session
context is biased toward the document just written; re-reading restores the design intent so the
harness reflects the *project*, not just this one document.

## First cycle — create the whole harness

Sources, in priority: the handoff's **Project Foundation** (`foundation-format.md`) → spec (design
intent) → the finished document and the project's material (fact). The Foundation's richness sets the harness's richness.

- **Foundation is a first-cycle invariant — fail-fast if absent.** `ready` always writes the
  Foundation in a first cycle (`foundation-format.md`, "First-cycle precondition"). So a first-cycle
  handoff with **no Foundation section** is a **precondition violation, not a degrade case** — do
  **not** guess a Foundation from spec + material. **Stop and ask the user to regenerate the 3-doc via
  `ready`** (escalate-don't-guess). This is a one-line precondition check, not a fallback mode.

Generate to `harness-format.md`:
1. If a CLAUDE.md or AGENTS.md exists, back each one up to `.dryforge/backup/`, review it
   critically, propose the disposition to the user, and rewrite only approved content.
2. The whole `docs/` structure (all files).
3. CLAUDE.md / AGENTS.md (identical content).
4. A series AGENTS.md per identified document series (if any).

Map the Foundation to files per `foundation-format.md` (business and stakeholder model →
business-rules + stakeholders + audiences; working decisions → security + standards + operations;
identity → the entry-point overview; future scope → status.md's "remaining"). Future-scope content
with no document yet is correct, not a hallucination.

## Delta — update only the changed scope

1. **Read all current `docs/` files first** and treat them as the existing project constraint — this
   catches non-dryforge hand-edits (there is no separate change-tracking).
2. Identify this cycle's change scope from the **3-doc task scope + the output diff**.
3. Judge which `docs/` files are affected (`harness-format.md`, "which file to touch") — your
   reasoning decides, but reviewing every relevant file is the floor.
4. Apply a **scope-limited** update; leave content outside the change scope untouched (whether
   hand-edited or written by a prior dryforge run).
5. Where this cycle must change something that already holds different content **in scope** →
   **escalate to the user** (don't silently overwrite).
6. status.md every cycle; working-notes.md gets non-obvious facts found while writing;
   decisions/ gets this cycle's trade-off decisions (only if they meet the criterion); findings.md
   updated on find/resolve.
7. A new series → create its AGENTS.md **and** update the navigation tree in CLAUDE.md / AGENTS.md.

**Delta is bidirectional.** Also verify this cycle's change hasn't invalidated an existing statement
elsewhere — updating stale content matters as much as adding new content.

## Archiving the 3-doc (after user approval)

After the user approves (final user gate), **move** the active 3-doc into `.dryforge/NNN/`: copy
`.dryforge/{handoff,spec,plan}.md` into the new `.dryforge/NNN/` (sequential number: highest existing
+ 1, e.g. `001`, `002`, ...) **and then delete them from the `.dryforge/` root.** Archiving is a *move,
not a copy* — after it, the root holds **no active 3-doc** (only `NNN/` archives, `status.json`,
`backup/`, and `deferred.md` when it has lines). This matters: if the root copies are left, the next cycle's producer finds a stale
previous-cycle 3-doc at the root and has to disambiguate + overwrite it; moving leaves a clean root so
the next producer just writes a fresh 3-doc. Then write `.dryforge/status.json`
(`{ "initialized": true }`) if not already present — the marker for the next cycle. (First cycle: the
Foundation is archived with the handoff; from the next cycle the harness carries project context, so
no Foundation is produced.)

## Re-run after a fix

If the final review triggers a fix:
- **Document changed** → re-run the completion gate (the base SHA moved), with the reader check
  bounded as in `reader-check-prompt.md` (affected questions only).
- **Harness text added or rewritten** → the harness re-check (below). Any fix counts — blocking or
  advisory, a lightweight edit included. A fix that deletes only **whole sentences or whole items**
  needs no re-check. A deletion **inside** a sentence — a source tag, a qualifier, a word that points
  elsewhere ("위와", "이 방안") — changes what the rest says and is re-checked like a rewrite.
- **Both changed** → re-run both.

## Harness re-check

One definition, used after the step-9 harness check and after the final review: a **fresh**
subagent with `harness-review.md` **dimensions 3–4** over this cycle's **whole harness diff**, given
the list of fixes and the lines each one added or rewrote, and the dialogue text verbatim. Dimension
4 checks every added or rewritten sentence against the dialogue and the material — a one-line edit by
the orchestrator is the same self-written text the harness check exists for, so it is not exempt.
An advisory the re-check raises is accepted with a reason or fixed by deleting a whole sentence or
item; a fix that would add or change text goes to the user gate instead (so the re-check never feeds
itself).

**Bounded.** A re-run judges blocking findings. The advisories it raises are triaged once
(a document advisory: lightweight fix or accepted with a reason; a harness advisory: as in "Harness
re-check") and do **not** start another re-run. Only a fix to a blocking finding starts a new round,
at most two rounds after the final review; still blocking → stop and ask the user. A fresh reviewer almost always finds new advisories — they are recorded, not
a reason to loop. An advisory a later review raises **again** after it was accepted with a reason is not
new: keep the recorded reason, unless the later review brings a fact the reason did not consider.

Do not approve/archive while a blocking finding is open.

## Out-of-scope review finding

If the final review surfaces a material/harness mismatch in a **harness region outside this cycle's
change scope**, do **not** fix it this cycle — that would break scope-limited delta. Record it in
`docs/tracking/findings.md` (with *why it can't be resolved now*) and leave it for a later cycle or
manual handling.

A **wording defect in the harness itself** outside the scope — an unsourced sentence, a word put on
a person, the docs describing themselves, a writing-guide rule copied into `docs/` — is not a project
problem, so it does **not** go into `findings.md` (the harness describes the project, never itself).
Name it at the user gate and add one line to `.dryforge/deferred.md` (local workspace, not harness):
the file, the sentence, and why it is a defect. The next cycle that touches that file fixes it and
removes the line; the user can also have it fixed by hand at any time.

## Universality guard

Stack- and company-agnostic. What a series, a reader, or a rule is — and which `docs/` file a change
touches — is discovered from the project at runtime, never assumed.
