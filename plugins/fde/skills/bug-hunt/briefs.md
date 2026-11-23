# The briefs

Three templates: a diagnosis subagent, a fix subagent, and the two lines that
go to the user.

## The diagnosis subagent

Read-only. Dispatch several at once when several bugs arrive together; they
are independent. Its job is to find the cause, not to fix it. The orchestrator
writes its conclusion into the tracker and hands that to the fix subagent, so
the fix does not re-diagnose.

> READ ONLY. Do not edit, write, or commit anything.
>
> Repos, both on branch `hardening/<name>`: `<path>/<be>` and `<path>/<fe>`.
>
> The bug, in the user's words: "<verbatim>"
>
> <Any context the user gave: a screenshot's contents, which screen, which
> milestone built it.>
>
> Report:
>
> 1. The cause, named to the repository, the file and the line.
> 2. Whether it spans both repositories, and which part is where.
> 3. The smallest fix, named to file and line.
> 4. What a test would have to assert to catch it.
>
> CRITICAL: separate what you OBSERVED in the code from what you INFERRED.
> Label every claim. If the report's premise turns out to be wrong, say so
> directly. I would rather be corrected than agreed with.
>
> Under <n> words.

Put your hypothesis in, and ask for refutation rather than confirmation. A
subagent given a leading hypothesis can confirm half, refute the sharpest
part, and find the real cause, such as a response object nobody had looked at.

Separating observed from inferred is not a formality. A subagent that reads
an assertion string out of a truncated log and names the test it probably
belongs to is guessing, and a brief that states the guess as fact sends the
fix to the wrong file.

## The fix subagent

It owns the bug end to end, in the hunt's worktree if that is free for this
repository, or in its own worktree lane if another fix is already running
there.

> Fix one bug, end to end, on branch `hardening/<name>` (or
> `hardening/<name>-<id>` if you are in a lane).
>
> Repos: `<path>/<be>` and `<path>/<fe>`, or your lane's worktree of either.
> Work only in the tree you were given.
>
> **The bug, in the user's words.** "<verbatim>"
>
> **The analysis.** <The diagnosis subagent's conclusion, or the
> orchestrator's own. Cause named to file and line.>
>
> **Decided already, so do not reopen.** <Anything settled, with its reason.
> A fix named without its reason is a fix nobody can tell is wrong.>
>
> **Other live agents.** <Files another lane or the hunt's worktree is
> touching right now, so you do not collide with them.>
>
> **The stop condition.** <What would make this task end in a measurement
> rather than a commit.>
>
> **How to work.**
>
> 1. Fix it completely. If it spans both repositories, fix both. There is no
>    other agent to hand a half to.
> 2. One commit per repository, with the bug id in the subject. Stage the
>    files you changed, by name. Never `git add -A`, `git stash`,
>    `git checkout .` or `git reset --hard`.
> 3. Run the checks your change touched, not the suite: the test files you
>    wrote or changed and the test file beside any module you changed, named
>    as files and never a directory, plus lint, typecheck, build, and the
>    schema and client checks. Name the command beside every number. Read
>    nothing through `tail` or `head`. Every command stays under five minutes
>    and runs in the foreground, because the watchdog kills a call at about
>    600 seconds. The suite runs once, at the merge gate, started by the
>    orchestrator. Never start it yourself.
> 4. Restart the worker after any Python change and report its start time
>    against your commit time. A prompt file is live on the next call; Python
>    is dead in the worker until the restart.
> 5. Push, and verify at origin rather than in your working tree.
> 6. Read `${CLAUDE_PLUGIN_ROOT}/skills/bug-hunt/verification.md` before you
>    start. It is how a hunt ships the wrong thing.
> 7. If the fix needs a record change, stop short of making it and list what
>    it is instead.
> 8. If you dispatch a subagent of your own, follow the global subagent rule, and always
>    pass its model explicitly.
>
> **Your report is ten lines.** Commit hashes, check numbers, what you
> decided that this brief did not, what you could not do, and how to see it:
> the path on `http://localhost/` to open, what to do there, and what the user
> should now see that they did not before. If you changed Python, say the
> worker has restarted, or the user will look, see the old behaviour and
> conclude the fix did not work. Anything longer goes in a file under the
> hunt folder's `notes/` named `<id>-<slug>.md`, and I will read it if
> something is wrong.
>
> **Never write to `<docs>`.**

### The stop condition

The most valuable line in a brief. Write what would make the task end without
a commit.

A task briefed as "extend the shortening to the other source" gets built,
because the rate came back clean. The same task briefed as "measure whether
that rule is safe on a string the model wrote, and stop if it is not" can end
in a measurement that declines the task and finds a defect in a commit that
shipped hours earlier. An instruction with a caveat gets built. A stop
condition gets measured.

### What makes a brief bad

1. Naming a fix without its reason. The subagent then cannot tell when your
   fix is wrong, and several times it will be.
2. Naming the instances you happened to see. A brief that names two yes/no
   questions when there are seven misses five. Say "these are the ones I
   found, check for others".
3. Naming a line number from a file that has since been reformatted. Say
   where the claim came from, so the subagent knows to verify it.

## The two lines to the user

When something lands, two lines in chat. The detail is in the tracker.

> BE-53 landed as `72960a4`, suite 1815 passed. The app now writes the
> sentence about what it recorded, so the model cannot claim a value went in
> when it did not.

When a task ends in a measurement rather than a commit, say that plainly and
say what the measurement found. When a fix is narrower than the bug the user
reported, say so in their terms rather than yours.
