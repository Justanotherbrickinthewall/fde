---
name: prototype
description: "Take one clickable HTML demonstrator from a starting point to a version the user calls done, in one session that survives compaction. Starts from a brief, a delivery, an idea or an existing screen, with or without a milestone. Grounds the work in the wiki's field spec and the extracted document grid, builds the first pass, then loops on the user's feedback and closes by writing the decisions into the record. Use when the user says \"prototype\", \"build the demonstrator\", \"show them what it looks like\", invokes /fde:prototype, or names a delivery that needs one. Demonstrators only; a feasibility spike is not this skill's job."
---

# Build the prototype

`/fde:prototype` has one behaviour. It makes a session record, builds the
first pass, then runs the phases below until the user says the prototype is
done. A user who stops after the first round has run a one-round session.
There is no flag and no second mode.

Lowest level of the planning loop. `/fde:fdc-session` widens the plan into
milestones, a prototype brief is written against a delivery, and this skill
turns that into something the client can click. Brief shapes are in
`setup/artifact-templates.md`.

**A prototype attaches to a delivery, never to a milestone.** A delivery is
what the client recognises; a milestone is how we build it, and no client
has ever asked to see one. One delivery may carry several prototypes or
none, and a prototype may span several milestones. A milestone is optional
input: the session starts with one, several, or none.

Generic mechanism. This engagement's corrections live in
`setup/planning-rules.md` § "Prototype rules" — read it first; those rules
override the steps below. Guardrails apply throughout, especially 3 (unknown
is an open question, never a plausible guess), 5 (client data stays local)
and 9 (no product code during scoping).

A demonstrator is not a spike and not a build. It is a disposable HTML file
whose job is to make the client react. The deliverable is the file itself,
and it never becomes the product.

## Finding the engagement

The umbrella is the nearest ancestor of the current directory holding a
`.engagement` file. Read that file first. It carries plain `key=value` lines:
`slug`, `docs`, `be`, `fe`, `stack`, `plugin_version`, `plugin_root`, `apps`,
`record`, `merge_into`, `integration`, `release` and `worktree`. The `docs`,
`be` and `fe` values are folder names inside the umbrella, and `be` or `fe` is
empty when that side does not exist yet. The last six keys are empty for a
one-app engagement, and the skill then behaves as it did before they existed.
`apps` lists the apps; when it is set, resolve the app first. `record` is the
record's path inside `<docs>`, and empty means the `<docs>` root. `merge_into`
is where a milestone branch merges, and empty means `main`. `integration` is
the branch the app branch merges up into, and empty means there is no such step.
`release` is the branch that deploys, and nothing touches it in away mode.
`worktree` is the naming pattern for a worktree beside its repository.
`fde:init` writes the file, and it replaces the fixed repository names these
skills used to carry.

Below, `<docs>` means the docs folder that `.engagement` names, `<be>` the
backend folder and `<fe>` the frontend folder. In a shell command they are
`$DOCS`, `$BE` and `$FE`, each an absolute path. `<record>` is the `record`
value with the app filled in, and `$REC` is `$DOCS/<record>`; where `record` is
empty, `$REC` is `$DOCS`. Every engagement path is written relative to
`<docs>`, so a command run from the umbrella needs that prefix in front of it. A session path keeps its `my-sessions/` prefix.

`${CLAUDE_PLUGIN_ROOT}` is the plugin's own directory, and every plugin path
below hangs off it. Where the variable is unset, read `plugin_root` from
`.engagement` and use that. Where that is missing too, ask the user once for
the plugin's path and write it back as `plugin_root`.

## What this skill will not do

- A `mode: feasibility` brief or question. That asks yes or no, and its
  deliverable is a written verdict. Say so and stop.
- Fragments. One session produces one self-contained file, never a partial
  page assembled with others. Assembly needs a host and a build step, and
  guardrail 9 forbids that during scoping.
- New scope. A prototype that would commit architecture beyond what was
  settled needs an ADR first (guardrail 6). Flag it and stop.
- Rebuild a file the user has accepted. Reworking one changes it round by
  round.

