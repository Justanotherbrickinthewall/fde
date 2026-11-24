# The engagement record

This repository holds the engagement record. It holds nothing else. Read
before doing anything, in order:

1. `setup/guardrails.md` — hard rules; the client and build kinds both apply
2. `setup/glossary.md` — the project language; use these terms exactly
3. `project/charter.md` — what we committed to, and the open rows

## Four repositories, and this is one of them

The application code lives in two others, and
[ADR-001](project/decisions/adr-001-the-stack.md) says why.

The code lives in `fde-be` and `fde-fe`. There are four siblings inside the
untracked umbrella, which is the parent of this repository. The fourth is
`my-sessions`, the session records. It is a plain folder with no git, kept on
this machine only. Claude is always started from the umbrella, so all four are
in view at once. The umbrella's own files live here as well: `umbrella/`
holds its `CLAUDE.md`, `justfile` and `docker-compose.yml`, and `/fde:init`
runs `bootstrap.sh` from the plugin to link them into the umbrella root. A
`settings.json` joins them when one exists.

`/fde:init <slug>` does what a `new-engagement.sh` script once did. It
renames the three repositories for the client and writes `.engagement` at
the umbrella root: the slug, the three folder names, the stack, and the
pinned plugin version. Every skill reads that file to find this engagement,
so none of them carries a fixed repository name.

This repository is always on `main` and it never branches. The record has no
merge to make, so a branch would only hide work from the other lanes.

`raw/` is gitignored and it is never committed, on any branch. Guardrail 5 is
what keeps it that way. Pushing this repository would otherwise send the
client's documents to GitHub, and nobody has approved that.
`${CLAUDE_PLUGIN_ROOT}/scripts/check_links.py` is what keeps the record's
own links honest, so run it after any move or rename.

## Where things are

- `raw/` — every artefact exchanged with the client, immutable.
  `raw/ledger.md` logs arrivals with authority tier and filing status.
  `/fde:file` creates both the first time it runs.
- [`wiki/`](wiki/index.md) — knowledge derived from raw. One home per fact.
  Every claim is sourced, or it is tagged as an assumption.
- `project/` — the engagement: charter, [risks](project/risks.md),
  assumptions, open questions, [findings](project/findings.md), ADRs,
  milestones, deliveries, gates, and [`plan-ledger.md`](project/plan-ledger.md),
  which says which wiki nodes the plan has not yet taken account of. Also
  [`ux-log.md`](project/ux-log.md), where an interface problem noticed
  mid-build waits until someone cuts a milestone for it. `/fde:ux-log` is
  what writes to it. Also [`artifacts/`](project/artifacts/index.md), the
  standing documents a milestone needs: briefs and specs that outlive any one
  session. And [`prototypes/`](project/prototypes/README.md), the clickable
  HTML those briefs produce. A session's own build spec,
  implementation plan and execution record live with that session in
  `my-sessions` instead. This repository never links to or cites a
  session record; extract the fact into the page that needs it.
  [`milestones/`](project/milestones/README.md) holds the vertical slices and
  [`deliveries.md`](project/deliveries.md) holds the dates promised to the
  client.
- `setup/` — this client's judgement, which the generic skills read.
  Guardrails, the glossary, the design pointer, and the filing, scoping and
  planning rules.
- The method itself is not filed here. Install the `fde` plugin once. Its
  README says how, and every skill then runs as `/fde:<name>`.

## Two roles, one record

The method runs on two roles, and the milestone file joins them. The forward
deployed consultant, the FDC, keeps the record true and cuts the milestones.
The AI engineer, the AIE, builds them.

An FDC session starts from whatever arrived: client material, a meeting
transcript, a pile of brain dumps, or their own research. It ends when that
input is in the record, and the open questions and milestones reflect it. An
AIE session takes one `ready` milestone through nine phases to a merged
branch.

Both roles read and write the whole record, `raw/` included. There is no
permission split. On a solo pod both roles are one person in two chats, so the
dated note is the only trail there is. The milestone file is the handoff:
the FDC writes it and marks it `ready`, and the AIE builds what it says.

## Writing to the record

The record changes by dated notes, never by rewriting a sentence already
there.

