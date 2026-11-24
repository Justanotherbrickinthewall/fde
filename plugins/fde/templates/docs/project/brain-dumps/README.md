# Brain dumps

Purpose: everything heard about a delivery that has no home yet.
Done when: never. A delivery's dump grows until that delivery ships.

One file per delivery, `dN-<slug>.md`, matching the rows in
[`../deliveries.md`](../deliveries.md).

## Why this exists

Fifty conversations with a client produce fifty pockets of understanding and
one written wiki node. The gap between them is where the real shape of the
solution sits: the pain a coordinator mentioned in passing, the workaround
nobody documents, the thing that always goes wrong in week three.

The wiki cannot hold that, because a wiki claim needs a source and a tier
(guardrail 2). A brain dump has looser rules on purpose. It is the holding
pen between hearing something and knowing what it is.

## Rules

Append, never rewrite. An entry is dated and it stays. If a later
conversation contradicts it, add the later entry and say so; the wrong one
stays visible.

Every entry names where it came from. A person, a meeting, a call, a
document, or "the FDE's own read". An entry with no source is still allowed,
tagged `ours`, and it is weaker than one with a name on it.

A brain dump is never evidence. Nothing here outranks `wiki/`, and guardrail
7's tier order does not apply to it, because these are not claims yet. When
an entry hardens into a fact it moves to `wiki/` with a real source, and the
entry takes a note saying where it went.

A question raised here is mirrored into
[`../open-questions.md`](../open-questions.md) with an owner. This file is
not a question tracker.

Nothing here goes to the client. It holds half-formed reads of what they
said, and guardrail 4 covers anything they see.

## What reads them

`/fde:fdc-session` reads a delivery's dump before cutting or detailing the
milestones behind it. The dump is what tells you the shape of the solution;
the wiki only tells you the shape of the documents.

`/fde:prototype` reads it before building a demonstrator, because the pain
points in it are what the demonstrator has to answer.

## Entry shape

```markdown
### <date> — <source>

`<tag>` <the thought, in full sentences>

<optional: what it would change, or what it contradicts>
```

Tags, one per entry: `pain` for something that hurts today, `idea` for a way
it might work, `constraint` for something that cannot change, `fact` for
something stated that belongs in the wiki once sourced, `question` for
something nobody can answer yet.
