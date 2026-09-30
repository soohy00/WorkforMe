# example-3doc.md — one complete, illustrative 3-doc

A worked example so the shape of a real `handoff` + `spec` + `plan` is concrete, not just
described. **It is illustrative, not a template to copy literally.** The company, the service, and
the people below are generic on purpose — a real 3-doc is **company-agnostic**, written against
whatever the project actually is, discovered at runtime. The **document kind is incidental too**: this
happens to be an alignment document for designers and developers, but the *identical* 3-doc shape
(spec = readers + content + fact ledger + reader-check questions, plan = parts + Execution Graph, a
deferred assembly step) applies to a proposal, an escalation, an investor update, or meeting material
— only the *content* of the contracts changes, never the structure. Copy the *structure and
altitude*, not the words or the domain. (Only the Execution Graph, the fact ledger, and the
reader-check questions are rigid; the prose layout is the author's to design — see
`output-format.md`.) The example is **delta-shaped**: its handoff carries no Project Foundation
section — in a first cycle the handoff additionally carries the Foundation (`output-format.md`), so do
not anchor on this example for that section's absence.

The example document: **payment-failure handling — alignment doc** for the product designer and the
two developers who will build it.

---

## handoff.md (governing doc)

**Document roles.** `spec.md` = what the document says and for whom (ground truth; on conflict, spec
wins; spec errors fixed only with user approval). `plan.md` = parts, order, file targets
(provisional; revise freely). Earlier documents in the project = HOW reference, never the authority
for WHAT.

**File locations** (project-root-relative): `.dryforge/spec.md`, `.dryforge/plan.md`,
`.dryforge/handoff.md`. Output: `outputs/2026-10-06-payment-failure/` (`parts/*.md` joined into
`payment-failure.md`).

**Execution shape.** One document; 5 parts; 3 waves. Wave 1: background + rules (parallel). Wave 2:
states + flow visual (parallel), then the assembly step joins parts. Wave 3: the first screen
(summary + open decisions), written last because it restates every part.

**Hard gates** (not derivable from the material alone):
- Classification: **Internal**. Recipients: the product designer, the frontend developer, the backend
  developer, the team lead. Marked at the top; no revenue figures (they would lift it to Confidential).
- The document must **not** promise a refund policy — refunds are owned by the operations team and
  are out of scope.
- The retry limit is **3** (settled with the team lead); never written as "a few" or "several".
- Verification: every reader-check question answered by an independent reader; every figure traced
  to the fact ledger.

**Intent captured live (not in spec/plan).** The user chose to put the open decisions on the first
screen, above the flow, because the designer starts on Monday and must know what is still undecided
before drawing any screen. (Recorded so a downstream agent doesn't "improve" it back to a
conventional background-first order.)

---

## spec.md (what to write — ground truth)

**Classification.** Internal. Recipients: product designer, frontend developer, backend developer,
team lead.

**Readers.** Primary: the **product designer** — knows the checkout screens, does not know the
payment provider's failure types, worries about designing screens that later change. Secondary: the
two developers (need the rules and exceptions), the team lead (needs the open decisions and their
owners).

**Outcome.** The designer starts the failure screens on Monday without another meeting; the
developers can estimate the work from the rules section.

**Key message.** When a payment fails, the user retries up to three times on one screen, then is
sent to support — and two decisions are still open, with owners and dates.

**Content**
- Why: payment failures are the top reason for abandoned orders (F1) — the goal is to recover them
  without new support load.
- Rules: a failure shows the retry screen with the provider's reason in plain words; after the
  **3rd** failure (F2) the user sees the support screen; a card-limit failure never auto-retries.
- States (each screen): retrying, failed with reason, failed three times, provider unreachable.
- Out of scope: refunds (operations team); saved-card management.
- Settled: the retry limit (3). Open: (a) whether the order is kept for 24 hours after the third
  failure — owner: team lead, by 2026-10-09 (F3); (b) the support channel shown — owner: operations
  lead, by 2026-10-09.

