---
name: aie-session
description: "Run one build session end to end, from an empty session folder to a merged branch. A milestone is optional; when one is given it must be marked ready by the FDC, and with none the session takes its scope from the user's words. Scaffolds a session folder in my-sessions, resolves any open items, says the scope back in plain words, reconciles the milestone against your feedback, hands design and plan to a method pack, opens a branch in the code repositories for the long implementation run, then walks the result in a browser, fixes what the walk found and merges it there. Use when starting a build, or when the user says \"start a session\", \"new session\", \"build the next milestone\", or invokes /fde:aie-session [milestone] <detail> [--afk]. Runs the superpowers method by default; a --<method> flag is only needed to pick a different one."
---

# aie-session

Take one piece of work from nothing to a merged branch, in one chat, with
the record written as you go. The work is a `ready` milestone when the user
names one, and whatever the user describes when they do not.

This is the AI engineer's workbook. The forward deployed consultant writes the
milestone and marks it `ready`. The AIE builds it. The milestone file is the
handoff between the two, so when one is given this skill reads it first and
refuses anything the FDC has not finished. A session with no milestone has no
such file and never refuses to start for want of one.

It is the single touch point for a build. It scaffolds, scopes, reconciles the
milestone, drives the spec and the plan, opens a branch in the code
repositories for the long run, walks the result in a browser, fixes what the
walk found, and merges it there.

Claude is always started from the umbrella. `<docs>` holds the engagement
record. `my-sessions` holds this session's folder, and `<docs>` never links
to it. `<be>` and `<fe>` hold the code, where they exist yet.

**How we build** is not written here. It is a method pack in `methods/`, and
`superpowers` is the default. The pack can change without this file changing.
`lanes.md` carries the worktree rules a long build needs.

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

## The milestone is the contract

A milestone is optional. The user may start a session without one. With one,
the slug is `<milestone>-<slug>` and every milestone step below runs. With
none, the slug is `<slug>` alone and the session takes its scope from the
user's words. Every step in every phase that reads, checks, edits or stamps a
milestone runs only when one was given, and is skipped without comment when
none was. A finding that would have gone back to the milestone through phase
2 goes into `notes.md` under **Scope, in plain words** instead.

A milestone carries one of five statuses in its front matter. The status is
the first word of the field, and a date follows it.

| Status | What it means |
|---|---|
| `draft` | the FDC is still writing it, so this skill will not start |
| `ready` | the FDC has finished it and the AIE may start |
| `building` | an AIE session has it. Phase 0 sets this |
| `built` | it is merged and walked. Phase 8 sets this |
| `dropped` | we chose not to build it, and the file stays to say why |

Only the FDC sets `ready`. This skill sets `building` and `built`, and sets
`draft` in the one case phase 1 names. It sets nothing else.

`waits-on:` sits beside `status:` and names the milestones this one needs
first. It is a field, not a status.

## Overriding a build guardrail

`setup/guardrails.md` holds two kinds of guardrail, and they are not treated
alike.

A client guardrail comes from the client, the law or the contract. The FDC owns
it. This session cannot override it, cannot soften it and cannot work around
it. Where one blocks the build, stop and raise it with the FDC.

A build guardrail is the FDC's suggestion about how to build. It binds until
the AIE overrides it. That is allowed in any phase, and it needs the FDC
conversation first, the same as a recut.

To override one, add a dated note under that guardrail in
`setup/guardrails.md`, in this shape:

*Overridden 07-09-26, AIE: the registry needs one shared client, so a second
one would duplicate the retry logic.*

The reason is the whole point. A note that says a guardrail was overridden and
not why leaves the next session to guess. Write the same line into `notes.md`
under Decisions, then commit and push it with the change that needed it.

Every guardrail names where it came from, and that line is what tells you which
kind it is. A guardrail with no source is a record lint finding, so raise it
rather than deciding its kind yourself.

## Invocation

```
/fde:aie-session [<milestone>] <detail> [--afk]
```

The milestone is optional. When one is given it has to read `ready`. Phase 0
checks the status before anything else and stops on any other word, so a build
never starts on a milestone the FDC has not finished. When none is given,
nothing is checked and the session starts.

Every session runs a method pack, with a milestone or without one.
`superpowers` is the default, so there is nothing to type:
`/fde:aie-session mNN <a few words>` runs it, and so does
`/fde:aie-session <a few words>`.

Two packs exist. `superpowers` runs the full ceremony: a design
conversation, a spec, a task-decomposed plan, and a reviewer after every
task. `quick` runs plan mode instead of the design and the spec, and one
implementer subagent per task with a single review at the end.

Both build in the code repositories and both build with subagents. Nothing here
ever builds inline. The pack changes the ceremony in front of the build, not
where the build happens and not how its context is isolated.

### Flags

Read the flags first, before anything is scaffolded. Phase 0 writes them into
`notes.md` as **Flags**, and every later phase reads them from there. A
resumed session trusts the file, not its memory of the command.

| Flag | Effect |
|---|---|
| `--afk` | The user is away. Nothing waits on them, as "Away from the keyboard" below says |
| `--<method>` | Picks a pack other than `superpowers`, and only if `methods/<method>.md` exists |

`--superpowers` still works and means the same as omitting it. Any other flag
is an error: list the flags above and what is in `methods/`, and stop.

### Away from the keyboard

`--afk` follows the "Away mode" rule in the global `CLAUDE.md`, and that rule
is the only place its text lives. The user may pass the flag, or say
mid-session that they are going away. Either one writes `afk` into **Flags**
in `notes.md`. A question already open when the flag lands is answered under
the rule, the moment it lands.

Under the rule, this skill adds two things.

1. `--afk` changes who answers a question, never how the walk runs. The
   regression and acceptance walks still run in full, with nobody at the
   keyboard.
2. Only two things stop an away session. The first is a confused milestone in
   phase 1, which applies only when a milestone was given. The second is a
   scenario entry that the walk cannot make pass.

Nothing else waits. The user's own words go into **Carry forward**.

## The nine phases

| # | Phase | Writes to | Ends when |
|---|---|---|---|
| 0 | Scaffold | `my-sessions` | the folder exists and `notes.md` is written |
| 0b | Resolve open items | `my-sessions` | every open item is settled or waiting on the user. Runs only with a milestone |
| 1 | Scope | `my-sessions` | the user has heard the scope in plain words |
| 2 | Reconcile | `<docs>`, the milestone file | the user says the scope is right. Runs only with a milestone |
| 3 | Design | `my-sessions` | the user approves `spec.md` |
| 4 | Plan | `my-sessions` | the user approves `plan.md` |
| 5 | Build | `<be>` and/or `<fe>` | the suite is green and every branch is pushed |
| 6 | Walk, in 6a store, 6b regression and 6c acceptance | `$REC/tests/scenarios`, and `my-sessions` | the store is updated, every scenario is walked or recorded as blocked, and the bugs are written down |
| 7 | Fix | `my-sessions`, and the code branches | the bugs are closed, the suite is green, and the user has answered the re-walk question |
| 8 | Close | `<docs>` and `my-sessions` | the milestone reads `built` and the record has graduated |

