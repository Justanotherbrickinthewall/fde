# Process

Purpose: what people actually do today, step by step, including what
happens when it goes wrong.
Done when: the exception paths are written, not just the happy path.

This node is `tier: ours` — our understanding of the work. A claim traced
to a raw artefact carries that artefact's tier in the Sources table below
instead.

Filled by `/fde:fdc-session`'s process check and annotated by its mechanism
check. Sourced like anything else in the wiki: cite the meeting or the file
and page, or tag `(assumption)` and mirror into
[`../project/open-questions.md`](../project/open-questions.md).

The verbal description is the idealised version. This table should come
from watching the work, from real examples and from the spreadsheets
people actually keep.

## Trigger

What starts the process, how it arrives, and roughly how often. Give the
tier, and a question id where the tier is `ours`.

## Steps

Number the steps against the client's own map of their work, so the two
read together. Do not renumber to suit us.

The mechanism column takes one of five letters. `D` is deterministic
software and `AI` is model reasoning. `A` is an agent with tools and `H` is
a person. `X` means the step should stop existing. Every letter needs a
written reason in the last column, and an `X` needs the process owner's
agreement.

| # | Trigger | Step | Decision | Data required | System | Human action | Output | Mechanism | Reason |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

## Shape

Count the letters and say what the shape means. How much of the process is
deterministic, and where the model work actually sits.

## Exceptions

Where the real architecture hides. Each prompt takes an answer or an
explicit "cannot happen, because …". A blank row is unfinished work, not
an absent exception.

| # | Exception | What happens today | How often |
|---|---|---|---|
| E1 | Data is missing | | |
| E2 | The request is invalid | | |
| E3 | Two systems disagree | | |
| E4 | A system is down | | |
| E5 | A human disagrees with the output | | |
| E6 | The answer is ambiguous | | |
| E7 | A value falls outside the normal range | | |

An exception with no frequency is not understood yet. One that fires in a
third of cases is the process, not an exception, and the design has to
carry it.

## Corrections

A dated note per correction. Name the source that outranked the claim, and
leave the original wording visible. A higher tier wins under guardrail 7,
and a same-tier contradiction is an open question rather than a judgement
call.

(none yet)

## Sources

| Claim | Source | Tier |
|---|---|---|
| | | |
