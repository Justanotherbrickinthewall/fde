# Gate 1: scoping to build

Purpose: decides whether a code space may be created.
Done when: every evidence cell holds a link and the footer is signed.

The evidence column accepts links only. "Done" or "yes" is invalid; if the
evidence is not a linkable artefact, the row is open and so is the gate.
Any gate is auditable by anyone at any time. The next gate is
[gate 2](gate-2-build-to-delivery.md), then
[gate 3](gate-3-delivery-to-done.md).

**Status: not tested. Scoping has not started.**

| Condition | Evidence (link) | Date |
|---|---|---|
| Scope ADR agreed with the client | | |
| Charter complete: every required row answered, success measure baselined | | |
| Every process step classified D, AI, A, H or X, with a reason per step | | |
| X-marked steps confirmed removable with the process owner | | |
| Exception paths written, not just the happy path | | |
| Every field the solution depends on has an authoritative source with a named owner and a working access path | | |
| Design names where the human stays in control | | |
| Design names how the system will be evaluated | | |

Signed by: — date: —

## Why this gate does not pass

Write one paragraph per failing condition. Say what kind of failure it is.
A sequencing problem clears with one meeting. A hole in the evidence does
not. A risk that should stop the build is a third thing again. They are not the same, and treating them
the same is how a gate gets waved through.

## What would clear it

List the moves, roughly in order of cost, and point each at the open
question or assumption it closes. Start the longest lead time first.

A build may open before this gate passes. It takes an ADR that says so,
names its bounds and sets a date to re-test the gate. That is an override
rather than a pass, and the failing rows stay failing.
