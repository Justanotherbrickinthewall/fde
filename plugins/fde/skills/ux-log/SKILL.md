---
name: ux-log
description: "Append an interface problem to project/ux-log.md as a dated, tagged, sourced entry, or mark an existing entry done. Use when the user says \"log a UX thing\", \"UX improvement\", \"record this UX finding\", invokes /fde:ux-log, or notices a screen problem mid-build that should not stop the work. Append only; never edits an entry and never writes a milestone."
---

# Log the UX finding

A UX finding must not stop the work it was found in. Widening a slice to fix
a screen is how a date slips. So it gets written down and the build carries
on.

Both the FDC and the AIE use this skill. An entry carries the hat of
whoever wrote it, after the source, for example `### 07-09-26 — the FDE's
own read, AIE`.

One file, `$REC/project/ux-log.md`. Read its header before writing; the rules in
that file override the steps below.

When `apps` is set, there is one UX log per app, so resolve the app first.
Take it from the command, or from the app whose screens the problem is on.
Ask once, in one line, where neither settles it, and never guess. With `apps`
empty, skip this.

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

## What this skill will not do

- Fix anything. It records and stops.
- Cut or edit a milestone. That is `/fde:fdc-session` and `/fde:aie-session`.
- Write `deliveries.md`. UX improvement is not a delivery, and the note at
  the head of `ux-log.md` says why.
- Edit an existing entry. A contradicted entry stays and the new one names it.
- Invent a source. An entry the user cannot attribute says so.

## Step 1 — check it belongs here

The log holds interface problems: a screen that confuses, a step that takes
too many clicks, something missing that a person expects.

Three things go elsewhere, so say which and stop.

1. A defect, where the code does not do what it says. That is a bug, and it
   goes to the session's `bugs-and-improvements.md` under `my-sessions/`.
2. A question only the client can answer. That is `open-questions.md`, with an
   owner and a `Blocks` value.
3. Something the client asked for that we do not build yet. That is a
   delivery matter and it goes to the brain dump for that delivery.

A finding can be both a UX problem and a question. Log it here and mirror the
question, then link the two.

## Step 2 — split and tag

Break what the user gave you into single thoughts. One entry, one thought. A
paragraph carrying three ideas becomes three entries.

Tag each one, exactly one tag. `pain` for something that hurts today, `idea`
for a way it might work. A pain and its proposed fix are two entries, because
the pain survives if we reject the fix.

Name the source on every entry: a person, a meeting, or "the FDE's own read".

Keep the user's own words where they carry the meaning. Where the words are
ambiguous, record the ambiguity in the entry rather than resolving it.

Present the split — tag, one-line summary — and **stop for the user's
go-ahead**.

## Step 3 — append

Add each approved entry under `## Entries`, newest last, in the shape the
file's header gives. Status is `open`. Never touch an entry already there.

## Marking one done

`/fde:ux-log done <what>` changes that entry's status to `done <date>` and
changes nothing else. The text stays exactly as written, including anything
it got wrong. If several entries match, list them and ask which.

## Step 4 — close the run

Report entries appended by tag, anything routed elsewhere and where it went,
and any question mirrored with its Q number.

Say whether the log is now worth acting on. Enough open entries means it is
time to cut a milestone carrying `delivery: none` and run `/fde:aie-session`.
That is the user's call, not this skill's.