Shorter, and it is the rule to remember:

| `/fde:aie-session` phase | Writes to |
|---|---|
| 0 to 4 | `my-sessions`, and the milestone file in `<docs>` at phase 2 |
| 5, the build | `<be>` and/or `<fe>` |
| 6 to 8 | `my-sessions`, the scenario store in `<docs>` at phase 6a, and the engagement pages in `<docs>` at phase 8 |

Phases 6 to 8 write the session record in `my-sessions`, apart from the scenario store in 6a. Phase 7's fixes
and phase 8's merge happen on the code branches as well. Nothing ever writes a
session record into `<docs>`, and `<docs>` never links to one.

Phase 0 and phase 8 each stamp one word on the milestone file, `building` and
`built`. That stamp is the only thing phase 0 writes outside `my-sessions`.

Run the phases in order. Never skip forward, and never start a phase whose gate
has not been answered.

Phases 3, 4 and 5 are the pack's. Everything else is this file's.

The directory column is invariant. It does not change with the pack, the size
of the milestone or the length of the build. A pack never opens a branch of its
own; this file does that around it.

## One branch per milestone, in each code repository

The branch name is the milestone id, or the slug when there is no milestone,
and it is identical in `<be>` and `<fe>`. That is rule 6 of
`${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/repo-layout.md`. A milestone
can need one repository or both, and phase 5 says which it opens.

`<docs>` never branches. The session folder, the spec, the plan and the
findings are all written into `my-sessions`, in every phase, and never
into `<docs>`. `my-sessions` is a plain folder with no git, so
there is nothing to pull or push there.

The milestone branch is cut at phase 5 and merged at phase 8. Nothing merges
in between, and phase 7 does not cut a second branch.

The walk is the reason. It runs against the branch, because that is where the
work is, and it is the first thing to say whether the work is usable at all.
A walk has found two dozen things on a build whose suite passed, and among
them a document nobody could sign. Merging that at phase 5 would have put a
delivery-shaped hole into `main` and called it built.

So the `merge_into` branch receives a session once: walked, fixed, and green. A session that
needs unmerged work branches off the milestone branch rather than off `merge_into`,
which is ordinary and costs nothing.

## The phase marker

`notes.md` carries `Phase:` in its front block. Update it the moment a phase
ends, before doing anything else.

This is the one thing that makes an eight-hour session survivable. Context
gets compacted, a chat gets closed, an agent gets replaced. Whoever picks it
up reads `Phase:`, `Branch:` and `▶ Resume here` and knows exactly where they
are, including which repository the work is in. A phase marker that lags
reality is worse than none.

## Context, and where to shed it

A full session runs past 500k tokens. Quality falls well before the window
does, so the trigger is quality and never capacity. Waiting for auto-compact
means a hundred thousand tokens were already spent thinking badly.

Three boundaries can shed context. The orchestrator decides at each one,
from how much it has spent.

| Boundary | Under 200k | 200k to 500k | Over 500k |
|---|---|---|---|
| 4 → 5, plan to build | carry on | compact | clear and restart |
| 5 → 6, build to walk | carry on | compact | clear and restart |
| 7 → 8, fix to close | carry on | compact | compact |

Read the remaining-token signal in your own context to decide. Where it is
not available, use the proxy: the design conversation ran more than about
thirty exchanges, or the build ran more than about ten tasks.

**Never let auto-compact fire on its own.** It fires when the window fills,
which is most likely in the middle of phase 5, and losing the plan's context
between task nine and task ten corrupts every task after it. Shed at a
boundary you chose.

If phase 5 crosses 500k mid-build, do not push on to the end. Finish the
current task, write the ledger, and clear. `subagent-driven-development`
resumes from its progress ledger, and `quick` resumes from the todo list in
`plan.md`.

### Write as you go

A session can be compacted at any point, and the user may close it and start
the skill again. So the session folder must hold what a compacted or fresh
orchestrator needs at every moment, not only at a phase end.

Compaction can land right after the user speaks and before you act on it. So
when they give any input (an answer, a decision, a correction, a flag), write
it into `notes.md` first, then act on it.

After every decision, every answer from the user and every subagent report,
write one line. It goes in `notes.md`, or in the phase's own file where one
exists, such as `decisions.md`, **Milestone changes** or
`bugs-and-improvements.md`. Keep it to one line, and link a report or a file
rather than copying it.

At the same moment, rewrite **▶ Resume here**: what you are doing now, and the
next step. A line that names a subagent still running says which one and what
it was sent to do.

### Resuming

The session folder's path is written at the top of `notes.md` and repeated in
**▶ Resume here**, so a compaction summary carries it.

A fresh session is the user starting `/fde:aie-session` again on the same
milestone, or with the same slug when there is no milestone. Phase 0 finds the
folder, and the session resumes from it rather than scaffolding a new one.

Both cases read the same way. Grep `notes.md` for `Phase:`, `Branch:`,
`▶ Resume here`, **Flags**, **Carry forward** and **Decisions**, and read each
as a line range. Then read the one ledger or file that **▶ Resume here**
names, and nothing more. Never re-read `spec.md` or `plan.md` whole. Where the
folder and the summary disagree, trust the folder.

### Flush before you shed

Compaction is safe exactly to the degree the record is current. Both
compacting and clearing need this first, every time.

1. `Phase:`, `Repositories:`, `Branch:` and `▶ Resume here` current in
   `notes.md`.
2. Anything the user said that is not yet in a file, written into one.
3. Any open code branch committed and pushed.

Step 2 is the one that gets skipped. A constraint stated once in
conversation and never written down does not survive either route.

### What to keep

Three things are genuinely unrecoverable from disk, and every instruction
below names them.

The approaches we rejected and why. `brainstorming` proposes two or three
and only the winner reaches `spec.md`. A later agent that does not know X was
rejected will propose X again.

Write each rejected approach into `spec.md`, and also into `notes.md` under
`## Carry forward` as `Rejected: <option>, because <reason>, <date>, <who>.`
A pointer such as "listed in spec.md" does not count.

Constraints the user stated in passing that never reached a document.

Which tasks needed a fix subagent. Those are where to look hardest during
the walk, and nothing on disk ranks them.

Add to **Carry forward** rather than replacing it.

### The instructions

At 4 → 5:

```
/compact Keep the session folder path, the branch, the code repositories in
play, the milestone id and the Phase marker. Keep every approach we rejected
and the reason it lost. Keep any constraint the AIE stated in conversation that is
not written into spec.md or plan.md. Drop the file contents we read, the
codebase exploration, and the drafts; the spec and the plan are on disk and
approved.
```

At 5 → 6:

```
/compact Keep the branch and the Phase marker. Keep which
tasks needed a fix subagent and what the fix was. Keep anything the final
review flagged and did not fix. Drop the per-task briefs and reports; they
are on disk in .superpowers/sdd/.
```

At 7 → 8:

```
/compact Keep the branch, every row still open with where it was routed,
and the grouping and ordering decided in triage. Drop the walk itself; the
findings are in bugs-and-improvements.md and the route is in
smoke-test-walk.md.
```

### Clearing instead of compacting

Above 500k at either of those two boundaries, clear rather than compact. A
summary is lossy in ways nobody can predict; a written record is lossy in ways
this skill already controls.

Both boundaries change what you are working on anyway, so a fresh session is
the natural shape. Start it with:

```
/fde:aie-session <milestone> <detail>
```

It finds the existing folder, reads `Phase:` and `Branch:`, and resumes. That
is what phase 0 step 5 is for.

### Phase 5 should not need this

The orchestrator dispatches a subagent, records a ledger line, and moves on.
It does not read diffs and it does not write code. If phase 5 is filling the
window, the orchestrator is doing work that belongs to a subagent.

---

## Phase 0 — Scaffold

### Inputs

- **Milestone** (optional): an id like `mNN`. Omit it to start without one.
  Never block on it, and never ask for one.
- **Detail** (required): a few words describing the work, e.g. "fact store
  tier cascade". With no milestone the detail is also the scope.
- **Method** (never given in practice): defaults to `superpowers`. Only a
  `--<name>` flag changes it, and only if `methods/<name>.md` exists.
- **Flags**: `--afk`, as "Flags" above says.

If the user gave no detail, ask one short question and then proceed. Under
`--afk` take the detail from the user's own words and carry on.

### Steps

No step below stops a session that has no milestone. Steps 2, 3 and 8 run
only when a milestone was given, and the others run as written.

1. **Read the flags and resolve the app.** Read the flags first. Then, only
   when `.engagement` sets `apps`, resolve the app: take it from the milestone
   id or the folder the milestone sits in, and where there is no milestone from
   the user's words. If neither names one, ask once. Under `--afk`, pick the
   first listed app and write the choice under **Decisions**. `$REC` is then
   `$DOCS/<record>` for that app. With `apps` empty, skip this step.

2. **Resolve the milestone.** Only when the user gave an id. Check
   `$REC/project/milestones/` for a file starting with it:

   ```bash
   ls "$REC"/project/milestones/ | grep "^m01-"
   ```

   No match means a typo. Say so, list the ids that do exist, and ask. Under
   `--afk`, take the one id that is closest, and write the choice under
   **Decisions**. Never scaffold against an id with no milestone file, because
   the folder would be unfindable by the one thing that names it.

3. **Check the status.** Only with a milestone. Pull `<docs>` first, because
   another session may have stamped this milestone since your last fetch. Then
   read `status:` in the front matter and take the first word of the field.

   `ready` is the only status this skill starts on. Carry on, and step 8
   stamps it `building`.

   `building` means a session already holds this milestone. Find its folder in
   `my-sessions`, say which one, and resume from its `Phase:` marker instead of
   starting again. If no folder exists, say so and ask before going on.

   `draft`, `built` or `dropped` stops the session. Name the status you found,
   say in one line what it means, and stop there. Never edit the milestone to
   get past this. A `draft` milestone is one the FDC is still writing, so ask
   them to finish it and mark it `ready`. Only the FDC marks a milestone
   `ready`, and this skill never does. The user can still start the same work
   with no milestone, by running the skill again without the id.

4. **Check the repositories.** You were invoked from the umbrella, so every
   folder `.engagement` names is in view. Confirm `<docs>` is on `main` and
   clean, and pull it if step 3 did not. If it holds another branch, say
   which and ask before going on. Note which of `<be>` and `<fe>` this work
   will touch, and say so if `.engagement` leaves one empty.

5. **Create the session folder.** Run it from the umbrella, or pass
   `--root <umbrella>`:

   ```bash
   python3 ~/.claude/skills/sessions/scripts/sessions.py new --type aie --slug <slug>
   ```

   With a milestone the slug is `<milestone>-<slug>`. With none it is
   `<slug>` alone. The script chooses the session folder path and the folder
   name, and writes `notes.md` from the shared template. Follow
   `~/.claude/skills/sessions/SKILL.md` for the notes contract and the close
   step. If a folder with that slug already exists, resume it rather than
   scaffolding a second one.

6. **Adopt a standalone smoke folder.** A folder holding a
   `bugs-and-improvements.md` and no `notes.md` came from a standalone
   `/fde:smoke-test` run. Write a `notes.md` at `Phase: 7 fix` and start
   there, because the walk has already done the scope work phases 1 and 2 do.

7. **Fill the front block.** Set the milestone link (or "none"), the detail,
   the method, the flags and `Phase: 0b open items` when a milestone was
   given, otherwise `Phase: 1 scope`. Use the AIE fields listed under
   "notes.md fields" below.

8. **Stamp the milestone `building`.** Only with a milestone. Set
   `status: building <DD-MM-YY>` in the milestone's front matter, so another
   session can see this one has it. The status is the first word of the field
   and the date follows it. Regenerate `$REC/project/milestones/index.md`, then
   commit and push, pulling first because other sessions push to `main` too.

   A resumed session finds `building` there already and leaves it alone. A
   status stamp is mechanical, so it carries no note. Phase 2's scope changes
   do.

9. **Say the path**, then go straight into phase 0b when there is a milestone
   and into phase 1 when there is not. Do not stop and wait.

---

## Phase 0b — Resolve the open items

Runs only when a milestone was given. With none, skip to phase 1.

A milestone often reaches the AIE with choices nobody has made. Which model
runs an extraction is the usual example. The record may say only that cost
should be low and quality high enough. This phase settles each such choice
before phase 1 reads the scope back, so the read-back describes a milestone
with its choices made.

### Find the open items

Read the milestone file and list every choice it leaves open. An open item is
any of these:

1. a question in its `waits-on` that nobody has answered;
2. a "to be decided", "tbd" or "or" left in its scope;
3. a model, library, approach or limit the milestone needs but does not name.

Write them into `notes.md` under **Open items**, one row each. If the list is
empty, say so in one line and go to phase 1.

If the milestone is too confused to list its open items, that is phase 1's
"When you cannot say it back" case. Apply it here and stop. Never spend a
spike on a milestone the FDC has not finished.