The note shape is `*Widened 04-09-26, AIE.*` The hat is `FDC` or `AIE`.

The verbs in use are widened, narrowed, corrected, answered, recut,
dropped, overridden and revised. Use another plain past-tense verb when
none fits.

A widen, narrow, recut or drop of a milestone needs a conversation first.
So does an override of a build guardrail. The two roles talk first, and
then whoever does the deed writes the note.

The note names the decision, not the conversation.

## The commands

`/fde:init` made this repository. These run the engagement after that.

| Command | Does | Whose |
|---|---|---|
| `/fde:fdc-session` | Takes whatever arrived to a record that reflects it, and closes with the questions for the next meeting | FDC |
| `/fde:file` | Files material into `raw/` with a ledger row and a tier, builds the page-anchored specimen store, then builds the knowledge graph | FDC |
| `/fde:aie-session` | Runs one `ready` milestone end to end, from an empty session folder to a merged branch | AIE |
| `/fde:brain-dump` | Splits what was heard about a delivery into dated, tagged, sourced entries | both |
| `/fde:ux-log` | Appends an interface problem to `project/ux-log.md`, or marks an entry done | both |
| `/fde:prototype` | Builds one clickable HTML demonstrator from a prototype brief | FDC |
| `/fde:smoke-test` | Walks the running application with a person, one scenario at a time | AIE |
| `/fde:bug-hunt` | Takes a pile of bugs to a merged branch from one session | AIE |
| `/fde:qa-session` | Checks the built feature against what was agreed, one fact at a time, before a delivery | AIE |
| `/fde:session-sync` | Harvests this engagement's chat transcripts into `my-sessions/` folders | both |
| `/fde:explain` | Explains one complicated thing in plain English, in chat | both |

`/fde:prototype` belongs to the FDC until an AIE prototype skill exists.

`/fde:file` runs in two layers. The cheap layer builds the page-anchored
specimen store, and the expensive layer builds the knowledge graph from it.
It runs the cheap layer over everything you hand it, then asks once whether
to run the expensive layer now or later. The expensive layer treats
`wiki/process.md` and `wiki/data-sources.md` as nodes like any other. It may
supersede their `ours`-tier content with `artefact` material under the
normal tier rules, and the losing claim takes a dated correction note.

The skills come from the `fde` plugin and it owns their mechanism. This
client's judgement sits in `setup/`. Filing judgement is in
[`setup/filing-rules.md`](setup/filing-rules.md). Scoping judgement is in
[`setup/scoping-rules.md`](setup/scoping-rules.md) and plan judgement is in
[`setup/planning-rules.md`](setup/planning-rules.md).

## The five milestone statuses

A milestone carries one of five statuses. `draft` means the FDC is still
writing it. `ready` means the AIE may start. `building` means an AIE session
has it open. `built` means it is merged and walked. `dropped` means we chose
not to build it, and the file stays to say why.

Only the FDC sets `ready`. `/fde:aie-session` refuses a milestone that is not
`ready`, sets `building` when it opens and `built` when it closes.
`waits-on:` is a field, not a status.

## Guardrails come in two kinds

A client guardrail comes from the client, the law or the contract, or it
governs what reaches the client, and the AIE cannot override one. A build
guardrail is the FDC's suggestion about how to build, and the AIE overrides
it with a dated note and a reason. Both sections are in
[`setup/guardrails.md`](setup/guardrails.md), where every live guardrail
names its source.

## The record lint

Run `python "${CLAUDE_PLUGIN_ROOT}/scripts/lint_record.py" .` from this
repository. Phase 6 of `/fde:fdc-session` and phase 8 of `/fde:aie-session`
run it, and you can run it by hand at any time. It calls `check_links.py`
and adds the record's own rules.
Those are milestone statuses, `waits-on` targets, the parts a `ready`
milestone holds, open-question owners, guardrail sources and every
milestone's delivery. It also flags any page under `project/` or `wiki/`
that nothing links to.

## Deliveries, milestones, brain dumps, prototypes

Four things, and a delivery is what ties them together.
[`project/deliveries.md`](project/deliveries.md) is the table of dates and
scope promised to the client. Each row points at all four.

