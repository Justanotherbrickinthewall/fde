---
name: fdc-session
description: "Run one forward deployed consultant session end to end, from whatever arrived to a record that reflects it. Scaffolds a session folder in my-sessions, reads what arrived and the state of the record in plain words, hands the digest, the confirmation, the grill and the update to a method pack, then runs the record lint and closes with the questions for the next meeting. Use when client material, a meeting transcript, a pile of brain dumps or your own research needs to reach the record, when the user says \"start an FDC session\", \"scope this\", \"grill me on the charter\", or invokes /fde:fdc-session <what arrived> <detail>. The grill method runs by default; a --<method> flag is only needed to pick a different one."
---

# fdc-session

Take whatever arrived and get it into the engagement record, with the open
questions and the milestones reflecting it.

This is the single touch point for the FDC. It scaffolds, reads what
arrived, splits it, confirms the split with you, grills you for the holes,
writes the record, lints it, and closes with the questions to ask next.

Claude is always started from the umbrella. `<docs>` holds the engagement
record. `my-sessions` holds this session's folder, and `<docs>` never links
to it. `<be>` and `<fe>` hold the code, and an FDC session never touches
them.

**How we scope** is not written here. It is a method pack in `methods/`, and
`grill` is the only one. The pack can change without this file changing.

The FDC's output is the record, not a branch. There is no build, no walk and
no merge in this skill. The cadence target is two milestones ahead of the
AIE.

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

## The app rule

This applies only when `apps` is set. With `apps` empty, skip this section and
the skill behaves as it does today.

The session learns the app one of three ways. The detail names it, the folder
the material sits in says it, or the material makes it plain. There is one raw
ledger per app. When the session needs an app and cannot tell, ask once, in
one line, and never guess.

Every arrival gets an app. A transcript that touches two apps is split, one
part per app, the way a dump spanning two deliveries already is.

## Invocation

```
/fde:fdc-session <what arrived> <detail>
```

The first argument is free text and phase 1 works out what it means. It can
be a path in `raw/`, a meeting transcript, the words "brain dumps", the word
"research", or nothing at all.

Examples:

```
/fde:fdc-session raw/meetings/Meeting3-120926.md third meeting
/fde:fdc-session "brain dumps" delivery 2 shape
/fde:fdc-session research the regulator's submission rules
/fde:fdc-session "" charter gaps
```

One pack exists and nobody types it. `grill` is the default, so
`/fde:fdc-session raw/docs/<file> <what it is>` runs it. A flag only
ever picks a *different* pack. An unknown flag is an error: list what is in
`methods/` and stop. `--grill` still works and means the same as omitting it.

## The eight phases

| # | Phase | Writes to | Ends when |
|---|---|---|---|
| 0 | Scaffold | `my-sessions` | the folder exists and `notes.md` is written |
| 1 | Read | `my-sessions` | you have heard what arrived and the state of the record in plain words |
| 2 | Digest | `my-sessions` | `digest.md` says where every piece of the input goes |
| 3 | Confirm | `my-sessions` | you have said yes or no to each split |
| 4 | Grill | `my-sessions` | you say stop, or no holes remain |
| 5 | Update | `<docs>` | every change is in the record with a dated FDC note |
| 6 | Lint | `<docs>` | the record lint passes |
| 7 | Close | `my-sessions` | `notes.md` says what changed, what went ready, and the questions for the next meeting, in order |

Shorter, and it is the rule to remember:

| `/fde:fdc-session` phase | Writes to |
|---|---|
| 0 to 4 | `my-sessions` |
| 5 and 6 | `<docs>` |
| 7 | `my-sessions` |

Nothing before phase 5 touches the record. That is the point of the digest
and the confirmation: you see the split before it lands.

Run the phases in order. Never skip forward, and never start a phase whose
gate has not been answered.

Phases 2 to 5 are the pack's. Everything else is this file's. Phase 2 is
skipped when nothing arrived, and the pack goes straight to the grill.

The directory column is invariant. It does not change with the pack, the size
of the input or the length of the session.

## The phase marker

