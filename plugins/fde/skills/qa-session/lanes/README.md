# Lanes

A lane is one tool family doing three jobs for its own surface. In phase 2 of
`/fde:qa-session` it proposes test cases. In phase 5 it writes the checks and
runs them. It owns nothing else.

This is a different thing from a lane in `aie-session/lanes.md`, which is a
build in its own worktree.

Four exist today.

| Lane | Surface | Flag |
|---|---|---|
| `postman.md` | the API | `--postman` |
| `playwright.md` | the interface, in a browser | `--playwright` |
| `anthropic.md` | review of the code and the running app, with Claude Code's own skills | `--anthropic` |
| `sql.md` | stored data | `--sql` |

With no lane flag, every lane that has kept test cases and whose tool is
installed runs. A lane flag runs only the lanes named. A fifth lane is a fifth file
here with its own `--<name>` flag. `SKILL.md` does not change when one is
added.

## Why this is a separate folder

The tools will change. The way facts are rebuilt, test cases are reviewed,
failures are judged and the session is closed will not. Keeping them apart
means swapping a tool costs one file.

Each lane also translates. An outside skill has its own vocabulary and its own
default paths, and this engagement has different ones. The lane is where that
translation is written down, so the outside skill runs unmodified and
`SKILL.md` never learns a word of it.

## The contract

A lane is handed eight things. It may rely on all of them.

1. The session folder path.
2. The fact table from `notes.md`.
3. `test-cases.md`, with the kept test cases assigned to this lane.
4. The target's base URL, up and proven. The lane tests that target and no
   other.
5. The names of the identities and where each credential comes from. Never a
   value.
6. The data files in `<session>/data/`, checked against the real constraints.
7. For a lane that writes checks into a repository: the `qa/<slug>` branch
   there, cut and clean, and the path under it where checks may go.
8. The change under test in each code repository, as a commit range, or
   `none found`.

Items 4 to 7 exist from phase 4. In phase 2 a lane has items 1 to 3, and it
writes nothing into a code repository.

A lane must do seven things.

1. **Check its tool is installed.** If it is not, report `not installed` with
   the install commands, and stop. Its test cases become `not run`.
2. **Propose test cases in phase 2.** Return `proposed` rows for its surface in
   the report, with no id. The core numbers them. Each is tied to a fact, or
   carries `Fact: none` and Type `exploratory`.
3. **Write one check per kept test case in phase 5.** Name each with the test
   case id. Write only under the path it was handed, and the tooling paths its own
   file names.
4. **Make every authoring brief specific.** Name the framework, the language,
   the behaviour, the test cases, the repository's conventions, the locator or
   assertion strategy, the expected results and the structure. A vague brief
   gets a vague check.
5. **Run the checks and write the results.** Write one row per test case into
   `<session>/results.md`, and the evidence under `<session>/evidence/<lane>/`.
   Several lanes write it at once, so read it immediately before each write and
   only append.

   | TC | Lane | Check | Result | Expected | Actual | Evidence |
   |---|---|---|---|---|---|---|

   Result is one of `pass`, `fail`, `flaky`, `weak` and `not run`.
6. **Show every priority 1 check fail once.** Run it with the expected result
   changed, and keep the output as evidence. A check that cannot be made to
   fail is reported as `weak`. A passing generated check is not automatically
   a good one. A lane that writes no check says in its own file what replaces
   the proof. Where nothing does, its priority 1 results are `weak`.
7. **Report back.** Either the run is done, or it is blocked and why. A lane
   never writes `notes.md`. It puts what the notes need in its report, and the
   orchestrator writes it. `/fde:qa-session` resumes at phase 6.

When the core asks in phase 7, a lane also tags the checks it was told to keep
as regression checks. It writes the command that runs that set alone into
`results.md`, under the heading `Regression: <lane>`.

## Invariants no lane may break

**Never author inline.** Every authoring task goes to its own subagent. A lane
may change how many subagents it spends. It may not spend none. The
orchestrator's context is for judging, and writing checks into it makes every
later judgement worse.

**The expected result comes from the test case.** It never comes from what the
application does today. A check built from current behaviour proves only that
the code does what the code does.

The other invariants.

- A check changes only when the check is wrong, such as a locator, a wait or a
  setup step. The change is logged. The expected result is never what changes.
- No check is skipped, disabled or marked to-fix to get a green run. A check
  that does not run is `not run`, with the reason.
- A pass against a mock or a simulation is reported as such. A pass on a retry
  is `flaky`.
- Nothing leaves the machine without the person's yes in chat. That covers
  published results, workspace syncs, hosted mocks, monitors and any call to a
  hosted service. A lane never asks the person anything itself. It stops that
  part, reports what needs a yes, and the orchestrator asks in chat.
- A credential never reaches a committed file, the notes, a command written
  into the notes, or the chat.
- Evidence under `<session>/evidence/<lane>/` holds no credential, cookie,
  token or secret. Remove them before the file stays, or leave the file out.
- A lane tests only the target it was handed.

## What a lane may never run

`git stash`, `git checkout .`, `git reset --hard`, and anything else that
discards a working tree. Put this in every brief.

An agent once ran `git stash` to check whether a failure pre-dated its own
change. The tree was shared, so it took two other agents' in-progress work with
it. To compare against `HEAD`, use `git diff`, or copy a file aside with `cp`.

## Who runs which checks

A lane runs the checks it wrote and no repository suite. The orchestrator runs
the repository's own suite and the regression set once, at the merge gate in
phase 8. A lane that
wants a second tree asks the orchestrator.

## What a lane reports and what it does not decide

A lane reports evidence. It does not name a root cause and it does not mark a
fact. Phase 6 does both, because a possible cause is a hypothesis until a
second observation confirms it, and a fact is judged across every lane.

A lane must not do these things.

1. **Add or reword a fact.** If a test case reveals a missing fact, write it
   under **Outside the facts** in `test-cases.md` and hand back to phase 2.
2. **Name a root cause.** Report the error, the check and the evidence.
3. **Open, switch or remove a branch or a worktree.** The orchestrator owns
   them. A lane that calls `EnterWorktree` or `git worktree add` has failed
   the contract.
4. **Merge.** Merging is phase 8.
5. **Edit product code.** QA fixes nothing in the product.
6. **Write to the engagement record.** `$REC/wiki/`, `$REC/project/` and
   `setup/` in `<docs>` belong to phase 8. A lane that finds a client question
   puts it in its report, and the orchestrator writes it under Open items.

## Writing one

Name it after the tool family, lowercase: `pytest.md` is selected by
`--pytest`. Say which outside skills it invokes and in what order. Say what it
overrides in those skills and why, and announce each override to the skill
before it runs. If it overrides nothing, say that too. Say which tooling files
it commits besides its checks.

Say where it writes: which repository, which path, and which session files.
Say how it proposes test cases, how it writes checks, and how it runs them.
Say what the lane does not cover, and which lane takes that surface instead.
