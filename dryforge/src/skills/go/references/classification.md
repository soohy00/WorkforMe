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

The level is a **content decision** (settled in `ready`'s ELICIT): recommend it with the reason, the
user decides. The recommendation is the **higher** of two readings — taking the higher one is the
normal case:

**(a) By the most sensitive content in the document** (minimum level):

| Content | Minimum level |
|---|---|
| Published facts, marketing material | Public |
| Internal processes, organization, plans already shared inside the company, work-in-progress designs | Internal |
| Revenue, costs, prices not yet public, contract terms, unreleased product plans, per-customer data, fundraising in progress, investor reports | Confidential |
| Security weaknesses, mergers or acquisitions, layoffs or pay, terms before a contract is signed, anything the user calls "only for the CEO" | Strictly confidential |
| Personal data — contact details, identifiers, evaluations, pay, health, anything private about a person | Confidential at least — and include only what the document needs (a colleague's name and work role in an internal document is Internal, not personal data in this sense) |

**(b) By the recipients** (typical, not a rule):

| Recipient | Typical level |
|---|---|
| Designers and developers on the team | Internal |
| Manager or CEO (escalation, report) | Internal, or Confidential when the content requires it |
| Investors, advisors, partners (outside, under a confidentiality agreement) | Confidential |
| Customers, the public | Public |

**When the reading is unclear, ask — with options and a recommendation.** The level is unclear when
the content sits between two levels, when the company's scheme does not say, or when someone other
than the user (a manager, a security owner) decides the level. Then never settle it silently, and
never just take the higher level without saying so: present 2–3 options, each with what it means for
the content and the recipients, and recommend one with its reason. One option may be a **provisional
level** — the level the document carries until the person who decides confirms it:

- marked as the level followed by "(잠정)" in the user's language (e.g. `사내한정(잠정)`);
- treated as that level for every rule below;
- the document asks the deciding person to confirm it (one line among its questions), and the user is
  told who must confirm before the document goes further than that person.

When a named recipient **may not receive** the level the content requires (an outside recipient and
Confidential revenue figures), **never lower the level to fit the recipient**. Either the content is
removed or generalized until a level the recipient may receive fits it ("revenue grew" instead of the
figure), or the recipient is dropped. That choice is the user's; present both with a
recommendation.

## What each level requires of the document

| Level | Marking (top of the document) | Distribution | Content |
|---|---|---|---|
| Public | the level + the intended audience | no limit | nothing above Public |
| Internal | the level + the recipients (a team or role is enough) | inside the company; no public links (a shared page open to "anyone with the link" is public) | nothing above Internal |
| Confidential | the level + the named recipients + date and version | only the named recipients; forwarding needs the author's consent; outside recipients only under a confidentiality agreement the user confirms | minimum personal data |
| Strictly confidential | the level + the named individuals + date and version | only the named individuals; never pasted into shared workspaces or chat tools | sensitive figures kept to what the decision needs; prefer "available on request" over including them |

**Downgrading is removing, never relabeling.** A Confidential draft becomes Internal only by taking out
the Confidential content.

## Hard gates (the handoff carries these; `go` enforces them)

- The document states its level and recipients at the top, in the form above.
- **Content above the level is a blocking finding** — never shipped, never "noted as a risk".
- A recipient the level does not allow → stop and ask the user; never lower the level, and never add
  a recipient, on your own.
- Personal data only as much as the document needs; never collected "in case".
- Internal ids from the design files (fact ids like `F1`, question ids like `Q1`, visual ids `V1`, task
  ids `T1`) never appear in the delivered document — they are working labels, not content.
- Nothing in this file overrides the law or the company's own rules; where they are stricter, they
  apply.