## Roles

The orchestrator takes every decision. It never reads the frontend, never
builds inline and never drives a browser. It sends each worker job to a
subagent, names the model every time, and takes a short report back.

| Work | Kind of job |
|---|---|
| Gathering the ground, writing the brief | A search-and-write job |
| The first build and each round of changes | An implementation job. Use the strongest tier when it fills a form or reshapes the interaction, and a mid tier for a small local change |
| A visual check | A search-and-report job |

Follow the global rule for subagent models. Tell every subagent the same
rule for its own subagents.

Whether to take a screenshot or open the file in a browser is the
orchestrator's call in each session. Never do it by default. Ask the user to
open the file once instead.

**Never poll a subagent.** Dispatch it and wait for the completion notice.

## The phases

| # | Phase | Ends when |
|---|---|---|
| 0 | Scaffold | the record exists and `notes.md` is written |
| 1 | Ground and scope | `context.md` is written and the user has heard the scope in plain words |
| 2 | Settle | the shape and the open questions are settled, and the user has nothing to add |
| 3 | Brief | `decisions.md` and `brief.md` are written |
| 4 | Build | v1 of the file is written and checked |
| 5 | Feedback | the user says the prototype is done |
| 6 | Close | the record holds what was decided, and the session has ended |

Run the phases in order. Update `Phase:` in `notes.md` the moment a phase
ends. A single pass is the same run, with phase 5 ended after round one.

## Keeping it resumable

Sessions compact, and the user may close one and start `/fde:prototype`
again at any point. So the session folder holds what a compacted or fresh
orchestrator needs at every moment.

1. When the user gives any input, write it into `notes.md` first, then act
   on it. That covers an answer, a decision, a correction and a round of
   feedback.
2. After every decision and every subagent report, write one line in
   `notes.md`, or in `decisions.md` once it exists. Link a report or a file
   rather than copying it.
3. Rewrite **Resume here** at the same moment: what you are doing now, the
   one next step, and any subagent still running.
4. Under **Carry forward**, append and never replace: layouts and approaches
   the user rejected and why, constraints stated only in conversation, and
   anything the user said to keep.

To resume, grep `notes.md` for `Phase:` and `Resume here`, then read
**Carry forward**, **Decisions** and **Versions** by line range. Read the one
file that **Resume here** names, and nothing more. Where the folder and a
summary disagree, trust the folder.

---

## Phase 0: scaffold

The starting point is any of these, alone or together: a brief in
`project/artifacts/prototype-brief-<slug>.md`, a delivery, one or more
milestone ids, an idea in the user's words, or an existing screen or file in
`project/prototypes/` to rework. If none was given, ask one short question.

1. **The app.** Where `apps` is set, a milestone id names it, or the
   invocation does. Where that does not settle it, ask once and never guess.
   Where `apps` is empty, there is no app and the slug has no app prefix.
2. **The ids.** Each milestone id must resolve to exactly one file under
   `$REC/project/milestones/`. No match is a typo: list the ids that exist
   and ask. No ids at all is fine.
3. **The slug.** The prototype's name in kebab case. It becomes the file
   name. A rework keeps the existing file's slug. A new one checks
   `$REC/project/prototypes/` for a clash.
4. **Never clobber.** Look under the prototype session folders for one
   ending `-<slug>` whose `Phase:` is short of `6 done`. If one exists, say
   which and resume from it.
5. **The record.** Run `python3 "${CLAUDE_PLUGIN_ROOT}/sessions/scripts/sessions.py" new --type prototype --slug <app>-<slug>`, or `--slug <slug>` where `apps` is empty. Run it from the umbrella. It chooses the folder and writes `notes.md` from the shared template. Follow `${CLAUDE_PLUGIN_ROOT}/sessions/CONTRACT.md` for the notes contract and the close step.
6. **Extend `notes.md`.** Add the sections in the template below, set
   `Phase: 1 ground`, and write the starting point under **Starting point**
   in the user's own words.
7. **Say the path**, then go into phase 1.

## Phase 1: ground and scope

### Ground it through a subagent

