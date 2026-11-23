# Lane: anthropic

This lane has not yet been run in a real session, so its commands come from
the tools' own docs.

The review lane. It questions the code and the running app with Claude Code's
own skills and Anthropic's plugins. It writes no check into a code
repository. Two of its tools may leave files there, and the lane names each
one and never commits it. Its test cases are of Type `security`, `error handling` and `exploratory`.
Its job is to find defects beyond the happy path and to say which changed
areas need more testing.

| Job | Skill or command | Reads | Produces |
|---|---|---|---|
| Bug review | `/code-review` | the milestone's change in `<be>` and `<fe>` | candidate findings |
| Security review | `/security-review`, `claude-security` | a branch diff, or one commit | candidate findings |
| Exploratory evidence | `/verify`, `/run`, `webapp-testing` | the running target | a screenshot, a log, an observation |
| Browser walk | Claude in Chrome | the running target in the person's browser | an observation, a GIF |

## Install check

Built in to Claude Code: `/code-review` (alias `/review`), `/security-review`,
`/verify` and `/run`. They need nothing installed.

Needs a plugin: `claude-security`. Install it from the official marketplace,
then reload:

```
/plugin install claude-security@claude-plugins-official
/reload-plugins
```

If Claude Code says the marketplace is not found, run
`/plugin marketplace add anthropics/claude-plugins-official` first.

Needs a skill: `webapp-testing`. It comes from the repository
`https://github.com/anthropics/skills`, under `skills/webapp-testing`. The
docs do not give an install command for it. If the session cannot see
the skill, report it as `not installed`, name that repository, and carry on
with the other parts.

Needs an extension: Claude in Chrome. It needs the Chrome extension at
version 1.0.36 or later, a `/login` sign-in on a direct Anthropic plan, and
`claude --chrome` or `/chrome` to connect. An API key does not work for it.
Read `/chrome` for the current requirements.

If a part is missing, the lane reports it and runs the parts it has.

## What this lane overrides

**`/code-review` runs on the milestone's change.** Give it the change in each
code repository as a range or branch target, such as `main...<branch>` or
`<sha>^..<sha>`. It never runs with `--fix`, because QA fixes nothing. It
never runs with `--comment` unless its brief records the person's yes,
because that posts outside the machine. It does not run at `max` or `ultra` unless the person
asks, because of their cost. `ultra` also sends the work to a cloud sandbox.

**A review finding is a candidate.** It becomes a finding of kind `bug` only
when a check or a reproduction confirms it. Otherwise it is written with "not
reproduced". The lane never names a root cause. It reports where the review
pointed and what the reproduction showed.

**`/security-review` needs an unmerged branch.** It reviews the current
branch against origin's default branch, and it needs an `origin` remote. Once
the milestone is merged there is no difference to read. Run it only where
the hand-over says the checkout is on the unmerged change. Otherwise use the
substitutes below. The docs do not say
that `/security-review` accepts a target, so the lane does not give it one.
What the lane uses then is `/code-review` on a commit range, which accepts a
range target, and `claude-security` in "scan changes" mode, which accepts a
branch diff, a pull request's diff or one commit.

**`claude-security` runs only on a yes.** It asks the person to confirm its
time and token cost. The lane runs it only when its brief records the
person's yes, and never under `--afk`. The subagent answers no to the tool's
own cost prompt unless its brief records the person's yes. Run only the
"scan changes" job and never "suggest patches". It writes a folder named
`CLAUDE-SECURITY-<timestamp>/` into the repository it scans. The folder has
its own `.gitignore`. The lane never stages it. Copy `CLAUDE-SECURITY-RESULTS.md`
and `CLAUDE-SECURITY-RESULTS.jsonl` into `<session>/evidence/anthropic/`, and
tell the person the folder is still in the repository. Before a copy stays in
the evidence, remove any secret, token or key a finding quotes. Name only its
file and line. Its findings are
candidates, and their severity (`CRITICAL`, `HIGH`, `MEDIUM` or `LOW`) is
carried over unchanged.

**Exploratory evidence gets no lasting check.** `/verify`, `/run` and the
`webapp-testing` skill give evidence for exploratory test cases that are not
worth a lasting check: a screenshot, a console log, an observation. They
produce a result row and no check. `webapp-testing` is Python Playwright. It
is separate from the playwright lane and shares no files with it. When
`/verify` has no recorded recipe, the docs say it writes one to
`.claude/skills/verify/SKILL.md`. That is a write into a code repository. Run
`git status` after it, report any such file to the person and never commit it.

