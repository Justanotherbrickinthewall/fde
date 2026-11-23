---
name: init
description: "Start an engagement. Makes the umbrella, the docs repository and any code repositories, writes .engagement, walks the four conventions one at a time, and leaves m01 ready to build. Use on day one of a new client, before any other fde command, when the user says \"start an engagement\", \"set up a new client\", \"scaffold the repos\", or invokes /fde:init <slug>. It runs once per engagement and it builds no application code itself."
---

# init

This is the first command a pod runs. It turns an empty folder into an
engagement: an umbrella, a docs repository, the code repositories you have,
and a first milestone somebody can build.

It is a conversation in six phases. Phase 1 builds the folders. Phases 2 to
5 walk the four conventions and ask, one at a time, whether this engagement
adopts each. Phase 6 writes m01 and hands over.

Init writes no application code. It ends by naming the command that does.

## Finding the engagement

Init writes `.engagement` rather than looks for one. Phase 1 writes it, and
every other skill reads the umbrella out of it from then on.

Below, `<docs>` means the docs folder that file names, `<be>` the backend
folder and `<fe>` the frontend folder. `${CLAUDE_PLUGIN_ROOT}` is the
plugin's own directory, and every plugin path hangs off it.

The format itself is in [`ENGAGEMENT.md`](../../ENGAGEMENT.md), and that
file is the authority.

## Invocation

```
/fde:init <slug>
```

The slug is the engagement's short id. It is lowercase letters, digits and
dashes, and it names the repositories. Give it or phase 1 will ask.

```
/fde:init acme
/fde:init northwind-permits
/fde:init
```

Run it from wherever the umbrella should sit, or from anywhere and give the
path when asked. Run it once per engagement.

## The six phases

| # | Phase | Writes to | Ends when |
|---|---|---|---|
| 1 | Scaffold | the umbrella | the folders exist and `.engagement` is written |
| 2 | Design | `<docs>`, `<fe>` | the design row is in `setup/conventions.md` |
| 3 | Auth and roles | `<docs>`, `<be>` | the auth row is in `setup/conventions.md` |
| 4 | Model gateway | `<docs>`, `<be>` | the gateway row is in `setup/conventions.md` |
| 5 | Repository layout | `<docs>`, `<be>`, `<fe>` | the layout row is in `setup/conventions.md` |
| 6 | Close | `<docs>`, `.engagement` | m01 is `ready` and ADR-001 says what the stack is |

Run them in order. Every phase asks a question and waits for an answer.
Never answer on the user's behalf, and never skip a convention because you
expect a no.

---

## Phase 1 — Scaffold

### Ask four things

Ask them together, in one short message, and wait.

1. The slug, unless it came in with the command.
2. The GitHub organisation the new repositories belong to.
3. Whether a backend repository already exists.
4. Whether a frontend repository already exists.

For the backend and the frontend, offer the same three answers:

- Bring your own. Give a clone URL or a local path, and init folds it in as
  `<slug>-be` or `<slug>-fe`.
- Take the reference implementation. `PeopleEquation/fde-be` is Django and
  DRF, and `PeopleEquation/fde-fe` is React and Vite. Both are optional, and
  neither is part of the method.
- None for now. The line in `.engagement` stays empty, and a later milestone
  creates the repository.

Also ask where the umbrella should sit, unless the current directory is
obviously it. The umbrella is one folder holding everything, and its name is
usually the slug.

### Run the script

The mechanics are one script, so nothing here depends on your typing:

```bash
"${CLAUDE_PLUGIN_ROOT}/scripts/scaffold.sh" \
  --slug <slug> \
  --org <org> \
  --umbrella <path> \
  --docs-template PeopleEquation/fde-docs \
  --be <url | path | reference | none> \
  --fe <url | path | reference | none>
```

The docs template is `PeopleEquation/fde-docs` unless the user names
another. A template written as `owner/repo` goes through
`gh repo create --template --clone`, so `gh` has to be signed in. A local
path is copied and `git init` runs in the copy.

The script makes the umbrella and then `<slug>-docs` from the template. It
places the code repositories you asked for. It renames every `fde-docs`,
`fde-be`, `fde-fe` and `fde-os` inside the docs repository. Then it writes
`.engagement` with `stack=` empty and makes `my-sessions/`. When
`~/.claude-shared` exists, `my-sessions` is a link to
`~/.claude-shared/records/<slug>/`. Otherwise it is a plain folder. The script
writes `<docs>/umbrella/CLAUDE.md` as a map of the repositories, and a stub
`CLAUDE.md` in each code repository that links `BRANCHING.md`. It never
overwrites a `CLAUDE.md` that exists. Last it runs `bootstrap.sh`. It prints
one line per step.