Dispatch one search-and-write subagent. The orchestrator does not read the
frontend, the wiki or the specimen store itself. Brief it with the starting
point, the app, and the session folder path. It reads, in this order.

1. The delivery's brain dump, `project/brain-dumps/dN-<slug>.md`. Every
   `pain` entry is something the demonstrator should answer, and every
   `constraint` entry is something it must not break. A demonstrator that
   answers no recorded pain is decoration. If the dump is empty, say so.
2. The existing UI patterns. The frontend screens and components nearest the
   starting point (read-only, never written), `setup/design.md`,
   `styles/app.css`, and every file in `project/prototypes/`.
3. The field spec: the wiki node that holds the fields, their suppliers,
   formulas and timing. Also the extracted document grid in
   `specimens/*/tables/*.csv`, the form row by row, verbatim from `raw/`.
4. Each milestone named, for its scope and the rules still open.
5. The ADRs those cite, for behaviour, and `setup/guardrails.md` for the
   human gates the prototype must show.
6. `setup/planning-rules.md` § "Prototype rules".

It writes `<session>/context.md`, under about 80 lines. Each point names the
file it came from. It says plainly what it could not find, such as an empty
brain dump or no field spec. It returns five lines at most.

Absence is not a value. A missing field spec means the prototype shows gaps,
and the brief says so. Use real field names and real row labels: a prototype
the client does not recognise is wasted work.

### Say the scope back

Read the subagent's short report, not `context.md`. Say back what the
prototype will show, in about 150 words and plain language: what the client
can click through and which delivery it serves, which existing patterns it
builds on, what it leaves out, and what is unknown and so shown as a gap.
Write it under **Scope, in plain words**, then ask: is this the shape you
want? Never argue the scope up or down here.

## Phase 2: settle

The only questions put to the user before the build come here, in order.

1. The shape. Where the user pushes back, rewrite **Scope, in plain words**
   and ask again until the shape is right.
2. The open questions, one at a time. Each is a genuine choice the record
   cannot settle. Where the record has not decided a business question,
   decide it here from the specimen, the raw documents, the wiki and the
   code. Phase 6 records it as a dated note, labelled a working assumption
   where the evidence is thin.
3. "Is there anything you want to add that I might have missed?" If the
   answer raises a question, ask it, then ask this again. Stop when the user
   has nothing to add.

Every answer goes into **Decisions** before you act on it. There is no
separate approval of a written brief.

## Phase 3: brief

Write `<session>/decisions.md`: every decision from phases 1 and 2, one line
each with its reason. It is the brief writer's only input from the
conversation, so a decision missing from it is lost.

Then dispatch a search-and-write subagent to write `<session>/brief.md`,
using the demonstrator template in `setup/artifact-templates.md`, filled from
`decisions.md` and `context.md`. A brief that already exists in
`project/artifacts/` is the starting text, and the subagent amends it.
`Must show` always holds a human gate from the guardrails. `Built:` and
`Known debt:` stay empty until phase 6. The subagent returns three lines.

The brief stays in the session folder while the prototype changes. Phase 6
writes it into the record once.

## Phase 4: build

Dispatch one implementation subagent. Hand it `build.md` in this skill's
folder, the session folder path, and the target file
`$REC/project/prototypes/<slug>.html`. It reads `brief.md` and `context.md`
itself. The orchestrator never builds inline.

When the report comes back, write one line under **Versions** for v1 and one
under **Progress log**. Put any `Must show` row it missed under **Known
debt**. Ask the user to open the file once, and give the full path.

## Phase 5: feedback

This phase loops until the user says the prototype is done. Each round:

1. Write the feedback into `notes.md` under **Feedback**, in the user's
   words, numbered by round. Do this before anything else.
2. Settle anything unclear with one short question and write the answer under
   **Decisions**. A change that adds new scope stops here, as "What this
   skill will not do" says.
3. Dispatch one implementation subagent to make the change. Hand it
   `build.md`, the round's feedback and the version number. It keeps the old
   version in `<session>/versions/`.
4. Write the new version under **Versions** with one line on what changed,
   then ask the user to reload it.

