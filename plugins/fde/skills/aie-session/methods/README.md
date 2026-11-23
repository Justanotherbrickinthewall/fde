# Method packs

A pack is one way of getting from a settled scope to working code. It owns
phases 3, 4 and 5 of `/fde:aie-session` and nothing else.

Two exist. `superpowers.md` is the default, so `/fde:aie-session` runs it with
nothing typed. `quick.md` is the lighter one, selected by `--quick`. A third
pack is a third file here with its own `--<name>` flag. `SKILL.md` does not
change when one is added.

If the default ever moves off superpowers, change it in `SKILL.md`'s
Invocation section. That sentence is the only place the default is named.

## Why this is a separate file

The way we build will change. The way a session is scaffolded, scoped,
reconciled, walked, fixed and closed will not. Keeping them apart means
swapping the build method costs one file.

Each pack also translates. Superpowers has its own vocabulary and its own
default paths, and this engagement has different ones. The pack is where that
translation is written down, so the foreign skill runs unmodified and
`SKILL.md` never learns a word of it.

## The contract

A pack is handed five things. It may rely on all of them.

1. The session folder path. `sessions.py new` chooses it.
2. `notes.md`, written, with the scope agreed and recorded.
3. The milestone id and its file path.
4. `<docs>` on `main`, clean and pushed, and the session folder present
   in `my-sessions`.
5. For its build stage only: a branch in each code repository the milestone
   touches, cut and green. The orchestrator opens them. The pack does not.

A pack must do five things.

1. **Write `spec.md` into the session folder.** Not into the method's own
   default location. Every artefact of this session lives in one folder.
2. **Write `plan.md` into the session folder.** Same rule.
3. **Stop at each gate.** The user reads the spec before a plan is written.
   The user reads the plan before code is written. A pack that runs design
   straight into implementation has failed the contract.
4. **Keep `Phase:` current** in `notes.md` through all three phases.
5. **Report back.** Either the build is done, or it is blocked and why.
   `/fde:aie-session` resumes at phase 6.

## Two invariants no pack may break

**Never build inline.** Every task goes to its own subagent, in every pack.
Design and plan already cost on the order of 200k tokens in the main session,
and implementing on top of that pushes it past half a million, where every
later judgement gets worse. A pack may change how many subagents it spends
per task. It may not spend none.

**The pack does not choose where the work lands.** Phases 0 to 4 write to
`<docs>`, phase 5 writes to `<be>` and `<fe>`, and phases 6
to 8 come back to `<docs>`. That holds whether the build takes forty
minutes or nine hours. A lighter method is a lighter method, and not a
different ideology.

## Who runs which tests

An implementer subagent runs the tests for the files it touched, and commits
on those. It does not run the full suite. It can only break what it touched,
and a targeted run costs seconds where the full suite costs a minute or more.

The orchestrator runs the full suite once per track. Run it when a set of
parallel tasks lands, and again before phase 6. That is the first moment
cross-task interference can exist, so it is the first moment worth looking
for it.

Measured on one fix run: seven agents each ran the full suite at least once
and several ran it three or four times, over twenty runs at about 68
seconds, nearly all of it re-proving untouched code. Three of those agents
ran it concurrently against one test database and dropped the schema under
each other, so those runs proved nothing at all.

If something distant breaks, it surfaces at the track boundary and costs a
bisect across two or three commits. That is cheaper than the insurance.

## What an implementer may never run

`git stash`, `git checkout .`, `git reset --hard`, and anything else that
discards a working tree. Put this in every brief.

An agent once ran `git stash` to check whether a test failure pre-dated its
own change. The tree was shared, so it took two other agents'
in-progress work and an uncommitted findings file with it. All of it was
recovered, none of it by design.

To compare against `HEAD`, use `git diff`, or copy a file aside with `cp`.

## Who writes the findings file back

Whoever closes a finding writes its row. Where agents run in parallel and
share one findings file, they are told to leave it alone so they do not
collide — and then the orchestrator writes every row at the track boundary,
in the same pass as the full suite.

Both halves are the rule. Telling agents not to touch it and stopping there
is how a findings file spends a whole run saying nothing has been done.

It has happened. Twenty-two findings were fixed and committed while the
table still read `open` for all of them, and a person found it rather than
the process.

A closed row names the commit that closed it, not just a date. `fixed
07-09-26 (114c106)` survives being read three weeks later; `fixed
07-09-26` does not. Where the write-up happens after the fact rather than
as each fix lands, say so at the head of the file, because the dates then
mean when the work landed rather than when the row was ticked.

A finding routed somewhere else is not `fixed`. A constraint that governed
the work reads `carried`. A scope call reads `decided`. A defect nobody
reproduced stays `open` and says why, and is never closed on a guess.

A pack must not do four things.

1. **Reopen the scope.** If the design uncovers a scope problem, hand back to
   phase 2. Do not decide it inside the pack.
2. **Open, switch or remove a branch or a worktree.** The orchestrator owns
   those, because it knows what the other sessions hold. A pack that calls
   `EnterWorktree` or `git worktree add` has failed the contract.
3. **Merge, walk or close the branch.** Those are phases 5's tail, 6, 7
   and 8.
4. **Write to the engagement record.** `$REC/wiki/`, `$REC/project/` and `setup/`
   in `<docs>` belong to phases 2 and 8. A pack that discovers a client
   question writes it into `notes.md` under Open questions, and phase 8
   promotes it.

## Writing one

Name it after the method, lowercase: `matt-pocock.md` is selected by
`--matt-pocock`. Say which skills or commands it invokes, in order, and where
each gate sits. Say which of its three phases write to `<docs>` and which
write to the code repositories. Say what it overrides in those skills, and why.
If it overrides nothing, say that too.