A **milestone** is how it gets built. Vertical slices, in
`project/milestones/`, one flat file each. A milestone names the delivery it
serves in its `delivery:` front matter, or `none`. One milestone can serve
several deliveries.

A **brain dump** is what we have heard. One file per delivery in
`project/brain-dumps/`, appended after every conversation that touches it,
never rewritten. The wiki holds the shape of the documents; the dump holds
the shape of the problem. Fifty conversations with a client produce fifty
pockets of understanding and one wiki node, and the gap between them is what
this file catches. `/fde:fdc-session` reads a delivery's dump before cutting
the milestones behind it, and `/fde:prototype` reads it before drawing
anything. An entry is never evidence and never outranks `wiki/`.

A **prototype** is what it should feel like. It attaches to a delivery, never
to a milestone, because a delivery is what the client recognises. It follows
[`setup/design.md`](setup/design.md), the same design language the
application uses.

**Milestones do not break into issues.** It has been tried and it measures
the wrong work. A milestone's issue list fills with client questions, our own
fieldwork and build tasks, all sharing one counter. The artifact shapes that were
worth keeping are at
[`setup/artifact-templates.md`](setup/artifact-templates.md), and the ADR
shape is at
[`project/decisions/adr-000-template.md`](project/decisions/adr-000-template.md).

How the work runs instead: `/fde:aie-session <milestone> <detail>` runs one
`ready` milestone end to end, in nine phases. Scaffold the session folder,
say the milestone's scope back in plain words, and reconcile the milestone
against the feedback. Then write the spec, write the plan, build, walk it in
a browser, fix what the walk found, and close. It is the AIE's single touch
point; `/fde:smoke-test` is its phase 6 rather than a separate step.

The build phase happens in the code repositories rather than here. A session
opens a branch named for the milestone in `fde-be` and in `fde-fe`, and the
backend merges first. This repository stays on `main` throughout. A session
writes its own folder in `my-sessions` and never writes a session record here.

Phases 3 to 5 are a method pack inside the plugin's `fde:aie-session` skill,
so the way we build can change without touching this repository. Two exist.
`superpowers` is the default
and nobody types it, and `--quick` runs plan mode instead of a design
conversation and a spec. Phase 1 proposes one and you confirm it. Neither
ever builds inline.

Client questions go to
[`project/open-questions.md`](project/open-questions.md), our own fieldwork
goes to [`project/next-steps.md`](project/next-steps.md), and build scope
stays in the milestone file. A milestone never carries a task list; the plan
is a separate document, written after the milestone is settled.

**A milestone is a vertical slice, not a client deliverable.** The promised
dates live in [`project/deliveries.md`](project/deliveries.md). A document is
a configuration of a module rather than a milestone of its own.

Do not size milestones to fit prototypes. One prototype often spans two.

`/fde:prototype` builds demonstrators only: disposable HTML that makes the
client react. A `feasibility` brief asks a yes-or-no and a person
answers it in writing. Everything in `project/prototypes/` is a scoping
draft under guardrail 9 and is never promoted into a code space.

## Current phase

Nothing has started. There is no client, no charter and no material in
`raw/`.

One milestone is built.
[m01](project/milestones/m01-sign-in-and-the-shell.md) ships with the
template: a person signs in, a super admin adds people and creates projects,
and every screen sits inside the shell. The stack it rests on is
[ADR-001](project/decisions/adr-001-the-stack.md), accepted 07-09-26.
[The milestone index](project/milestones/index.md) has that one row.

Everything else is empty and says so. The charter's rows are the discovery
agenda. `setup/guardrails.md` carries the build guardrails and no client
guardrails yet. `wiki/process.md` and `wiki/data-sources.md` are stamped
empty. [Gate 1](project/gates/gate-1-scoping-to-build.md) has not been
tested.

**The first move is `/fde:fdc-session` on the proposal, before the first client
meeting.** Feed it whatever we already have: the proposal, the statement of
work, the notes from the sales conversation. It fills what it can and writes
down what it cannot. What comes out is the list of questions to take into
that meeting. That is the whole point of doing it first.
