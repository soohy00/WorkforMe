# doc-types.md — the floor of each document kind (ELICIT)

What a document of a given **kind** must answer, so ELICIT knows which silences are gaps. Loaded in
ELICIT next to `elicitation.md`; the kind-silence probe (`gap-analysis.md`) reads it.

**Floor, not ceiling — and not a template.** Each kind lists what must be *answered*, never a heading
list to fill. Structure is designed per reader at PLAN. "Commonly silent" items are slot-finders for
the lenses, not a question list: each one still clears `grounds-gate.md` and the enumerate ≠ ask
filter. A document may combine kinds (meeting material that is also a proposal) — then it carries
both floors.

## Common floor (every kind)

- One **primary reader**, named by role; the action they take after reading.
- A **key message** that fits in one sentence and appears first (the reader who stops after the first
  screen still gets it).
- Every figure, date, name, and quotation traceable to the fact ledger; an unsourced one is shown as
  unconfirmed in the document, never smoothed over.
- The project's terms (the harness), and every term the reader may not know explained where it first
  appears.
- A classification level and recipients (set by the user).

## Proposal — asks someone with authority to approve

- **Primary reader:** the approver (little time; judges by money, risk, time, fit with goals).
- **Works when:** the approver can answer yes / no / yes-with-conditions.
- **Floor:** the request on the first screen (what, how much, by when); the problem and why now; the
  proposed approach; the expected effect (sourced figures only; an estimate is labeled as one, with
  its assumptions); scope — in and **out**; cost, time, and people as the approver weighs them; risks
  and their handling; alternatives including doing nothing.
- **Commonly silent:** how success will be measured; the decision deadline; who is accountable; for an
  external reader, why us.
- **Visual candidates:** current vs proposed flow; timeline; cost breakdown; before/after figures;
  option comparison.
- **Reader-check examples:** "What exactly am I asked to approve?" · "What does it cost and when does
  it end?" · "What happens if we don't?"

## Alignment document — designers and developers start work from it

Feature brief, design brief, requirements or policy definition, handoff note.

- **Primary reader:** the maker (designer or developer). Both → shared body plus a part per role.
- **Works when:** the maker starts **without another meeting**, and knows where they are blocked.
- **Floor:** why (the user problem and the business goal — makers need the reason to make judgment
  calls); target users and the key usage scenes; what is **settled / open / to be decided**, each open
  item with an owner and a due date; scope — now / not now / later; priority (must / nice to have).
  - For designers: user flow, screen list, and every screen's states (empty, loading, error, no
    permission), brand or tone constraints.
  - For developers: rules and their exceptions, data items, integrations, permissions, acceptance
    criteria written so "was this met?" is decidable.
- **Commonly silent:** failure, cancel, duplicate, and permission cases; state changes; conflicts with
  existing features; fixed dates inside the schedule; who answers questions during the build.
- **Visual candidates:** user flow; state diagram; screen flow (grey boxes, not a design); swimlane of
  who does what; system context.
- **Reader-check examples:** "When payment fails, what does the user see next?" · "What is out of
  scope this time?" · "Who decides X, and by when?"

## Escalation / upward report — manager or CEO

Status report, issue escalation, decision request.

- **Primary reader:** the manager or CEO (reads the first lines; wants the situation, the impact, and
  what is needed from them).
- **Works when:** the reader knows the situation in one minute and acts (decides, unblocks, or knowingly
  does nothing).
- **Floor:** the situation in one or two sentences; the impact (on dates, money, customers, people);
  what is needed from the reader and by when — or "no action needed, for your information"; the
  options with a recommendation when a decision is asked; what has already been tried.
- **Commonly silent:** the deadline for the decision; what happens if no decision is made; who else
  already knows; whether the bad news is complete.
- **Visual candidates:** timeline with the slip marked; options comparison; a small figure panel.
- **Reader-check examples:** "What do you need from me, by when?" · "What happens if I do nothing?"

## Investor update / results report

- **Primary reader:** the investor (compares against what was promised before; looks for risk and
  momentum).
- **Works when:** the investor sees progress against the last promise, the bad news included, and
  what comes next — and trusts the numbers.
- **Floor:** headline figures against the previous period and against the stated goal (each with its
  definition, period, and source); what was promised last time and what happened; what went wrong
  and the response; next period's goals; any ask (introductions, hiring help, funding).
- **Commonly silent:** metric definitions (what exactly is counted); the comparison baseline; cash
  runway if the reader expects it; what must not be disclosed (classification).
- **Visual candidates:** metric trend with goal line; figure panel; milestone timeline.
- **Reader-check examples:** "Did they do what they said last time?" · "What is the biggest risk now?"

## Meeting material — pre-read, agenda and decision memo, presentation

- **Primary reader:** the attendees (read it five minutes before, or see it on a shared screen).
- **Works when:** the meeting **ends in a decision** (or the agreement it aimed for).
- **Floor:** the meeting's purpose and what it ends with (decision / agreement / information); per
  agenda item: background in three lines at most, the options, the recommendation and why, who
  decides; the figures needed beforehand; a place for the follow-ups (owner, date).
- **Commonly silent:** time per item; what is already settled and not reopened; the expected
  objection; the next step if no decision is reached.
- **Form note:** a pre-read → a short document; a shared screen → one message per slide; both → slides
  plus an appendix document.
- **Reader-check examples:** "What are we deciding today?" · "What is the recommendation and why?"

## Visual explainer — makes something text cannot hold

Flow chart, user journey, service structure, roadmap, organization or role map, concept map.

- **Primary reader:** everyone who must reach the **same** understanding from the same picture.
- **Works when:** a reader can state the point from the picture alone, and two readers do not read it
  two ways.
- **Floor:** one question per visual (written as its caption); a legend for every color, line, and
  shape — never meaning by color alone; flows with a clear start and end and a condition on every
  branch; three lines of reading guidance under the visual.
- **Commonly silent:** the exception paths; who performs each step; the direction of time; the scale
  (numbers).
- **Choosing the form (signal → form):** "first ... then ... if ..." → flow chart; several people taking
  turns → swimlane flow; "changes to ...", waiting/done/cancelled → state diagram; the user's steps and
  feelings → journey map; moving between screens → screen flow; what connects to what → structure
  diagram; option A vs B → comparison table; dates and milestones → roadmap; who decides and who does
  → responsibility table; a number over time → line chart; numbers side by side → bar chart. More
  than about twelve elements → split the visual or group a level up.

## Operations document — policy, procedure, retrospective

- **Primary reader:** the operator who follows it, or the manager who oversees it.
- **Works when:** a policy or procedure can be followed alone; a retrospective changes what happens
  next.
- **Floor:** policy/procedure — scope, rules with decidable criteria, exceptions and who approves them,
  effective date, owner; retrospective — what happened (facts), why (causes, not blame), what changes
  (actions with owners).
- **Commonly silent:** metric definitions; the comparison baseline; exception handling; revision
  history.
- **Visual candidates:** procedure flow; decision tree; owner table; metric trend.