It refuses to overwrite an existing `<slug>-docs`. If it stops there, the
engagement was already scaffolded, so read `.engagement` and go to phase 2.

### Report

Say back four things in plain words: where the umbrella is, which
repositories exist, what `.engagement` holds, and that `stack=` is empty
until phase 6. Then go straight into phase 2.

A repository taken from the reference has no `origin`. The script removes
it after cloning, so a stray push cannot reach `PeopleEquation`. A
repository copied from a local path never had one. Say that the pod adds
the engagement's own remote before the first push.

A repository brought in by URL keeps its own `origin`, which is correct.

---

## Phases 2 to 5 — one convention each

The four conventions are the parts of an application every engagement builds
the same way. They are files, not commands. Each holds a spec, a checklist
and a `reference/` folder of portable files.

```
${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/design.md
${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/auth-and-roles.md
${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/model-gateway.md
${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/repo-layout.md
```

### The shape every one of these four phases follows

1. Say what the layer is, in the two or three sentences written under the
   phase below. Do not read the whole convention out loud.
2. Say which repository the files would land in, and say plainly when there
   is no such repository yet.
3. Ask one question: does this engagement adopt the layer, yes or no?
4. Wait for the answer. A no is a normal answer, so ask for the reason and
   write it down as given.
5. On a yes, append a row to `<docs>/setup/conventions.md` saying adopted.
6. On a yes, copy the portable files into the matching code repository, but
   only if that repository exists. Where it does not, the files wait and the
   rules become part of m01's scope.
7. On a no, append a row saying declined, with the reason in the row.

Nothing here builds anything. Copying a reference file into a repository is
not a build, and a milestone still has to make it work.

### setup/conventions.md

The file does not ship in the template, so phase 2 creates it. It carries a
short header and one table with five columns.

```markdown
# Conventions

Which of the four conventions this engagement adopted, and when. Phase 8 of
`/fde:aie-session` reads this table and runs every adopted checklist against
what merged. A failing checklist blocks `built`.

| Layer | Adopted | Date | Reason | Checklist |
|---|---|---|---|---|
| design | yes | 07-09-26 | one look across every screen, and the client sees it early | `skills/init/conventions/design.md` |
| auth-and-roles | no | 07-09-26 | the client's own SSO is the credential, so this is theirs | `skills/init/conventions/auth-and-roles.md` |
```

The layer is the convention's file name without the extension. Adopted is
`yes` or `no`. The date is `DD-MM-YY`. The reason is the user's own words,
one line, on a yes as well as on a no. The checklist is the convention file,
relative to the plugin root, because that file is where the checklist lives.

Four rows, always. A convention nobody asked about is a convention that gets
adopted by accident in month three.

---

## Phase 2 — Design

### Say this

Every screen should look like it came from one place. One file holds every
colour, corner, type size and spacing step the product may use, and screens
spend those values rather than inventing their own. A written document sits
beside that file and says what each value means, and a test holds the two
together.

Then say what it costs. No hex and no raw pixel size appears anywhere but
the token file. Fonts are vendored into the bundle rather than fetched at
run time.

### What it drops, and where

Into `<fe>`, and only if a frontend repository exists. The source is
`${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/design/reference/`.

| File | Lands at | When |
|---|---|---|
| `DESIGN.md` | `<fe>/packages/ui/DESIGN.md` | always |
| `theme.css` | `<fe>/packages/ui/src/theme.css` | always |
| `no-stray-styles.test.ts` | `<fe>/packages/ui/src/__tests__/no-stray-styles.test.ts` | the frontend runs Vitest |

`no-stray-styles.test.ts` is written for Vitest, Tailwind and HeroUI. It
also expects that exact path, because it walks up from its own directory to
find `apps/web`. On another frontend it does not run, so rule 11 of the
convention goes into m01's scope as work instead.

`design-tokens.test.ts` is not copied. It imports `../field-states`, and
`design.md` says that file is not carried here, so the copy would not
compile. It stays in `reference/` as the worked example of rule 10, and
writing this engagement's version is m01's job.

The paths above are the reference frontend's. On a brought-in frontend, put
each file beside its equivalent and say in the report where each one went.

`<docs>/setup/design.md` ships in the template and already points at
`DESIGN.md` and `theme.css` as the live pair. Phase 1 renamed the repository
in it, so it needs no edit here.

