# material-intake.md — received documents, raw data, and spoken facts (shared by ready, go, migration)

How information the user gives reaches a project, where it is kept, and how a fact in the document
traces back to it. Shared byte-identical between `ready`, `go`, and `migration` (a build guard
enforces it).

The user often cannot hand over company documents (security). Information then arrives in three
ways, often mixed:

| Way | Example | Kept where | Fact-ledger source |
|---|---|---|---|
| **Shareable document** | an onboarding page, a meeting note the user may share | `material/` (committed) | the file path |
| **Raw dataset** | a CSV or table export, cut down by the user | `material/raw/` (**never committed**) + a **data card** in `material/` (committed) | the card path |
| **Spoken** | "MAU was 4,200 in September, from the dashboard" | nowhere but the 3-doc (and the harness when it is project knowledge) | `user, in dialogue (YYYY-MM-DD)` |

## Folder layout and the git rule

```
material/                 committed — shareable documents, data cards
  <name>.card.md          one card per raw file
  raw/                    IGNORED by git — raw datasets only
```

- The project's `.gitignore` holds the line `material/raw/`. Whoever creates the project (or first
  receives a raw file) adds it and commits the `.gitignore` before any raw file is put there.
- **Raw data is never committed.** Before every commit that touches `material/`, confirm the raw
  file is ignored (`git check-ignore material/raw/<file>` prints the path). If it is not, stop — fix
  the `.gitignore` first. A raw file committed even once stays in the history.
- The card is committed; it keeps the project traceable after the raw file is deleted.
- Never copy raw rows into the 3-doc, the harness, a commit message, or a subagent prompt beyond the
  figures the document uses.
- Delete a raw file only when the user asks. Its card stays.

## The data card (fixed format)

One card per raw file, written when the file arrives (ask the user for whatever is missing — never
fill a field by guessing):

```
# <name> — data card
- raw file: material/raw/<file>      (deleted: <date>, when the user removes it)
- source: <where the data comes from — system, report, person>
- as of: <YYYY-MM-DD, or the period>
- received: <YYYY-MM-DD>
- classification: <level of the raw data, by classification.md or the company's scheme>
- masked: <what the user replaced with aliases, e.g. customer names → 고객사 A/B/C; "none">
- definitions:
  - <column or metric>: <what exactly is counted>
- figures used:
  - <figure> = <value> (<as of>) — used in <document folder>
```

`figures used` grows as figures enter a document's fact ledger (`ready` adds the row; it is the
only part of the raw data the project keeps). The alias map itself (which alias is which real name)
stays with the user — never in the project.

## Spoken facts

- A spoken fact enters the fact ledger as **user-stated**, source `user, in dialogue (YYYY-MM-DD)`.
- For a **figure**, it needs three things to be usable: **as of** (which date or period), **where it
  was seen** (dashboard, report, a person), and **what is counted** (the definition). Ask only for
  the ones the user did not give, in one question. A figure the user heard from someone else carries
  that ("영업에게 들음") — it stays user-stated, and the document says whose figure it is.
- A spoken fact that is project knowledge beyond this document (a metric definition, who decides
  what) goes into the harness through the normal harness update — written as a rule, not as a quote.

## Asking for less

- Ask only for what the document needs: the columns, the period, the figures. Suggest the user cut
  a dataset down before sharing it.
- Suggest aliases for customer and person names in raw data. A real name makes the content
  Confidential (`classification.md`); an alias usually keeps it Internal.
- Personal data (contacts, evaluations, pay, health) is not needed in raw data for a document —
  ask the user to remove it before sharing.
