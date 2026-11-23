# Method packs

A pack is one way of getting from whatever arrived to a record that reflects
it. It owns phases 2, 3, 4 and 5 of `/fde:fdc-session` and nothing else.

One exists. `grill.md` is the default, so `/fde:fdc-session` runs it with nothing
typed. Nobody types `--grill`, though the flag works and means the same as
omitting it. A second pack is a second file here with its own `--<name>`
flag. `SKILL.md` does not change when one is added.

If the default ever moves off `grill`, change it in `SKILL.md`'s Invocation
section. That sentence is the only place the default is named.

## Why this is a separate file

The way we scope will change. The way a session is scaffolded, read, linted
and closed will not. Keeping them apart means swapping the scoping method
costs one file.

The pack is also where a foreign skill gets translated. `grill` is modelled
on the superpowers `brainstorming` skill, which has its own vocabulary and
its own default paths. The pack carries that translation, so the foreign
skill runs unmodified and `SKILL.md` never learns a word of it.

## The contract

A pack is handed four things. It may rely on all of them.

1. The session folder path. `sessions.py new` chooses it.
2. `notes.md`, written, with what arrived and the state of the record
   recorded.
3. `<docs>` on `main`, clean and pulled.
4. The checks in its own `checks/` folder, current. They are what tell it
   what a hole is.

A pack must do five things.

1. **Write `digest.md` into the session folder**, where something arrived.
   Not into a default location of its own. Every artefact of this session
   lives in one folder.
2. **Stop at each gate.** You read the split before the grill starts. You
   read the change before it reaches the record.
3. **Keep `Phase:` current** in `notes.md` through all four phases.
4. **Write every record change through a subagent.** The orchestrator holds
   the conversation and dispatches. It does not edit `<docs>` inline.
5. **Report back.** Either the update is done, or it is blocked and why.
   `/fde:fdc-session` resumes at phase 6.

## Two invariants no pack may break

**Nothing reaches the record before phase 5.** The digest and the
confirmation exist so the split is visible before it lands. A pack that
writes to `wiki/` during the grill has failed the contract.

**Never guess.** An unknown leaves the row open and writes an open question
with a named owner. That is guardrail 3, and a lighter method is a lighter
method rather than a different ideology.

A pack must not do four things.

1. **Touch the code repositories.** `<be>` and `<fe>` belong to
   the AIE. An FDC session never opens a branch there.
2. **Set a milestone to `building` or `built`.** Those are `/fde:aie-session`'s.
   The FDC sets `draft`, `ready` and `dropped`.
3. **Run the record lint.** That is phase 6, and it belongs to `SKILL.md`.
4. **Write a session record into `<docs>`.** The record never links to
   `my-sessions`.

## Writing one

Name it after the method, lowercase: `socratic.md` is selected by
`--socratic`. Say which skills or commands it invokes, in order, and where
each gate sits. Say what it reads to know what a hole is, because `grill`
reads `grill/checks/` and another pack may not. Say what it overrides in the
skills it calls, and why. If it overrides nothing, say that too.
