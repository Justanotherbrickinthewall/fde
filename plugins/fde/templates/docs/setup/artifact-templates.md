# Artifact templates

Purpose: the shapes an artifact takes, so one is written by hand without
re-deciding its structure.
Done when: never. Add a kind when this engagement needs one.

Artifacts are written by hand against a milestone, and these are the shapes
they take.

An artifact settles one question. It lives at
`project/artifacts/<kind>-<slug>.md`, with no number, because artifacts have
no order among themselves and nothing should imply one.

Implementation plans also live in `project/artifacts/` and have no template
here. A plan is written out of a brainstorming session on a settled
milestone, in whatever shape the tooling of the day produces.

## Front matter

```markdown
---
kind: data-intake-spec | prototype-brief | eval-spec | document
status: stub | drafting | complete | superseded
mode: feasibility | demonstrator          # prototype-brief only
---
```

## Data intake spec

```markdown
# Data intake — <what is being asked for>

Settles: <the question, one sentence>.

Asked of: <persona or named party, linked to its entity file>.

Wanted:

| Item | Form | Why it is needed | Known from | Status |
|---|---|---|---|---|
| <the thing> | <file, table, answer> | <the node input it feeds, linked> | <node link or —> | have / wanted |

Acceptance: <what makes a supplied item good enough — the check, not a hope>.

Unresolved: <what nobody has answered yet, and who must>.
```

## Prototype brief, feasibility

```markdown
# Prototype brief (feasibility) — <what is being tested>

Settles: <the yes-or-no this answers>.

Input: <the specimen or file it runs against, linked>.

Expected output: <the artifact it produces>.

Bar: <the measurable threshold, cited to the node that sets it>.

Falsified if: <the observation that makes the answer no>.

Out of scope: <guardrail 9 applies during scoping — the code is disposable and the written verdict is the deliverable>.

Unresolved: <unknowns, and who must answer>.
```

A feasibility brief never reaches `/fde:prototype`. A person answers it in
writing.

## Prototype brief, demonstrator

```markdown
# Prototype brief (demonstrator) — <what is being shown>

Settles: <what the client is being asked to react to, one sentence>.

Shown to: <the persona or named party who must recognise it, linked to its entity file>.

Grounded in: <the field spec node, the extracted grid, the decisions whose behaviour it must obey — each linked>.

Must show: <the states, the gates and the gaps the walkthrough has to reach; a human gate from the guardrails is not optional>.

Recognised if: <what makes the client say that is our form and that is our process>.

Out of scope: <guardrail 9 applies — the file is disposable, never promoted into a code space>.

Built: <link to project/prototypes/<slug>.html once /fde:prototype has run, or — >.

Known debt: <what the built file does not do, including any `Must show` row it does not reach. Written by /fde:prototype, empty until then>.

Unresolved: <unknowns, and who must answer>.
```

## Eval spec

```markdown
# Eval spec — <what is being judged>

Settles: <what "good enough to put in front of a reviewer" means here>.

Sample set: <the specimens judged against, linked; how many, and what they do not cover>.

Criteria:

| Criterion | How it is checked | Pass bar |
|---|---|---|

Adjudicates: <the named party who has the final say — a person or role, never "the expert">.

Unresolved: <unknowns, and who must answer>.
```

## Document

```markdown
# <Document name>

Settles: <the question, one sentence>.

Must contain: <the sections or answers required, each traced to the node or exit criterion demanding it>.

Owner: <who writes it>.

Unresolved: <unknowns, and who must answer>.
```

## Rules that came with the templates

An empty section is the correct output where the wiki is silent. Inventing
its content is guardrail 3.

A stub states what the artifact must answer and who can answer it. Filling it
is later work by whoever owns it.

No backlinks. An artifact never lists what needs it. Reverse lookup is
`grep -rl <artifact-slug> project/`.

An artifact cites wiki nodes for anything it carries in, first mention as a
link, the same as everywhere else.

Amend a filled artifact with a dated note, the same shape as a wiki
correction. Never rewrite one that has been filled in.