**Claude in Chrome needs a yes.** It drives the person's real, signed-in
browser. Use it only when its brief records the person's yes, and never under
`--afk`. It pauses
at a login page or a CAPTCHA, and the person handles those.

Nothing else is overridden.

## Phase 2: propose test cases

1. Read the milestone's change in each code repository with `git diff` on the
   range the hand-over names. Where it says `none found`, skip both reviews,
   say so in the report, and run the exploratory test cases.
2. List the changed areas. For each one, note the area next to it that the
   change could have broken.
3. Return one `proposed` row for each risk in the report, with no id. Use Type
   `security`, `error handling` or `exploratory`, and set Lane to `anthropic`.
4. Tie each row to a fact. A risk that matches no fact is `Fact: none`, Type
   `exploratory`.
5. Take Expected result from the fact. The code shows what the system does,
   and it never sets what it should do.
6. Report which changed areas have no fact and no other lane's test case.
   Those are the areas that need more testing. Phase 7 reads that list.

## Phase 5: run

Every task below goes to its own subagent, and each
brief carries three standing lines. It never runs `git stash`,
`git checkout .` or `git reset --hard`. It writes no credential anywhere. It
tests only the target it was handed. Never review or reproduce inline.

1. Run `/code-review` on the range, with the effort the person chose. Without
   a choice, use the default. Save the text of the reply to
   `<session>/evidence/anthropic/code-review-<repo>.md`.
2. Run `/security-review` while the branch is still unmerged. Otherwise use
   the substitutes above. Save the reply the same way.
3. For each finding, write one line in
   `<session>/evidence/anthropic/candidates.md`: the repository, the file and
   line the review gave, the claim, and "not reproduced" until it is.
4. Try to reproduce each candidate that maps to a test case. Use the running
   target, or report it as needing a check from the playwright, postman or sql
   lane. A reproduction states its steps and its observed result.
5. Run the exploratory test cases with `/verify`, `/run` or `webapp-testing`.
   Save each screenshot or log under `<session>/evidence/anthropic/`, after
   removing any cookie, token or person's data it shows.
6. Write one row per test case into `<session>/results.md`. Lane is
   `anthropic`. Check is the command used. Evidence is the saved file.

Result is `fail` when a reproduction shows the expected result broken, and
`pass` when it shows the expected result held. It is `not run` with the reason
when nothing could try it.

The failing-once proof for priority 1 does not apply to a review. In its place
a finding counts only when reproduced. A review that finds nothing proves
nothing, so a priority 1 test case that only a review covers is `weak`.

Several lanes write `results.md` at once, so read it immediately before each
write and only append.

The lane writes no lasting check, so it has no regression set. When the core
asks in phase 7, write `none, the lane writes no lasting check` under
`Regression: anthropic`.

A pass on a retry is `flaky`. A pass against a mock is reported as such. The
lane does not skip or disable anything to get a green run.

## What this lane does not cover

1. Lasting checks. The playwright, postman and sql lanes write them.
2. Fixes. The lane never runs `/code-review --fix` or `claude-security`'s
   "suggest patches" job.
3. Security that needs a person with a threat model. The review finds
   candidates and nothing more.
4. Anything outside the milestone's change and what sits next to it.
5. Pull request comments, unless the person says yes.

It never adds or rewords a fact, never marks one and never names a root
cause. It does not open, switch or remove a branch or worktree, and it does
not merge. It edits no product code and writes nothing to the engagement
record. Nothing goes to a hosted service without the person's yes in chat.
The lane never asks the person itself. It stops that part, reports what needs
a yes, and the orchestrator asks.

## Reporting back

The lane never writes `notes.md`. It reports, and the orchestrator writes
what the notes need. Report one of two things.

1. Done. Give the counts of each Result. List the candidates, each marked
   reproduced or "not reproduced". List the parts that were `not installed`
   and the parts skipped for want of a yes. Point at `<session>/results.md`
   and `<session>/evidence/anthropic/`.
2. Blocked. Say what stopped the lane and what it needs.

State the changed areas that still need more testing. Name any file a tool
wrote into a code repository.
