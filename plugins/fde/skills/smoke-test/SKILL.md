---
name: smoke-test
description: "Walk the running application by hand with a person, one scenario at a time, and write what it finds into a bugs-and-improvements file. The agent brings the stack up, hands over credentials, gives one scenario, waits, reads the reply, probes the running system to confirm what it suspects, and records every finding as it arrives. Use when the user says \"smoke test\", invokes /fde:smoke-test, or asks to walk a milestone before a delivery. Finds and records only. The one exception is a bug that blocks the rest of the walk, which it puts to the person as a question and, if they say so, hands to a subagent."
---

# Smoke test, with a human in the loop

The suite proves the code. This proves the product. A person clicks
through the screens and reads what the page says back, because a green
suite has never once said that a form is unreadable.

A milestone walked this way typically gives up more findings than the
suite did. The ones that matter are the things only a browser shows: a
control that renders for nobody, a status pill contradicting the value
printed beside it, our own working notes printed on a document the client
will file. That is what this skill exists to catch, and it is why the walk
happens before every delivery.

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

## Scope

Find and record. Nothing else.

Do not fix anything during a smoke test, however small and however
obvious. A fix mid-walk changes the thing being walked, and the person
loses their place. Write the finding down, propose the fix inside it,
and carry on. Fixing is separate work with its own session.

There is one exception, and it is a bug that blocks the rest of the
walk. That one goes to the person as a question, because carrying on
past it wastes the whole second half of the walk. The person decides,
never you, and a subagent does the fixing. See "When a finding blocks
the rest of the walk" in phase 4.

Do not run the test suites as part of this. They prove different
things. Run them before you start if you want a baseline, and quote the
numbers.

## The five phases

1. Bring the stack up and prove the login yourself.
2. Open the findings file.
3. Build the scenario list.
4. Walk it, one scenario at a time.
5. Close.

## Phase 1: bring it up, and prove it before handing over

Never send a person to a URL you have not opened. Half the setup
failures in a walk are yours, and finding them costs the person their
patience before the first scenario.

Bring the whole stack up from the umbrella, not one repository at a
time:

```bash
just up
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/
curl -s -o /dev/null -w "%{http_code}\n" http://localhost/api/schema/
```

`just up` runs `docker compose up -d` against the umbrella's own
`docker-compose.yml`, which starts the backend, the worker, the frontend
bundle and the proxy together. Everything is reached on port 80 through the proxy. `/api/*`
goes to the backend and everything else goes to the bundle. Both those
checks must return 200 before you go any further.

Check the migrations ran. A process at head against a database that is
not fails silently, until a request touches the missing column.

Django's own commands make and reset the first account, in the backend
container:

```bash
BEC="docker compose exec -T be"
$BEC python manage.py createsuperuser
$BEC python manage.py changepassword "$ADMIN_EMAIL"
```

`$BEC` is the container alias, kept apart from `$BE`, which is the backend
folder. The admin address is the engagement's own, not a fixed one. Read it
from the seed command in `<be>`, which takes it from the environment. Grep the
management commands for the field, or read `<be>/.env`. Ask the user if
neither says. `.engagement` holds no admin field.

Then prove the credentials from the shell before you hand them over.
Find the sign-in route in `<be>/openapi.json`, post to it, and read
the response. A 200 that sets a session cookie passes. A 400 or a 401
means the password is wrong, so fix it here rather than in front of the
person.

Then hand over the exact URL, the email and the password, in three
lines. Send them to the sign-in screen, not the bare host.

## Phase 2: open the findings file

Open it before the first scenario, not after the first finding. Say so
in one line and move on.

Findings always go in `my-sessions`, whichever repository the fault is
in. They never go in `<docs>`. Run `python3 ~/.claude/skills/sessions/scripts/sessions.py new --type smoke --slug <slug>`. It chooses the session folder path and the folder name, and writes `notes.md` from the shared template. Follow `~/.claude/skills/sessions/SKILL.md` for the notes contract and the close step.

The findings file is `bugs-and-improvements.md` inside the folder
`sessions.py` created.

### The shape of the file

Front matter with `kind: feedback`, a status, the milestone if there is
one, and the date opened. Then a table, one row per finding. Then one
section per finding, in the same order.

