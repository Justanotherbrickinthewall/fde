---
name: qa-session
description: "Answer one question before a delivery: does the built feature match what was agreed. The session rebuilds the agreed facts from the record alone, turns them into test cases that a person reviews, runs the approved test cases through lanes side by side, and judges each fact from the evidence. Use when a milestone is built and about to be delivered, or when the user says \"QA this\", \"start a QA session\", \"write test cases for\", \"test this feature\", \"does it match what we agreed\", or invokes /fde:qa-session [milestone] <detail> [--afk]. With no lane flag, every lane that has kept test cases and whose tool is installed runs, and a --<lane> flag runs only the lanes named. It finds and records, and it never fixes product code. A pile of failures is /fde:bug-hunt and a walk by hand is /fde:smoke-test."
---

# qa-session

Check one built feature against what was agreed, in one chat, with the
evidence written as you go. The session ends with a result for every agreed
fact and a list of what nobody tested.

It runs after the build, the smoke test and the bug hunt, and before a
delivery. It writes test cases, writes checks and runs them. It never changes
the product.

**The tools are not written here.** Each is a lane in `lanes/`. A lane can
change without this file changing. `lanes/README.md` is the contract.

## The loop, and who does what

The method has six steps, shown in the phase table below. The session
generates, and a person decides.

The person keeps business understanding, risk analysis, test strategy,
exploratory testing, defect judgement and the quality decision. The session
never makes those calls for them.

## Finding the engagement

The umbrella is the nearest ancestor of the current directory holding a
`.engagement` file. Read that file first. It carries plain `key=value` lines:
`slug`, `docs`, `be`, `fe`, `stack`, `plugin_version`, `plugin_root`, `apps`,
`record`, `merge_into`, `integration`, `release` and `worktree`. The `docs`,
`be` and `fe` values are folder names inside the umbrella, and `be` or `fe` is
empty when that side does not exist yet. The last six keys are empty for a
one-app engagement.
`apps` lists the apps; when it is set, resolve the app first. `record` is the
record's path inside `<docs>`, and empty means the `<docs>` root. `merge_into`
is where a milestone branch merges, and empty means `main`. `integration` is
the branch the app branch merges up into, and empty means there is no such step.
`release` is the branch that deploys, and nothing touches it in away mode.
`worktree` is the naming pattern for a worktree beside its repository.
`fde:init` writes the file.

Below, `<docs>` means the docs folder that `.engagement` names, `<be>` the
backend folder and `<fe>` the frontend folder. In a shell command they are
`$DOCS`, `$BE` and `$FE`, each an absolute path. `<record>` is the `record`
value with the app filled in, and `$REC` is `$DOCS/<record>`; where `record` is
empty, `$REC` is `$DOCS`. Every engagement path is written relative to
`<docs>`, so a command run from the umbrella needs that prefix in front of it.
A session path keeps its `my-sessions/` prefix.

`${CLAUDE_PLUGIN_ROOT}` is the plugin's own directory, and every plugin path
below hangs off it. Where the variable is unset, read `plugin_root` from
`.engagement` and use that. Where that is missing too, ask the user once for
the plugin's path and write it back as `plugin_root`.

## Words used the same way everywhere

A fact is one agreed, checkable statement rebuilt from the record, with an id
such as `F1` and a source. A test case is one row in `test-cases.md`, with an
id such as `TC-001`, tied to a fact. A check is the executable form of one
test case, written by a lane and named with the test case id. A lane is one
tool family that proposes test cases, writes checks and runs them. Lanes run
side by side. The target is the running system under test.

A QA lane is a tool family. In `aie-session/lanes.md` a lane is a build in its own
worktree, and this skill reads that file only for its worktree rules.

## Invocation

```
/fde:qa-session [<milestone>] <detail> [--afk] [--<lane> ...]
```

The milestone is optional, and a QA session never refuses to start for want
of one. It does not check the milestone's status either. A milestone still
`building` gets a warning in **For the user**. With no milestone the scope
comes from the user's words, and the facts from the wiki pages and
conventions those words point at.

### Flags

Read the flags first, before anything is scaffolded. Phase 0 writes them into
`notes.md` as **Flags**, and every later phase reads them from there. A
resumed session trusts the file, not its memory of the command.

| Flag | Effect |
|---|---|
| `--afk` | The user is away. Nothing waits on them, as "Away from the keyboard" below says |
| `--<lane>` | Runs only the lanes named, such as `--postman` or `--playwright --sql`. Valid only if `lanes/<lane>.md` exists |

