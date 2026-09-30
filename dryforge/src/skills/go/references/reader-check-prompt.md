# reader-check-prompt.md — the independent reader (the document's acceptance test)

A document passes when **a reader who never saw the dialogue or the 3-doc** reaches the answers the
spec expects. The writer cannot run this check on their own work: the writer fills every gap from
memory (A=A). So the reader check is always a **fresh subagent**, dispatched by the orchestrator at
the completion gate on the whole assembled document (all questions), and again after a fix that
touches the first screen or the key message.

> You are in a fresh session with no live user conversation — do **not** ask the user directly.
> Return your structured result; the orchestrator relays anything that needs the user.

## What the reader is given — and what it is not

- **Given:** the assembled document (path), the reader's role from the spec and the harness
  (`audiences.md` entry: what they know, what they worry about, what they decide; first cycle — the
  harness does not exist yet, so from the spec's reader model only), and the
  **reader-check questions — the questions only**.
- **Not given:** the expected answers, the 3-doc, the dialogue, the writer's summary. An expected
  answer in the prompt turns a reading test into a matching exercise; the reader then finds what it
  was told to find.
- Read-only. General-purpose agent (it must read the files).

## Required elements of the prompt (wording is yours)

1. **Role.** "You are [the primary reader's role]. You received this document and have never talked
   to its author. You are busy."
2. **First screen first.** Read only the title block and the first screen, then state in one sentence
   what the document wants from you.
3. **Questions.** Read the whole document, then answer each question **from the document alone**,
   citing where the answer is (heading or visual). If the document does not answer it: `not
   answered`. If it can be read two ways: `ambiguous: <the two readings>`.
4. **What else stops this reader** (only when present): terms this reader would not know and the
   document does not explain; claims stated without support; figures, names, dates, or scope that
   disagree between two places; an action without an owner or a date; a visual that is hard to read or
   says something different from its caption; the one to three questions this reader would ask in the
   meeting.
5. **No praise, no rewriting.** Do not suggest better wording unless the meaning is wrong or
   ambiguous.

## Structured return

```
first-screen: <one sentence — what the document wants from me>
Q1: <answer> | where: <heading / visual> | status: answered | not answered | ambiguous
...
other:
- kind: term | support | inconsistency | owner | visual | reader-question | where: ... | what: ...
```

## What the orchestrator does with it

1. **First screen.** Compare the reader's sentence with the spec's key message and outcome. A mismatch
   is the most important finding — fix the first screen first.
2. **Per question.** Compare each answer with the spec's expected answer (the orchestrator holds it).
   Same meaning → pass. `not answered` / `ambiguous` / different → the owning part is fixed. If the fix
   needs content the spec does not hold → **stop and ask the user**; never invent it.
3. **Other.** Unexplained term → explain it or use the harness term; unsupported claim or unsourced
   figure → trace to the ledger or remove; inconsistency → reconcile to the ledger; visual → redraw.
   A reader-question the document should answer and cannot within the spec's scope → tell the user.
4. **Re-check.** After a fix, re-run the fact trace; re-run the reader check on the affected questions
   (all questions if the first screen or the key message changed). If the same question fails twice,
   stop and tell the user.

**Pass:** every question `answered` with the expected meaning, the first-screen sentence matches the
key message, no inconsistency, no unsourced figure.
