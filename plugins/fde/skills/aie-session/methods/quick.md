# Method pack: quick

Selected by `--quick`. Owns phases 3, 4 and 5 of `/fde:aie-session`, the same
three as `superpowers`.

Use it when the milestone is settled and ordinary. It cuts the ceremony in
front of the build, and nothing else. Same repositories, same branch, same
never-inline rule, same walk afterwards.

| Phase | Mechanism | Writes to | Produces |
|---|---|---|---|
| 3 Design | Claude plan mode | `<docs>` | no spec |
| 4 Plan | the approved plan, written out | `<docs>` | `plan.md` |
| 5 Build | one implementer subagent per task | the code repositories | commits |

## What it is not

**It is not an inline build.** Every task goes to its own subagent, exactly
as `superpowers` does. The orchestrator dispatches, records and moves on; it
never writes the code itself.

The reason is context, not taste. Design and plan already cost on the order
of 200k tokens in the main session. Implementing on top of that pushes it
past half a million, and the quality of every judgement made after that point
falls. The main session's context is the scarce resource on this engagement
and the whole point of a subagent is to spend somebody else's.

**It does not change where the work lands.** Phases 0 to 4 write to
`<docs>`, phase 5 writes to the code repositories, and phases 6 to 8 come
back to `<docs>`. That is the same for every pack, and a pack does not get
a vote. `/fde:aie-session` cuts the branches before this pack's phase 5 starts.

## What it actually saves

Against `superpowers`, three things go.

The spec document. `brainstorming` writes `spec.md`, holds a two-or-three
approaches conversation, and takes approval section by section. Where the
approach is obvious, that is a round trip that changes nothing.

The verbose plan. `writing-plans` writes for an engineer with zero context
and questionable taste. That is right for sixteen tasks and wrong for four.

The per-task review. `subagent-driven-development` runs a reviewer subagent
after every task, then a fix subagent for its findings, then a re-review.
That is two or three subagents per task. This pack runs one, and reviews once
at the end over the whole branch.

The subagent count roughly thirds. The isolation does not change.

## When to use `superpowers` instead

Hand back when any of these is true, because per-task review earns its keep
where a bad task landing silently is expensive.

- The plan includes a migration.
- The plan builds a mechanism later milestones sit on.
- The milestone waits on an unanswered question, so the design has real
  choices in it rather than one obvious road.
- Plan mode comes back with more than about six tasks.

Say which condition fired, and stop. Picking the wrong pack should cost one
conversation, never a bad build.

## Phase 3 and 4 — Plan mode

Set `Phase: 3 design`. Writes to `<docs>`, on `main`.

Call `EnterPlanMode`. Research the codebase, then propose the plan. Feed it
three things it will not find on its own.

The scope, as agreed in phase 2. Paste **Scope, in plain words** from
`notes.md` and name the milestone file.

The evidence the milestone rests on. Name the wiki nodes and any open
question it waits on. Guardrail 15 forbids inventing a value later, so
where a question is open the plan says the field renders as a gap.

The global constraints below.

Use `AskUserQuestion` where a genuine choice exists. Do not use it to ask
whether the plan is good; `ExitPlanMode` is what asks that.

Write the plan to `<session>/plan.md` rather than leaving it in the plan
file, with this front matter:

```yaml
---
kind: implementation plan
status: draft
milestone: <id>
method: quick
date: <DD-MM-YY>
---
```

Each task needs the same four things `superpowers` plans carry, because a
subagent with no context has to execute it: exact files to create and modify,
what it consumes from earlier tasks, the test that proves it, and the commit.
Shorter prose is the saving. Missing detail is not.

Then `ExitPlanMode`. Set `Phase: 4 plan`.

**Gate.** The user reads `plan.md`. Changes, re-read, approval. Set
`status: ready`, commit and push. The plan is on the remote before any code
is written.

Then check the context. This is the 4 to 5 boundary, and everything plan mode
produced is now on disk. `SKILL.md`'s "Context, and where to shed it" says
what to do at which threshold. Plan mode's research is the expensive half
here, so this boundary matters even in the lighter pack.

## Global constraints

Every plan on this engagement carries these, and every subagent is given
them:

- The backend runs in Docker. There is no host Python and no virtual
  environment. `docker compose --profile tools run --rm test` in `<be>`
  is its suite, and `just test` from the umbrella runs both suites.
- The frontend runs on pnpm and Vitest. `pnpm -r test` is its suite.
- Tests need a database whose name ends `_test`. The suite refuses any other.
- Tailwind utilities only. Every design value is a token in
  `packages/ui/tailwind.config.ts`. Utility strings are written only in
  `packages/ui/src/components/`.
- No application code reads the `<docs>` record at runtime.
- A missing fact renders as a gap and is never invented. Guardrail 15.

## Phase 5 — Build

Set `Phase: 5 build`. Writes to the code repositories, on the branch named for
the milestone. `/fde:aie-session` has already cut it and proved each suite
green.

Read `plan.md` and make a todo per task. Then, for each task in order:

1. Dispatch one implementer subagent. Give it the task verbatim, the global
   constraints, the paths of `plan.md` and the session folder, and the
   interfaces the earlier tasks produced. Tell it to implement, run the
   tests for the files it touched, and commit. Not the full suite; that is
   the orchestrator's, once per track.
2. When it reports, record the task as done in the progress ledger and move
   to the next one. Do not read the diff and do not review it here.
3. If a subagent reports blocked, stop and say which task and what it was
   waiting on. Do not work around it yourself.

Run continuously. Do not check in with the user between tasks; they are
walking another branch or planning another milestone while this runs.

When every task is done:

4. Run the full suite once over the whole branch. It must be green. This is
   the orchestrator's run and the first one in this phase.
5. Dispatch one reviewer subagent over the full `main...<branch>` diff, for
   correctness and for spec compliance against `plan.md`.
6. Dispatch fix subagents for what it finds. Re-run the suite.

That final review is the only review in this pack, so it is not optional and
it is not skimmed.

What it finds goes into `<session>/bugs-and-improvements.md`, the same file
phase 6 writes, so the fix session reads one list. Take the next free number,
read the file immediately before every write because phase 6 may share it,
and never renumber a published entry.

## Reporting back

Write into `notes.md`: the tasks that ran, what the final review found, and
anything left unfinished. Set `Phase: 6 walk`.

`/fde:aie-session` pushes the branch, leaves it checked out, and walks the result
in a browser. Do not merge and do not remove the tree; the branch merges once,
at phase 8.

If the build blocked, say which task, what it was waiting on, and what you
tried. Set `Status: paused`, start `Owes:` with `blocked`, and put the one unblocking action in
**▶ Resume here**.