Four lanes exist: `postman`, `playwright`, `anthropic` and `sql`. With no lane
flag, every lane runs that has kept test cases and whose tool is installed.
A lane whose tool is missing reports so, and the session carries on without
it.

Any other flag is an error. List the flags above and what is in `lanes/`, and
stop.

### Away from the keyboard

`--afk` follows the "Away mode" rule in the global `CLAUDE.md`, and that rule
is the only place its text lives. The user may pass the flag, or say
mid-session that they are going away. Either one writes `afk` into **Flags**
in `notes.md`. A question already open when the flag lands is answered under
the rule, the moment it lands.

Under the rule, this skill adds these.

1. `--afk` changes who answers a question and never how the run goes. Every
   kept test case still runs.
2. Two things stop an away session. The first is a target that is not local
   and was not named. The second is a stack that will not come up.
3. An away session never sends anything to a hosted service. Its only push is
   phase 8's, to the engagement's own remote. It never changes CI, and it
   never merges where CI would turn red.
4. An away session never claims a person reviewed the test cases. Phase 3 says
   how it records that.

Nothing else waits. The user's own words go into **Carry forward**.

## The nine phases

| # | Loop step | Phase | Owner | Ends when |
|---|---|---|---|---|
| 0 | | Scaffold | core | the folder exists and `notes.md` is written |
| 1 | Understand | Facts | core | the fact table is in `notes.md` |
| 2 | Ask | Test cases | core and lanes | `test-cases.md` and `test-plan.md` are drafted |
| 3 | Review | Review | core | the person has decided every test case, or `--afk` has |
| 4 | | Stand up | core | the stack is proven, and the identities, data and branches exist |
| 5 | Execute | Execute | lanes | every kept test case has a row in `results.md` |
| 6 | Validate | Judge | core | every fact has a result |
| 7 | Improve | Improve | core | the coverage table, the gaps and the memory gaps are written |
| 8 | | Close | core | the checks are merged and the hand-over is written |

Run the phases in order. Never skip forward, and never start a phase whose
gate has not been answered. Phase 7 may send the session back through phases
2 to 6 once, as its section says.

Phase 5 is the lanes'. Everything else is this file's.

## The phase marker

`notes.md` carries `Phase:` in its front block. Update it the moment a phase
ends, before doing anything else. Context gets compacted and chats get closed.
Whoever picks the session up reads `Phase:`, `Branch:` and **Resume here** and
knows where they are. A marker that lags reality is worse than none.

## Subagent models

Subagent models follow the global rule, and every dispatch passes the model
explicitly. Pick by the kind of job.

- Reading the record, mapping routes, finding a checklist: search and mapping.
- Generating test cases, analysing a failure, planning: judgement.
- Writing test data, writing a check from a specific brief, fixing a check or
  a blocking product bug: implementation.
- Running a command and reporting counts and failures: mechanical, checked by
  its output.

Say which kind a dispatch ran as in the progress log. Tell every subagent to
follow the same rule for its own subagents. Every brief carries the never-run
list: `git stash`, `git checkout .`, `git reset --hard`, and anything else
that discards a working tree. To compare against `HEAD`, use `git diff`.

## Phase 0: Scaffold

If the user gave no detail, ask one short question. Under `--afk` take it
from the user's own words.

1. **Read the flags, resolve the app and the milestone.** Where `.engagement`
   sets `apps`, take the app from the milestone id or the user's words, and
   ask once if neither names one. With a milestone id, check
   `$REC/project/milestones/` for a file starting with it. On a typo, list
   the ids that exist and ask. Under `--afk` take the closest choice and
   write it under **Decisions**.
2. **Check the repositories.** Confirm `<docs>` is on `main` and clean, and
   pull it. Note which of `<be>` and `<fe>` the feature touches.
3. **Create the session folder.** Run it from the umbrella, or pass
   `--root <umbrella>`:

   ```bash
   python3 ~/.claude/skills/sessions/scripts/sessions.py new --type qa --slug <slug>
   ```

   With a milestone the slug is `<milestone>-<slug>`. With none it is
   `<slug>` alone. The script chooses the folder path, which is
   `my-sessions/qa/<date>-<slug>/`, and writes `notes.md` from the shared
   template. Follow `~/.claude/skills/sessions/SKILL.md` for the notes
   contract and the close step. If a folder with that slug exists, resume it.