### Three ways to settle an item

Settle each item one of three ways. Try them in this order.

1. **Decide it yourself.** First read the record and every earlier spike.
   Earlier spikes sit in `my-sessions/misc/*spike*/`, each with a `report.md`.
   A spike already run often holds the number that settles the item. Decide
   when the evidence settles it, when the choice is cheap to reverse, or when
   the record's own rules point to one answer. A business question is decided
   this way too, in the FDC hat.
2. **Ask the user.** Ask only when the choice is genuinely theirs and they are
   at the keyboard. Their choices are those that spend money, change what the
   product does for the client, or go against something they said. Ask one
   item at a time, with your recommendation first.
3. **Run a spike.** Run one when a measurement would settle the item, the
   record cannot, and a wrong guess is costly to undo. Model choice, cost per
   project, extraction recall and speed under load are all spike questions. For
   a model choice, run the candidates on one real document and pick the
   cheapest that clears the bar.

Under `--afk` nothing goes to the user. An item that would have been theirs is
spiked if a measurement settles it. Otherwise it is decided under the "Away
mode" rule.

### How a spike runs

Each rule below cost a lesson to learn.

1. A spike answers one question, named in its brief, with a number. It stops
   at the edge of that question.
2. A subagent doing judgement work leads it. It runs on its own stack and
   never on the port the main stack uses. It makes no product code changes,
   because a spike measures what exists.
3. It scores against a truth set built from a real client document in
   `$REC/raw/`. Client documents stay on this machine.
4. Paid model calls get a dollar budget, written in the brief. The lead checks
   the key's usage before it starts, logs spend to a file as it goes, and stops
   at the budget. Nobody changes the key's own settings.
5. The lead returns its report as text. The orchestrator writes it to
   `my-sessions/misc/<DDmmmYY>-spike-<slug>/report.md`, so later sessions find
   it by the same glob.
6. A product bug the spike finds goes into its report and into the **For**
   section of `notes.md`. The spike does not fix it.

Spikes on separate items run in parallel, each with its own budget.

### Record each answer

Each settled item gets its answer, the way it was settled and its evidence in
**Open items**. The evidence is a file path, a spike report or the user's
words. Copy each answer into **Decisions** as well, so `decisions.md` carries
it to the writers after phase 2.

Where an answer changes the milestone itself, phase 2 makes the edit with its
dated AIE note. This phase writes nothing in `<docs>`.

The phase ends when every item is settled, or is marked as waiting on the user
with the reason. A waiting item goes to phase 2's questions. Then go straight
into phase 1.

---

## Phase 1 — Scope, in plain words

With a milestone, read its file and say back what we are about to build, in
words a person can follow. With none, say back the scope from the user's own
words, and ask whether it matches what they want built. This is a read-back,
not a design and not a plan.

Keep it to roughly 200 words. Cover four things and nothing else.

1. What a person will be able to do at the end that they cannot do now.
2. The parts being built, named plainly.
3. What is deliberately out, and which milestone holds it instead.
4. What the milestone waits on, and what it is missing. Name the open
   questions by id and say plainly that nobody has answered them.

Then write it into `notes.md` under **Scope, in plain words**. With no
milestone, items 3 and 4 cover only what the user said was out, and what the
work waits on.

### Propose the pack in the same breath

Do not ask which method to use. Read the milestone, or the user's words when
there is no milestone, and say which one it looks like, with the reason, then ask the one question that covers both: does this
match what you want built, and is `<pack>` the right weight for it?

Propose `superpowers` when any of these is true:

- the milestone builds a mechanism later milestones sit on
- it needs a migration
- it waits on an unanswered question, so the design has real choices in it
- its **In scope** runs to five blocks or more

Otherwise propose `quick`. With no milestone, judge by the same signs in what
the user described.

**A thin milestone file is not evidence of small work.** One milestone may
run to 2000 words with ten scope blocks while every other one is 400 to 800.
On length alone the short ones look like the smallest jobs on the plan. They
are often thin because the wiki has not been filed over the material they
rest on. Before proposing `quick` on a short milestone, check
`$REC/project/plan-ledger.md`. If its nodes are still pending, the answer is
neither pack. The milestone is not ready to build, so send it back to `draft`
by the rule below and hand it to the FDC.

Write the chosen pack into `notes.md` as **Method**.

Two rules for this phase.

Use the milestone file as the only source, or the user's words when there is
none. If the source is thin, say it is thin. Do not fill the gap from the wiki, from a brain dump or from your
own reading — that is phase 3's job, and doing it here hides how thin the
milestone actually is.

Never argue the scope up or down here. You are checking you read it the same
way they did.

### When you cannot say it back

This section applies only when a milestone was given. With none, a read-back
that will not come is one short question to the user. Under `--afk`, take the
reading that is easiest to reverse and write it under **Decisions**.

Sometimes the read-back will not come. The scope is ambiguous, two sections
contradict each other, or the milestone names something nobody has written
down. That is a milestone the FDC has not finished, and guessing here does not
fix it.

Set the milestone's `status:` to `draft <DD-MM-YY>` and add a dated note in the
milestone file, where the confusion sits:

*Returned to draft 07-09-26, AIE: the exit criteria name a signed document and
the scope names an unsigned one.*

Name what was unclear, and never what you would have built instead. Then
regenerate `$REC/project/milestones/index.md`, commit, push, write the same line
into `notes.md`, and stop the session. The FDC finishes the milestone and marks
it `ready` again, and a fresh session picks it up. Do not go on to phase 2, and
do not settle the scope yourself.

---

## Phase 2 — Reconcile the milestone

Runs only when a milestone was given. With none, the scope is the user's
words in `notes.md`: skip to phases 3 to 5 once the user says the read-back is
right.

A loop. The user pushes back on the scope, you edit the record, you show what
changed, they push back again. It ends when they say the scope is right.

This phase exists because the milestone file is the authority and the session
is not. A scope decision taken in chat and never written down is lost the
moment the chat is.

### What you may change

**Edit this session's milestone.** In scope, out of scope, the assertion in
its title, and its `waits-on`. A widen, a narrow or a recut needs the FDC
conversation first, and then the note below. `status:` is not yours to move
here: phase 0 set it to `building` and phase 8 sets it to `built`.

**Edit another milestone.** Allowed when scope moves between them. Moving a
capability out of one milestone means that one loses it and another gains
it, and writing only one half is how the two files start lying to each
other.

**Create a milestone.** Allowed, and it costs more. A new milestone needs its
file, a row in `$REC/project/milestones/index.md`, a `delivery:` value or `none`,
and a row in `$REC/project/plan-ledger.md` recording that this session made it. It
starts at `status: draft <DD-MM-YY>`, because only the FDC marks a milestone
`ready`. Say out loud that the FDC will reconcile it against the wiki on their
next run. Until then it rests on a conversation rather than on evidence.

