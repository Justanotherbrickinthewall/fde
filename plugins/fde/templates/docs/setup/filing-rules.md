---
extract_version: 1
lint_version: 1
---
# Filing rules

Purpose: this engagement's judgement about its own documents. What was
captured, what a section is, where it goes, and how it connects. Everything
`/fde:file` decides that the generic skill cannot decide for you.
Done when: never. Rules accrete from `/fde:file --investigate` walkthroughs.

The skill body is generic mechanism and the template owns it. This file is
the client's judgement, and a correction edits this file only. Rules here
override the skill's general steps.

This file is what `/fde:file --investigate` fills. Walk a document, correct
what you see, and the correction is written here as a dated rule. It is the
only way this file grows.

## The two sections, and which one a rule belongs in

A rule belongs in the cheap layer when it is about capture. A header that
should have been stripped, a table that resolves with different column
boundaries, a page range that was wrong.

A rule belongs in the expensive layer when it is about meaning or placement.
What a section is, where it goes, what it connects to.

Putting a judgement rule in the cheap layer breaks idempotency, which is the
one property that layer sells.

## The two version keys

The front matter carries both keys, and they invalidate different work.

`extract_version` is the cheap layer's cache key. Bump it when a cheap layer
rule below changes, and every source is captured again on the next run.
Capture is cheap, so bump freely.

`lint_version` is the expensive layer's cache key. Bump it when an expensive
layer rule changes, and every node goes stale in one line while capture stays
cold. A doctrine change becomes a re-run rather than a rebuild.

Keep them separate. One key for both would force a full re-capture every time
a filing opinion changed, which is the cost the split exists to avoid.

## How a rule is written

Each rule is dated with its provenance — `— 18-08-26, from investigate on
<source>`. Amend in place rather than deleting; the original reading stays
visible, because knowing a rule changed is worth more than a tidy file.

The headings below are the shape most engagements grow into. Empty ones are
not a gap; they are a question about whether this client has an opinion there
yet.

## Cheap layer — what was captured

What was captured, and what was dropped — never what it means.

(none yet)

## Expensive layer — what it means and where it goes

What an extracted section is, where it goes, and how it connects.

### Node identity and structure

(none yet)

### Authority and sourcing

(none yet)

### Entities and registers

(none yet)

### Links

(none yet)

### Samples and divergence

(none yet)
