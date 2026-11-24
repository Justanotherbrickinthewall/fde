# ADR-001: three repositories, a Django backend and a React frontend

Date: 07-09-26. Status: accepted.

This is the stack the template ships with. It is decided before the
engagement starts, so a pod can build on day one rather than argue about
frameworks. Reopen it with a later ADR if this client's constraints make it
wrong.

## Context

An engagement has two halves that move at different speeds. The engagement
record changes every time someone talks to the client. The application
changes on a milestone branch and merges when the walk passes. Putting both
on one branch means planning the next milestone lands inside the current
milestone's history, which is a real cost paid every week.

The work also splits by kind. Authentication and roles are the same on
every engagement. Document handling is pure computation over bytes. The
client's domain is where all the judgement lives, and it is the part that
gets rewritten. Those three want a boundary a directory can enforce.

Most of what an FDE engagement does to a document is Python work: reading
PDFs and workbooks, writing Word files, handling geometry. Moving the
centre of gravity to TypeScript would mean calling out to Python for
everything that carries value.

This is a hard-to-reverse decision, so it is an ADR under guardrail 6.

## Decision

**1. Three repositories.** `fde-docs` holds the engagement record.
`fde-be` is the backend. `fde-fe` is the frontend.

**2. An untracked umbrella.** The three sit as siblings inside a folder
that has no `.git` and never will. It carries `.claude/`, `CLAUDE.md`, a
`justfile` and a `docker-compose.yml`, all linked in from `fde-docs`.
Claude is always started from the umbrella, so all of it is in view at
once. A fourth sibling, `my-sessions`, holds session records and is never
committed anywhere.

**3. `fde-docs` never branches.** It is always on `main`. The record has
no merge to make, so a branch would only hide work from the other lanes.

**4. `fde-be` is Django.** With DRF, `drf-spectacular`, Celery on Redis,
Postgres and S3-compatible storage. Django's migrations, permissions and
admin serve an auditable record directly.

**5. Backend layering, in three rules.** `core/` is authentication and
RBAC only, and it imports nothing from a domain. Document handling is pure
functions with no models and no database. Everything else lives under
`domains/`. A thing moves down out of a domain only when a second domain
needs it. A test enforces the first rule rather than a convention.

**6. `fde-fe` is a workspace.** `packages/ui` holds the components and the
design tokens, `apps/web` holds the screens. React, Vite and TanStack
Query. The API client is generated from `fde-be/openapi.json` and never
hand-edited.

**7. Compose per repository.** Each repository runs alone. The umbrella
file uses `include:` to stitch them together and adds one proxy. It owns
nothing itself, which is why it is allowed to be untracked.

**8. One origin at the edge.** `/api/*` goes to the backend and everything
else goes to the bundle. That keeps the session cookie and any file
download working without CORS.

**9. One branch name across two repositories.** The branch is the
milestone id, identical in `fde-be` and `fde-fe`. The backend merges
first, because the frontend's generated client reads the backend's
`openapi.json`.

**10. Sessions are server-side.** Sign-out deletes the row, so a cookie
captured beforehand stops working.

## Rejected alternatives

**One repository holding everything.** The smallest setup, and one deploy
rather than two. Rejected because the record and the code then share a
branch, which is the cost this decision exists to remove. It also gives
the layering rules no boundary to sit on.

**A server-rendered Python application with no Node.** Fewer moving parts,
no build step, no generated client. It is the right answer for the first
week and the wrong one by the second month. An FDE application needs a panel
that fills as you type, an evidence viewer and a chat beside a form. That is
what a single-page application is for.

**A JavaScript backend.** One language across both halves. Rejected
because the document work is Python. Reading PDFs and workbooks, writing
Word files and handling geometry all have mature Python libraries and thin
JavaScript ones. The backend would end up calling Python anyway.

**A frontend deployment per domain.** Each domain agent shipping on its
own cadence. Rejected because it multiplies deployments before the second
domain exists, and it fights decision 8. One origin is what keeps the
cookie working. A second domain is a second entry under `apps/`, and it
shares `packages/ui` for free.

## Consequences

**Easier.** The record stops sharing a branch with the application, so
planning one milestone while another builds costs nothing. The document
layer is testable without a database. A second domain is a directory
rather than an argument.

**Harder.** There are two deployment artefacts instead of one, and the
client's IT team run them. A change that spans the API and a screen costs
two repositories, two branches and a merge order.

**Constrains next.** Every milestone is built in this shape, against a
generated API client the frontend never edits by hand. A backend change
that alters the API is not done until `openapi.json` is regenerated and
the client is rebuilt.

**Rests on open ground.** Where the system eventually runs is undecided,
and so is what it authenticates against. Both belong in
[`../open-questions.md`](../open-questions.md) with a named owner in the
first `/fde:fdc-session`.
