# Check: the charter

Covers `project/charter.md`.

*Lifted from the `discover` skill on 07-09-26, when the six scoping skills
folded into `/fde:fdc-session`.*

This engagement's corrections live in `setup/scoping-rules.md` § "Discovery
rules". Read them first; they override what is below. Guardrails always
apply, especially 3 (unknown is an open question, never a plausible guess)
and 10 (client-stated requirements are changed only by the client).

The charter's empty rows are the discovery agenda. That is why it is written
before it can be filled in.

## Complete looks like

Every required row holds an agreed answer, or an open question with a named
owner. Not our guess.

Three things carry more weight than the rest.

The process owner is named. An engagement that cannot name the process owner
has not started, whatever has been built. Where the row stays open, that fact
is the headline of the report, not a footnote.

The out-of-scope list exists and is explicit. It is the half people skip, and
it is the half that prevents an argument later.

The success measure has a baseline that existed before we arrived.

## Read state first

Parse `project/charter.md`. Classify every row as filled, open or diverged.
Count the open rows and start there. A filled row is never re-asked unless
the user asks for it.

## What to ask when it is not complete

### The header

Us, and the process in scope.

The process in scope is one sentence naming a business process, not a
technology. Where the answer names a technology, ask what process that
technology serves, and record the process.

### The seven people rows

Ask each one that is open. They are usually not the same person.

| Role | What it means |
|---|---|
| Executive sponsor | signs the money, and unblocks where the coordinator cannot |
| Process owner | carries responsibility for the work itself |
| Primary users | the people who do the process every day |
| Secondary users | the people who feed it or receive from it |
| Data owners | who owns the content the process produces |
| System owners | who owns the systems it runs on |
| Security and IT | who decides whether client data may leave the network |

Where one name covers several roles, say so and ask whether that is really
true, or just who we happen to have met.

Offer names already given elsewhere in the charter as choices, so the same
person is never typed two ways.

### Scope

What is committed, in deliverables, one row each.

What is out of scope, said plainly, with why the line sits there. Ask for
this list explicitly.

### The success measure

The hard part, and the reason this check exists.

Four things: a measure, its baseline, its target, and whether the client has
confirmed it.

The baseline must be a number that existed before we arrived. Our own demo
timings do not count.

Where no baseline exists, do not invent a target and do not accept one.
Instead, four steps:

1. Leave the row open.
2. Write "no baseline exists for <measure>; the client has never measured
   this" as blocking question 1 in the charter.
3. Append a row to `project/findings.md` recording that the engagement
   started without a measurable success criterion.
4. Add an open question naming who could establish the baseline and what it
   would take.

An engagement can proceed from here. It cannot proceed pretending the number
exists.

### Tier and mirror

Every answer captured takes `stated` or `ours`, per the interview discipline
in `setup/scoping-rules.md`.

Every `ours` answer that bears on scope or success is mirrored into
`project/open-questions.md` as something to confirm with the client. Our read
of the client's business is not the client's statement of it.

## Template

```markdown
# Charter

Purpose: what we are doing for <client>, and how we will know it worked.
Done when: every required row holds an agreed answer, not our guess.

| | |
|---|---|
| Client | <name> |
| Us | <who, with roles> |
| Process in scope | <one sentence naming a business process> `<tier>` (<source>) |
| Started | <DD-MM-YY> |

## People

Usually not the same person. A row left open is a discovery gap.

| Role | Name | Notes |
|---|---|---|
| Executive sponsor | | `<tier>` (<source>) |
| Process owner | | `<tier>` (<source>) |
| Primary users | | |
| Secondary users | | |
| Data owners | | |
| System owners | | |
| Security and IT | | |

## Scope

### In scope

| # | Deliverable | Note |
|---|---|---|
| D1 | | |

### Out of scope

| # | Not doing | Why the line sits here |
|---|---|---|
| X1 | | |

## Success criteria

| Measure | Baseline | Target | Client confirmed |
|---|---|---|---|
| | <a number that existed before we arrived> | | yes / no |

## Blocking questions

1. <what stops this charter being finished, and who can answer it>
```

## What to report

Rows filled this session, rows still open, questions raised, and the
headline: whether the process owner is named and whether a baseline exists.