`notes.md` carries `Phase:` in its front block. Update it the moment a phase
ends, before doing anything else.

This is the one thing that makes a long session survivable. Context gets
compacted, a chat gets closed, an agent gets replaced. Whoever picks it up
reads `Phase:` and `▶ Resume here` and knows exactly where they are. A phase
marker that lags reality is worse than none.

## Keeping it resumable

Four things let anyone pick the work up cold. Keep them current every time
you stop, and bump **Last updated**.

- **Phase** — which of the eight you are in.
- **▶ Resume here** — the single next action.
- **Progress log** — a dated line for what you did.
- **Status** — where things stand.

Write a **Carry forward** block into `notes.md` at every phase boundary. This
skill keeps a record, so what is lost with a closed conversation is never a
stack trace. It is what a fresh reader cannot rebuild by rereading the files:

- a constraint the user stated once, not yet written into `digest.md` or an
  answer in a check;
- a hole the grill found and the answer given, where the write to the record
  is still pending;
- the reason behind a judgement call, where the record shows the outcome but
  not why.

Empty is a normal answer. A session that flushed everything to its proper file
needs no carry forward.

Resuming is phase 0 step 3. If the folder already exists, read `Phase:` and
carry on from there rather than starting at phase 1.

## Context, and where to shed it

An FDC session is shorter than an AIE one, and it usually finishes inside one
window. Two boundaries can shed context if it does not.

| Boundary | Under 200k | Over 200k |
|---|---|---|
| 3 → 4, confirm to grill | carry on | compact |
| 4 → 5, grill to update | carry on | compact |

Flush before you shed, every time. `Phase:` and `▶ Resume here` current in
`notes.md`, and anything you said that is not yet in a file, written into
one. Step two is the one that gets skipped. A compaction replaces the
conversation with a summary of it, so a constraint stated once and never
written down does not survive.

At 4 → 5:

```
/compact Keep the session folder path and the Phase marker. Keep every hole
the grill found and the answer you gave, including the ones that became open
questions. Keep any constraint stated in conversation that is not yet in
digest.md or notes.md. Drop the file contents we read; they are in raw/ and
in the wiki.
```

**Never let auto-compact fire on its own.** It fires when the window fills,
which is most likely in the middle of the grill, and losing half the answers
means asking them again.

## The orchestrator never edits the record inline

Every write to `<docs>` goes to a subagent. The orchestrator holds the
conversation, decides what changes, dispatches, and reads what comes back.

The one exception is the grill conversation itself, which stays with the
orchestrator because it is the conversation with you. A subagent cannot ask
you a question and wait for the answer.

Kind of job per phase:

| Work | Kind of job |
|---|---|
| Digest, phase 2 | Judgement |
| Grill, phase 4 | The orchestrator, whatever model the session runs on |
| Research, wherever it happens | Judgement |
| Filing and moving text, phase 5 | Mechanical work that something else checks |
| ADR writing, phase 5 | Judgement |
| Milestone edits, phase 5 | Search and implementation |

The three kinds are mechanical work that something else checks, search and
implementation, and judgement. The user's global instructions say which model
runs each kind. This file never names one.

**Verify what a report claims, where the claim is load-bearing.** A subagent
report is evidence of what an agent believes, not of what is in the tree.
Check the rows it says it wrote and the links it says now resolve.

---

## Phase 0 — Scaffold

### Inputs

- **What arrived** (optional): a path, a transcript, "brain dumps",
  "research", or nothing. Phase 1 resolves it. Do not block on it.
- **Detail** (required): a few words describing the session, e.g. "third
  meeting" or "charter gaps".
- **Method** (never given in practice): defaults to `grill`. Only a
  `--<name>` flag changes it, and only if `methods/<name>.md` exists.

If the user gave no detail, ask one short question and then proceed.

### Steps

1. **Check the record.** You were invoked from the umbrella. Confirm
   `<docs>` is on `main` and clean, then pull it, because other sessions
   push there. If it holds another branch, say which and ask before going on.

