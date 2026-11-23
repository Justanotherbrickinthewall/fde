# grill

The default pack. It owns phases 2 to 5 of `/fde:fdc-session`: digest, confirm,
grill and update.

It is modelled on the superpowers `brainstorming` skill and keeps its spine.
Read the context first. Ask one question at a time. Prefer multiple choice.
Present in sections and get approval after each. Write. Self-review.

What changes is the output. `brainstorming` ends in a design document. This
ends in the engagement record, and the record has a shape the checks
describe.

The interview discipline at the head of `setup/scoping-rules.md` governs
every question asked here. Guardrails always apply, especially 2 (no
unsourced facts in the wiki), 3 (unknown is an open question, never a
plausible guess) and 10 (client-stated requirements are changed only by the
client).

---

## Phase 2 — Digest

Skipped when nothing arrived. A research session runs a research pass here
instead, and writes what it found into `digest.md` the same way.

### How the material is read

| What arrived | How it is read |
|---|---|
| A client document, meaning anything that becomes a claim source | through `/fde:file`, so it gets a ledger row, an authority tier and a page-anchored specimen, meaning a copy of its text that still says which page each line came from |
| A meeting transcript or a mail chain | read directly. It is our own note of what was said, and it never becomes a claim source without a ledger row |
| Brain dumps | read `project/brain-dumps/` directly. They are already in the record |
| Research | no input. Gather, then write what was found and where it came from |

A document that arrives as a paste rather than a file still goes through
`/fde:file`. The rule is about what the material is, not how it reached you.

### Send it to a subagent

One judgement agent, the whole input. Its brief is one question: where does each
piece of this go?

It answers in six columns, and it never writes to the record.

| Piece | Goes to | Kind | What it says | Confidence | Note |
|---|---|---|---|---|---|

- **Piece** — a quotable fragment, with its anchor. A page, a timestamp, a
  line.
- **Goes to** — the file and the section. `wiki/process.md` § Exceptions,
  `project/charter.md` § People, `project/brain-dumps/dN-<slug>.md`,
  `project/milestones/mNN-<slug>.md` § In scope.
- **Kind** — new fact, correction to something the record already says,
  answer to an open question by id, or scope signal.
- **What it says** — one sentence, in the source's own terms.
- **Confidence** — `stated` where the client said it, `artefact` or
  `statutory` where a document carries it, `ours` where it is our read.
- **Note** — what it contradicts, what it supersedes, what it leaves open.

A piece that fits nowhere gets a row saying so. That row is usually the
interesting one, because it means the record has no home for something the
client thinks matters.

Write the table to `digest.md` in the session folder. Group it by
destination, because that is the order phase 3 walks it in.

---

## Phase 3 — Confirm

Show the split and ask yes or no, one section at a time. A section is one
destination file.

For each section: the rows going there, what each changes, and the one
question. Does this land in the right place?

Three answers are possible. Yes, and it stands. No, and you say where it
should go instead. Or not yet, and it becomes an open question rather than a
record change.

**A correction that is about this client's documents is a rule, not a
one-off.** Sometimes you say a piece was filed wrongly because of how this
client's documents work. This table is always a continuation, that heading is
furniture, an annexure is never a claim source. Write a correction like that
into `setup/filing-rules.md`, dated, with the piece that produced it. That
is how `--investigate` works in `/fde:file`, and it is the same file.

A correction that is about this piece only stays in `digest.md`. The test is
whether the same mistake would recur on the next document of the same kind.

Update `digest.md` as you go, so an interrupted session loses nothing. The
approved split is what phase 5 executes.

---

## Phase 4 — Grill

Hunt for holes. This is the conversation, and it stays with the orchestrator
because a subagent cannot ask you a question and wait.

### What a hole is

`checks/` says. One file per part of the record, and each one says what
complete looks like, what to ask when it is not, and the template where
there is one.

| Check | Covers | Reads |
|---|---|---|
| `checks/charter.md` | the header, the seven people rows, scope in and out, the success measure | `project/charter.md` |
| `checks/process.md` | the trigger, the step rows, the seven exception prompts | `wiki/process.md` |
| `checks/mechanism.md` | the five mechanism letters and a reason on every row | `wiki/process.md` § Steps |
| `checks/data-sources.md` | the eleven source rows and the four architecture questions | `wiki/data-sources.md` |
| `checks/design.md` | what an ADR must name, and its rejected alternatives | `project/decisions/` |
| `checks/plan.md` | what a `ready` milestone holds, and the add, edit, recut and drop rules | `project/milestones/`, `project/plan-ledger.md` |

