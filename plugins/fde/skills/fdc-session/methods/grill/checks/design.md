# Check: the design

Covers `project/decisions/`.

*Lifted from the `design` skill on 07-09-26, when the six scoping skills
folded into `/fde:fdc-session`.*

This engagement's corrections live in `setup/scoping-rules.md` § "Design
rules". Read them first; they override what is below. Guardrails always
apply, especially 6 (decisions that constrain later work get an ADR) and 9
(no product code, no framework or schema commitments during scoping).

Design only against the workflow, the data, the security posture and the
evaluation strategy. Architecture is a consequence of those, and they are
discovery outputs.

## Complete looks like

The architecture decision record, the ADR, names both things it must name:
where the human stays in control, and how the system will be evaluated. The
final section is not written until each has an answer.

Every assumption surfaced along the way is in `project/assumptions.md` with
its validation and who can perform it.

## Read state first

Read `project/charter.md`, `wiki/process.md` and `wiki/data-sources.md`.

Report anything the design would rest on that is still open: an unnamed
process owner, unclassified steps, a field with no authoritative source.

Designing over an open field is allowed. It is recorded as an assumption
rather than passed over in silence.

## What to ask when it is not complete

### The shape

Work from the classified table. The mechanism column is the design: the
sequence of `D`, `AI`, `A` and `H` steps is the architecture. The job here is
to name what runs each one, and what carries data between them.

Do not commit to a model, a vector store, an agent framework, a workflow
engine, a frontend library, a cloud or a database because it is familiar.
Where one is chosen before the evidence exists, record it as an assumption
with the evidence that would confirm or kill it.

The cloud in particular is a client constraint, never a default.

### The rejected alternatives

Ask what else was considered, and why it lost.

A design with no rejected alternative has not been designed, it has been
assumed. Two is usually enough, and the reason matters more than the count.

Write them down while the reasons are cheap. The gate question — why this,
and what was rejected — is answered in the ADR, not reconstructed later.

### The conventions it takes, and the stack

Ask which conventions this ADR takes. There are four, and each is specified
in `${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/<name>.md`: `design`,
`auth-and-roles`, `model-gateway` and `repo-layout`. Name the ones it takes
in the ADR, and say in one line why it declines any it does not. Each file
holds a checklist, and `/fde:aie-session` phase 8 runs it before a milestone
can read `built`.

Ask which stack it commits to. Write that answer into `.engagement`, so every
later skill reads one stack rather than guessing. `fde:init` writes the file
and this check writes `stack=`, which is one of the two later writes
`ENGAGEMENT.md` allows.

Do the write here, once the ADR names the stack:

1. Find `.engagement` by walking up from the working directory to the nearest
   ancestor that holds one. Stop at the filesystem root and ask the user if
   none is there.
2. Replace that file's `stack=` line with `stack=<value>`. The key already
   exists, so change the value in place. Change no other line, and add none.
3. Read the file back and confirm the new value is on it.
4. Record the write in the session's `notes.md`, under **Decisions**: the ADR
   number, the stack, and the date.

### The two things an ADR must name

Neither is optional, and the ADR is not finished without both.

`## Human in control` — which step holds the human, what they see when they
get there, and what happens to the work if they say no.

`## Evaluation` — what the system is evaluated against, what the dataset is
and who labels it, the thresholds, and what happens when a change moves them.
A design without an evaluation strategy is not finished.

Both headings go in verbatim.

## Writing it

Copy `project/decisions/adr-000-template.md` to
`project/decisions/adr-NNN-<slug>.md`, NNN being the next free number.

```markdown
# ADR-NNN: <title>

Date: <DD-MM-YY>. Status: proposed | accepted | superseded by ADR-NNN.

## Context

The forces at play. What question this decision answers, and why now.

## Decision

What we chose. One decision per ADR.

## Rejected alternatives

What else was considered and why it lost.

## Human in control

Which step holds the human, what they see, and what happens if they say no.

## Evaluation

What it is judged against, the dataset and who labels it, the thresholds, and
what happens when a change moves them.

## Consequences

What becomes easier, what becomes harder, what this constrains next.
```

An ADR is amended with a dated note, never rewritten. Superseding one writes
a new ADR and sets the old one's status.

## What to report

The ADR written, assumptions raised, and what remains open.

Where this ADR completes the scoping-to-build gate, fill
`project/gates/gate-1-scoping-to-build.md`. It has eight conditions and each
one needs a link rather than the word "done". Only with that gate signed is a
code space created.