4. **Fill the front block.** Set the fields listed under "notes.md fields",
   and `Phase: 1 facts`.
5. **Say the path**, then go straight into phase 1.

## Phase 1: Understand

This is the clean-room read, and it is the heart of the skill. The session
gets only the feature or milestone name. It rebuilds what was agreed from the
record, so that a fact the record lost shows up as a gap later.

Read only `my-sessions/INDEX.md`, the knowledge index when the memory line
names one, the milestone file, and what it links to in `$REC`.

The core does not read the builder's session notes, `spec.md`, `plan.md` or
the code while it writes the fact table. Later phases read code only for
their own surface, and never for an expected result. The builder's notes wait
for phase 7.

Three sources feed the fact list.

- The milestone's scope and its "Walk this" list.
- The wiki pages the milestone cites.
- The checklist of each convention the engagement adopted.
  `<docs>/setup/conventions.md` is a table with one row per convention, and
  the Checklist cell names the file, relative to the plugin root. Read each
  row marked `yes`. The checklist is in that file under "The checklist".

A checklist item that the running system can show is a fact, with the
convention file as its source. An item that only the code can show, such as a
layering test, is also a fact, and the lane that can read code takes it.

Write the facts into `notes.md` under **Findings**, one row each.

| ID | Fact | Source |
|---|---|---|
| F1 | One checkable sentence | `$REC/project/milestones/m03-x.md`, "Walk this" step 4 |

The source is a path with a heading or a line. A fact without a source is not
a fact.

Never invent a fact, a number or a threshold. A statement too vague to check,
such as "it should be fast", goes under **Open items** in the person's words,
marked as an open question. It is not a fact.

Then list the surface: every route and method in `<be>/openapi.json`. The
fact list and the route list are the two inventories. Phase 7 reports on both.

If the record yields no facts at all, say so in one line. The session can
still run, with test cases marked `Fact: none`. Its result can then never
read as "matches what was agreed", and the summary says that.

Write **Scope, in plain words** next: about 200 words on what is under test,
which facts and routes exist, and which conventions apply. Set
`Phase: 2 ask` and go straight into phase 2.

## Phase 2: Ask

Generate test cases. A tool asked a vague question gives a vague answer, so
give every generating subagent the same context: the facts, their sources, the
route list, the conventions, and the fixed shape below.

### What a test case is

A test case has a fixed shape. The file is `<session>/test-cases.md`, with
front matter and one table.

```yaml
---
kind: test-cases
status: draft
milestone: <id>
date: <DD-MM-YY>
---
```

| ID | Fact | Type | Scenario | Steps | Test data | Expected result | Priority | Lane | Status |
|---|---|---|---|---|---|---|---|---|---|
| TC-001 | F3 | negative | A non-member opens a project | 1. Sign in as the non-member. 2. GET the project | `data/members.csv` row 2 | 404 with a body | 1 | postman | proposed |

- **ID** is `TC-001`, in the order written. Never renumber one.
- **Type** is one of positive, negative, edge, boundary, security, session and
  error handling. A test case with `Fact: none` has Type `exploratory`.
- **Priority** is 1, 2 or 3. Priority 1 means the delivery cannot go out if it
  fails.
- **Lane** is the lane that will run it: `postman`, `playwright`, `anthropic`
  or `sql`.
- **Status** starts as `proposed`. Phase 3 changes it.

### Where the expected result comes from

The expected result comes from the record, never from what the application
does today. A check built from current behaviour proves only that the code
does what the code does.

A test case whose expected result has no source in the record is not a test
case. It goes under **Outside the facts** in the same file, as a question for
the person. It is never run.

### Coverage by type

For every fact, write test cases across the seven types. Say for each fact
which types do not apply, and why, in one line. A missing type is then a
decision and never an oversight.

The types are positive (valid input), negative (invalid input and forbidden
actions), edge (empty, one, many, long), boundary (either side of a stated
limit), security (who may see or change what), session (sign-in, sign-out,
expiry, the cookie) and error handling (what the user sees on failure).

A boundary test case needs a limit stated in the record. Where there is
none, the type does not apply, and the missing limit goes under **Open items**.

### The lanes propose too

Before the dispatch, find the change under test in each code repository. It is
the branch named with the milestone id or the slug, or its merge on
`<merge_into>`. Write each as a commit range, such as `<base>..<head>`, under
**Repositories** in `notes.md`. Where none is found, write `none found`.

