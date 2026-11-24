# Planning rules

Purpose: this engagement's corrections to how the plan is derived from
the wiki. One section per skill; each skill reads only its own.
Done when: never. Rules accrete from corrections you give in a run.

The skill bodies are generic mechanism and the template owns them. This
file is the client's judgement, and rules here override the skills'
general steps.

Each rule is dated with its provenance. Amend in place rather than
deleting; the original reading stays visible.

There is no version key here. Planning output is reconciled by diff on
every run rather than cached. So a new rule reaches the plan the next time
the relevant skill runs, with no invalidation step.

## Sync rules

Read by `/fde:fdc-session`, in the plan check. What counts as a milestone, how
they are ordered, what a delta is allowed to change.

The template ships four standing rules here. A milestone is a vertical
slice of the system, never a client deliverable, and the promised dates
live in [`../project/deliveries.md`](../project/deliveries.md) instead. A
document is a configuration of a module rather than a milestone of its own.
One milestone has one reason to change, and a file with two gets cut. Every
milestone file carries a "Walk this" section. It is a numbered list of what
to click, written so someone can follow it without reading the rest of the
file.

Milestones do not break into issues. Pick a milestone and brainstorm it
whole. Write an implementation plan with the session that builds it, build
it in one pass, then walk it in a browser. Client questions go to
[`../project/open-questions.md`](../project/open-questions.md) with a named
owner, our own fieldwork goes to
[`../project/next-steps.md`](../project/next-steps.md), and build scope
stays inside the milestone file.

This engagement's own rules:

(none yet)

## Artifact rules

Artifacts are written by hand against a milestone, and the shapes they take
are in [`artifact-templates.md`](artifact-templates.md).

A prototype brief carries a `mode`. `feasibility` answers a yes-or-no and
its deliverable is a written verdict. `demonstrator` answers what the
interaction should feel like and its deliverable is a clickable file. Only
`demonstrator` briefs reach `/fde:prototype`. A prototype brief names the
delivery it serves, not a milestone.

A milestone file carries no task list, ever, however tempting during a
build. The milestone says what is being built and what done means; the plan
says how, and it lives with the session that builds it.

This engagement's own rules:

(none yet)

## Brain dump rules

Read by `/fde:brain-dump`. What gets captured, against what, and what a
dump may never become.

One brain dump per delivery, never per milestone. A milestone is how we
build and a delivery is what the client talks about. The conversations
behind a delivery arrive long before its milestones are cut. Conventions
are in
[`../project/brain-dumps/README.md`](../project/brain-dumps/README.md).

Append only. A contradicted entry stays and the later entry says what it
contradicts. A brain dump is never evidence and never outranks `wiki/`.
Guardrail 7's tier order does not apply to it, because an entry is not yet
a claim. An entry that hardens into a fact moves to `wiki/` with a real
source, and the entry takes a note saying where it went.

This engagement's own rules:

(none yet)

## Prototype rules

Read by `/fde:prototype`. What a demonstrator must show here, what it must
never do, and how it is checked.

A prototype attaches to a delivery, never to a milestone, because a
delivery is what the client recognises. One delivery may carry several
prototypes or none, and a prototype may span several milestones.

A demonstrator reads the delivery's brain dump before it is drawn, and
every `pain` entry is something it should answer. A demonstrator that
answers no recorded pain is decoration.

A prototype uses the design language in [`design.md`](design.md): the same
palette, type ramp, radii and shadows the application uses. A client seeing
one look in the demonstrator and another in the product learns that neither
is real. The application's own rules do not carry over, because a prototype
is one self-contained file with no build step. It writes plain CSS and
declares the tokens in its own `:root`. What must match is the values.

The document preview renders the extracted grid from the specimen store,
verbatim, never the field spec. A client recognises their own form and does
not recognise our data model.

Every demonstrator shows at least one human gate from
[`guardrails.md`](guardrails.md).

Facts carry provenance and an authority tier. Never simplify a field to one
value. A same-tier contradiction is shown as a conflict the person
resolves, and the system never picks.

Open rules from the milestone are shown as visible gaps. Hiding them makes
the prototype look finished and hides the questions the client needs to
answer.

This engagement's own rules:

(none yet)
