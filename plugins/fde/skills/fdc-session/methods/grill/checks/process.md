# Check: the process

Covers `wiki/process.md`.

*Lifted from the `map-work` skill on 07-09-26, when the six scoping skills
folded into `/fde:fdc-session`.*

This engagement's corrections live in `setup/scoping-rules.md` § "Process
rules". Read them first; they override what is below. Guardrails always
apply, especially 2 (no unsourced facts in the wiki) and 3 (unknown is an
open question).

Do not only ask what they want built. Ask them to show you the work.

## Complete looks like

Every exception prompt has an answer, or a stated reason it cannot fire.

The step rows describe what people actually do today, not the idealised
version. The verbal description is always the idealised version, and the
table should come from watching the work, from real examples and from the
spreadsheets people actually keep.

The trigger is named, with a frequency.

## Read state first

Parse `wiki/process.md`. Count filled step rows and answered exception
prompts. Report both, and ask only for what is blank.

Where `raw/ledger.md` marks material unfiled, say so. The process may already
be written down somewhere nobody has read.

## What to ask when it is not complete

### The trigger

What starts this process, and how often.

A process with two triggers is two processes. Splitting them here saves an
argument when the steps are classified.

### The steps

One row at a time, in order. For each row, six things: what happens, what
decision is made, what data is needed, which system holds it, what the human
does, what comes out.

Push back on a step described as a single verb where a system is involved.
"They check the claim" is three steps and a decision.

Ask where each answer came from, and record it in the Sources table with its
tier. An answer that comes from our own inference is `ours` and belongs in
`project/open-questions.md` too.

### The seven exception prompts

Asked one at a time, none skipped. This is the part the check exists for,
because nobody volunteers the exceptions.

| # | Prompt |
|---|---|
| E1 | Data is missing |
| E2 | The request is invalid |
| E3 | Two systems disagree |
| E4 | A system is down |
| E5 | A human disagrees with the output |
| E6 | The answer is ambiguous |
| E7 | A value falls outside the normal range |

For each: what happens today, and how often it fires.

Frequency matters more than people expect. An exception that fires in a third
of cases is the process, not an exception, and it belongs in the Steps table.

An answer of "that cannot happen" is accepted only with a reason, and the
reason is recorded. "It has never happened" is not the same as "it cannot
happen", and the difference is worth saying out loud.

Where a prompt does not apply to this client, that judgement goes into
`setup/scoping-rules.md` § "Process rules", not into a blank row.

A blank row is unfinished work, not an absent exception.

### Where the exceptions decide the design

E3 and E5 are usually the same hole seen twice: somebody resolves conflicts
and rejects drafts on judgement that exists nowhere in writing. An agent
cannot inherit an unwritten rule, and there is no record of past calls to
learn from. Capturing that decision is design work, and it belongs in an ADR
through `checks/design.md`.

E1's assumed-value path is the risk an agent scales. A human assumes a figure
a few times per report and remembers to flag it. A system that does the same
across every field, on every project, produces a report nobody can audit. The
flag has to be structural.

## Template

```markdown
# Process

Purpose: what people actually do today, step by step, including what happens
when it goes wrong.
Done when: the exception paths are written, not just the happy path.

## Trigger

<what starts it, and how often> `<tier>` (<source>)

## Steps

| # | Trigger | Step | Decision | Data required | System | Human action | Output | Mechanism | Reason |
|---|---|---|---|---|---|---|---|---|---|

## Exceptions

Each prompt takes an answer or an explicit "cannot happen, because …".

| # | Exception | What happens today | How often |
|---|---|---|---|
| E1 | Data is missing | | |
| E2 | The request is invalid | | |
| E3 | Two systems disagree | | |
| E4 | A system is down | | |
| E5 | A human disagrees with the output | | |
| E6 | The answer is ambiguous | | |
| E7 | A value falls outside the normal range | | |

## Sources

| Claim | Source | Tier |
|---|---|---|
```

The Mechanism and Reason columns are filled against `checks/mechanism.md`.
They stay empty until the steps are captured.

## What to report

Steps captured, exception prompts answered, sources still untiered, and
questions raised.
