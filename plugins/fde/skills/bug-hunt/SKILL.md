---
name: bug-hunt
description: "Take a pile of bugs to a merged branch from one session, the bug-fixing counterpart of aie-session and fdc-session. The orchestrator takes in bugs, holds a tracker, decides each one, sends exploring subagents to diagnose and verify, and dispatches a fix subagent the turn each bug is diagnosed, one per repository's hunt worktree and any other in its own worktree lane, to fix a bug end to end across whichever repositories it touches. Use when bugs cross the backend, the worker and the frontend, when the user says \"start a bug hunt\", \"hardening session\", \"fix this pile of bugs\", \"work through these bugs\", or invokes /fde:bug-hunt <name>. A milestone is optional. One ready milestone is /fde:aie-session instead."
---

# bug-hunt

Take a pile of bugs to a merged branch, from one session, without losing
anything the user said.

It is a session in the same sense as `/fde:aie-session` and
`/fde:fdc-session`. `/fde:fdc-session` keeps the record true,
`/fde:aie-session` builds a milestone, and this one fixes a pile of bugs. The
orchestrator takes in what the user says and takes every decision. Subagents
do the work and report back briefly.

Claude is always started from the umbrella. `<docs>` holds the engagement
record, `<be>` and `<fe>` hold the code, and `my-sessions` holds this
session's folder.

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
`.engagement` and use that.

Repositories, branches and worktree names come from `.engagement` and never
from fixed names. Where `apps` is set, the app is part of the hunt's name.
The base branch is the one the user names, then `merge_into`, then `main`.

## Invocation

```
/fde:bug-hunt <name>
```

The name gives the branch and the folder. A hunt named `d1` branches
`hardening/d1`. A milestone is optional: the hunt starts with one or without
one, and a milestone only adds context to the tracker.

## When to use it

Use it when the bugs cross the backend, the worker and the frontend, and
there are more than a handful. A hunt earns its setup at about ten bugs.

Do not use it for one bug. Fix that where you are.

A hunt runs after the build. `/fde:smoke-test` finds bugs and records them,
and this skill fixes a pile of them at speed.

## The shape

One session. The orchestrator, at the umbrella, holding a tracker. It takes
bugs from the user, decides what each one needs, dispatches a subagent to fix
it, records the outcome in one line, and stays free to take the next bug.

Each bug is fixed end to end by one subagent, and fixing is parallel. The
hunt's worktree of each repository takes one fix at a time. Any other fix in
flight opens its own worktree lane (see Parallel lanes). One subagent
diagnoses, fixes, runs the checks its change touched, commits, pushes and
reports. A composite bug is one task, not two coordinated halves.

Subagent models follow the global rule, and every dispatch passes the
model explicitly. Pick by the kind of job.

| Work | Kind of job |
|---|---|
| Diagnosis, searching the code, browser or screenshot verification | search and mapping |
| Check runs, which run the command and report what it printed | mechanical, checked by its output |
| An ordinary fix, mechanical or well-specified | implementation |
| A fix whose cause the analysis left unknown, a fix an implementation subagent failed, design-heavy UI, cross-repository work, or a fix the user has rejected once | judgement |
| The end-to-end checker | search and mapping, or judgement where the call is hard |

Say which kind a fix ran as in the tracker line. Tell every subagent to
follow the same rule for its own subagents.

The orchestrator never drives a browser. Anything that needs one goes to a
subagent, and the subagent reports what it saw.

Decide, don't ask. The user only reports bugs. Every design choice is a
stated assumption, recorded in the tracker or `notes.md` under Decisions, and
told to the user in one line. Prefer the option that keeps a recorded rule
and adds the least scope, unless the user has rejected it already. The only
questions the hunt asks are about merges, deploys and anything
outward-facing.

There is no backend session, no frontend session, no checker session and no
cross-session messages. Beside the tracker sits one short `notes.md`, which
says where the hunt is so a compacted or fresh session can pick it up.