**Drop a milestone.** Not here. Dropping one means re-pending every wiki node
folded into it, and that work is the FDC's. Make the case for dropping it and
hand it over.

### What you must not change

Only touch the milestones the change actually reaches. If a scope move
affects two of them, the rest are not opened, not reformatted and not
re-worded. Untouched means untouched.

`$REC/project/milestones/index.md` is a derived view, so regenerate its table
from the files rather than hand-editing a row.

### Every note carries the AIE hat

A change to the record says which hat made it. This session wears `AIE`, so
every note it writes ends with that word:

*Widened 04-09-26, AIE.*

The verb is what happened: widened, narrowed, recut, dropped. The date is the
day of the change. The note names the decision and never the conversation that
reached it. So `*Widened 04-09-26, AIE, after talking it over with the FDC.*`
is wrong, and `*Widened 04-09-26, AIE.*` is right.

A widen, a narrow or a recut needs the FDC conversation first. The FDC owns
what a milestone claims, even while the AIE builds it. Moving that without them
is how the two roles start building different things. On a solo pod both hats
are one person in two chats, so the note is the only trail there is.

### Every loop, do these four things

1. Make the edit, with its dated AIE note.
2. Name every file you touched, and say why each one had to move.
3. Append the change to **Milestone changes** in `notes.md`, dated.
4. Ask again: is the scope right now?

### When the loop ends

Commit and push. Everything so far is engagement record on `main`, and other
sessions read it, so pull before you push. A question for the client goes to
`$REC/project/open-questions.md` with an id, in the same commit.

---

## Phases 3 to 5 — Hand off to the method pack

Read `methods/<method>.md` and follow it. It owns design, plan and build.

### Read the milestone's conventions before phase 3

Only with a milestone. It names its conventions in its "Guardrails" or "Rests on"
section. Read each named one from
`${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/<name>.md`, and hand it to the
pack with the scope. A convention the milestone does not name is not read.
Each file holds a spec and a checklist, and phase 8 runs the checklist.

Four things this file guarantees the pack, and the pack may rely on them.

The session folder exists and its path is known. The pack writes `spec.md`
and `plan.md` into it, never into a path of its own choosing.

The scope is settled and written down. The pack does not reopen it. If the
design uncovers a scope problem, the pack hands back to phase 2 rather than
quietly deciding.

`<docs>` is on `main`, clean and pushed. The session folder exists in
`my-sessions`.

The code branches exist and their suites are green **before the pack's build
stage starts**. This file does that, not the pack. See "Opening the build
branches" below.

The pack reports back one of two things: the build is done, or it is blocked
and why. Then this file resumes at phase 6.

**Verify what a report claims, where the claim is load-bearing.** A subagent
report is evidence of what an agent believes, not of what is in the tree.
Check the removals it says it made and the tests it says now fail. On one
run that caught nothing wrong in six reports and one thing right in a
seventh: an agent told to fix a cause named in a finding tested that cause
first, disproved it *and* the hypothesis in its own brief, and found the real
one. Read what came back rather than filing it.

### The decisions file comes first

Straight after phase 2 (or after phase 1, with no milestone), the
orchestrator writes `<session>/decisions.md`. It holds every decision from the
conversation, one line each with its reason. Keep it short. It is the writers'
brief, so a decision missing from it is a decision the spec will not carry.

Then a writer subagent writes `spec.md` from it, and a plan writer writes
`plan.md`. `quick` writes no spec. That may be one subagent or two. The plan
writer does judgement work, so where one subagent writes both, it is a
judgement-work subagent. A checker subagent then checks the plan against the
spec and `decisions.md`, and returns a short verdict and any open question.
For the spec writer and the checker, the orchestrator picks the model by how
hard the job is, under the user's subagent-model rule, and names it on the
dispatch.

The orchestrator reads the verdict and the open questions, and never the whole
plan. It settles each open question itself and appends it to `decisions.md`.
Only a question that is genuinely the user's goes to them. Under `--afk` the
orchestrator settles that one too.

### The go-ahead

Once the tasks are written and the branches are ready to cut, ask one line:
"Shall I start the build?" The build starts on the user's yes. Under `--afk`
it starts without asking.

### Bound the plan's reading

Whoever writes `plan.md` is given a named list of files to read, never "read
the codebase". One past plan writer, reading freely, reached 817k tokens
before it produced anything. Where a search subagent explores for the plan, it
gets the same named list and reports back what it found.

### Extracting the plan into the backlog

Once the checker's verdict is clean, write one task file per plan task into
`$REC/backlog/tasks/`, all at `To Do`. Commit and push them before any branch
is cut. The format and the rules for moving a task are in `backlog.md`, beside
this file.

The pack never does this, because a pack does not write to the record. This
file does it, at phase 4's end. During phase 5, keep each task's status true
as the pack reports, and write the changes at each track boundary.

A task file never links to or cites `my-sessions`. The plan stays there and
stays the plan. The tasks are the record's extract of it.

### Opening the build branches

The pack's design and plan stages write to `my-sessions`. Its build stage
does not.

Between phase 4 and phase 5, this file:

1. Names which code repositories the milestone touches, and says so out loud.
   A milestone can need one or both.
2. Cuts a branch in each of them from `origin/<merge_into>` (`main` when empty) with `--no-track`, named for the milestone id or the slug.
3. Runs each suite once and confirms it is green. A build that starts on a red
   suite cannot tell you which failure it caused.
4. Writes the repositories and the branch into `notes.md`.

Two builds at once inside one repository need a worktree each. `lanes.md` has
the block that makes one, and the two things a fresh worktree does not have.

Between phase 5 and phase 6, this file pushes every branch it opened. Each
branch stays checked out in its repository, because the walk runs against it.

**Nothing merges here.** The walk has not happened, so nothing on the branch is
known to work. See "One branch per milestone, in each code repository" above.

### Targeted tests per agent, the full suite once per track

An implementer runs the tests for the files it touched, which takes seconds.
The full suite is the orchestrator's. Run it once when a set of tasks lands,
and again before the walk.

Measured on one fix run: seven agents ran the full suite over twenty times at
about 68 seconds each, nearly all of it re-proving untouched code. Three of
those runs raced each other against one test database and proved nothing at
all. Something distant that breaks surfaces at the track boundary instead, and
costs a bisect across two or three commits.

---

## Phase 6 — Walk it

Phase 6 has three parts, run in order: 6a updates the scenario store, 6b
walks for regressions, and 6c walks for acceptance. Set the marker to
`Phase: 6a update the scenario store`, then `6b regression`, then
`6c acceptance`.

