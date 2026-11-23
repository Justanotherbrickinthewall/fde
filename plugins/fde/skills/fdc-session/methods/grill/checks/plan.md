# Check: the plan

Covers `project/milestones/` and `project/plan-ledger.md`.

*Lifted from the `plan-sync` skill on 07-09-26, when the six scoping skills
folded into `/fde:fdc-session`.*

This engagement's corrections live in `setup/planning-rules.md` § "Sync
rules". Read them first; they override what is below. Guardrails always
apply, especially 3 (no invented facts), 4 (nothing client-facing without
review) and 9 (no product code during scoping).

The plan is a derived view over the wiki. Only the wiki holds knowledge, and
this check converges `project/` toward current wiki state by diff.

## Complete looks like

Every milestone the AIE may start is `ready`, and a `ready` milestone holds
everything the list below names.

Every pending row in `project/plan-ledger.md` is folded or marked
`no-impact`, with a word of why.

The derived views are current: `project/milestones/index.md`,
`project/open-questions.md` and `project/next-steps.md`.

## Two write disciplines, never confused

**Judgement files** are `milestones/*.md`. They carry human enrichment. They
are reconciled: propose the diff, apply after the go-ahead, amend with dated
notes, never rewrite wholesale, never delete.

**Derived views** are `open-questions.md`, `next-steps.md` and
`milestones/index.md`. They are pure aggregations of the nodes. Regenerate
them freely each run, with no approval needed.

Never the reverse.

## What a `ready` milestone holds

Eight things. The record lint checks every one is present and every link
resolves.

1. A title that makes a claim. A full assertion — "Applications draft end to
   end from the intake form with reviewer sign-off" — never an activity like
   "build drafting agent". A title someone cannot disagree with on evidence
   has failed.
2. Front matter, the fenced block of fields at the top of the file, with
   `status`, `delivery` and `waits-on`.
3. Why now, linking the wiki node or nodes that created or last changed this.
4. In scope.
5. Out of scope.
6. The guardrails that bind it, by number.
7. What it rests on: the wiki pages and the ADRs, each linked.
8. Walk this: the manual browser pass, numbered, in order — what to click and
   what should happen. Omit only for a milestone with no screen.

Why not sooner is welcome and not required.

Only the FDC sets `ready`. Setting it on a thin milestone is how an AIE
session spends its first hour discovering the scope was never settled.

## The five statuses

| Status | Means |
|---|---|
| `draft` | the FDC is still writing it |
| `ready` | the AIE may start |
| `building` | an AIE session has it |
| `built` | it is merged and walked |
| `dropped` | we chose not to build it, and the file stays to say why |

The status is the first word of the field, and a date may follow it. The FDC
sets `draft`, `ready` and `dropped`. `/fde:aie-session` sets `building` and
`built`.

`waits-on:` is a field, not a status. It names the milestone id in front of
this one, or `none`. A milestone held up by an unanswered question is not
waiting on a milestone: it stays `draft` and names the question by id.

## Detect the delta

1. **First run**, with no `project/plan-ledger.md`: create it. A header with
   the last-sync date, one row per wiki node, all `pending`. The whole wiki is
   the delta.

   A node is any folder carrying its own `index.md`, at any depth, or a flat
   node file such as a meeting or an entity. A family's furniture —
   `index.md`, `outline.md`, `samples.md` — shares one row per family.

2. **Otherwise**: changed or new means files under `wiki/` newer than
   `plan-ledger.md`. The ledger's own last-modified time is the watermark. Map
   each file to its node and re-pend those rows, meaning set them back to
   `pending` so this run reads them again. Add rows for nodes not yet in the
   ledger.

   If the last-modified times look mass-reset, meaning everything is newer,
   fall back to per-row folded dates against wiki correction-note dates, and
   say so in the report.

3. **Note the wiki gaps.** A `raw/ledger.md` row that is unfiled or partial
   means the wiki is incomplete there. Plan on what exists, flag the gap,
   never guess the rest.

4. **The queue is the pending rows.** An empty queue means say so, refresh the
   derived views if they are stale, and stop.

## Read the delta

Read each pending node's `index.md`. Specimens are evidence only.

Collect what bears on the plan: new or changed Inputs, which are dependency
edges; output contracts; confirmations or contradictions of `tier: ours`
content; scope signals such as client commitments and priorities; questions
raised.

## The four milestone rules

Renamed from create, edit and retire. Four now, because a recut is not an
edit and calling it one hides a scope move.

**Add** when the delta exposes a coherent outcome not yet covered: a
buildable cluster in the dependency graph, a committed deliverable, a data
intake need. It costs a file, a row in `project/milestones/index.md`, a
`delivery:` value or `none`, and a row in `project/plan-ledger.md`.

**Edit** when the delta changes an existing milestone's scope, ordering, exit
criteria or risk, and the milestone stays the same milestone. Amend in place
with a dated note carrying the hat:
`*Revised 12-09-26, FDC: exit criteria tightened per [<node> index](…).*`