A subagent's argument never enters the orchestrator's context. A ten-line
report does. That is the failure this shape exists to prevent: the hunt
losing the context the user gives it.

## Phase 0: scaffold

1. **The folder.** Run `python3 "${CLAUDE_PLUGIN_ROOT}/sessions/scripts/sessions.py" new --type hardening --slug <app>-<name>`, from the umbrella, with no app in the slug where `apps` is empty. It chooses the folder path and writes `notes.md` from the shared template. Follow `${CLAUDE_PLUGIN_ROOT}/sessions/CONTRACT.md` for the notes contract and the close step.

   Never clobber. First look in the `hardening` sessions folder for a folder ending `-<name>` whose `notes.md` has `Phase:` short of `2 done`. A fresh session on a later day computes a different date, so match on the name. If one exists, say which, skip the rest of this phase, and resume from it.

2. **The tracker.** `tracker.md` holds every bug, and it is the only state about bugs this hunt keeps. Write it before the first bug arrives. Add the hunt's `Phase:` line to `notes.md` as `0 scaffold`.

3. **The branch.** Cut `hardening/<name>` off the base branch in each code repository, from a clean tree, and push it. Never cut off whatever happened to be checked out. Then make the hunt's own worktrees with `git worktree add`, named by the `worktree` pattern (such as `<be>-<name>` and `<fe>-<name>`) at the umbrella root, on `hardening/<name>`. Note the commit each branch was cut from; every later "ours or pre-existing" argument rests on it.