The scenario store is `$REC/tests/scenarios/scenarios.md`. Each entry has an
id, a `kind` of `flow` or `compare`, what the walker does, what it `sees`,
and the fields `initiated-by`, `updated-by` and `retired-by`. Where a
milestone was given, those fields name the milestone. With none, they name
the session slug. `/fde:smoke-test` owns the method for walking one scenario
with a person, and it wins wherever this phase and it disagree.

### 6a. Update the scenario store

This part changes the store before anything is walked.

1. Retire any entry that describes behaviour this session removes. Set its
   `retired-by`.
2. Rewrite in place any entry whose behaviour this session changes. Append
   the session to its `updated-by`. Never edit the milestone file that
   started the entry.
3. Add this session's own new entries, marked `initiated-by`. A session
   initiates 10 to 20 entries in total, never more.
4. Regenerate `by-milestone.md` beside the store. Where no milestone was
   given, the entries group under the session slug.
5. Commit and push `<docs>`.

If the store does not exist yet, 6a creates it with this session's entries.
That store holds nothing older to regress against, so 6b is skipped and 6c
covers all of it.

The marker stays on 6a until the push lands.

### 6b. Regression

6b runs only when the store existed before 6a began. It walks the entries
the session did not initiate, so it proves the build broke nothing.

Where the engagement has an automated screen diff, run it first over every
live `compare` entry. An entry that comes back `same` is closed. Then walk
the `flow` entries, and any `compare` entry the diff flagged, but only those
whose route or screen this session's diff touches. A backend-only session
walks the flows for the screens its changed modules serve. Walking the whole
store belongs to the combined run before a delivery, never to this session.

**Bring the stack up from the umbrella.** Use the engagement's own command,
`just up`. A worktree has no proxy of its own, so walk a worktree with the
stack command that `lanes.md` names, on its own project name and port. Never
point a walk at the primary checkout when the branch under test lives in a
worktree.

Check that the migrations ran before any walker starts. A process at head
against a database that is not fails silently, until a request touches the
missing column. The branch you are about to walk carries new migrations, so
it is exactly the moment this bites.

Before the first walker, dispatch one preflight subagent, of the kind that
checks a claim and reports. It returns pass or fail on four things: the
seed password is set in the environment, the stack answers on its health
route, a route to the screen exists, and the walker's account seeds and
signs in. Seed every local account with the password the umbrella
`CLAUDE.md` names, never a generated or invented one, and never print it.
Fix a failed check before any walker starts. A check that only the user can
fix goes to them as one line naming the exact command to run.

How a walker reaches the screen is the orchestrator's call: browser tools, a
scripted browser, or something else the session has. The rules below hold for
any of them.

**Brief the walkers.** A walker is a subagent of the kind that searches and
verifies. The user's global instructions choose its model. Walkers walk the
`flow` entries and the flagged `compare` entries, taken from the central
store and not from a session-only list.

1. A walker goes through the screen, not the API, the local database or a
   curl call. An API step is allowed only where the screen truly cannot reach
   the check. Mark it "API step" in the walk record with the reason. A walk
   made mostly of API steps is blocked, not passed.
2. A walker probes the running system before naming a cause.
3. Walkers run one at a time, because they share one browser profile and one
   cookie jar. Each signs in once and never switches user.
4. A walker reports findings briefly, and the orchestrator writes them into
   the findings file.
5. A walker never clicks a print, export, save or download control to prove
   a file. Where an entry's own step is the click, the walker clicks once and
   checks the downloads folder for a new file within 15 seconds. A file
   appearing is the pass. If a dialog appears instead, it presses Escape
   once, records the entry as blocked with the dialog's text, and moves on.
   It never waits for the user.
6. A scenario whose proof is a produced file is proven through the API: call
   the endpoint with the signed-in session's cookie, and check the status,
   the `Content-Type` and a non-zero `Content-Length`. The entry names it in
   `sees` as `file: <type> from <endpoint>`, so the walker knows not to click.

**Do not fix while walking.** A fix mid-walk changes the thing being
walked, and the second half of a walk is where the interesting findings are.
Record the finding with its proposed fix, and carry on.

A stale entry, a walker error, or a finding that is the browser tab rather
than the product is not a discrepancy. The orchestrator corrects the store
entry, records it, and does not re-walk it in this session.

**Unless the finding blocks the rest of the walk.** A finding that stops the
remaining scenarios being reached, or makes their results meaningless, goes
to the orchestrator the moment a walker sees it. Without `--afk`, the orchestrator puts it
to the user as a question and fixes it only on a yes. Under `--afk`, the
orchestrator decides under the Away mode rule. A fix goes to one fix
subagent, one finding, on the session's own branch, never a second branch.
The walk record then says which scenarios ran after the fix, because from
there the walk is against different code. Expect this to be rare.

**Fix only what this session broke.** For each regression discrepancy, a
subagent checks whether the code behind the failing behaviour is in the
session's diff, using `git diff <base>..HEAD` against the `merge_into` branch
the session branch was cut from. If it is, a fix subagent fixes it on the
session branch and a walker re-walks that scenario once. If it is not, the
discrepancy is pre-existing. It goes under **For the user** as one line naming
the scenario and the fault, and a bug hunt fixes it, never this session. A
pre-existing failure never blocks 6c or the merge.

**A fix breeds its own defects, and only a walk finds them.** It has
happened twice in one milestone.

Three findings said one panel asks for too much. The redesign answered all
three, and the person walked the result and raised a new finding: the panel
now fills a screen for one field. The same complaint, one level down.

Another finding said opening a field navigates away from the form. The fix
made rows open in place, and that created a finding of its own: a write
swaps the panel and never the row above it, so one edit leaves the whole page
stale. Before the change the defect could not exist.

A test caught neither. The suite was green both times. So a structural fix
is exactly what the re-walk exists for, and "the fixes were small" is not a
reason to skip it.

**What 6b produces.** Every regression entry is closed by the diff, walked,
or recorded as blocked. Every discrepancy this session caused is fixed and
re-walked once. Every pre-existing one is listed under **For the user**. The
findings file and the walk record carry the regression results.

**The shape of 6b is one walk, one fix round, one re-walk.** This is a
design, not a quota. The first walk collects every finding before anything
is fixed, so the fix round can answer all of them at once. The re-walk covers
only the scenarios the fixes touched. It exists to prove the fixes landed and
bred nothing. When it comes back clean, 6b is done.

The re-walk can still find something: a finding the first walk missed, or a
defect a fix bred. That is fixed too, and the scenarios that fix touched are
walked again. The work ends when the scenarios pass, not when a count runs
out. What the method forbids is repeating a round without learning from it.
Three rules hold the loop closed.

