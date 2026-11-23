# Check: the mechanism

Covers the Mechanism and Reason columns of `wiki/process.md` § "Steps".

*Lifted from the `classify` skill on 07-09-26, when the six scoping skills
folded into `/fde:fdc-session`.*

This engagement's corrections live in `setup/scoping-rules.md` §
"Classification rules". Read them first; they override what is below.
Guardrails always apply, especially 3 (unknown is an open question) and 9
(architecture thoughts during scoping are drafts, clearly marked).

AI is not the default. Most useful systems are mostly deterministic, with
model reasoning at the edges where language and ambiguity live.

## Complete looks like

Every step row carries a mechanism and a reason.

Every `X` row has been put to the process owner as an open question, and is
marked unconfirmed until the answer comes back.

## Read state first

The Steps table needs two columns, giving this header:

```
| # | Trigger | Step | Decision | Data required | System | Human action | Output | Mechanism | Reason |
```

Existing rows keep their content and take two empty cells. Rows already
carrying a mechanism and a reason are not re-asked.

Where the process table is empty, stop. There is nothing to classify, and
`checks/process.md` comes first.

## The five letters

Offer them as choices, one row at a time, with the rule attached to each.

| Letter | Means | Choose it when |
|---|---|---|
| `D` | deterministic software | the rules are known, exactness matters, money or state changes, or someone must be authorised |
| `AI` | model reasoning or generation | the input is language, the classification resists encoding, or the reasoning is over something genuinely ambiguous |
| `A` | agent with tool use | the tools cannot be picked in advance, and selection is itself part of the problem |
| `H` | human | the consequence is high, or the judgement is organisational |
| `X` | remove the step entirely | the step exists because something else needed filling, and nothing downstream needs it |

## What to ask when it is not complete

### A reason is required

It is not optional prose. A step marked `AI` with no reason is a step nobody
has thought about, and this check will not write one for it.

### Challenge the expensive answers

Challenge `AI` where the rules look knowable. Challenge `A` where the tool
list is in fact short and fixed. Both are the expensive answer, and both get
chosen by habit.

### Record the shape as it emerges

A typical one runs: request, `AI` reads intent, `D` validates, `D` queries,
`D` calculates, `AI` explains, `H` approves, `D` acts. Say the shape out loud
when it appears, because it is the architecture.

### The X rows

`X` is the option people forget. A step that exists because a spreadsheet
needed filling can often be deleted rather than automated.

Removability is the process owner's call and never ours. Every `X` row writes
a row into `project/open-questions.md`, naming the process owner and asking
whether the step can go. The mechanism stays `X`, and the row is marked
unconfirmed until the answer comes back.

## What to report

Rows classified, the D/AI/A/H/X counts, any `AI` or `A` row whose reason
looks thin, and the `X` rows now waiting on the process owner.
