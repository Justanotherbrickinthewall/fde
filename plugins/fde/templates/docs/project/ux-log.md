# UX log

Purpose: every interface problem we notice while building, kept in one place
until someone picks it up.
Done when: never. It fills as we build and empties as we fix.

A delivery is what the client asked for, and the client never asks for good
UX as a separate item. They assume it in everything we hand over. So UX
findings live here rather than in [`deliveries.md`](deliveries.md).

## How it works

Notice it, write it here, carry on. The whole point is that a UX finding
does not stop the work it was found in. Widening a slice to fix a screen is
how a date slips.

`/fde:ux-log` writes the entry. `/fde:ux-log done <what>` closes one.

When enough has piled up, cut a milestone for it and run `/fde:aie-session`.
The milestone carries `delivery: none`, because it serves every delivery
rather than one. Pick the entries still marked `open` and close them in
that session.

This is the one place a UX finding goes to outlive the session that found
it. `/fde:smoke-test` writes its findings to a `bugs-and-improvements.md`
under `my-sessions/`, and that file dies with its session. So anything in it
that is UX and unfixed gets copied here.

## Rules

Append only. An entry stays once written, and a later entry that
contradicts it says so. A fixed entry has its status changed to `done` with
a date, and its text is never edited.

This is not a brain dump. Brain dumps are one per delivery, by the rule in
[`brain-dumps/README.md`](brain-dumps/README.md), and UX is not a delivery.

This is not `wiki/` and it is not evidence. Nothing here is a claim.

Nothing here goes to the client.

## Entry shape

```markdown
### <date> — <source>

`<tag>` `<status>` <the thought, in full sentences>
```

Tags: `pain` for something that hurts today, `idea` for a way it might work.
Status is `open` or `done <date>`.

## Entries
