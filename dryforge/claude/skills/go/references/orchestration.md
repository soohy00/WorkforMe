# orchestration.md — wave lifecycle (force-load)

The mechanics behind the SKILL's per-wave flow: scheduling, dispatch constraints, status handling,
context budget, and failure handling. Loaded for the whole run. The wave lifecycle is a proven
scaffold — keep its structure and the safety constraints; use judgment inside each step.

## Reporting principle

User-facing text = wave completion, blockers, final results. Internal operations (merge, gate,
worktree lifecycle, branch cleanup, dependency install) produce **no text output**. Output tokens
are direct cost.

## Verification Plan

Before the first wave, write a compact verification plan in the orchestrator's working notes:

- the verify set and its purpose (fact trace, classification check, rule check, reader check, any
  named sign-off), and the list of project rules that apply to this document
- which reader-check questions each part owns (the writers' self-check)
- the per-wave gates (fact trace, classification check, rule check) and the completion-gate-only check (the full
  reader check by a fresh reader, on the whole document, once its first screen exists)
- what the fact trace covers (every figure, date, proper name, quotation) and how an `unconfirmed`
  fact must appear in the text

The plan prevents re-deciding verification every wave. Independent checks may run in parallel as long
as each result is captured separately. The completion gate remains the full safety net.

## Wave scheduling

- Topologically sort the plan's `depends` into waves: a wave = tasks with no unmet dependency.
- **Classify each wave:** multiple tasks = **parallel** (worktrees). Single task = **sequential**,
  whose execution mode is set by the task's `risk`:
  - **`MECHANICAL` / `NONE`** → the **orchestrator implements directly on the base** (no worktree, no
    dispatch, no integration gate) — commit on the base, **verify with captured evidence** (same floor
    as a dispatched writer: the part's fact trace captured; an owned reader-check question left
    unanswerable = not done), advance. **You own conformance here — the final review is insurance, not your check.**
  - **Omitted `risk`** → the producer did *not* judge; treat it as **unclassified, not `MECHANICAL`** —
    judge at read time and bias toward dispatch / stronger verification if it shows any behavioral
    surface (degrade-don't-corrupt).
  - **`RISKY`** → **dispatch one subagent in a worktree** + merge-gate (independent verification, A=A
    avoidance; the merge-gate protects the base from risky work). This is the parallel-wave machinery
    with a single task — the final review must not be the *only* independent check on risky work.
  - A **no-file-diff** task always uses the base-pinned-subagent path (next bullet), regardless of risk.
- **Parallel wave:** task worktrees branched from the base; ≤8 concurrent. Integration gate after
  merge catches cross-task interactions.
- **ROI collapse (objective conditions, not a free judgment).** A multi-task wave defaults to parallel
  worktrees. Collapse to **orchestrator-direct on the base** **only** on an objective condition — a
  **single shared outside resource** the parts cannot isolate within (one outside page all parts write to), or a
  **new** project where cross-agent convention drift (terms, tone) outweighs the parallelism. This is a *rule*,
  not a free "ROI doesn't pay" call. **Record the collapse internally** (which wave, which condition) —
  do **not** surface it for a non-technical user to adjudicate (they cannot evaluate a parallelism/
  isolation trade-off, and the terms are internal tokens). Collapsed tasks carry the per-task evidence
  floor and are **reviewed as if independently authored** — collapse removes dispatch overhead, never the
  verification bar. **Collapse does NOT skip the cascade-guard:**
  the conditional mid-run spec-review still fires for any task meeting its narrow bar — **RISKY +
  downstream dependents + deviation-cascade risk** — even when implemented inline. Collapse saves
  dispatch / worktree / merge / per-wave-gate overhead, **not** that targeted guard. (RISKY alone
  never triggers a spec-review — it sizes test ceremony and single-task execution mode, not review
  topology — so "more RISKY" ≠ "more spec-reviews", and collapse stays cheap.)
- **No-file-diff tasks stay off the worktree path.** A task whose declared work targets are
  **state / external only** — its result lives *outside* the tree (a DB migration run, an external
  config applied, a remote registration), so it produces **no file diff** — is handled on the
  **base sequentially** (a base-pinned implementer; verified by commit message + captured external
  evidence per `implementer-prompt.md`), **never dispatched into a parallel worktree.** Two reasons:
  the parallel **merge-gate is file-diff-based** (`git diff base...task` must touch declared targets)
  and would reject its empty file diff; and a worktree isolates *files*, not the external runtime it
  mutates, so parallel isolation buys nothing while costing worktree + dispatch overhead. If
  topological sort places such a task in a multi-task wave, **peel it off** and run it on the base
  before/after the worktree batch — do not put it in the pool. (Recognize it from the plan's work
  targets: files | state | external — a task with no `files` target is this case.)
- **Batch ≤8 concurrent.** If a parallel wave has more than ~8 tasks, split into sub-batches.
- Do not recompute or reorder dependencies — the producer owns the graph. Parse failure / cycle /
  dangling `depends` → **stop and escalate** (producer-side defect).

## Dispatch ROI checklist

Before spawning any subagent, ask whether the dispatch buys at least one of:

- physical file isolation for parallel writes
- independent review perspective for risky/spec-sensitive work
- meaningful context isolation for broad exploration or log/diff analysis
- wall-clock speed from truly independent work

If none apply, keep the work inline. Inline work still needs a commit and **captured evidence**, and
you **own its conformance** — the final review is insurance, not your check. The optimization removes
dispatch overhead, never the verification bar.

## Sequential wave — execution

A single-task wave runs in one of three modes (by `risk` + target type; see Wave scheduling).

- **Orchestrator-direct** (`MECHANICAL` / `NONE` file-diff task; an omitted-`risk` task takes this
  path only after the read-time judgment finds no behavioral surface — see Wave scheduling). The orchestrator
  writes directly on the base — it reads the task's content contract + spec slice itself (no
  prompt authoring, no dispatch), writes the part, runs right-sized verification (capturing the fact
  trace and the answering sentence per owned question), and commits on the base. No worktree, no dependency install, no integration gate, **no
  implementer status protocol** — the orchestrator knows its own state. If the task turns out
  ambiguous, behavioral, multi-file, or riskier than declared, treat it as a **runtime risk upgrade**
  (`graph-contract.md`): strengthen verification (conditional spec-review or final-review focus); do
  not silently push on. **Keep the sawtooth** — load the task's files, work, commit, drop what the
  next task won't need.
- **Subagent in a worktree** (`RISKY`, file-diff task). The parallel-wave machinery with one task:
  create a worktree off the base, dispatch one implementer (pinned to the worktree absolute path;
  do not enable the platform's worktree-isolation dispatch option — the worktree already exists;
  verify with `git rev-parse --show-toplevel`), collect its structured
  summary, then **merge-gate** into the base (strictly ahead + diff touches declared targets).
  Independent verification is the point.
- **No-file-diff task (any risk) — base-pinned subagent.** Dispatch one implementer pinned to the
  **base** directory (again, no platform isolation option); it commits on the base. Verification is the
  **commit message + captured external evidence** (command exit / render / API or state response),
  not a file diff. (A worktree would isolate files, not the external runtime it mutates, and the
  file-diff merge-gate can't verify it.)

**Both dispatched modes:** verify the commit after return (`git log`; for file-diff, the diff touches
declared targets — never trust self-report); **restore the orchestrator's cwd** (subagent runs can
drift it); **subagent output is bounded** (large results → file + digest). **No integration gate** for
a sequential wave — the self-checks run on the cumulative base (which already includes all prior
waves); with a single task cross-task interaction risk is zero, and the completion gate catches
cross-wave interactions at the end.

## Parallel wave — dispatch constraints (safety, non-negotiable; unordered)

- **Do not enable the platform's worktree-isolation option on implementer dispatch** — the
  worktree is already created; omit any isolation so the implementer runs in place, **pinned to the
  pre-created absolute worktree path**, and verify
  location with `git rev-parse --show-toplevel` at the subagent's start.
- **Create worktrees serially, under `.dryforge/worktrees/`.** Each task worktree lives at
  `.dryforge/worktrees/<task-id>` — inside the gitignored `.dryforge/`, so worktrees never sprawl into
  the project tree or get tracked, and cleanup stays contained. Concurrent `git worktree add` contends
  on `.git/config.lock` → create serially. **Worktree pool:** when multiple parallel waves exist,
  create the maximum number needed by any single wave **once** (under `.dryforge/worktrees/`) before
  the first parallel wave. Between waves, reset a pooled worktree with `git checkout <new-base-tip> &&
  git reset --hard` instead of remove + recreate. Gitignored symlinks (dependency shares) survive
  `reset --hard`. After all waves complete, **clean up all pooled worktrees in one batch** (not
  per-wave): remove the worktree entries, the now-empty `.dryforge/worktrees/` directory itself, and
  any task scratch/temp dirs created under `.dryforge/`. **Leave no litter** — once the run finishes
  (3-doc moved into `NNN/` at archiving), `.dryforge/` holds only `NNN/` archives, `status.json`, and
  `backup/` (the active 3-doc lives at the root only between the producer writing it and archiving).
  This avoids repeated create/remove cycles and a cluttered `.dryforge/`.
- **Task worktrees do not contain the 3-doc.** `.dryforge/` is gitignored, so a freshly-added task
  worktree has **no** `spec.md` / `plan.md` / `handoff.md`. Pass every spec slice, task contract,
  and hard gate **inline in the subagent prompt**.
- **Verify the work before merging (objective, not existence-only)** — the task branch must be
  strictly *ahead* of the base (`git rev-list base..task` non-empty) AND its diff non-empty and
  touching declared targets — checked with **three-dot** diff (`git diff base...task`).
- **Restore the orchestrator's cwd after each wave.**
- **Subagent output is bounded.**
- **Practical parallelism ~5–8.**
- **Build tooling (only if the project has any).** A document project normally has no build cache,
  dependencies, or dependency symlinks, and none of upstream's build-cache, dependency-sharing, or
  slash-less-gitignore steps apply. If a project does carry tooling (a diagram renderer, a
  converter), install it once, share it across worktrees, and ignore any symlink with a slash-less
  pattern (`<dir>`, not `<dir>/`) before the first parallel wave.
- **Worktrees isolate *files*, not *runtime*.** Shared external resources (DB, cache, queue, ports)
  are shared across all tasks. Treat mutations as dangerous; on unexpected state drift, **stop and
  escalate**.
  - **Declared shared-resource expectations** (clean-slate / state-agnostic / additive-only /
    forbidden-mutations) are honored per the producer's dependency-calc rules.
  - **Ordering / external-state deps** — `go` honors explicit `depends` and serializes declared
    external-state writers.
  - **Name agent-created ephemeral resources deterministically.** When a task (or scaffold) spins up
    an external runtime resource that takes a name — a container, a service instance, a database
    schema, a namespace, a temp queue — derive the name from a stable identifier (project +
    task/wave id), **never a random name.** Random names leak (the orchestrator can't find them to
    clean up) and risk silent collisions across parallel tasks sharing the runtime. *What* needs a
    name is discovered from the project (stack-agnostic); the rule is deterministic-not-random, and
    tear the resource down when its task/wave completes.

## Agent status protocol

Each **dispatched** implementer returns one status (orchestrator-direct sequential work has none —
the orchestrator knows its own state):

| Status | Meaning | Orchestrator response |
|---|---|---|
| `DONE` | complete, self-checks pass | merge (review per policy — the single final review, or a mid-run spec-review if it triggers) |
| `DONE_WITH_CONCERNS` | complete, but flags something | record the concern; weigh at final review (or mid-run spec-review if review policy triggers it) |
| `NEEDS_CONTEXT` | missing info to proceed | provide the missing context, re-dispatch |
| `BLOCKED` | cannot proceed (conflict, ambiguity) | analyze; walk the bounded escalation ladder (below), then **escalate to the user** |

**Bounded escalation ladder** (for `BLOCKED` / `NEEDS_CONTEXT`): **attempt 1** — re-dispatch with
more context (the missing slice, the resolved ambiguity); **attempt 2** — re-dispatch with a
stronger model where the platform allows it; if it is **still BLOCKED**, **escalate to the user**
with full context: what was tried, what each attempt produced, and why it failed. The budget is
bounded — do not loop re-dispatching past the ladder.

## Context budget

- **Resident**: the 3-doc + wave schedule + accumulated per-task summaries
  (~100–200 tokens each) + spec-review verdicts (~20 tokens each).
- **Temp-load → use → drop**: authoring an implementer prompt (the relevant plan+spec slice),
  analyzing a failure (the error output). Drop after the judgment.
- **Sequential direct execution → sawtooth.** When the orchestrator implements a `MECHANICAL` /
  `NONE` task itself, it temporarily holds that task's file context. Load → implement → commit →
  **drop**; don't carry one sequential task's files into the next.
- Keep raw diffs out of the orchestrator — spec review runs in the subagent's context.
- **Watch retry bloat**: temp-loads have per-item caps but no total cap; repeated failures can
  swell the orchestrator. Compress to summaries and drop promptly.

## Per-wave step order

> **Review policy.** Default: a single **final review** after all waves merge — one subagent
> checks the full base diff for spec conformance + writing quality. Mid-run spec-review is added only
> when the orchestrator judges that a **RISKY task with downstream dependents** could cascade a
> deviation. When dispatched, spec-review is always a subagent (never inline) to preserve
> independence.

### Sequential wave (single task)

1. **Pick the execution mode by `risk`** (see Wave scheduling): `MECHANICAL`/`NONE` →
   orchestrator implements directly on the base (omitted `risk` = unclassified — judge at read time,
   and take the direct path only when no behavioral surface shows); `RISKY` → a worktree subagent +
   merge-gate; a no-file-diff task → a base-pinned subagent. (Details in "Sequential wave — execution".)
2. **Spec review** (conditional, **before merge**) — only when the review policy calls for it.
   Review the task branch's diff before the merge-gate, so a deviation is caught before it lands on
   the base (a no-file-diff task is judged from its commit message + captured external evidence —
   `spec-review-prompt.md`).
3. **Land it on the base** — orchestrator-direct / no-file-diff: verify the commit on the base
   (`git log`; file-diff touches declared targets; no-file-diff: commit message + captured external
   evidence). RISKY worktree: verify commit existence, then **merge-gate** into the base (strictly
   ahead + diff touches declared targets). Never trust self-report.
4. **Regen barriers** — run barriers whose `after` is now satisfied. Commit regenerated output if a
   later task depends on it. Recovery: if a barrier exits non-zero, capture command + exit + stderr,
   analyze whether a prior merge broke a precondition; if it would overwrite merged files, escalate.
5. **Assembly** — regenerate the assembled document (see "Assembly" below). Commit on the base.
6. **No integration gate.** The self-checks ran on the cumulative base. → next wave.

### Parallel wave (multiple tasks)

1. **Spec review** (conditional, **before merge**) — only when the review policy calls for it
   (a RISKY task with downstream dependents + cascade risk): review that task's branch diff before
   merging it, so a deviation is caught before it lands on the base.
2. **Merge serially** into the base (commit-existence verified first). **Merge-gate:** task branch
   strictly ahead, diff touches declared **file** targets (three-dot). (No-file-diff tasks never
   reach this path — they were handled on the base; see Wave scheduling.) Merge commit must satisfy hooks.
   Recovery: inspect hook output, verify branch state, retry with discovered convention; else escalate.
3. **Regen barriers** — same as sequential. Commit if downstream depends on it.
4. **Assembly** — regenerate the assembled document (see "Assembly" below). **Commit on the base** —
   an uncommitted assembly is silently lost to later worktrees and the final merge.
5. **Integration gate** — run the fact trace across all landed parts, and the classification check and
   the rule check on the assembled base; **green = all passed, evidence captured** (trace table,
   marking check, rule table). The
   reader check is reserved for the completion gate. This catches cross-part interactions. Failure → fix-dispatch or escalate. **Record
   the base tip SHA after the gate passes** (e.g. `GATE_SHA=$(git rev-parse HEAD)`) — the completion
   gate compares against it to avoid redundant re-runs (see SKILL.md, Completion gate). **Run
   independent checks in parallel** — capture each result separately so failure attribution is
   clear.
6. **Clean up or recycle** task worktrees — if a later parallel wave exists, **recycle** pooled
   worktrees (reset to the new base tip — Dispatch constraints, worktree pool) instead of removing;
   batch-remove all worktrees only after the last parallel wave. When removing: only after asserting
   ancestor (`git merge-base --is-ancestor`); safe remove (no `--force`); remove share-symlinks
   first. Delete merged task branches. Failed tasks' worktrees preserved for diagnosis. → next wave.

### Assembly (after every wave, before any gate)

The assembled document is the one shared file parallel writers never touch; the orchestrator is its
single writer. After each wave's merges and regen barriers, **regenerate it from scratch**: overwrite
the file (the name the skeleton fixed) with `parts/_header.md` followed by every landed
`parts/NN-*.md` in number order. **Never append** — appending puts a part written late (the first
screen) at the bottom and duplicates parts on a re-run. Regeneration is idempotent: running it twice
yields the same file. Commit on the base. It is not a graph task. (Upstream's "deferred wiring" —
appending registrations to a shared file — applies only to another shared file the plan names, such
as a glossary index; conflicts there → escalate.)

### Advancing waves

**Sequential waves advance immediately** — no gate to wait for, so the next wave can begin as
soon as the commit is verified and regen/wiring are done.

**Parallel waves:** **by default, overlap** the next wave's provisioning (worktree creation +
dependency share) with the current wave's integration gate — begin provisioning as soon as the
merge + wiring commits land, before the gate finishes. Gates are the **largest wall-clock sink**
(verify/build/container time), so overlapping provisioning with them is a real, free speedup — do it,
don't run strictly sequentially by default. The next wave's **dispatch still waits for a green gate**,
but the worktrees and dependencies are already ready. On gate failure the provisioned worktrees
are harmless (no task work yet) — remove or reuse after the fix. Fall back to fully serial advance
only if lock contention or refresh bookkeeping makes overlap unsafe. (Intermediate per-wave gates may
also trace only the parts that landed in the wave; the completion gate always runs the full set.)

