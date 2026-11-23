# Method pack: superpowers

The default pack. It runs unless a `--<method>` flag names another one, so
nobody types `--superpowers`. Owns phases 3, 4 and 5 of
`/fde:aie-session`: design, plan, build.

Three superpowers skills run in order, with a human gate between each. They
run unmodified. Everything this engagement does differently is an override
stated here and announced to the skill before it starts.

| Phase | Skill | Writes to | Produces | Gate |
|---|---|---|---|---|
| 3 Design | `brainstorming` | `<docs>` | `spec.md` | the user approves the spec |
| 4 Plan | `writing-plans` | `<docs>` | `plan.md` | the user approves the plan |
| 5 Build | `subagent-driven-development` | the code repositories | commits | none, it runs to the end |

The work moves to the code repositories between phase 4 and phase 5, and
`/fde:aie-session` makes that move. This pack starts phase 5 with the branches
already cut and already green. It never opens a branch and never runs
`git worktree`.

## What this pack overrides

**Where the spec goes.** `brainstorming` saves to
`docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`. Here it saves to
`<session>/spec.md`. This repository has no `docs/` directory and is not
getting one: a session folder already collects everything about one piece of
work, and splitting the spec away from the notes is how a spec gets orphaned.

**Where the plan goes.** `writing-plans` saves to
`docs/superpowers/plans/YYYY-MM-DD-<feature>.md`. Here it saves to
`<session>/plan.md`. That skill already says user preferences override its
default, so state the preference before invoking it.

**Which execution route.** `writing-plans` ends by offering subagent-driven
or inline. Always answer subagent-driven. Inline execution burns the
coordinating context on implementation detail, and these plans run sixteen
tasks.

**Where the workspace comes from.** `writing-plans` and
`subagent-driven-development` both expect `using-git-worktrees` to have run.
It has not, and it must not. `/fde:aie-session` cuts the branches itself between
phases 4 and 5. Where two builds share one repository it also makes a worktree,
using `lanes.md`, which knows the two things a fresh worktree does not have.
Tell both skills the workspace already exists and give them its path.

Nothing else is overridden. Do not rewrite the skills' own questions, their
gates or their review loops.

## Phase 3 — Design

Set `Phase: 3 design`. Writes to `<docs>`, on `main`.

Announce the overrides, then invoke `brainstorming`.

Two things to feed it that it will not find on its own.

The scope, as agreed in phase 2. Paste the **Scope, in plain words** section
from `notes.md` and name the milestone file. The skill's first checklist item
is exploring project context, and this is the context that matters most.

The evidence this milestone rests on. Name the wiki nodes, the brain dump for
its delivery, and any open question it waits on. A design that quietly
assumes an answer to an unasked question is the failure mode this engagement
keeps hitting, and guardrail 15 forbids inventing the value later. Where a
question is open, the design says the field renders as a gap.

The skill runs its own loop: questions one at a time, two or three
approaches, then the design in sections. Let it. Do not shortcut to a
finished design because the milestone file looks complete.

When it writes the spec, it writes `<session>/spec.md` with this front
matter:

```yaml
---
kind: build-spec
status: draft
milestone: <id>
date: <DD-MM-YY>
---
```

**Gate.** The user reads `spec.md`. They will ask for changes. Make them,
show what moved, ask again. When they approve, set `status: approved` and
name them and the date in the first paragraph, the way every approved spec
under `my-sessions/<session>/spec.md` does.

If a change here turns out to be a scope change rather than a design change,
stop. Hand back to phase 2, get the milestone edited, then come back. The
test is simple: if the milestone file would now be wrong, it is a scope
change.

## Phase 4 — Plan

Set `Phase: 4 plan`. Writes to `<docs>`, on `main`.

`brainstorming` ends by invoking `writing-plans`. Let it. Before it starts,
restate the plan path and the fact that the workspace already exists.

The plan opens by naming its spec, and says the spec wins where the two
disagree. Front matter:

```yaml
---
kind: implementation plan
status: draft
milestone: <id>
date: <DD-MM-YY>
---
```

Global constraints for this engagement, which every plan here carries:

- The backend runs in Docker. There is no host Python and no virtual
  environment. `docker compose --profile tools run --rm test` in `<be>`
  is its suite, and `just test` from the umbrella runs both suites.
- The frontend runs on pnpm and Vitest. `pnpm -r test` is its suite.
- An implementer runs only the tests for the files it touched. The full suite
  is the orchestrator's, once per track. See `methods/README.md`.
- Tests need a database whose name ends `_test`. The suite refuses any other.
- Tailwind utilities only. Every design value is a token in
  `packages/ui/tailwind.config.ts`. Utility strings are written only in
  `packages/ui/src/components/`.
- No application code reads the `<docs>` record at runtime.
- A missing fact renders as a gap and is never invented. Guardrail 15.

**Gate.** The user reads `plan.md`. Changes, then re-read, then approval. Set
`status: ready`, commit and push. The spec and the plan are on the remote
before any code is written, so the build branches off something everyone can
see.

Then check the context. This is the 4 to 5 boundary, and it is the largest
one in the whole session: everything the design conversation produced is now
on disk. `SKILL.md`'s "Context, and where to shed it" says what to do at
which threshold, and carries the `/compact` instruction that keeps the
rejected approaches.

This gate is the expensive one to skip. The build after it runs for hours
without stopping, so a wrong task boundary here costs the whole run.

## Phase 5 — Build

Set `Phase: 5 build`. Writes to the code repositories, on the branch named for
the milestone. `/fde:aie-session` has already cut it and proved each suite
green.

`writing-plans` offers the execution choice. Answer subagent-driven. Invoke
`subagent-driven-development`.

It runs to the end without checking in. That is its design and it is correct
here: the user is walking another branch or planning another milestone while
it runs. It stops only when it is blocked, ambiguous or done.

Its working files land in `.superpowers/sdd/`, which is gitignored and lives
in whichever tree the build runs in. Per-tree, so two builds never collide.

Before dispatching task 1, give it the spec path, the plan path, the session
folder, and the global constraints above.

Its final whole-branch review finds things a browser cannot show. Those
findings go into `<session>/bugs-and-improvements.md`, the same file phase 6
writes, so the fix session reads one list. Take the next free number, read
the file immediately before every write because phase 6 may share it, and
never renumber a published entry. That review usually contributes a fifth
or so of a walk's findings, and they are the ones a browser could not show.

When it finishes it runs `finishing-a-development-branch`. Stop there. Do not
let it merge and do not let it remove the tree. `/fde:aie-session` pushes the
branch and leaves it checked out for the walk. The branch merges once, at
phase 8, after the walk and the fixes.

## Reporting back

Write into `notes.md`: the tasks that ran, what the final review found, and
anything left unfinished. Set `Phase: 6 walk`. Then `/fde:aie-session` brings the
stack up and walks it in a browser.

If the build blocked, say which task, what it was waiting on, and what you
tried. Set `Status: paused`, start `Owes:` with `blocked`, and put the one unblocking action in
**▶ Resume here**.
