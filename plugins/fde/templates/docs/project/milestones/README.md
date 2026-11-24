# Milestones

Purpose: the vertical slices of the system, and what done means for each.
Done when: each milestone file says what done means before work starts.

One file per milestone, named `mNN-short-title.md`. No folders and no issue
files. [index.md](index.md) is the derived list of them.

## A milestone is a slice, not a deliverable

A milestone is a capability the system gains. A delivery is a date we
promised the client with a scope against it. They live in different files:
milestones here, deliveries in [`../deliveries.md`](../deliveries.md).

Mixing the two axes in one numbered list makes the plan unreadable. A
slipped slice then hides inside a renumber. It never shows up as a
threatened date. One file ends up carrying a platform build, a document
build and a pile of unasked client questions at once.

The test for a milestone: it is one reason to change. If a file has two,
cut it.

## No issue breakdown

Milestones do not break into issues here. A milestone's scope is prose in
the milestone file, and the plan that builds it is a separate document
written after the milestone is settled.

Counting issues measures the wrong work. A milestone's issue list fills up
with three different kinds of thing: client questions, our own fieldwork and
build tasks. They share one counter. So "0 of 10 done" means nothing anyone
can act on.

How the work runs instead. Pick a milestone and brainstorm it whole. Write
an implementation plan, build it in one pass, then walk it in a browser.
Whatever the browser shows comes back as a correction. The plan is the unit
of work and it lives with the session that builds it, in `my-sessions`,
never here.

Client questions belong in [`../open-questions.md`](../open-questions.md)
with a named owner. Our own fieldwork belongs in
[`../next-steps.md`](../next-steps.md). The artifact shapes a milestone may
need are in
[`../../setup/artifact-templates.md`](../../setup/artifact-templates.md),
and the rules behind all of this are in
[`../../setup/planning-rules.md`](../../setup/planning-rules.md).

## What a milestone file holds

Front matter carries `status` and `delivery`, and, where they exist,
`target` and `waits-on`. Status is one word, and a date may follow it.

`draft` means the FDC is still writing the milestone. `ready` means the
AIE may start it, and only the FDC sets `ready`. `building` means an AIE
session has it open. `built` means it is merged and walked. `dropped`
means we chose not to build it, and the file stays to say why.

`waits-on` names what the milestone depends on: a milestone id, a
delivery, or `none`. It is a field, not a status. A milestone can be
`draft` and wait on nothing, or `building` and still carry a `waits-on`
line describing what it once waited for. Ordering otherwise comes from
the dependency graph and history lives in git.

The body holds why now, in scope, out of scope, guardrails, what it rests
on, exit criteria, a walk-through and the risks. The record lint checks a
`ready` milestone for those parts, because `ready` is a promise the AIE can
start on.

The walk-through is the manual pass. It is a numbered list of what to click,
in order. Write it so someone can follow it without reading the rest of the
file. It is the gate today and the specification for a smoke test later.

Solo-pod convention: work state lives in the same file as the rationale.
Adopt a tracker when a second person joins the engagement, and not before.