**Form.** Alignment document, Markdown, pasted into the team's workspace page; about two pages; plain,
direct tone. Visuals: **V1** flow — "after a failure, where does the user go?"; **V2** state table —
"what does each screen show in each state?".

**Thinking-base.** Open decisions go first (see handoff). The provider's error codes are *not*
listed — the designer needs the four user-facing reasons, not thirty codes; the developers get the
mapping from the provider's documentation (rejected alternative: a full code table, dropped as noise
for the primary reader).

## Fact ledger
| id | fact | source | status |
|---|---|---|---|
| F1 | Payment failure is the top abandonment reason in September | Sept funnel review (shared by user) | sourced |
| F2 | Retry limit 3 | team lead, per user in dialogue | user-stated |
| F3 | Decision date 2026-10-09 | user, in dialogue | user-stated |

## Reader-check questions
| id | question | expected answer (gist) | answered in |
|---|---|---|---|
| Q1 | After a failed payment, what does the user see next? | the retry screen with the reason | rules, V1 |
| Q2 | When does the user get sent to support? | after the 3rd failure | rules, V1 |
| Q3 | Which failure never auto-retries? | card limit | rules |
| Q4 | What states must each screen handle? | retrying, failed with reason, failed 3×, provider unreachable | V2 |
| Q5 | What is still undecided, who decides, by when? | order hold (team lead), support channel (ops lead), by 10-09 | first screen |
| Q6 | Is the refund policy part of this work? | no — operations team | first screen, scope |

---

## plan.md (what to do — parts + the machine graph)

**T1 — background.** Content contract: why this matters (F1) in three sentences; no revenue figure.
File target: `parts/01-background.md`. Verify: F1 traced. *Do not* touch `payment-failure.md`.

**T2 — rules.** Content contract: the retry rule, the limit (F2), the no-auto-retry case, what is out
of scope. File target: `parts/02-rules.md`. Verify: Q1–Q3 answerable from this part; F2 traced. *Do
not* touch `payment-failure.md`.

**T3 — flow visual (V1).** Content contract: the flow from failure to retry to support, with the
limit on the branch. File target: `parts/03-flow.md`. Verify: Q1–Q2 answerable from the visual and its
caption.

**T4 — state table (V2).** Content contract: each screen × each state, one line of what the user sees.
File target: `parts/04-states.md`. Verify: Q4.

**T5 — first screen.** Content contract: classification header, key message, the two open decisions
with owners and dates (F3), scope note. File target: `parts/00-first-screen.md`. Verify: Q5–Q6; F3
traced; key message matches the spec word for word in meaning.

**Assembly (single deferred writer — NOT a graph task).** Join `parts/` in number order into
`payment-failure.md`. This runs as the **orchestrator's** per-wave assembly step, so it is
deliberately **absent from the Execution Graph below** — shared-write assembly is a prose step, never
a `depends`-bearing node (see `dependency-calc.md`, "shared-write (prose hint, not graph)").

**Reader's path (for humans).** The designer reads the open decisions first, then the rules, then
checks the flow and the state table while designing.

```yaml
tasks:
  - id: T1
    depends: []
    risk: MECHANICAL   # optional; restates one sourced fact
  - id: T2
    depends: []
    risk: RISKY        # optional; rules and an edge case the developers will build
  - id: T3
    depends: [T2]
  - id: T4
    depends: [T2]
  - id: T5
    depends: [T1, T2, T3, T4]
    risk: RISKY        # optional; the first screen and the open decisions
regen_barriers: []
```

(Five graph tasks → three waves: `{T1, T2}`, then `{T3, T4}`, then `{T5}`. The first screen depends on
every part because it restates them — it is written last and read first.)

(The `risk:` atoms are **optional** — `RISKY | MECHANICAL | NONE`. They size the writer's per-part
verification ceremony and, for a single-task wave, go's execution mode. Omitting one leaves the task
unclassified: go leans toward stronger verification.)

(No `regen_barriers` here — nothing regenerates from another part. If the document numbered its
figures across parts, a figure-index rebuild after T3–T4 would be one.)