| # | Kind | Found in | What | Status |
|---|---|---|---|---|
| 1 | bug | setup | One line, specific enough to act on | open |

Four kinds.

`bug` means the thing is wrong. `improvement` means it works and should
be better. `constraint` means something must survive a change that is
already planned. `decision` means the person settled a scope question
during the walk.

Status is `open`, `fixed`, `wontfix` or `decided`, with the date it
changed.

### Numbering

Number in the order found. Never renumber a published entry; other
documents cite these numbers.

Another agent may be writing to the same file. Read it immediately
before every write and take the next free number. If a collision has
already happened, move yours and leave theirs, because theirs is more
likely to be cited elsewhere.

### What a section says

Four things, in this order. What happens, in the concrete. Why, named
down to the repository, the file and the line. What should happen
instead. Where it was found and who raised it.

Name the repository every time. The umbrella holds more than one, so a
bare path is ambiguous. Write `<be>/src/domains/<domain>/api/record.py:88`,
never `record.py:88`.

A finding with no proposed fix is half a finding. A finding that names
no cause is a report, so say plainly that it is not reproduced rather
than inventing a cause.

Quote the person. Their framing is usually sharper than the
restatement, and it is what makes the entry persuasive three weeks
later.

## Phase 3: build the scenario list

In order of preference:

1. The milestone's own "Walk this" list, in
   `<docs>/project/milestones/`.
2. The session spec's "Done when" list.
3. The screens themselves, if neither exists.

Reconcile it against what was actually built before you start. A
milestone's walk list is written before the build and often assumes a
control that never shipped. Read the session notes and the spec, and
know which steps cannot be done in a browser before you ask a person to
try one.

Order the scenarios so each leaves the state the next one needs. The
empty case first, then filling, then the derived work, then the
conflicts, then the output. A person should never have to undo
something to reach the next scenario.

## Phase 4: the walk

One scenario per message. Never dump the list.

### Giving a scenario

Give it a heading and one line saying what it proves. Then numbered
steps in the second person. Then what passes and what fails. Then stop
and wait.

Name the exact field, the exact value and the exact tier. "Enter total
plot area as 12000, unit m2, tier stated" beats "enter a value". A
walked scenario has to be repeatable by somebody else next month.

Point at one or two things worth watching that are not the subject of
the scenario. The downstream field, the row on the printed page, the
pill on the list. Most findings come from those asides.

Ask a closing question that needs a specific answer. "Tell me what the
net plot area panel says" gets you something. "Let me know how it goes"
does not.

### Reading the reply

Replies come as prose, screenshots, pasted API responses or pasted
documents. All four are evidence and all four are partial.

The person names some findings explicitly. Record those. They also
walk past things they have not noticed, and those are yours to catch,
so read every screenshot for what is missing as well as what is wrong.
A panel with no history on it looks fine until you ask what should have
been there.

When something looks wrong, go and prove it before you write it down.
Read the code, query the database, render the artefact yourself. A
finding that names `<be>/src/documents/resolve/state.py:630` is
actionable; a finding that says "seems like the state logic is off" is
noise. A fault in a screen is usually `<fe>`. A fault in a
number or a rule is usually `<be>`. Say which one you read.

Look one step past what the person is looking at. They report the field
they opened. Check what the fields computed from it now say, and what
the rendered document prints. The worst findings usually come from
looking downstream of something the person has already called a pass.

Never take a suspicion to the person as a fact. Say what you
reproduced, say what you could not, and mark an unreproduced item as
such in the file.

### When a finding blocks the rest of the walk

Some findings stop the walk. A page that returns a 500, a save that
never lands, a role that cannot sign in. Everything after it either
cannot be reached at all, or it can be reached and proves nothing,
because the fault is already upstream of the answer.

Say so the moment you see it. Do not carry on quietly, and do not
decide alone.

Two tests, and either one on its own is enough:

1. A later scenario cannot be performed until this is fixed.
2. A later scenario can be performed, but its result would be
   meaningless. A pass there would be a false pass.

Anything else is an ordinary finding. Write it down and carry on.
Nudging on every defect turns the walk into a fix session, which is the
thing this skill exists to prevent.

#### The nudge