After the core's own pass, dispatch each lane that will run, in one message.
Each returns its proposed rows in its report, with no id. The core numbers
them and writes them into `test-cases.md`. A lane's proposal is tied to a
fact, or it carries `Fact: none` with Type `exploratory`. In phase 2 a lane
writes nothing in a code repository and does not explore the live
application, because neither the branch nor the target exists yet.

Merge the proposals, remove duplicates, and keep the lane that fits best.

### The test plan

Write `<session>/test-plan.md` with `kind: test-plan` and `status: draft`.
Keep it to one page. It holds the scope and what is out of scope, the
objectives, the lanes and why each runs or does not, the target, the
identities, the test data, the risks, and the entry and exit criteria.

The exit criteria are written before anything runs. For example: every
priority 1 test case passes on the real target, and no fact is `fail`. A
criterion written after the run is a description of the run.

Set `Phase: 3 review` and go on.

## Phase 3: Review

This is the gate, and it is the point of the method. A generated test case is
a possibility. The person decides which possibilities belong in the test
strategy.

The person reads `test-cases.md` and `test-plan.md`. Put these five questions
to them in plain words.

1. Does each test case match the actual requirement?
2. Does it apply to this application?
3. Are business rules missing?
4. Is each expected result correct?
5. Are the security requirements right?

Take their strikes and their additions. Each test case becomes `kept` or
`dropped`. A drop carries a one-line reason in the **Status** cell.

A test case with `Fact: none` is kept only on the person's word.

Show what moved after each round, and ask again. When they approve, set
`status: approved` on both files and name them and the date in the first
paragraph.

Under `--afk` the session applies the five questions itself. It writes each
decision and its reason into `test-cases.md`, and sets
`status: approved (not reviewed by a person)` on both files. It carries that
phrase into the Summary at close. A `Fact: none` test case still runs, and its
failure can only become a finding of kind `improvement`.

A change that alters what was agreed is the FDC's call. Write it under
**Open items** and carry on without it.

Set `Phase: 4 stand up` and go on.

## Phase 4: Stand up

The core owns the environment because it belongs to the engagement.

### The target

QA runs against the local stack, or a test environment the person names. It
never sends an unsafe request to production or to a client's live system.

If the target's URL is not local and nobody named it, stop and ask. That
holds under `--afk`.

### The stack

Bring the stack up and prove it the way `/fde:smoke-test` phase 1 does. Read
`${CLAUDE_PLUGIN_ROOT}/skills/smoke-test/SKILL.md` for the steps. Do not
copy them here. Never hand a lane a URL you have not opened.

Stop before smoke-test's hand-over. Never reset a password and never print
one. Prove the sign-in with the credential the environment already holds.

### The identities

Checks on roles need at least a super admin, a member and a non-member,
where the auth convention is adopted. The super admin comes from the seed. Its
credential is read from the environment the seed uses, and a lane is told only
where it lives.

For the other two, look for a seed command or a fixture in `<be>` first.
Otherwise each lane's setup makes its own, through the API as the super admin.
The setup script generates the credential at run time, so no agent chooses,
types or sees it, and it is never written down. Each lane's identities carry
the prefix `qa-<slug>-<lane>-`.

The agent never writes, prints or chooses a credential. A credential the
person supplies is read from the environment, and the skill reports only
whether it is set. A lane is told where each credential comes from, never its
value.

### The test data

Generate test data into `<session>/data/`, as CSV or JSON, one file per need.
Cover the valid, invalid, boundary and duplicate rows that the kept test cases
require.

- It is synthetic. Never copy production rows or a client document into it.
- Check each file against the application's real constraints before a lane
  uses it: the serializer or model rules, and the schema in
  `<be>/openapi.json`. A row they make impossible is corrected or removed,
  with a note in the file's header.
- A row never holds a credential that signs an identity in, because the postman
  lane commits the data. An invalid value used as a test input is fine.
- Everything a run creates carries the prefix `qa-<slug>-`, so leftovers can
  be found. A run must be repeatable.

A second subagent checks the data against the constraints, because an author
checking its own data finds what it expected to find.

### The branches

The checks are a lasting asset, so they live in the code repositories.

