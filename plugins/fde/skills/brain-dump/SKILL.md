---
name: brain-dump
description: "Capture what was heard about a delivery into project/brain-dumps/dN-<slug>.md — split a conversation, a call transcript or a stream of thought into dated, tagged, sourced entries, append them without rewriting anything, and mirror any question into open-questions.md. Use when the user says \"brain dump\", \"dump this\", \"notes from the call\", invokes /fde:brain-dump, or hands over raw conversation notes about a delivery. Append only; never a wiki claim and never client-facing."
---

# Capture the brain dump

The holding pen between hearing something and knowing what it is. A wiki
claim needs a source and a tier (guardrail 2), so most of what a client says
in a meeting has nowhere to go. It goes here.

Both the FDC and the AIE use this skill. An entry carries the hat of
whoever wrote it, after the source, for example `### 07-09-26 — the FDE's
own read, AIE`.

One run can carry several dumps, and each one is handled by its own
subagent. Conventions are in `$REC/project/brain-dumps/README.md` and this
engagement's corrections are in `setup/planning-rules.md` § "Brain dump
rules" — read both first; those rules override the steps below.

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

- Write `$REC/wiki/`. An entry here is not a claim and never becomes one by being
  written down. Promotion to the wiki is a separate, deliberate act.
- Rewrite or delete an entry. Append only. A contradicted entry stays and the
  later entry says what it contradicts.
- Invent a source. An entry the user cannot attribute is tagged `ours` and
  says so. Guessing who said it is guardrail 2.
- Go to the client. Nothing in a brain dump is client-facing (guardrail 4).
- Answer a question. A `question` entry is mirrored to `open-questions.md`
  and left open.

## How a run works

The orchestrator does not process a dump. It resolves which delivery the
material belongs to, hands the dump to a subagent, and reports what came
back. One subagent per dump, dispatched together where several arrive at
once.

Everything else happens inside the subagent: reading the ground, splitting
the material, writing the entries, raising the questions. The orchestrator
writes no file.

The reason is that dumps arrive in a stream. The next one lands while the
last is still being written, and an orchestrator busy editing a file cannot
take it. Blocking the user mid-flow is the thing this shape avoids.

A subagent is given the dump verbatim, the delivery it belongs to, the file
it may write, and this skill. Never a summary of the dump. A summary is the
exact loss this skill exists to prevent.

## Asking, without waiting

Ask when a line is genuinely ambiguous and the record would otherwise carry a
guess. A dictated sentence that reads two ways is the common case, and so is
a name nobody can attribute.

Do not wait for the answer. The entry is written either way, with the raw
line quoted and a note saying it reads both ways and stays open until the
user settles it. A question asked is never a gate.

There is no go-ahead step anywhere in this skill. The user invoking it is the
go-ahead. Write the entries, then report what was written and what was asked.

## Write it full

An entry is closer to a transcript than to a wiki node, and the README says
so. Compressing a dump into one-line claims is the failure this skill sees
most often, and it is silent: the file looks tidy and the context is gone. A
milestone cut months later reads this file and cannot ask the client again.

Every entry carries four things.

1. The claim, in a sentence or two, straight after the tag.
2. The source's own words, quoted, wherever they carry the meaning.
3. The example they gave, in full, with its numbers.
4. What it would change, or why it matters, marked as the writer's reading
   rather than as the source's words.

A five-line dump becomes a fifteen-line entry, not a one-line row. Where an
entry touches a milestone, a wiki node, an earlier decision or another entry,
link it.

## Step 0 — resolve the app, then the delivery

One file per run, at `$REC/project/brain-dumps/dN-<slug>.md`.

Resolve the app first, and only when `apps` is set. Delivery numbers are per
app, so one app's d1 is not another's. With `apps` empty, skip this block and
start at the delivery.

- Take the app from the invocation, or from the material where it makes the
  app plain. Where one app is the only one whose deliveries table has rows,
  that is the app.
- Where none of that settles it, ask once, in one line. Never guess.
- If the material spans two apps, split it, one part per app, the way a dump
  spanning two deliveries is split. Say which entries went where.

Then resolve the delivery.

1. Named in the invocation, or the user names it. Check it against the rows
   in `$REC/project/deliveries.md`.
2. If the material spans two deliveries, split it and say which entries went
   where. Never write one entry into two files; pick the delivery it most
   affects and cross-reference the other.
3. If it belongs to no delivery — a platform capability, a role, a way of
   working — it still gets written. Put it in the delivery it most affects
   and say inside the entry that it serves no single delivery. Never open a
   dump outside the `dN` set, and never refuse the material. A dump that
   reaches no file is lost, and that is worse than a dump filed one row off.

## Step 1 — read the ground

1. The delivery's own row and section in `$REC/project/deliveries.md`.
2. The existing entries in the dump. A new entry that repeats one already
   there is not appended; it is noted as a second hearing on the original.
3. The milestone or milestones behind the delivery, for what is already
   scoped.
4. `open-questions.md`, so a question already tracked is not raised twice.

## Step 2 — split the material

Break what the user gave you into single thoughts. One entry, one thought.
A paragraph carrying three ideas becomes three entries.

Tag each one, exactly one tag:

| Tag | Means | Where it ends up |
|---|---|---|
| `pain` | Something that hurts today | The demonstrator has to answer it |
| `idea` | A way it might work | Feeds the milestone cut |
| `constraint` | Something that cannot change | Feeds scope and the guardrails |
| `fact` | Something stated that belongs in the wiki once sourced | Flagged for promotion |
| `question` | Nobody can answer it yet | Mirrored to `open-questions.md` |

Name the source on every entry: a person, a meeting, a call, a document, or
"the FDE's own read". Keep the user's own words where they carry the meaning;
this file is closer to a transcript than to a wiki node.

Write the split straight into the file. There is no approval step. The
report comes afterwards, in step 4, and it names the line numbers so the user
reviews what was written rather than authorises what was not.

## Step 3 — apply

1. Append approved entries under `## Entries`, newest last, in the shape the
   README gives. Never touch an existing entry.
2. A `fact` entry gets a line naming the wiki node it would belong to, or
   saying no node exists yet.
3. A `question` entry gets a new row in `open-questions.md` with an owner and
   a `Blocks` value, and the entry links to its Q number. If the question is
   already tracked, link the existing row instead of adding one.
4. An entry that contradicts an earlier one names it and says how.

## Step 4 — close the run

Report: entries appended by tag, with the line numbers each one landed on,
questions mirrored with their new Q numbers, questions put to the user and
left open, facts flagged for promotion to `$REC/wiki/`, and anything that belonged
to a different delivery.

The line numbers are the point of the report. They are what makes the write
reviewable after the fact, which is what replaced the go-ahead.

Say plainly whether any entry changes the shape of a milestone already cut.
That is `/fde:fdc-session`'s decision to make, not this skill's, but it should not
have to discover it.

## Rules

- Append only, always. The file is a record of what was heard and when, and a
  rewritten record is worth nothing.
- Never write `$REC/wiki/`, `plan-ledger.md`, a milestone file or `deliveries.md`.
  `open-questions.md` is the one file outside `brain-dumps/` this skill
  touches.
- A brain dump never outranks the wiki. Guardrail 7's tier order does not
  apply here, because these are not claims yet.
- Write first, report second. There is no go-ahead, and a question never
  holds up a write.
- Never compress. An entry that drops the example, the quote or the reason is
  a failed entry, however tidy it reads.
