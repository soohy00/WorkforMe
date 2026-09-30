# classification.md — document classification (shared by ready, go, migration)

Every document carries a **classification level** and a **recipient list**. The level decides what
the document may contain and where it may go. Shared byte-identical between `ready`, `go`, and
`migration` (a build guard enforces it).

## The company's policy wins

A company that has its own classification scheme **overrides this file**. `migration` (or the first
`ready` cycle) asks whether the company has one; if it does, the project harness's `security.md`
records it, and every later cycle uses **that** scheme — map this file's rules onto the company's
levels, never apply this default on top of it. Until the company's policy is known, use the default
below and say so in the handoff.

## Default levels (the common four-level scheme)

| Level | Korean label | Who may receive it |
|---|---|---|
| Public | 공개 | anyone, inside or outside the company |
| Internal | 사내한정 | people inside the company (and contractors working inside it) |
| Confidential | 대외비 | only the **named** recipients — inside, or outside under a confidentiality agreement |
| Strictly confidential | 극비 | only the named individuals who must decide on it |

Write the label in the user's language (for Korean: 공개 / 사내한정 / 대외비 / 극비).

## Setting the level — recommend, the user decides

The level is a **content decision** (`elicitation.md`): recommend it with the reason, the user
decides. The recommendation is the **higher** of two readings:

**(a) By the most sensitive content in the document** (minimum level):

| Content | Minimum level |
|---|---|
| Published facts, marketing material | Public |
| Internal processes, organization, plans already shared inside the company, work-in-progress designs | Internal |
| Revenue, costs, prices not yet public, contract terms, unreleased product plans, per-customer data, fundraising in progress, investor reports | Confidential |
| Security weaknesses, mergers or acquisitions, layoffs or pay, terms before a contract is signed, anything the user calls "only for the CEO" | Strictly confidential |
| Personal data (names with contact details, identifiers, anything about a person) | Confidential at least — and include only what the document needs |

**(b) By the recipients** (typical, not a rule):

| Recipient | Typical level |
|---|---|
| Designers and developers on the team | Internal |
| Manager or CEO (escalation, report) | Internal, or Confidential when the content requires it |
| Investors, advisors, partners (outside, under a confidentiality agreement) | Confidential |
| Customers, the public | Public |

When (a) and (b) disagree — a recipient who may not receive the content's level — **do not relabel**.
Either the content is removed or generalized until the level fits the recipient ("revenue grew" instead
of the figure), or the recipient is dropped. That choice is the user's; present both with a
recommendation.

## What each level requires of the document

| Level | Marking (top of the document) | Distribution | Content |
|---|---|---|---|
| Public | the level | no limit | nothing above Public |
| Internal | the level | inside the company; no public links (a shared page open to "anyone with the link" is public) | nothing above Internal |
| Confidential | the level + the named recipients + date and version | only the named recipients; forwarding needs the author's consent; outside recipients only under a confidentiality agreement the user confirms | minimum personal data |
| Strictly confidential | the level + the named individuals + date and version | only the named individuals; never pasted into shared workspaces or chat tools | sensitive figures kept to what the decision needs; prefer "available on request" over including them |

**Downgrading is removing, never relabeling.** A Confidential draft becomes Internal only by taking out
the Confidential content.

## Hard gates (the handoff carries these; `go` enforces them)

- The document states its level and recipients at the top, in the form above.
- **Content above the level is a blocking finding** — never shipped, never "noted as a risk".
- A recipient the level does not allow → stop and ask the user; never widen the level on your own.
- Personal data only as much as the document needs; never collected "in case".
- Nothing in this file overrides the law or the company's own rules; where they are stricter, they
  apply.