**Advisory findings are recorded, never dropped.** Findings not fix-dispatched must be explicitly
marked accepted — never silently dropped.

### Fix-dispatch and lightweight fix

**Substantive fix-dispatch** (bugs, review blocking findings): dispatched as a subagent on a branch
off the base — reuse a task worktree if present, else create a fresh one. The subagent commits;
the orchestrator merges back under the same merge-gate.

**Lightweight fix** (trivial advisory findings — 1–2 files, non-behavioral): the orchestrator MUST
triage each advisory after the final review. Trivial (1–2 files, no change to a claim or fact — e.g. a
typo, a heading level, a term swapped for the harness term) → edit directly on the base, commit, re-run the
completion gate. The default disposition is lightweight fix, not "accepted." Only mark an advisory
as accepted when a fix is genuinely inappropriate (design trade-off, spec-intentional behavior).
Do not skip advisories as "accepted" when a lightweight fix would take seconds. Scoped to trivial,
non-behavioral changes only — substantive findings still go to an independent fix-dispatch. Each
advisory is triaged once; a re-run after an advisory fix judges blocking findings only (go SKILL.md
step 11, bounded).

## Failure handling

| Failure | Response |
|---|---|
| `BLOCKED` / `NEEDS_CONTEXT` | walk the bounded ladder: attempt 1 more context → attempt 2 stronger model where the platform allows it → escalate |
| max retries exceeded | **escalate to the user + preserve the worktree for manual recovery** (do not discard) |
| mid-run spec-review fail | re-dispatch with the specific fix |
| final review fail | fix-dispatch the blocking findings, re-run final review (at most two rounds, then escalate) |
| merge conflict | analyze; resolve if mechanical / same-intent, else escalate |
| merge commit-msg hook rejection | inspect hook name + full output; verify branch state (`git log`); retry with the producer-discovered commit convention; else escalate with hook name + error + attempted message + branch state |
| regen-barrier non-zero / conflicting output | capture command + exit + stderr; analyze whether a prior merge broke a precondition; if it would overwrite merged files, escalate |
| deferred-wiring conflict | capture file + conflicting lines + involved tasks; escalate (never auto-pick a winner) |
| integration gate fail | analyze → identify the causing task → fix-dispatch |
| writing-quality issue (final review) | fix-dispatch |
| architecture mismatch / suspected spec violation / data-corruption risk | **stop and escalate** |