**Recut** when the boundary between two or more milestones moves. Every
milestone the move reaches is edited in the same pass. Moving a capability
out of one milestone means that one loses it and another gains it, and
writing only one half is how two files start lying to each other. A recut is a conversation with the
AIE first, then the note.

**Drop** when a milestone's driver is contradicted or superseded. Front
matter goes to `status: dropped <DD-MM-YY>` with a dated reason. The file
stays. Every node folded into it is re-pended in the ledger, because the
reason it was folded no longer holds.

A milestone is always one flat file. Never promote it to a folder, and never
write task or issue files beneath it.

## Derivation rules

- A milestone is a falsifiable outcome, and its title is a full assertion.
- Order by the dependency graph aggregated from the nodes' Inputs tables. A
  section that needs nothing is a day-one target; a section behind another
  names it in `waits-on`.
- The first build milestone is a walking skeleton: the thinnest end-to-end
  slice through system, human checkpoint, output. Never a horizontal layer.
- A milestone is a vertical slice of the system, never a client deliverable.
  Promised dates and page counts belong in `project/deliveries.md`. A
  milestone names the delivery it serves in its `delivery:` front matter, or
  `none`. One milestone, one reason to change.
- Before cutting or detailing the milestones behind a delivery, read that
  delivery's brain dump at `project/brain-dumps/dN-<slug>.md` as well as the
  wiki nodes. The wiki gives the shape of the documents; the dump gives the
  shape of the problem. A milestone cut from the wiki alone misses every pain
  point the client mentioned in passing. A `pain` or `constraint` entry that
  no milestone answers is a finding, and it is named in the report.
- Respect the phase gates. Build milestones sit behind the scoping-to-build
  ADR. Scoping milestones — ingestion completion, data intake, charter, scope
  ADR — are actionable now.
- Content derived from `tier: ours` nodes carries that as a named risk.
  Confirmation belongs in the exit criteria.
- A milestone cites its driving nodes inline, first mention as a link. No
  backlink tables anywhere; reverse lookup is
  `grep -rl <node> project/milestones/`.

## Propose before you apply

Present a proposal table — action, milestone, driving nodes, one-line change
— then stop for the go-ahead. Apply only what is approved. A rejected diff
gets its reason recorded in the report.

A diff that constrains later work beyond the plan itself — scope,
architecture, a client commitment — also needs an ADR through
`checks/design.md`, drafted in the same batch.

## Milestone template

```markdown
---
status: draft | ready | building | built | dropped
target: <date or —>
waits-on: <milestone id, or none>
delivery: <dN, or none — with a word on why>
---
# <Assertion — the outcome, falsifiable>

Why now: <driver, linking the wiki node(s) that created or last changed this>.

Why not sooner: <optional>.

## In scope

<what this milestone owns, in blocks>

## Out of scope

<what it deliberately does not own, and which milestone holds it instead>

## Guardrails

<the guardrails that bind this work, by number, with a word each>

## Rests on

<the wiki pages and the ADRs, each linked>

## Exit criteria

<checkable statements; a human approval checkpoint counts as one>

## Risks / unconfirmed

<especially `tier: ours` drivers>

## Walk this

<the manual browser pass, numbered, in order — what to click and what should
happen. Omit for a milestone with no screen.>
```

A milestone carries no task list. How it gets built is an implementation plan
written by the AIE session, in `my-sessions`.

## Regenerate the derived views

- `project/open-questions.md` — aggregate every node's "Questions raised"
  section, one row per question, with a link to the owning node and a named
  owner. Questions answered per node correction notes move to an Answered
  section, never deleted.
- `project/next-steps.md` — the active milestone's front, pending plan-ledger
  rows, unfiled raw rows, and the questions blocking the next client session.
- `project/milestones/index.md` — one row per milestone file: number,
  assertion, status, what it waits on.

## Close the run

1. Mark each processed ledger row `folded <date>`, or `no-impact <date>` with
   a word of why.
2. Update the ledger header's last-sync date.
3. Write the ledger last. That write resets the last-modified watermark, so
   every other change must already be on disk.

## Rules

- Delta only. A folded row is settled until a newer wiki change re-pends it.
  Never regenerate milestones wholesale.
- Reconcile judgement files; regenerate derived views. Never the reverse.
- No milestone write without the go-ahead. Derived views are autonomous.
- Plan claims trace to nodes the way wiki facts cite sources. A need with no
  node behind it is an open question, not a milestone.
- Where the charter is absent or unfilled, flag that exit criteria have no
  anchor. Propose charter work as a scoping item, and never write charter
  content unprompted.
- Never write `wiki/` from here. Knowledge flows one way.
- Engagement and commercial terms — duration, phase shape, pricing — never
  enter through wiki nodes, because the wiki excludes them by filing rule. The
  plan cites them from `raw/` directly, or from the charter or an ADR once
  decided.
- A correction you give goes into `setup/planning-rules.md` § "Sync rules",
  dated, never into this file.

## What to report

Diffs applied and rejected, derived views refreshed, wiki gaps flagged, and
which milestones went `ready`. Anything client-facing goes to the user for
review, never sent.