The orchestrator cuts one branch, `qa/<slug>`, in each repository a running
lane writes to. That is `<be>` for `postman`, and `<fe>` for `playwright` or
for the postman lane's real app traffic part. The `anthropic` and `sql`
lanes write no checks into a repository, and they get no branch.

Cut it from `origin/<merge_into>` (`main` when empty) with `--no-track`, as
`${CLAUDE_PLUGIN_ROOT}/skills/aie-session/lanes.md` shows, with `qa/<slug>` as
the branch name. Where the repository's primary checkout is held by another
session, use a worktree as that file describes, with the path
`<repo>-qa-<slug>` and the `worktree` key from `.engagement`.

Hand each lane its path: `<be>/postman/` for `postman`, and a folder under the
Playwright `testDir` in `<fe>` for `playwright`.

A lane never opens, switches or removes a branch, and no two lanes write in
the same checkout. `<docs>` never branches. Run each repository's own test
suite once on the clean branch, so a later red is the lane's and not the base's.

Write the repositories and the branch into `notes.md`, set
`Phase: 5 execute`, and go on.

## Phase 5: Execute

Read `lanes/<lane>.md` for each running lane and follow it. Each lane writes
the checks for its kept test cases and runs them.

Dispatch every running lane in one message, so they run side by side. Each
brief carries what `lanes/README.md` says a lane is handed, the never-run list
and the subagent-model rule.

The orchestrator never writes a check. A lane whose tool is not installed
reports `not installed` with the install commands. Its test cases become
`not run`, and the lane goes under **For the user**. There is no gate. The
lanes run to the end and stop only when blocked.

A lane never asks the person anything itself. When a lane reports a part
waiting on a yes, put the question to the person in chat. On a yes, dispatch
the lane again for that part alone. Under `--afk` that part is `not run`.

When every lane has reported, `<session>/results.md` holds one row per test
case per lane. Read the rows and the lanes' reports. Do not read the raw
output. A report is evidence of what an agent believes, so where a claim is
load-bearing, such as a check said to fail on purpose, read the evidence file.

Set `Phase: 6 validate`.

## Phase 6: Validate

The lanes report checks, and the core judges facts.

### Analyse a failure before changing anything

A possible root cause is not a confirmed root cause. For every failed check:

1. Gather the evidence: the error, the check's code, the screenshot or trace,
   the logs and the expected result.
2. Write the possible causes, each with the evidence for it, and mark each
   `hypothesis`.
3. Confirm one by reproducing the failure a second way. That can be a direct
   request, a second lane or a read of the code. Only now read the code.
4. Write a confirmed cause as the cause. Write an unconfirmed one as "possible
   cause, not confirmed".

### Then classify

Every failure is one of three things.

1. The product is wrong. It is a finding of kind `bug`.
2. The check is wrong. A subagent fixes the check. The change is logged, the
   check runs again, and the expected result is never what changes.
3. The fact is unclear. It becomes an **Open items** entry for the client,
   and its test cases become `not run`.

### Read the passes as well

For each fact, ask whether its passing test cases prove it, or only its happy
path. What the fact requires that no test case covers is a coverage gap for
phase 7.

A result of `weak` means the evidence was never shown to catch a break. For a
check, it could not be made to fail. For a review, nothing reproduced it. It is
not a pass. A result of `flaky` means it passed only on a retry. It is not a
pass. A `weak` or `flaky` check goes to a subagent to fix it, and it runs
again. A `weak` review result is a coverage gap for phase 7.

### Judge each fact

Write the result into the fact table, with the evidence in one line: the
check's name, expected and actual.

A fact is `pass` when every kept test case for it passed on the real target.
It is `fail` when any failed and the product is wrong. Anything else is
`not checked`, with the reason. A fact with no kept test case is `not checked`.
A pass against a mock or a simulation is not a pass on the fact.

### Write the findings

Write each `fail` into `<session>/bugs-and-improvements.md`. The format is
smoke-test's, and it is not repeated here. Read "The shape of the file" in
`${CLAUDE_PLUGIN_ROOT}/skills/smoke-test/SKILL.md` and use it row for row:
the same front matter, table columns, kinds and statuses, and one section per
finding with repo-qualified paths.

The **Found in** column names the test case id and the lane, such as
`TC-014 postman`. A review finding from the `anthropic` lane that nobody
reproduced is written with "not reproduced", as smoke-test does. Evidence
never holds a credential, a cookie, or a person's data copied from a
response. Read the file before every write, and never renumber an entry.

### Nothing is fixed here