Read every check that the session touches. A session about a meeting
transcript usually touches all six; a session about one drawing may touch
two.

### How to run it

Read the check, read the file it covers, and list the holes before asking
anything. Then ask one at a time.

Prefer multiple choice wherever the answer space is closed: an authority
tier, one of the five mechanism letters, a role already named in the
charter, one of the five milestone statuses. Open-ended is fine where it is
not.

One question per message. If a topic needs more than one, break it up.

Order by consequence. A hole that blocks a milestone from going `ready` is
asked before a hole that tidies a wiki row. Say why you are asking, in a
clause, so a question that looks small is not answered small.

### Every tentative value becomes an open question

An answer given as "probably", "I think it is about", "they said something
like" or "we can assume" is not a fact. Write it into the record with the
tier that fits, and write an open question beside it, with a named owner and
what would settle it.

The owner is a person, never a department. An open question nobody owns is a
note.

This is the rule the grill exists for. A plausible answer invented here is
worse than a blank row, because six weeks later it reads as something the
client said.

### A hole you cannot answer becomes a question for the client

Ask you first. Where you do not know either, the hole goes to
`project/open-questions.md` with an id, the owner who could answer it, and
what it blocks. Then it goes into `notes.md` under **Questions for the next
meeting**, in the order to ask them.

### When it ends

You say stop, or no holes remain. Both are normal endings, and a session
that stops with holes open says so in `notes.md`.

Before handing to phase 5, present what will change, in sections, and get
approval on each. That is the last gate before the record moves.

---

## Phase 5 — Update

Send the changes out to subagents. The orchestrator dispatches and reads what
comes back. It does not edit `<docs>` inline.

### Order

1. **Wiki pages.** `wiki/process.md`, `wiki/data-sources.md` and any node the
   digest touched. Mechanical work that something else checks, one agent per file.
2. **Charter and setup.** `project/charter.md`, `setup/filing-rules.md`,
   `setup/guardrails.md` where the session produced one. Search and implementation.
3. **Decisions.** Any ADR the grill settled, against `checks/design.md`.
   Judgement, because the writing is the thinking.
4. **Open questions and assumptions.** `project/open-questions.md`,
   `project/assumptions.md`, `project/risks.md`. Search and implementation.
5. **Milestones.** Added, edited, recut or dropped, against `checks/plan.md`.
   Search and implementation, one agent per milestone file.
6. **Derived views.** `project/milestones/index.md`, `next-steps.md`, and the
   answered section of `open-questions.md`. Regenerated, not hand-edited.
7. **`project/plan-ledger.md`, last.**

### Every note carries the hat and the date

`*Widened 12-09-26, FDC.*` The shape is in `CLAUDE.md`. Amend with a dated
note rather than rewriting; the original reading stays visible.

A milestone is added, edited, recut or dropped, never rewritten wholesale and
never deleted. `checks/plan.md` has the four rules and what each one costs.

A dropped milestone keeps its file and says why. That is the whole point of
`dropped` as a status.

### Statuses

The FDC sets `draft`, `ready` and `dropped`. `/fde:aie-session` sets `building`
and `built`.

A milestone goes `ready` only when `checks/plan.md` says it holds everything
a `ready` milestone holds. Setting `ready` on a thin milestone is how an AIE
session spends its first hour discovering the scope was never settled.

Say out loud which milestones went `ready` this session, and write them into
`notes.md`.

### plan-ledger.md is written last

The ledger's own last-modified time is the watermark that decides what is
stale. Writing it before the wiki writes means the next session sees a wiki
older than the ledger and folds nothing.

So every other write lands first. Then each processed row is marked
`folded <date>` or `no-impact <date>` with a word of why, and the header's
last-sync date is updated. Then the file is saved, and that is the last write
of phase 5.

### Self-review before handing back

Read what the subagents wrote, with fresh eyes, against four things.

1. **Placeholders.** Any `TBD`, any half-finished row, any milestone section
   with a heading and no content.
2. **Contradictions.** Does a new wiki row disagree with one the same file
   already carries? Does a milestone's scope overlap another's?
3. **Tiers and sources.** Does every new claim carry a tier and cite where it
   came from?
4. **Owners.** Does every open question written this session name a person?

Fix what you find, through a subagent, then report back to `/fde:fdc-session`.
Phase 6 runs the record lint, which catches a different set of things, and
neither replaces the other.
