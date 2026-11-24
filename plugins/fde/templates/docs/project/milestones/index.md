# Milestones

Derived view. One row per milestone file, in dependency order. Regenerate
rather than edit.

A milestone is a vertical slice of the system. The dates promised to the
client are in [`../deliveries.md`](../deliveries.md). Why the two lists are
separate is in [README.md](README.md).

Status is one of five words: `draft`, `ready`, `building`, `built` or
`dropped`, each defined in [README.md](README.md). Only the FDC sets
`ready`. `Waits on` names what a milestone depends on: a milestone id, a
delivery, or `none`.

The assertion column carries a claim, not a topic. "Sign-in and users" is
not an assertion; "a person signs in and a super admin adds people" is.

| # | Assertion | Status | Waits on | Delivery |
|---|---|---|---|---|
| [m01](m01-sign-in-and-the-shell.md) | A person signs in, sees an empty project list, and a super admin adds people and creates projects | **built** 07-09-26 | none | none |

## What is true today

m01 ships with the template. It is built, walked and merged, and it is the
only milestone that exists.

Nothing else is cut. The first `/fde:fdc-session` reads what arrived, fills the
[charter](../charter.md), and cuts the next milestone from it. A milestone is not `ready`
until the FDC says so, and `/fde:aie-session` refuses one that is not.