With no frontend, nothing is copied. Say so, and carry the four files into
m01's scope.

---

## Phase 3 — Auth and roles

### Say this

This layer decides who is signed in and what they may see. A person signs in
with an email and a password and gets a session cookie the server holds, so
signing out really ends the session. Everyone belongs to an organisation,
and a person sees a project only by being a member of it.

Then say the sharp edge: a non-member gets 404 rather than 403, so nobody
learns what work exists by guessing at addresses.

### What it drops, and where

Into `<be>`, and only if a backend repository exists. The source is
`${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/auth-and-roles/reference/`.

| File | Lands at | When |
|---|---|---|
| `models.md` | `<be>/src/core/MODELS.md` | always |
| `rbac.py` | `<be>/src/core/rbac.py` | Django, and both folders already exist |
| `test_layering.py` | `<be>/tests/domains/test_layering.py` | the backend is Django |

`models.md` is the four tables written as prose, so it carries to any stack.
The other two are Django and pytest. On another backend they go into m01's
scope as rules to build rather than files to copy.

`test_layering.py` counts two directories up from itself to find `src/`, so
the path above is the one that works. Put it anywhere else and fix the
`parents[2]` on the copy.

`rbac.py` needs four things in place before it runs. Two are settings and
two are models.

1. `settings.RBAC_PROJECT_MODEL`, the label of the project model.
2. `settings.RBAC_PROJECT_MEMBER_MODEL`, the label of the membership model.
3. A project model, reached by its primary key.
4. A membership model carrying `project_id`, `user_id`, `role` and a `user`
   relation.

So copy `rbac.py` only where `<be>/src/core/` and `<be>/src/domains/`
already exist. Otherwise leave it in `reference/`, say so in the report, and
put the gate into m01's scope. A copied file with no settings behind it
fails on the first request, and that failure is hard to read.

With no backend, nothing is copied.

---

## Phase 4 — Model gateway

### Say this

The application asks a language model for help in exactly one place, and
that place is the gateway. Every prompt lives in a file rather than in code,
one file per task, so a person can change a prompt without touching a
program. The key that pays for the calls lives only in the environment, and
a commit hook keeps it out of the history.

Then say the rule that shows on screen: a refused call renders visibly, and
never as a silent gap or an invented value.

### What it drops, and where

Into `<be>`, and only if a backend repository exists. The source is
`${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/model-gateway/reference/`.

| File | Lands at | When |
|---|---|---|
| `no-secrets` | `<be>/bin/no-secrets`, executable | always |
| `gateway-interface.md` | `<be>/src/gateway/INTERFACE.md` | always |
| `task-file.toml` | `<be>/prompts/task-file.toml` | always |

`no-secrets` is a standalone Python script and it runs on any repository, so
it is the one file here that never depends on the stack. Wire it into
`<be>/.pre-commit-config.yaml` as a local hook, or say in the report that
the wiring is m01's job.

Two environment names go into `<docs>/umbrella/.env.example`, which
`bootstrap.sh` links to the umbrella root:

```
OPENROUTER_API_KEY=
OPENROUTER_BASE_URL=
```

That file is in the docs repository, so those two lines land whether or not
a backend exists. Never write a real key into it.

---

## Phase 5 — Repository layout

### Say this

An engagement has three repositories side by side inside one folder that is
not itself a repository. A milestone opens one branch, with the same name in
the backend and the frontend, and the backend merges first. One person or
agent works in one checkout at a time, so two of them never fight over the
same files.

Then say what phase 1 already did. It built that tree. So adopting this
layer is mostly agreeing to the branch rule and the API check.

### What it drops, and where

Into `<be>` and `<fe>`, each only if it exists. The source is
`${CLAUDE_PLUGIN_ROOT}/skills/init/conventions/repo-layout/reference/`.

| File | Lands at | When |
|---|---|---|
| `branch-rule.md` | `<be>/BRANCHING.md` | a backend exists |
| `branch-rule.md` | `<fe>/BRANCHING.md` | a frontend exists |

Each code repository's own `CLAUDE.md` already links its `BRANCHING.md`,
because phase 1 wrote that stub. The rule is stated once per repository.

`umbrella.md` is copied nowhere. It describes the tree phase 1 already
built, and `<docs>/umbrella/CLAUDE.md` says the same thing from inside the
engagement.

The API check has no reference file, because it depends on the framework.
`bin/check-openapi` in the backend and the generated client in the frontend
both go into m01's scope.

---