1. A fix never goes in mid-walk, so no walk is repeated because its code
   changed under it.
2. A fix round takes everything the previous walk found, together. Never one
   finding, one fix, one walk, and round again.
3. A finding that survives two fix attempts is a diagnosis problem, not a
   walking problem. Stop walking it, write what was tried under **▶ Resume
   here**, and dispatch one diagnosis subagent of the kind that needs
   judgement before any further fix. If that does not close it, leave it for
   the user, away or not. Never send a third walker at the same finding on
   the same fix.

A pass is one walker over every flow it covers, or two where the list is
long. A walker per scenario multiplies walks by the size of the store.

### 6c. Acceptance

6c walks this session's own entries, the ones 6a added or updated. It runs
the same way as 6b: the screen diff first where there is one, then walkers on
the `flow` entries and the flagged `compare` entries. The rules in 6b on
walkers, blocked findings and re-walks apply here too. Without a milestone,
the entries are the ones that name the session slug.

**What 6c produces.** Every acceptance entry is walked or recorded as
blocked, and the findings are written down.

If one of this session's own entries still fails after two fix attempts and
the diagnosis 6b describes, the session does not merge. It commits what is
done, records the failing entry and the fixes attempted under **▶ Resume
here**, and stops at a clean point, away or not. The user decides the next
step. Until that point the entry is fixed and walked again, because a
session merges working.

### The findings files 6b and 6c write

Two files in the session folder, and neither is the same as the other.

`bugs-and-improvements.md`, `kind: feedback`, is what was found. One row per
finding in a table, then a section each. Four kinds: `bug` is wrong,
`improvement` works and should be better, `constraint` is something that must
survive a change already planned, `decision` is a scope call settled mid-walk.
Status is `open`, `fixed`, `wontfix` or `decided`.

`smoke-test-walk.md`, `kind: walk-record`, is the route taken. The scenario
list with its result, the setup used, any shell command a scenario needed,
and the chain of state the walk built. It lets somebody cover the same ground
next month without rediscovering the order.

### Phase 5 writes into the same file

`subagent-driven-development`'s final whole-branch review finds things a
browser cannot show. They belong in the same `bugs-and-improvements.md`,
because a fix session should read one list.

So two phases write to it and the numbering is shared. Read the file
immediately before every write and take the next free number. Never renumber
a published entry; other documents cite them.

---

## Phase 7 — Fix what the walk found

On the session's own branch, in whichever code repository holds the fault.
Not a new branch, and not off `merge_into`. The findings file stays where it
is, in `my-sessions`.

### Triage before fixing

Not every finding is a fix, and working the table top to bottom is wrong. A
walk of two dozen findings will typically carry three or four that should
never reach a fix branch.

Route every row first:

| The row | Goes to |
|---|---|
| `bug`, reproduced | fix here |
| `bug`, not reproduced | stays `open`. Reproduce it first or leave it |
| `bug`, already `fixed` during the walk | nothing to fix. It is on the branch. Re-check it in the second pass |
| `improvement`, small and local | fix here |
| `improvement`, a redesign of a workflow | a milestone, through phase 2 when one exists. With none, `notes.md` under **Scope, in plain words**, and a line under **For the user** |
| `constraint` | not a fix. It becomes a rule in the milestone or the spec |
| `decision` | phase 2 when a milestone exists. With none, it stays in `notes.md` and is marked `decided` |
| a scope hole between the spec and the milestone | phase 2 first, then fix. With no milestone, between the spec and the user's words: fix it, and note it |

Then do two passes over what is left.

**Group by cause.** Findings that share one fault are one piece of work, and
fixing them separately produces three half-answers. Three improvements can
be the same complaint on three screens.

**Order by dependency.** One finding often cannot be fixed before another,
because the second is what makes the first safe. Read the entries for that
before you start, not after.

Write the routed list into `notes.md` before starting. That is the plan for
this phase.

### Then fix

The orchestrator decides what is fixed, and implementer subagents fix it.
For each finding: fix it, add the test that would have caught it, mark the
row `fixed <DD-MM-YY> (<commit>)` with what changed named down to the file,
and re-walk the scenario it came from.

Where several agents run at once they are told to leave the findings file
alone, so they cannot collide in it. The other half of that rule is yours:
write every row at the track boundary, in the same pass as the full suite.
Telling agents not to touch it and stopping there is how a findings file
spends a whole run saying nothing has been done.

A finding the user decides not to act on is `wontfix <DD-MM-YY>` with the
reason in its section. A row routed to phase 2 or to a milestone stays `open`
and says where it went. Every finding routed to "fix here" also becomes a
task, as `backlog.md` says.

The phase ends when every row is `fixed`, `wontfix`, `decided`, or `open`
with its destination named, and the suite is green.

### Ask before closing

Do not go straight to phase 8. Ask, in one line: the fixes are in and the
suite is green, do you want to walk it again before I close? Under `--afk`
the orchestrator answers under the Away mode rule and writes the answer into
`notes.md`.

Recommend a re-walk when the fixes touched shared mechanism, and say so. A
suite cannot tell you a semantic change is wrong. A person walking the screen
can. Where the fixes were local and independent, say that too, and let the
per-finding re-walks in this phase stand on their own.

**If the answer is yes, go back to phase 6.** It is a second pass, not a new
phase, and the marker reads `Phase: 6 walk (pass 2)`. Three tiers of
scenario, in this order:

1. Every scenario that produced a finding now marked `fixed`. This is the
   proof the fix landed.
2. Every scenario downstream of a mechanism the fixes changed, even where it
   passed the first time.
3. The rest, if there is appetite. Optional.

Findings from a second pass take new numbers in the same file. Append the
second pass to `smoke-test-walk.md` rather than overwriting the first.

**A bug found in pass 2 on a scenario that passed in pass 1 is a regression
from the fixes.** It outranks everything still open, and it goes back through
triage before anything else is touched.

### A walk with no session behind it

`/fde:smoke-test` runs on its own, before a delivery or against any idea, and
writes to the misc folder rather than a session folder. It finds and records;
it never fixes.

Fixing is this phase, and a standalone walk enters it directly: run
`/fde:aie-session <detail>` against the folder holding the findings file.
Phase 0 sees the file and starts here rather than at phase 1, because the
scope work those phases do has already been done by the walk.

---

## Phase 8 — Close

The session ends once this phase is done. It never starts another piece of
work, and the next one gets a fresh session. Every orchestrator turn re-sends
the whole context.

Reached only once phase 7 has ended, including any second pass it chose.