QA fixes nothing in the product. The one exception is smoke-test's. A failure
that blocks the rest of the run is put to the person as a question, with a
recommendation. One subagent fixes it only on their yes, on the branch the
target runs from. Read "When a finding blocks the rest of the walk" in the
smoke-test skill.

Set `Phase: 7 improve`.

## Phase 7: Improve

### Coverage

Write a table into `notes.md` under **Coverage**. One row per fact, one column
per type. Each cell is the count of kept test cases, or the reason there is
none.

| Fact | positive | negative | edge | boundary | security | session | error handling |
|---|---|---|---|---|---|---|---|
| F1 | 2 | 3 | 1 | no limit in the record | 2 | n/a, no sign-in | 1 |

State the totals: facts, test cases by status, and routes in `openapi.json`
with and without a check. Every route has at least one check or a written
reason.

### Gaps

List what phase 6 found uncovered. These are facts whose passing test cases
prove only the happy path, types with no test case and no reason, and routes
with no check.

Run one more round of phases 2 to 6 for the gaps the person picks. Under
`--afk` the round covers priority 1 gaps only. Only in this round, when the
target and `qa/<slug>` exist, may the `playwright` lane's planner explore the
live application for more proposals.

After that one round, the rest are listed as owed. The loop runs one extra
round on purpose, so that a session ends. Write the second round's start and
end in the progress log.

### The regression set

Name the checks that stay as regression checks. A failing check stays too,
because it is the regression test the bug hunt turns green. Name every tooling
file a lane committed, such as the Playwright agent definitions and `.mcp.json`
in `<fe>`.

Dispatch each lane that wrote checks to tag the set in the way its tool
allows, and to write the command that runs that set alone. The command goes
into `results.md` under `Regression: <lane>`.

### What the record lost

Only now read the builder's notes: the build session's `notes.md`, `spec.md`
and `plan.md` for this milestone. Find them through `my-sessions/INDEX.md`.

Every fact found there that the record did not give you is a row in the
**Findings** table. Mark its Result cell `memory-gap`, and give where it was
found as its Source. A memory gap means the record is missing something that was agreed. It is the record's
failure, and it is listed for the FDC to file.

### What was not explored

Exploratory testing stays a person's job. End the phase with the areas no
test case touched, and recommend a walk by hand. That recommendation becomes
the `Owes:` line for `/fde:smoke-test`.

Set `Phase: 8 close`.

## Phase 8: Close

The session ends once this phase is done. It never starts another piece of
work, and the next one gets a fresh session.

1. **Check CI.** Read each repository's CI configuration, and find out
   whether it already runs these checks. If it does, the merge turns CI red,
   because a failing check stays. Say so and ask first. Under `--afk` in that
   case, leave the branch unmerged and write it under **For the user**.
   `.mcp.json` changes every developer's tools in `<fe>`, so ask before it
   merges. Under `--afk` leave `qa/<slug>` in `<fe>` unmerged and write it under
   **For the user**.
2. **Merge the checks, the backend first.** Merge the target into each
   `qa/<slug>`. The target is the `merge_into` value, and `main` when empty.
   Read `<docs>/setup/branching.md` when it exists. Run the repository's
   own suite and the regression set once, in a subagent of the kind that runs
   a command and reports, on each branch head, with 2 workers. Every check
   that passed in phase 5 must pass, and every known `fail` must still fail.
   Anything else stops the merge and goes under **For the user**. Then merge `qa/<slug>` into the target and
   push. Open the `<fe>` change only after the `<be>` one has merged, as rule
   7 of `${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/repo-layout.md` says.
3. **Merge up.** When `integration` is set, merge the target into it with
   `--no-ff` and push, as phase 8 of `/fde:aie-session` says. Never merge into
   `release`.
4. **Offer CI, never assume it.** Adding the checks to CI changes how every
   later merge behaves, so it is a question to the person. Under `--afk` it is
   written under **For the user** and not done.
5. **Retire what the session built.** Remove each worktree it made, with its
   containers, volumes and images, as
   `${CLAUDE_PLUGIN_ROOT}/skills/aie-session/lanes.md` says. Remove only what this
   session built. Delete the `qa-<slug>-` data the run left, if any.
6. **Promote what the session raised.** The record is not changed by QA,
   except by this step. Client questions go to
   `$REC/project/open-questions.md` with ids. Our own fieldwork goes to
   `$REC/project/next-steps.md`. The memory gaps are not promoted. They go to
   the person as a list for the next FDC session.