## Phase 6 — Close

### Rewrite m01

The template ships one milestone, `<docs>/project/milestones/m01-*.md`, and
it is marked built because the template's own m01 was built. Rewrite it as
this engagement's m01. Rename the file if the assertion changed.

The front matter reads:

```yaml
---
status: ready
target: <DD-MM-YY>
delivery: none
waits-on: none
---
```

Only the FDC sets `ready`. The FDC is the forward deployed consultant, the
role that keeps the record true and cuts the milestones. On day one there is
no record yet, so init stands in. Say that in the report.

A `ready` milestone holds one H1 and six parts, and the record lint checks
for all seven. The six are why now, in scope, out of scope, guardrails,
rests on, and walk this. Keep exit criteria too.

The H1 is an assertion, not a topic. Not "sign-in and the shell", but "a
person signs in, sees an empty project list, and a super admin adds people
and creates projects".

Scope is the adopted layers and nothing else. A layer declined in phases 2
to 5 does not appear. Guardrails names the conventions the milestone takes,
so `/fde:aie-session` phase 3 reads the right ones.

Walk this is the manual browser pass, in order, one numbered step per thing
a person clicks. Write it for the layers actually in scope. The template's
eight steps are a good start where auth and design were both adopted.

### m01 is different for a brought-in repository

Where phase 1 folded in an existing backend or frontend, m01 is a
conformance pass rather than a build.

Run each adopted convention's checklist against what arrived, one subagent
per layer. Each item gets one of three answers: pass, fail, or not
applicable. The failures are the milestone's scope, one line each, in
the checklist's own words.

Say the count back before writing: eleven design items, five failing.

A conformance pass with no failures is a real answer. Write m01 as `ready`
anyway, with the checklist run itself as the scope. Init never sets `built`,
because only `/fde:aie-session` does, and it closes m01 the same way it
closes any other milestone.

### Rewrite ADR-001

`<docs>/project/decisions/adr-001-the-stack.md` ships accepted, because the
template picked Django and React. That is only true here if the pod took the
reference implementation.

Where either `--be reference` or `--fe reference` was taken, keep it
accepted. Date it today. Name Django and DRF for the backend, and React and
Vite for the frontend. Keep the three decisions phase 1 already made true:
the three repositories, the untracked umbrella, and the docs repository
never branching.

Otherwise set the status to `proposed` and leave the stack blank. Keep the
context and the repository decisions, and delete the framework choices. Add
one line saying the stack is undecided, and that the first
`/fde:fdc-session` picks it. Then raise it as a row in `<docs>/project/open-questions.md` with
a named owner.

### Write stack, in one case only

`.engagement` gets `stack=django-react` only where ADR-001 stayed accepted,
which is only where the reference implementation was taken. Edit that one
line and change nothing else in the file.

This is init finishing its own write rather than one of the two later writes
[`ENGAGEMENT.md`](../../ENGAGEMENT.md) allows. Where the stack was left
open, `stack=` stays empty and `/fde:fdc-session` fills it in when ADR-001 is
accepted.

### Tidy the record behind you

Three files still describe the template rather than this engagement.

1. `<docs>/project/milestones/index.md` — regenerate the row for m01, with
   the new assertion and the new status.
2. `<docs>/CLAUDE.md` — the "Current phase" section says m01 ships built.
   Rewrite it to say what is true: the engagement is scaffolded, the
   conventions are recorded, m01 is ready and nothing is built.
3. `<docs>/setup/conventions.md` — check it holds four rows.

Then run the record lint from the umbrella and fix what it finds:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/lint_record.py" "$DOCS"
```

### Hand over

Close with four short lines and stop.

1. What exists now: the umbrella, the repositories, `.engagement`.
2. Which conventions were adopted and which were declined.
3. What m01 says, in one sentence.
4. The next command:

```
/fde:aie-session m01
```

Say plainly that init built nothing. It made folders, copied reference files
and wrote a milestone. The first line of application code is written by
`/fde:aie-session`, against the milestone init just left.

## Notes

- Init runs once per engagement. A second run stops at phase 1, because
  `scaffold.sh` will not overwrite an existing docs repository.
- The conventions are data and this skill only reads them. A fix to a
  convention is a change to the plugin, not to an engagement.
- `<docs>` is always on `main` and it never branches. Init makes no branch
  and no pull request.
- Adopting a layer with no repository to put it in is normal on day one. The
  record says adopted, and m01 carries the work.
- Do not write a provider key, a password or a client's own material into
  anything init touches.