2. **Find or create the session folder.** Look in `my-sessions/INDEX.md`, under Active, for an open `fdc` row. If there is one, reuse that folder and say so. Read its `Phase:` marker and resume from there, rather than starting at phase 1. A folder with no marker starts at phase 1.

   Only when there is no open row, run `python3 ~/.claude/skills/sessions/scripts/sessions.py new --type fdc --slug <slug>`. It chooses the session folder path and the folder name, and writes `notes.md` from the shared template. Follow `~/.claude/skills/sessions/SKILL.md` for the notes contract and the close step.

4. **Fill the front block.** Set what arrived, the detail, the method and `Phase: 1 read`, using the FDC fields listed under "notes.md fields" below.

5. **Say the path**, then go straight into phase 1. Do not stop and wait.

---

## Phase 1 — Read, in plain words

Two things get said back: what arrived, and where the record stands. Keep the
whole thing to roughly 250 words.

### Work out what arrived

The argument is free text. Resolve it to one of five:

| It looks like | Then |
|---|---|
| a path under `raw/` | a client document. It goes through `/fde:file` at phase 2 |
| a path or paste that is a transcript or a mail chain | read it directly. It never enters `raw/` as a claim source without a ledger row |
| the word "brain dumps" | read `project/brain-dumps/` for entries dated since the last FDC session |
| the word "research" | nothing arrived. Phase 2 is a research pass instead of a digest |
| nothing | nothing arrived. Skip phase 2 and go to the grill |

Where the argument is a path that does not exist, say so, list what is near
it, and ask. Never guess a file.

### Read the state of the record

Five files say where the record stands. Read all five, every session. Where
`apps` is set, read them for the session's app, and `<record>` in the table is
that app's path. Where `apps` is empty, they sit at the paths shown.

| Read | For |
|---|---|
| `$REC/raw/ledger.md` | material that arrived and was never filed |
| `$REC/project/charter.md` | rows still open |
| `$REC/wiki/process.md` | exception prompts still blank |
| `$REC/project/plan-ledger.md` | nodes still pending |
| `$REC/project/milestones/` | milestones short of `ready` |

Say back what you found, one line each, with counts. Then write it into
`notes.md` under **State of the record**.

Two rules for this phase.

Say what is thin. A charter with four open rows is a charter with four open
rows, and softening that hides the work.

Never fill a gap from your own reading here. That is the grill's job, and
doing it now hides how thin the record actually is.

---

## Phases 2 to 5 — Hand off to the method pack

Read `methods/<method>.md` and follow it. It owns digest, confirm, grill and
update.

Four things this file guarantees the pack, and the pack may rely on them.

The session folder exists and its path is known. The pack writes `digest.md`
into it, never into a path of its own choosing.

What arrived is resolved and written down. The pack does not re-resolve it.

`<docs>` is on `main`, clean and pulled.

The checks in `methods/grill/checks/` are current. They are what the pack
uses to know what a hole is.

The pack reports back one of two things: the update is done, or it is blocked
and why. Then this file resumes at phase 6.

---

## Phase 6 — Lint