4. **Bring the stack up, and prove the sign-in before handing it over.** The project's `CLAUDE.md` says how to start the stack and which environment variable holds the local password. Follow it exactly, point `localhost` at the hunt's worktrees with an untracked, reversible override (never by switching the primary checkouts' branch), record the revert steps in `revert.md` in the hunt folder, and prove the sign-in from the shell before the user is sent anywhere. A subagent opens the sign-in page for the user. The user signs in. The agent never types a credential into a form. Never send a user to a URL you have not opened.

5. **The baseline, measured, in the background.** Once the user has sign-in access, run each repository's full check set as a background job and write the numbers into the tracker with the command beside each one. Not a subset, and nothing read through `tail` or `head`. A red check is cleared by the first task rather than carried as a number.

6. **Say the tracker's path out loud**, so the user can open it. Set `Phase: 1 loop` in `notes.md`.

## The loop

1. The user pastes a bug, in their own words.
2. Write it into the tracker immediately, verbatim, before anything else. This is the step that stops context being lost.
3. Analyse it. Where the bug names its own cause, that is the analysis. For anything else, dispatch a read-only diagnosis subagent (`briefs.md`), which names the cause down to the repository, the file and the line. Where the record never specified the behaviour, the diagnosis says so, and the bug is still fixed here. Write the conclusion into the tracker, never the transcript.
4. Dispatch its fix in the same turn. If the bug's repository's hunt worktree is free, dispatch there. If it is busy, open a lane and dispatch there. Name in the brief any files another live agent owns right now, and tell the agent to put independent commands in one call.
5. It reports back in ten lines. Record the commit and the status in the tracker. Merge the fix into `hardening/<name>` in the hunt's worktree at once. A lane merges in by the rule under Parallel lanes. A backend fix that changes worker code also needs the worker restarted.
6. Tell the user in two lines, and one of them says how to see it: the path to open, what to do there, and what they should now see that they did not before.
7. Verify it, then the user looks. Where a fix shows on screen, a subagent checks it first in the browser or by screenshot. A bug is not done because the suite is green. It is `done` when the user has seen it fixed, or has said they will look later. Until then it is `landed`.

The orchestrator stays free throughout. A bug can arrive while a fix is running: write it in, analyse it, queue it.

A dead or stalled fix agent (a watchdog timeout, a sign-in expiry, an error) is re-dispatched at once with the same brief, noting what it left uncommitted. Feedback on a fix that is still running never goes to that agent. It becomes a new id, such as `07b`. When the user is away, the orchestrator keeps working the queue and pushing to `hardening/<name>` and its lanes. It never merges into the base branch or any other branch without the user's word that day.

When the user stops pasting, ask: "Is there anything you want to add that I might have missed?" If the answer raises a question, ask it, then ask this again. Stop once they say they have nothing to add. Everything they add goes into the tracker verbatim.

## The tracker

One file. Every bug is one section, and it grows in place.

```markdown
# <name> bug hunt: tracker

Opened <DD-MM-YY>. Branch `hardening/<name>`, cut from `<sha>` in
`<be>` and `<sha>` in `<fe>`.

Baseline: backend <n> passed, <n> skipped, <other checks> green.
Frontend <n> across <n> files, <other checks> green.

## Open

| id | the bug, in their words | status |
|---|---|---|
| 07 | Accept all button doesn't work intermittently | analysing |

## Done

| id | the bug | commit | note |
|---|---|---|---|
| 01 | no nav back from the access page | `fb13d79` | crumb, not a back link |

---

## 07: accept all doesn't work intermittently

**Theirs.** "<verbatim>"

**Analysis.** <the conclusion, to file and line>

**Landed.** `58eee77`. Frontend 522 across 74 files.
```

The statuses, in order: `queued`, `analysing`, `fixing`, `landed`, `done`. `landed` means committed, pushed and green. `done` means the user has seen it fixed. A bug moves to the Done table only at `done`. The two tables are a status, not a log, so rewrite them on every landing.

## Keeping it resumable

Sessions auto-compact, and the user may close one and start `/fde:bug-hunt <name>` again at any point. The folder must hold what a compacted or fresh orchestrator needs at every moment.

When the user gives any input (an answer, a decision, a correction), write it into `notes.md` first, then act on it. After every decision, answer and subagent report, write one line: a line about a bug goes in that bug's tracker section, and a line about the hunt goes in `notes.md`. At the same moment, rewrite the Resume here section in `notes.md`: what you are doing now, and the next step, naming the tracker row in progress by id.

On resuming, grep `notes.md` for `Phase:`, Resume here, Carry forward and Decisions, and read each as a line range. Then read the tracker's two tables and the one bug section Resume here names, and nothing more. Where the folder and the summary disagree, trust the folder.

Beyond the shared template's sections, `notes.md` keeps these headings: Resume here, Carry forward (what no file holds: a constraint stated only in conversation, a rejected approach and why, a subagent still running), Decisions (each choice about the hunt as a whole, with its reason), and Progress log.

## The fix subagent

It owns the bug completely. `briefs.md` holds the template. A fix past turn 60 is split: the first agent commits at a clean point and reports what is left, and a fresh subagent carries on.

It fixes every repository the bug spans. No handover, no released half.

It runs the checks its change touched, not the suite: the test files it wrote or changed, plus the test file beside any module it changed, named as files and never a directory, plus lint, typecheck, build and the schema and client checks where the backend's shape changed. Every command stays under five minutes and runs in the foreground, because the subagent watchdog kills a call at about 600 seconds. It reports the numbers with the command beside each.

The suite runs once per hunt, at the merge gate, started by the orchestrator with 2 workers, and never by a fix agent. A change to shared mechanism (the engine, auth, a migration on a shared table) also runs that mechanism's own test directory once, when it lands. A failed merge run goes to a fix agent that runs only the failing files, then the suite runs once more. A third run means stop and write it under Resume here.

Where a fix needs a record change, it stops short of making it and lists the change. The orchestrator collects these as record notes for the FDC at the merge gate.

It commits on the hunt branch, one commit per bug with the id in the subject, stages the files it changed by name, and pushes. It restarts the worker after any Python change and says so, with the container's start time against the commit time. A prompt file is live on the next call; Python is dead in the worker until the restart.

Its report is ten lines: commit hash, check numbers, what it decided that the brief did not, and what it could not do. Anything longer goes in a file under the hunt folder's `notes/`, which the orchestrator reads only when something is wrong.

## Seeing a fix

A fix is observable on `localhost` the moment it is live. It does not need a deploy or a merge to the base. A fix still in a lane is not visible until it merges in.

The frontend is live on save, because the source is bind-mounted and hot-reloads. The browser can show work in progress. The backend is live only after the worker restarts, so a backend fix can be committed, green and still invisible. Holding only one of those rules makes you read the other container wrong.

The fix subagent reports how to see its fix: the path, the action, and the before and after. If it changed Python, the report also says the worker has restarted.

When the user cannot see a fix they were told is in, check the container before the code. The first question is always what the running thing is running.

## The end-to-end check

A subagent, fired when a fix touches model behaviour. `checker.md` is its brief. A prompt rule is asserted and never proved: the suite can assert a sentence is in a prompt file and can never assert the model obeys it. Take a baseline pass before a prompt change lands. Without a before, a prompt change has no after.

## Branching

The base branch is whichever the user names, then `merge_into`, then `main`. Each repository gets one long-lived `hardening/<name>`. Every fix is its own commit with the bug id in the subject. Read `<docs>/setup/branching.md` when it exists. `<docs>` stays on its own branch and never gets a hunt branch.

Take the base in whenever it moves, by reverse merge. Merging a fix into `hardening/<name>` needs no consent, because that branch is the hunt's own. Merging `hardening/<name>` into the base needs the user's word that day, with `--no-ff`. Where `integration` is set, the base then merges up into it. `release` is never touched by a hunt.

### Parallel lanes

The hunt's own worktree of each repository takes the first fix in flight on it. Any other concurrent fix on that repository opens its own worktree, named by the `worktree` pattern with the bug id, on branch `hardening/<name>-<id>` cut from `origin/hardening/<name>`, made with `git worktree add`. Never the `EnterWorktree` tool, which nests the tree inside the repository. `${CLAUDE_PLUGIN_ROOT}/skills/aie-session/lanes.md` has the mechanics. A lane uses its own test database, and the brief names any files another live agent is touching.

A lane pushes its own branch. The orchestrator merges lanes into `hardening/<name>` one at a time as each lands, runs the tests the merge touched after each merge, and never merges two lanes in one step. Stage the files you changed, by name. Never `git add -A` on a shared branch, and never `git stash`, `git checkout .` or `git reset --hard`. Never switch a checked-out branch under the running stack.

### When to merge

Only when the user says so in their own words, on the day of the merge. A merge may be a deploy, and a standing yes from earlier does not cover today's. Ask again that day and name the deployment. A condition is not consent unless the condition is external: "merge once the checker is clear" works, because the checker answers join or stop.

## The merge gate

The session ends after this merge. It never takes on a second hunt or a milestone. Set `Phase: 2 merge gate` in `notes.md`, work through the list, and put the answers in the tracker.

1. Every bug in the Open table has landed or been explicitly dropped.
2. Both check sets pass on the merged head, run once after the last commit, with 2 workers. This is the only suite run in the hunt. Where the base has not moved, the branch head is the merged head, and there is no merge commit to test. Say so.
3. The worker has been restarted after the last commit that changed Python, and its start time post-dates that commit.
4. The branch is verified at origin, not only in the working tree.
5. The checker has answered join or stop, if one was used.
6. Every named limit is written down with its rate and its worst case.
7. The user has walked the app, or has said they will after the deploy.
8. Every record note the hunt owes is listed for the FDC by name.
9. Say out loud the behaviour changes anyone who saw the old build will notice.
10. The user has said go that day, with the deployment named.

Then merge the backend into the base, push, and tell the user the commit. Then the frontend. Then revert `localhost` to the primary checkouts using `revert.md`, restart the containers, repeat the health checks, and remove the hunt's worktrees. Teardown also removes each lane's volumes and test image with `docker compose -p <project> down -v --rmi local`. Set `Phase: 2 done`, write the last Progress log line, and clear Resume here to say the hunt is finished.

At the close step, set `Status: done`, write `Summary:` in one line, and set `Owes:` to what is still owed, or `none`. Then run `python3 "${CLAUDE_PLUGIN_ROOT}/sessions/scripts/sessions.py" check <folder>`. If it exits non-zero, fix the notes and run it again. When it passes, run `python3 "${CLAUDE_PLUGIN_ROOT}/sessions/scripts/sessions.py" index --write`.

Check what your green actually ran. The test service may run the test runner alone, while CI also runs the linter, the framework's own check, the migration check and the schema checks. Name the command beside every green.

## The standing answers

Questions already settled, so the hunt never stops to ask them again.

1. A pre-existing red linter is cleared, not recorded. Record the count and the breakdown first, so the clearing is its own commit, then clear it.
2. A number from truncated output does not count. Never report a check's result from anything piped through `tail`, `head` or a `grep` that could drop a package. A top-N, a `LIMIT` or a sample is a `tail` with better manners.
3. A number whose parts do not sum cannot be checked. Sum per-package totals with a script and quote the script.
4. A check that fails once and then passes is a bug, not a flake. Chase it to its cause.
5. Split a sweep by blast radius: the free changes, the ones that change behaviour, and the ones that delete code.
6. Fix the prose that introduces a command, not just the command.
7. A rate is necessary and not sufficient. The rate goes first, because it stops you constructing cases that flatter your design. Then construct the cases the corpus cannot contain.
8. A measurement with nothing to say is not reassurance. A rate over a corpus that never contains the case is not evidence about the case.
9. A hunt fixes scope as bugs. A report that turns out to be unspecified or new scope is fixed in the hunt, never routed to a new milestone. Write into the tracker whether the record specified it, and where a fix reverses a milestone's exit criterion, say so as a behaviour change at the merge gate.
10. No business question goes to the client. Decide it in the hunt, in the FDC hat, from the specimen, the raw documents, the wiki and the code, and send the decision to the FDC as a record note at the merge gate, labelled a working assumption where the evidence is thin.
11. Absence is not a value. A missing proposal, a silent turn or an empty field is not evidence that nothing is wrong. Ask what the check could not have seen.
12. Write stop conditions into briefs, not instructions with a caveat. "Extend X" gets built. "Measure whether X is safe, and stop if it is not" gets measured.
13. A rule should say what it is for, so it can be weighed rather than only obeyed or abandoned.

## The rules, short

1. Write the user's bug into the tracker verbatim before anything else.
2. The orchestrator decides, dispatches and records one line. It does not build, and it never drives a browser. Every dispatch names its model.
3. One subagent owns a bug end to end across every repository it touches, dispatched the turn it is diagnosed. Never two writers in one working tree.
4. A subagent's report is ten lines. Its reasoning goes in a file.
5. The tracker holds the bugs, and `notes.md` says where the hunt is. Keep Resume here on the row in progress.
6. A fix is not live until it is in `hardening/<name>` and the worker's start time post-dates the commit that changed Python.
7. Merge into the base only at the merge gate, on the user's word that day.
8. A prompt rule is asserted and never proved. The checker is the only thing that measures it.
9. A number from a part is not a number about the whole.
10. The stack is up and the sign-in proved before the first bug. The user signs in.
11. A bug is `done` when the user has seen it fixed, not when the suite is green.
12. Checks per fix are the touched test files plus lint, typecheck, build and the schema and client checks. The suite runs once, at the merge gate.
13. Where a fix needs a record change, it stops and lists the change for the FDC.

## The supporting files

`briefs.md` holds the templates: the diagnosis subagent, the fix subagent and the two-line report to the user. `checker.md` holds the end-to-end checker, for a hunt whose subject is model behaviour. `verification.md` holds the discipline that catches a wrong fix. Every fix subagent reads it, and the orchestrator reads it before believing any report.
