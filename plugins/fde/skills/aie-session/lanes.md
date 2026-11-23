# Worktrees

`<docs>` is always on `main` and it never branches, so nothing you plan can
land inside a build's history. A build opens a branch in `<be>` or `<fe>` and
merges it there. Those folder names come from `.engagement`, and `$DOCS`,
`$BE` and `$FE` are their absolute paths.

What follows is small, and every line of it was learned the hard way.

## Never two agents in one checkout

Two builds at once need two worktrees inside the repository being built. Agents
sharing one checkout share a working tree and a test database, so they
overwrite each other.

One agent once ran `git stash` to see whether a failure predated its own
change. It took two other agents' work with it, along with an uncommitted
findings file. All of it was recovered, none of it by design.

No agent may run `git stash`, `git checkout .` or `git reset --hard`. Every
brief says so. To compare against `HEAD`, use `git diff`, or copy the file
aside with `cp`.

## Claiming a worktree

A branch can only be checked out in one tree at a time and git refuses the
second attempt. So `git worktree list` is the register, and there is no file to
keep in step with it.

A worktree sits beside its repository, at the umbrella root. Its path comes
from the `worktree` key in `.engagement`, a pattern such as
`<repo>-<id>`, where `<id>` is the milestone id or, with no milestone, the
session slug. When the key is empty, use `<repo>-<id>`. `$WORKTREE` below is
that path, made absolute.

Two things depend on that place. A frontend test may read a file from the
backend folder by a relative path, and it only resolves when the tree has the
backend beside it. The compose file reaches the same way.

Never use the `EnterWorktree` tool here. It writes to
`<repo>/.claude/worktrees/<name>`, which is inside the repository and two
levels below the root. A build that landed there needed a hand-made symlink to
find the backend at all. Use `git worktree add` with the path above.

The branch is cut from `merge_into`, never from `release`. When `merge_into`
is empty, cut it from `main`. `<docs>/setup/branching.md` says more when it
exists.

```bash
REPO="$BE"          # or "$FE", whichever this lane builds
ID=mNN              # the milestone id, or the session slug when there is none
BASE=main           # the merge_into value; main when it is empty
WORKTREE="$REPO-$ID"   # follow the worktree pattern from .engagement
git -C "$REPO" fetch origin
git -C "$REPO" worktree add "$WORKTREE" -b "$ID" --no-track "origin/$BASE"
cp "$REPO/.env" "$WORKTREE/.env"
echo "COMPOSE_PROJECT_NAME=$(basename "$WORKTREE")" >> "$WORKTREE/.env"
```

`--no-track` is there because a repository may set `push.default upstream`.
A branch cut from `origin/<base>` otherwise tracks `<base>`, and under that
setting even `git push origin X` goes to `<base>` rather than to `X`. Push
with the refspec in full, such as `git push origin <id>:<id>`.

Two things a fresh worktree does not have.

`.env` is gitignored, so copy it in. Then set `COMPOSE_PROJECT_NAME` to a name
of its own, or two trees collide on one database.

`.git` is a file in a worktree rather than a directory. It holds one line,
`gitdir: <repo>/.git/worktrees/<name>`. A test service that mounts only the
tree cannot follow that line, so every git-based test fails. Mount the
repository's real `.git` at its own absolute path.

## Parallel lanes run as separate sessions

A piece of work large enough for parallel lanes gets one orchestrator session
per lane, each in its own worktree opened as above. Every subagent a lane
dispatches works in that tree and nowhere else. The sessions message each
other sparingly, and only about names the plan gives an owner.

A brief is sized to finish in under 60 turns. A walker or comparison task
takes one screen or one milestone per subagent. A fix task that reaches turn
60 commits at a clean point and reports what is left, and the orchestrator
dispatches a fresh subagent for the rest rather than sending the same one on.
Long subagents were among the heaviest token users in one week's retro.

## Walking a worktree

A worktree pair has no proxy of its own. The engagement's stack command for a
walk takes the backend folder, the frontend folder, a project name and a port,
and runs the umbrella's own services against that pair. The engagement's
teardown command stops that one project. Phase 6 uses these.

A compose file may hardcode its project name, so a bare `docker compose down`
run in a worktree can take down the primary stack instead of the worktree's
own. Every docker compose command run in a worktree carries an explicit
`-p <project>` or an inline `COMPOSE_PROJECT_NAME=<project>`, never the bare
command.

## Retiring a worktree

Delete its images as well as the tree and the branch. Nothing else knows the
compose project is dead, so the images stay for good. Ten of them from four
dead trees once filled the Docker disk, and the next build failed with
`exit code: 100` over an apt cache with no room in it.

Teardown also removes the lane's volumes and its test image, with
`docker compose -p <project> down -v --rmi local`. If the auto-mode classifier
denies that call, run a plain `docker compose -p <project> down` instead, put
the denial into **For the user**, and carry on.

Every lane brief carries this rule, and the lane acts on it in the same run.
Once a worktree's work is merged into the branch that ends its life, the lane
removes that worktree and every container, volume and image built for it.
That branch is `integration` when it is set, and `merge_into` when it is not.
The reason is that the Docker disk once reached 100%, and a lane's test
database failed with `No space left on device`.

Remove only what that lane built. Never run `docker volume prune` or
`docker system prune`, and never remove a shared test image or the primary
project. A lane merged only into `merge_into` keeps its worktree until that
branch reaches `integration`. For a lane's own resources this replaces any
"prune nothing" line in a brief.

## Test runs

A test run takes 2 workers by default, because several lanes run suites at
once. A session alone on the machine may use more.

A lane runs no suite until the merge. During the build, the per-task review,
phase 6 and phase 7 it runs only the test files it wrote or changed, named as
files. The suite runs once at phase 8, started by the orchestrator, with 2
workers. Two sessions never run a suite at the same time in one lane. A suite
per task cost 20 minutes and four cores each time, and three lanes at once
choked the machine.
