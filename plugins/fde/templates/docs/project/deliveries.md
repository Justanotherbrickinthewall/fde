# Deliveries

Purpose: the dates we promised the client, and what each one needs.
Done when: never. This file changes when the schedule changes.

A milestone is a vertical slice of the system and it is ours. A delivery is
a date and a page count, and it is the client's. Mixing them in one
numbered list is what makes a plan hard to read. A slipped slice then hides
inside a renumber, and never shows up as a threatened date.

Name the schedule this table comes from, and give it a tier.

| # | Date | Deliverable | Pages | Built by | Brain dump | Prototype | State |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

Every delivery ends with a named client person approving it. That is a
client guardrail, and it is not repeated in each row.

## The four things a delivery carries

A delivery row points at four things and each answers a different question.

**Milestones** answer how it gets built. They are in
[`milestones/`](milestones/README.md), one file per vertical slice, and a
milestone names the delivery it serves in its front matter. One milestone
can serve several deliveries.

**The brain dump** answers what we have heard. One file per delivery in
[`brain-dumps/`](brain-dumps/README.md), appended after every conversation
that touches it. The wiki holds the shape of the documents; the brain dump
holds the shape of the problem, and the two are not the same thing.
`/fde:fdc-session` reads a delivery's dump before cutting or detailing the
milestones behind it.

**The prototype** answers what it should feel like. It attaches to a
delivery and not to a milestone, because a delivery is what the client
recognises. One delivery may have several prototypes or none, and a
prototype may span several milestones. Prototypes obey
[`../setup/design.md`](../setup/design.md), the same design language the
application uses.

**The pages and the date** answer what the client was promised. They are
theirs, not ours, and they change only when the client changes them.

## What each delivery is made of

One section per delivery, added as the schedule is agreed. Each says what
the delivery contains, which questions stand behind it, and what is not
settled about it.
