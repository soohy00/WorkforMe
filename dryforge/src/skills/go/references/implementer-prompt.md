# implementer-prompt.md — the writer subagent prompt

One subagent writes one part of the document, **verified-first** (question-first where it fits), in
its pinned worktree, then commits and reports. (The file keeps its upstream name; the role is the
*writer* of a document part.) The prompt has **required elements** (mandated — the scaffold)
and **wording you adapt** (the example below is one phrasing, not a fixed script).

## Required elements (every implementer prompt must pin)

- **Task contract** — the part's job for the reader and its **work targets (files | state |
  external resource)**, from the plan (a content contract, not premature prose). **Defer plan-owned
  decisions to the plan — do not restate them.** Terms, figure names, file names, and the heading
  outline the plan already fixes must be referenced ("use the plan's terms"), not re-specified in
  the prompt: a prompt that restates them in different words makes parallel writers diverge. Pin only what
  *this* task adds. For a task that declares **no file diff** (a state-change / operational /
  external-config target), verification is by **commit message + captured external evidence**
  (command exit / render / API or state response), not necessarily a file diff — the
  captured-evidence floor still holds.
- **Spec section** — the spec content this part realizes, **quoted inline in this prompt**: the
  reader and their situation, the claims and requests of this part, the **fact-ledger rows** it may
  use, and the **reader-check questions it owns** (the task worktree has no `.dryforge/` files to read
  — `.dryforge/` is gitignored). Write to the spec, not just to the task line ("correct" = matches the
  spec).
- **Hard gates** — the relevant non-negotiable constraints from the handoff, always including the
  classification level and what it forbids, and what the document must never say or promise.
- **Verify-first, right-sized** — drive the work against the part's **real verification gate**: the
  reader-check questions it owns and the fact trace of every figure, date, name, and quotation it
  uses. **Consume the producer-set tier — don't re-derive "is this risky?" from scratch.** This task
  is classified RISK=<tier> by the producer. RISKY → question-first: before writing, list the
  owned questions and confirm each is **unanswerable** from the empty part (RED); write the part;
  then, for each question, quote the sentence that answers it (GREEN), and build the fact-trace
  table. MECHANICAL → a confirming fact trace and one pass over the owned questions, no RED
  ceremony. NONE → appropriate evidence (the assembly joins every part in order, the headings
  render), no question ceremony. If the tier looks wrong for what you find, return
  `DONE_WITH_CONCERNS` and say so — do not silently upgrade or skip. If the producer omitted the tier,
  judge risk yourself. The floor is *captured-evidence verification*, not ceremony — **but a figure
  left untraced or an owned question left unanswerable is still needs-fix**. (Your own answers are
  not the acceptance test — the orchestrator's independent reader check is; your job is to hand over
  a part that can pass it.)
- **Shared-write constraints** — which part file is this task's to write, and which **not** to
  touch (the assembled document and any shared glossary or index a later assembly step owns).
- **Worktree pin** — the absolute worktree path + branch; **omit isolation** (do *not* enable the
  platform's worktree-isolation dispatch option — the orchestrator already
  created the worktree; see `orchestration.md`); verify with `git rev-parse --show-toplevel` before
  editing.
- **Report contract** — commit when done; return the structured summary below. Do not dump diffs.

## Example skeleton (one wording — adapt; the elements above are required)

```
Write <task id / the part's job> in the worktree at <ABS PATH> (branch <name>).
First: `git rev-parse --show-toplevel` must equal <ABS PATH> — if not, stop and report.
Reader: <role and situation>.  Content to deliver: <spec slice>.  Hard gates: <classification +
must-not-say>.  Facts you may use (and no others): <fact-ledger rows>.  Questions this part must
answer: <owned reader-check questions>.
File yours to write: <parts/NN-name.md>.  Do NOT touch: <assembled document, shared glossary>.
This part is RISK=<tier>: RISKY → question-first (confirm each owned question is unanswerable from the
empty part → write → quote the answering sentence per question) + fact trace; MECHANICAL →
confirming fact trace + one pass over the owned questions; NONE → assembly evidence. Show an
`unconfirmed` fact as unconfirmed in the text. If the tier looks wrong, return DONE_WITH_CONCERNS.
When done: commit, then return ONLY the structured summary. Do not inline the text.
```

## Structured return

- `status`: `DONE` | `DONE_WITH_CONCERNS` | `NEEDS_CONTEXT` | `BLOCKED`
- `files_changed`: paths — or, for a declared no-file-diff task (state-change / operational /
  external-config), the work target touched plus the commit that records it
- `verification`: the **fact-trace table** (each figure, date, name, quotation in the part → its
  fact-ledger id) and, per owned question, the **quoted sentence** that answers it (evidence, not
  "done"). A claimed pass with no trace or no quote is needs-fix; a figure not in the ledger is
  needs-fix (never add a fact the spec does not hold — return `NEEDS_CONTEXT`)
- `concerns`: anything the orchestrator should weigh (or what is blocking)

## escalate-don't-guess (for the implementer)

If the task is ambiguous, conflicts with the spec, or can't be done as written — **do not
guess or quietly improvise.** Return `NEEDS_CONTEXT` or `BLOCKED` with specifics; the
orchestrator decides and escalates to the user if needed. A wrong guess is worse than a stop.

You are in a fresh session with no live user conversation — do NOT ask the user directly. Return
`NEEDS_CONTEXT` or `BLOCKED` instead; the orchestrator relays escalations to the user.

**Honor any shared-resource expectation the task declares** (a shared file, an outside page the plan
says should be in a given state). If you find that shared resource in an
unexpected state, return `BLOCKED` with the specifics — do not work around it silently.