- **Partial wave failure — cleanup order + retry semantics**: keep the merged successful tasks.
  **Preserve the failed task's worktree for diagnosis** (do not clean it). **Clean up only the
  successful worktrees**, and only after the ancestor check (`git merge-base --is-ancestor`).
  **Never delete the base.** On retry, create a **FRESH worktree branched from the
  CURRENT base tip** — which now includes this wave's already-merged successes (the base tip
  advances per merge), so the retry builds on the integrated state, not the stale pre-wave tip. The
  wave doesn't proceed until all pass.
- **Safety net**: worktree isolation means a discarded failed task never affects the base.
  Verify real work exists (`git log` / `git diff`) before relying on a result.

## Escalate = ask the user

Anything you can't safely resolve — architecture mismatch, suspected spec violation,
unresolvable conflict, data-corruption risk — **stop and ask the user.** Don't guess; the spec
is ground truth and only the user changes it.

**Escalation is synchronous.** The orchestrator→user escalation **pauses** the run and waits for
the user's answer — it never silently hangs, fires-and-forgets, or proceeds on an assumption while
"waiting." (Subagents run in fresh sessions with no live user conversation, so they cannot ask the
user; they return their escalation through their structured result, and the orchestrator relays it
to the user synchronously.)

**Pass the user's words, not a summary.** When a user's answer feeds a later subagent (a writer, a
fix-dispatch, a reviewer), quote it verbatim — the question as asked, the options shown, the answer.
A summary loses the reason the user accepted with an option, and a reviewer then flags that reason as
invented.

**The user changes content mid-run.** When the user's answer to an escalation changes what the
document says (a line removed, a comparison dropped, a marking changed), update the spec first — and
the plan and handoff where they carry it (a hard gate, the marking string) — and record the change
and its reason in the spec's thinking-base. Then fix the document and re-verify against the updated
spec. The archived 3-doc must match the delivered document. Only the user's decision changes the
spec; a reader's or reviewer's suggestion alone never does.

**Detection ≠ diagnosis.** Spotting that something broke is not the same as correctly
attributing *why*. A confident but wrong cause-attribution is possible — verify it against the
actual commands and output (not a self-report or a shallow grep) before acting destructively or
recording it as a durable fact. A misattribution that gets written down propagates.