7. **Run the record lint** from the umbrella, and fix what it finds:

   ```bash
   python "${CLAUDE_PLUGIN_ROOT}/scripts/lint_record.py" "$DOCS" "$REC"
   ```

   Do not change the milestone's status. QA does not decide that a milestone
   is delivered.
8. **Set the front fields and check them.** Set `Status: done`, write `Summary:` in one line, and set `Owes:` to what is still owed, or `none`. Use `blocked` only inside `Owes`. Then run `python3 ~/.claude/skills/sessions/scripts/sessions.py check <folder>`. If it exits non-zero, fix the notes and run it again. When it passes, run `python3 ~/.claude/skills/sessions/scripts/sessions.py index --write`.

   The Summary carries the counts and the review status, such as: "41 facts:
   36 pass, 3 fail, 2 not checked. 118 test cases, 4 lanes. Reviewed by a
   person." An away run writes "Not reviewed by a person." instead.

   `Owes:` names a bug hunt on `bugs-and-improvements.md` for the number of
   failed facts, such as "for 3 failed facts", when any fact failed.
   It names a smoke test for what was not explored. It reads `none` when
   neither applies.
9. **Set `Phase: 8 done`**, write the last **Progress log** line, and clear
   **Resume here** to say the session is finished. The closing message names
   every **For the user** item.
10. **Push.** Pull `<docs>` first, because another session may have moved
    `main`. `my-sessions` has no git.

End on the hand-over. Say where `bugs-and-improvements.md` is and name the
first fix to make. Offer no menu and no fix, because that work belongs to the
bug hunt named in `Owes:`.

## notes.md fields

`sessions.py new` writes the shared front block and sections. This skill adds
these front fields, each on its own line.

- Milestone: `$REC/project/milestones/<file>.md`, or "none".
- Lanes: the lanes that ran, such as `postman, playwright`, and any that were
  not installed.
- Phase: `0 scaffold` to `8 close`, or `8 done`.
- Status: active | paused | done. Use `blocked` only inside Owes.
- Target: the base URL, and whether it is local.
- Repositories: the backend, the frontend, both, or "none".
- Branch: `qa/<slug>` in each repository that has one, and whether it is
  committed, pushed or merged.
- Flags: the flags the session was started with, such as `afk`.

It adds these sections after **Resume here**.

- **Scope, in plain words**: phase 1's read-back.
- **Findings**: the fact table, with the result and the evidence one line
  each once phase 6 has run.
- **Coverage**: phase 7's table and totals.
- **For the user**: what the person must see or decide, such as a lane that
  was not installed, a branch left unmerged, or CI.

Sibling files sit beside `notes.md`: `test-plan.md` and `test-cases.md`
(phases 2 and 3), `results.md` and `evidence/<lane>/` (the lanes, phase 5),
`bugs-and-improvements.md` (phase 6), `data/` (phase 4) and `sql/` (the `sql`
lane).

## Keeping it resumable

Keep these current every time you stop, and bump **Last updated**: `Phase`,
`Repositories`, `Branch`, `Status`, the single next action under **Resume
here**, and a dated line in the **Progress log**. Never put a secret in
`notes.md`. Name where it lives.

## The rules, short

1. Rebuild the facts from the record alone. Read the builder's notes only in
   phase 7.
2. Never invent a fact, a number or a threshold. A vague statement is a
   question.
3. A test case comes from a fact, and its expected result comes from the
   record, never from what the application does.
4. For every fact, cover the seven types, or say why one does not apply.
5. A person decides which test cases stand. Under `--afk` the session
   records that nobody did.
6. The target is local, or named by the person. Never production.
7. The agent never writes, prints or chooses a credential.
8. Generated data is checked against the real constraints before use.
9. Lanes run side by side, and no two write in the same checkout.
10. A `weak` check, a `flaky` check and a pass against a mock are not passes.
11. A possible cause is a hypothesis until a second observation confirms it.
12. Never weaken an assertion, skip a check or change an expected result to
    get a green run.
13. QA fixes no product code. A blocker goes to the person as a question.
14. Findings use smoke-test's format. The loop runs one extra round.
15. Nothing goes to a hosted service without the person's yes in chat. The
    phase 8 push to the engagement's own remote is the one exception. Every
    dispatch names its model and carries the never-run list.