Never queue a second round onto a subagent still running. Wait for its
report, then start the next round.

A visual check is only needed when a report leaves a real doubt, such as a
layout the script checks cannot see. Whether to run it is the orchestrator's
call each time, and it goes to a subagent that reports in a few lines.

## Phase 6: close

Reached when the user says the prototype is done. The session ends once this
phase is done. It never starts another prototype, and the next piece of work
gets a fresh session.

1. **Write the brief into the record.** Copy `brief.md` to
   `$REC/project/artifacts/prototype-brief-<slug>.md`. Set `status: complete`,
   fill `Built:` with a link to the file, and fill `Known debt:`. A
   `Must show` row the file misses is debt, and the brief does not reach
   `complete` with one unrecorded.
2. **Regenerate the derived views.** `project/artifacts/index.md` gains the
   brief's row with its `Built` link. The Now section of `next-steps.md` is
   refreshed, since a finished prototype may unblock work. Both are derived
   views and need no approval.
3. **Record what was decided.** A business question decided in phase 2 goes
   to `project/open-questions.md` with an id and a dated note, labelled a
   working assumption where it is one. The brief's `Unresolved:` names it. A
   UX point that belongs to the product goes to `project/ux-log.md` in its
   own format.
4. **Record corrections.** A correction to how prototypes are made goes in
   `setup/planning-rules.md` § "Prototype rules", dated. Never in this file.
5. **Lint and check links**, with the scripts the engagement carries in
   `<docs>/scripts/`, and fix what they find.
6. **Close the record.** Set `Status: done`, write `Summary:` in one line, and set `Owes:` to what is still owed, or `none`. Run `python3 "${CLAUDE_PLUGIN_ROOT}/sessions/scripts/sessions.py" check <folder>`. If it exits non-zero, fix the notes and run it again. When it passes, run `python3 "${CLAUDE_PLUGIN_ROOT}/sessions/scripts/sessions.py" index --write`.
7. **Set `Phase: 6 done`**, write the last **Progress log** line, and clear
   **Resume here** to say the session is finished. The closing message names
   the file, its final version, the known debt and every open question by id.

## Sections added to notes.md

`sessions.py new` writes the front block and its own sections. Add these
after them.

```markdown
- **App:** <app, or "none">
- **Delivery:** <dN, or "unknown" until phase 2 settles it>
- **Milestones:** <ids, or "none">
- **Prototype:** <project/prototypes/<slug>.html>
- **Phase:** <0 scaffold … 6 close | 6 done>

## Resume here
<the session folder path; what you are doing now; the ONE next step; any
subagent still running. Rewrite after every answer and every report.>

## Starting point
## Carry forward
## Scope, in plain words
## Decisions
## Feedback
<round N: the user's words, written before the round is acted on>
## Versions
- v<N> — <DD-MM-YY> — <what changed>
## Known debt
<Must show rows the file does not reach; invented figures by name>
## Progress log
- <DD-MM-YY> — <what was done>
```

Four more files sit beside `notes.md`. The ground subagent writes
`context.md`. The orchestrator writes `decisions.md`, and the brief writer
writes `brief.md`. Each round's subagent keeps the old version in
`versions/`.

## Rules

- Write the user's input into `notes.md` before acting on it.
- The orchestrator decides. Subagents gather, write and build, and every
  dispatch names its model.
- One session, one self-contained file. No fragments, no build step, no
  dependencies.
- An unknown is shown as a gap, never filled with a plausible number
  (guardrail 3).
- Never write `wiki/` or a milestone body. The brief is the only judgement
  file this skill writes, and only its status, its `Built:` line and its
  `Known debt` section. Its `Settles`, `Shown to` and `Must show` belong to
  whoever wrote the brief.
- The prototype is disposable. It is never promoted into a code space, and a
  code space needs gate 1 regardless.
- One subagent per round, and every round records its version.
- The session ends at its close and never starts the next piece of work.

## Reference

`build.md` is the build subagent's brief. `reference/exemplar.md` walks the
worked example, its structure and its known debt.