One short message, then stop and wait. It says the finding number, what
breaks, which scenarios it blocks, and the question.

> Finding 7 blocks scenarios 5 to 9. The block list never loads, so
> nothing past the record screen can be reached. Do you want me to fix
> it now, or log it and skip to scenario 10?

Give your recommendation in the same message. Fixing now is right when
the cause is narrow and named, and the blocked scenarios are the ones
worth walking. Logging is right when the fix is a redesign, or when the
remaining scenarios can be reordered around the fault.

The person decides. If they say log it, mark the blocked scenarios
`blocked` in the walk record, skip them, and carry on. Never fix
without a yes.

#### If they say fix it

Dispatch one subagent. Never fix in this session, because the walk is
this session's job and a fix inside it loses the person's place.

Hand the subagent the finding, the repository, the file and line you
named, and the proposed fix. One instruction: fix that finding and
nothing else. It runs the suite for the repository it touched before it
reports back.

Where the fix lands depends on what is being walked:

- A standalone walk runs against `main`. The subagent works on a short
  branch named for the finding, merges it to `main` and pushes. It has
  to reach `main`, because the running containers mount the primary
  checkout and that is where the walk is looking.
- A walk inside a session runs against the milestone branch. The fix
  goes on that branch, alongside the rest of the milestone's work, and
  merges with it later.

One blocking fix at a time. Never hand a second finding to an agent
that is already running.

#### After it lands

Restart the stack and prove the fix from the shell yourself before you
send the person back. Same rule as phase 1: never send anybody to a
screen you have not opened.

Then ask them to re-run the scenario that raised it. Mark the finding
`fixed` with the date and keep the entry whole. It is still the
evidence that the walk earned its place, and phase 7 triage reads the
status rather than the row.

Record the interruption in the walk record. Say which finding stopped
the walk and which scenarios ran after the fix, because the second half
of the walk ran against different code from the first.

### When the person raises a product point

Some of the best findings are not defects. They are the person saying
the workflow is wrong.

Record those in their own words, with the reasoning, as an
`improvement`. Do not soften them into a defect and do not argue them
into a question. If the same complaint arrives on a third screen, say
so in the entry, because a repeated complaint is one design fault, not
three.

If the person makes a scope decision during the walk, record it as a
`decision` with the date, and delete anything you raised as a question
on the same point. A decision by the person who owns the engagement
does not stay open as a question.

### Between scenarios

Record findings as they arrive, not in a batch at the end. Say in one
line what you wrote and what number it took, then give the next
scenario. Do not restate the whole table.

## Phase 5: close

Say what the walk cost and what it found. The counts, split by kind.
How many were invisible to the suite, and the suite's number for
contrast.

Then name what to fix first and why, in one short list. Group findings
that share a cause, because they are one piece of work.

Do not fix any of it here. Do not open a branch.

At the close step, set the front fields in `notes.md` and check them. Set `Status: done`, write `Summary:` in one line, and set `Owes:` to a bug hunt that names the findings file, for example `Owes: bug hunt on bugs-and-improvements.md`. Use `blocked` only inside `Owes`. Then run `python3 ~/.claude/skills/sessions/scripts/sessions.py check <folder>`. If it exits non-zero, fix the notes and run it again. When it passes, run `python3 ~/.claude/skills/sessions/scripts/sessions.py index --write`.

Then hand the file over and stop. End on the hand-over. Do not offer a menu of next steps or offer to start any fix, because that work belongs to the bug hunt named in `Owes:`.

## The rules, short

1. Find and record. Never fix, unless the person tells you to fix a
   blocking one.
2. Prove the setup yourself before handing over a URL.
3. Open the findings file before the first scenario.
4. One scenario per message, with exact values and a closing question.
5. Probe the running system before naming a cause. Say "not reproduced"
   rather than guessing.
6. Name the repository in every path. Three of them exist.
7. Look downstream of whatever the person is looking at.
8. Record the person's own framing, quoted.
9. Read the file before every write; another agent may share it.
10. Never renumber a published entry.
11. Propose a fix inside every finding.
12. A finding that blocks the rest of the walk goes to the person as a
    question. They decide, a subagent fixes it, and it lands on the
    branch the walk is running against.