1. **Take the target branch in, run the suite once, then merge, and the
   backend goes first.** The target is the `merge_into` value, and `main`
   when it is empty. Read `<docs>/setup/branching.md` first when it exists,
   because it holds the branch rules for this engagement. Merge the target
   into the session branch in each code repository. This is the merge gate,
   so the suite runs here once, with 2 workers, in a subagent of the kind
   that runs a command and reports, started by the orchestrator, on each
   branch head. It must pass. If it fails, a fix agent runs only the failing
   files until they pass, and the suite runs once more. That second run is
   the last. A third means stop and write it under **▶ Resume here**. Then
   merge the session branch into the target in each code repository, and
   push. Open the `<fe>` pull request only after the `<be>` one it needs has
   merged, as rule 7 of
   `${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/repo-layout.md` says.
2. **Merge up.** When `integration` is set, merge the target into the
   `integration` branch with `--no-ff` straight after, and push. When it is
   empty, there is no such step. A branch another checkout holds is merged in
   a detached temporary worktree, and the files are verified at origin after.
   Never merge into `release`. A push there deploys, and only a delivery
   moves it. This is the only merge in the session, and it happens after the
   walk and the fixes. During the build only the touched test files run, and
   the whole suite runs once, here.
3. **Do not tag.** The delivery tag goes on `release` when the delivery is
   released, which is its own step. Where this session completes a delivery,
   say so in `notes.md` and in the closing message, so the release is not
   missed.
4. **Graduate the record.** See Graduation below.
5. **Run every adopted checklist.** `<docs>/setup/conventions.md` says which
   conventions this engagement adopted. Run each adopted checklist against
   what merged, and record the answers in `notes.md`. A failing checklist
   blocks `built`. Fix it, or get the user's written waiver into
   `setup/guardrails.md` first.
6. **Update the milestone**, when one was given: set `status:` to
   `built <DD-MM-YY>`, and regenerate `$REC/project/milestones/index.md`.
   The status is the first word of the field and the date follows it, so the
   whole field reads `built 07-09-26`. With none, skip this step.
7. **Close the tasks.** Every task for this session in `$REC/backlog/tasks/`
   reads `Done`, or stays `To Do` with one sentence saying why. See
   `backlog.md`.
8. **Promote what the session raised.** Client questions to
   `$REC/project/open-questions.md` with ids, our own fieldwork to
   `$REC/project/next-steps.md`.
9. **Run the record lint** from the umbrella, and fix what it finds:

   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/lint_record.py" "$DOCS" "$REC"
   ```

   The script takes the docs root, then the record root. Links and
   guardrails are checked at the docs root; the milestone, question and wiki
   checks read the record root. See "Finding the
   engagement" above where `CLAUDE_PLUGIN_ROOT` is unset.

   It prints one line per finding with a path, and exits non-zero on any of
   them. Fix every one before going on. Most will be this session's own work.
   It finds a milestone missing a required part, a `waits-on` that no longer
   resolves, an open question with no owner, a guardrail with no source. A
   finding that belongs to the FDC's half of the record goes to them by name,
   and `notes.md` says so. The session does not close on a red lint.
10. **Set the front fields and check them.** Set `Status: done`, write `Summary:` in one line, and set `Owes:` to what is still owed, or `none`. Use `blocked` only inside `Owes`. Then run `python3 ~/.claude/skills/sessions/scripts/sessions.py check <folder>`. If it exits non-zero, fix the notes and run it again. When it passes, run `python3 ~/.claude/skills/sessions/scripts/sessions.py index --write`.
11. **Set `Phase: 8 done`**, write the last **Progress log** line, and clear
    **▶ Resume here** to say the session is finished. The closing message
    names every **For the user** item. The walk has run as part of this
    session, so nothing is owed to a later combined run.
12. **Push.** Pull `<docs>` first; another session may have moved its
    `main` while this one ran. `my-sessions` has no git, so it needs no
    push.

## notes.md fields

`sessions.py new` writes the shared front block and sections. The AIE adds
these front fields, each on its own line:

- Milestone: `$REC/project/milestones/<file>.md`, or "none".
- Method: `superpowers`, or the pack the `--<method>` flag named.
- Phase: `0 scaffold` to `8 close`, or `8 done`, with `0b open items` between 0 and 1 when there is a milestone.
- Status: active | paused | done. Use `blocked` only inside Owes.
- Repositories: the backend, the frontend, both, or "none".
- Branch: `<milestone id>`, or the slug when there is no milestone, and whether it is committed or uncommitted.
- Flags: the flags the session was started with, such as `afk`.

It adds these sections after **Resume here**: **Scope, in plain words**
(phase 1's read-back, rewritten in phase 2 whenever the scope moves) and
**Milestone changes** (phase 2's log, one dated line per change, append
only). It also adds **For the user**, the list of things the user must see or decide, such as a pre-existing failure phase 6 found. It also adds **Changes** (files touched, commits, migrations) and
**Engagement trail** (wiki nodes read or written, open questions raised by
id, risks touched, guardrails that bound the work).

Four more files sit beside `notes.md`. The pack writes `spec.md` and
`plan.md`. Phase 6 writes two: `bugs-and-improvements.md`, what was found,
and `smoke-test-walk.md`, the route taken. Screenshots land here too.

## Keeping it resumable

Five things let anyone pick the work up cold. Keep them current every time
you stop, and bump **Last updated**.

- **Phase** — which of the nine you are in.
- **Repositories** — which code repositories are in play.
- **▶ Resume here** — the single next action.
- **Progress log** — a dated line for what you did.
- **Branch** and **Status** — where things stand.

## Graduation

The session is the working record and never the authority.

- A hard-to-reverse decision → an ADR in `$REC/project/decisions/`.
- A forward-looking constraint → `setup/guardrails.md`.
- A build guardrail this session overrode → a dated note under it in
  `setup/guardrails.md`, with the reason.
- A fact derived from client material → `$REC/wiki/`.
- A change to a promised date or page count → `$REC/project/deliveries.md`.
- A question the client must answer → `$REC/project/open-questions.md`, with an id.
- A change to what a milestone owns → the milestone file itself, in phase 2.
- The route a walk took, so the same ground can be covered again →
  `<session>/smoke-test-walk.md`.

## Notes

- Session folders sit at the root of `my-sessions`, a sibling of
  `<docs>`. It is a plain folder with no git, kept on this machine only. `<docs>` never holds or links to a session record.
- A screenshot may be kept in a session folder. A client PDF, spreadsheet
  or drawing goes to `raw/` through `/fde:file` instead, so it gets a ledger
  row and an authority tier. A copy in a session folder has neither.
- Do not put secrets in `notes.md`. Redact before pasting.
- This scaffolds **up front**. For chats nobody scaffolded, run
  `/fde:session-sync` afterwards.
- Adding a way of building means adding a file to `methods/`. Read
  `methods/README.md` for the contract it has to meet. Nothing in this file
  changes.