Run the record lint from the umbrella. The script ships with the plugin:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/lint_record.py" "$DOCS" "$REC"
```

The script takes the docs root, then the record root. Links and
guardrails are checked at the docs root; the milestone, question and wiki
checks read the record root. See "Finding the
engagement" above where `CLAUDE_PLUGIN_ROOT` is unset.

It checks six things:

- every milestone holds its required parts;
- every `waits-on` resolves;
- every open question has an owner;
- every guardrail names its source;
- every milestone names its delivery or `none`;
- no page under `project/` or `wiki/` is unlinked.

It exits non-zero on a finding.

When the engagement has a knowledge folder, also run, beside `lint_record.py`:

```bash
python3 ~/.claude/skills/sessions/scripts/wiki_lint.py --knowledge <path>
```

Treat its findings the same way as the record lint's.

Every finding is fixed in this session or written into `notes.md` with the
reason it stands. A finding left silent is a finding that will be inherited.

A fix goes to a subagent, one finding at a time, the same as every other
write to the record.

---

## Phase 7 — Close

1. **Write the five blocks in `notes.md`**: what arrived, what changed in the
   record, what went `ready`, the decisions made on assumption, and the questions
   for the next meeting in the order to ask them.

   The order matters. A meeting runs out of time, and the question that
   unblocks a milestone should not be the one that got cut.

   The decisions block lists each business question the FDC decided this
   session on thin evidence, its open-question id, and that it is a working
   assumption. The user glances at it. Empty is a normal answer.

2. **Promote what the session raised.** A question the client must answer goes to
   `project/open-questions.md` with an id and a named owner. Our own fieldwork
   goes to `project/next-steps.md`.

3. **Write `handoff-<who>.md`** only where something has to reach a person the
   record does not reach. Most sessions do not need one.

4. **Set the front fields and check them.** Set `Status: done`, write `Summary:` in one line, and set `Owes:` to what is still owed, or `none`. Use `blocked` only inside `Owes`. Then run `python3 ~/.claude/skills/sessions/scripts/sessions.py check <folder>`. If it exits non-zero, fix the notes and run it again. When it passes, run `python3 ~/.claude/skills/sessions/scripts/sessions.py index --write`.

5. **Set `Phase: 7 done`**, write the last **Progress log** line, and clear
   **▶ Resume here** to say the session is finished.

6. **Push `<docs>`.** Pull first; another session may have moved `main`
   while this one ran. `my-sessions` has no git, so it needs no push.

## The session folder

`sessions.py new --type fdc` chooses the path. The folder always holds
`notes.md`. It holds `digest.md` when something arrived. It holds any artefact
the FDC makes, by name. It holds `handoff-<who>.md` only when something has to
go to a person the record does not reach.

It is thinner than the AIE's folder, because the FDC's output is the record
rather than a branch.

## notes.md fields

`sessions.py new` writes the shared front block and sections. The FDC adds
these front fields:

- What arrived: a path, transcript, brain dumps, research, or "nothing".
- Method: `grill`, unless a flag picked another.
- Phase: `0 scaffold` to `7 close`, or `7 done`.
- Status: active | paused | done. Use `blocked` only inside Owes.

It adds these sections after **Resume here**: **What arrived** (phase 1's
read-back), **State of the record** (phase 1's five lines: unfiled material,
open charter rows, blank exception prompts, pending plan-ledger nodes,
milestones short of ready), **What changed in the record** (phase 5's log, one
dated line per change, append only), **What went ready** (milestone ids set to
`ready` this session, and what made each one ready; empty is a normal answer)
and **Decisions made on assumption** (each business question the FDC decided on
thin evidence, its open-question id, and whether it is a working assumption)
and **Questions for the next meeting** (in the order to ask them, each linking
its open-question id).

## Writing to the record

Every note the FDC writes carries the hat: `*Widened 04-09-26, FDC.*` The
hat is `FDC` or `AIE`. `CLAUDE.md` holds the rule and this file follows it.

Only the FDC sets a milestone to `ready`. `/fde:aie-session` sets `building` and
`built`, and refuses anything that is not `ready`.

A widen, narrow, recut or drop is a conversation between the two roles
first. Then whoever does the deed writes the note. On a solo pod that
conversation is one person across two chats, so the note is the only trail
there is.

A client guardrail comes from the client, the law or the contract, and the
FDC owns it. A build guardrail is the FDC's suggestion about how to build,
and the AIE may override it with a dated note and a reason. Every guardrail
names where it came from.

## Notes

- Session folders sit at the root of `my-sessions`, a sibling of
  `<docs>`. It is a plain folder with no git, kept on this machine only. `<docs>` never holds or links to a session record.
- A client PDF, spreadsheet or drawing goes to `raw/` through `/fde:file`, so
  it gets a ledger row and an authority tier. A copy in a session folder has
  neither.
- Do not put secrets in `notes.md`. Redact before pasting.
- This scaffolds **up front**. For chats nobody scaffolded, run
  `/fde:session-sync` afterwards.
- Adding a way of scoping means adding a file to `methods/`. Read
  `methods/README.md` for the contract it has to meet. Nothing in this file
  changes.
