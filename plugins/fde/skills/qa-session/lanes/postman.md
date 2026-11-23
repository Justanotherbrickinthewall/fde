# Lane: postman

This lane has not yet been run in a real session, so its commands come from the
Postman plugin's own files.

The API lane. It covers the backend's HTTP surface: status codes, schemas,
data validation, access by identity and error handling. It runs by default when
its tool is installed. `--postman` runs this lane alone.

It uses the Postman plugin's skills, named `postman:<name>` in Claude Code.
They run unmodified. Everything this engagement does differently is an
override stated here and announced to the skill, and to every brief, before it
starts.

| Job | Postman skill | Writes to | Produces |
|---|---|---|---|
| Propose test cases (phase 2) | none, it reads `<be>/openapi.json` and the facts | `test-cases.md` | `proposed` rows |
| Write checks (phase 5) | `postman:api-testing`, `postman:collection-schema-v3` | `<be>/postman/` | a collection |
| Drive checks from data | `postman:datasets`, only where a test case needs a query or join | `<be>/postman/` | iteration data |
| Run checks (phase 5) | `postman:api-testing` | `results.md`, `evidence/postman/` | one row per test case |
| Dependency failure | `postman:api-simulation`, only where a test case needs it | `<be>/postman/` | a simulation |
| Load | `postman:performance-testing`, only where the record states a number | `<be>/postman/` | a threshold run |
| Real app traffic | `postman:application-testing`, only on the person's yes | `<fe>` | a contract match |

The checks go to `<be>`, on `qa/<slug>`. The last row is the one exception,
and it needs a branch in `<fe>`.

## Before anything: is the plugin there

If the `postman:` skills are not available, stop. Report `not installed`
and give the two install commands.

```bash
claude plugin marketplace add anthropics/claude-plugins-official
claude plugin install postman@claude-plugins-official
```

The test cases for this lane become `not run`.

If the skills are there and `postman` is not on `PATH`, follow
`postman:cli-install`. It puts the CLI on `PATH` and reports the version.

Local work needs no Postman account. The lane never signs in.

## What this lane overrides

**Where results go.** Seven Postman commands publish their results to a
connected workspace by default: `postman collection run`,
`postman application test`, `postman spec lint`, `postman workspace push`,
`postman runner start`, `postman flows run` and `postman request`. A client's
routes and data do not go to a Postman workspace unless the person says yes in
chat. Every command the lane runs that is on that list passes
`--report-events=false`. The plugin's files also spell it `--report-events false` and
`--no-report-events`, so read `-h` for the installed version. Pass it also to
any other command whose `-h` lists it, such as the lint, dataset, performance
and simulation commands. The plugin's files do not say whether those publish.
The lane never runs `workspace push`, `runner start` or `flows run`. Results go to `<session>/results.md` and
`<session>/evidence/postman/`.

**No workspace.** The lane does not connect the folder to a workspace, and it
does not run `postman init` without the person's yes. `postman init` opens a
temporary session with Postman and writes skills into `postman/skills`. The
plugin also registers Postman's hosted MCP server when it installs. Any MCP
call reaches Postman by design, so it is a cloud action and needs the same
yes. If the CLI suggests signing in or signing up, put the suggestion under
**For the user** and carry on locally.

**Who orchestrates.** `postman:api-engineer` does not run. It would design,
implement and deploy, and `/fde:qa-session` is the orchestrator here. The
plugin's SessionStart hook tells an agent to load `postman:api-engineer`
whenever the project has a `postman/` directory. That starts on the first
commit of this lane's work. Every brief says to ignore it, as the hook itself
allows for a subagent dispatched to a specific task.

**Where the checks live.** `<be>/postman/`, on `qa/<slug>`. That is
`postman/collections/` and `postman/environments/` in the Native Git v3
layout. Anything else a skill wants to write into the repository is reviewed
and put to the person before it is committed.

**Secrets.** `postman:variables` decides how a secret is supplied, under one
rule. The value stays out of committed files, out of the notes and out of the
chat. The shared vault and `postman secret create` need a signed-in CLI and
store the secret in Postman's cloud, so they need the person's yes. A credential the
run generates stays inside the run and is never written to an environment
file.

**Mocks and simulations never produce a pass on a fact.** `--use-mock` and
`postman:api-simulation` test the request and assertion logic, or the code
against stand-ins, and not the real service. A result from either is reported
as such. `postman simulation push` and `postman simulation deploy` are cloud
actions and never run. Deploy is public by default. The simulation's capture
file, `sim.ndjson`, is not committed, because bodies and headers are logged as
sent.

**Exit codes.** The exit code of `postman collection run` reflects failed
assertions, so a 200 can fail. The exit code of `postman application test` is
Playwright's, so the lane reads its summary table. A local collection under
`postman/collections/` supports only the `cli` reporter, and `-r junit` or
`-r html` exits 1 without running anything. `--output <folder>` keeps the run
summary.

Nothing else is overridden. Do not rewrite the skills' own questions or
their verification steps.

## Phase 2: proposing test cases

The lane writes no check yet. It reads the facts and `<be>/openapi.json`, and
returns `proposed` rows in its report with Lane
`postman` and no id.

For each route a fact touches, propose test cases on these.

1. The status codes the spec allows, and the one each case expects.
2. The response schema, and the data type of each field.
3. Required fields, and what happens when one is missing.
4. Invalid payloads, and the values either side of a stated limit.
5. Error handling: the status and body the fact says an error returns.

Where the auth convention is adopted, propose the access cases for each
identity. An unauthenticated request gets 401 with a body. A signed-in
non-member of a project gets 404 and never 403. An unsafe request without the
CSRF token is refused. Take the cookie and header names from the backend and
never from memory.

Each case is tied to a fact. A route no fact touches may still get a surface
case, with `Fact: none` and Type `exploratory`. The expected result comes from
the fact's source. Where the spec and the fact disagree, the fact wins, and the
disagreement goes under **Outside the facts**.

## Phase 5: writing the checks

Each group of checks is one subagent, of the
implementation kind. The orchestrator never writes one.

A brief names these things, because a vague brief gets a vague collection.

1. The framework: a Postman v3 collection, written under `postman:api-testing`
   and `postman:collection-schema-v3`.
2. The language: YAML for the files, JavaScript for `pm.test` assertions.
3. The test cases, by id, with steps, test data and expected result copied
   from `test-cases.md`.
4. The conventions: inherited auth and variables stay at collection or folder
   level, and no request copies them.
5. The assertion strategy: derive each assertion from the expected result and
   never from the current response.
6. The structure: the layout below.
7. The never-run list, the override list and the instruction to ignore the
   SessionStart hook.

The structure.

- One folder for setup, one folder per fact named with its id, and one folder
  for teardown. Use spaced `order` values.
- One request per test case, named with its id, such as `TC-014`. The result
  maps back with no guessing.
- Sign-in comes first, once per identity. The identities use a cookie session,
  so the setup signs in and carries the cookie and the CSRF token. The plugin's
  files do not say how a run carries a cookie. The first subagent proves it
  with a one-request run before the rest is written.
- The setup folder makes, and the teardown folder removes, the data a case
  needs. Every created record is named with the prefix `qa-<slug>-`.
- The base URL is a non-secret variable in
  `postman/environments/<name>.environment.yaml`. Run `postman environment lint`
  on the file.
- Data files come from `<session>/data/`. Copy each one the checks use into
  `<be>/postman/data/`, so the checks repeat after the merge. Run a plain file
  with `-d`. Use `postman:datasets` only where a test case needs a query or a
  join, and only with local file sources. The skill says a dataset should earn
  its extra configuration.

After each group, run `postman collection lint <collection-path>` and read the
warnings as well as the errors. Commit on `qa/<slug>` as each group is written.

### Optional parts

Each runs only when a kept test case calls for it.

**Dependency failure.** A test case that says what happens when a service the
backend depends on fails, such as a refused model call, uses
`postman:api-simulation`. It needs CLI 1.70.0 or later. The backend under test
is never a member. Each member needs `origin:` in the `.sim.yaml`, or its
traffic reaches the real service. The run is a server that never exits, so
start it in the background with its log in a file. Read the log to confirm the
path ran. Commit the mock, the `.sim.yaml` and its `<name>.context.yaml`. Do
not commit `postman/.dependencies/` or the log.

**Load.** `postman:performance-testing` runs only when the record states a
number to meet. With no agreed number there is no load test, because a
threshold nobody agreed is a guess. Use the local runner only, so no load is
generated from Postman's infrastructure. `postman performance run -h` names
the option. Put the record's number into the threshold, such as
`--pass-if "less_than(p95, 500)"`, with the metric the record names. Start
small, because writes carry the `qa-<slug>-` prefix and still land in the
target.

**Real app traffic.** `postman:application-testing` runs only on the person's
yes in chat. It runs only after the `playwright` lane has reported, because two
lanes never write in one checkout. Its edits to `<fe>` are put to the person
before they are committed. Its setup, `postman app setup-capture`, edits the Playwright
config and `package.json` in `<fe>`, and the first run writes
`postman.config.cjs`. The orchestrator must cut `qa/<slug>` in `<fe>` first.
It runs from the repository root and spawns the Playwright command. The exit
code is Playwright's, so read the summary. A request that is `not matched` is a
coverage gap and not a failure. Report the captured, matched and not-matched
counts. This lane writes no Playwright test, because that is the
`playwright` lane's job.

## Phase 5: running the checks

Each run is a subagent of the mechanical kind. It reports counts and failures,
and the raw output goes to a file.

1. Run each group with `postman collection run <collection-path>` and
   `--report-events=false`. Use `-e` for the environment, `-i` for one
   request, and `-d` for a data file. Use `--output <folder>` to keep the run
   summary under `<session>/evidence/postman/`.
2. Read what `--output` wrote and remove any cookie, header value or credential
   before the evidence stays in the session folder.
3. Write one row per test case into `<session>/results.md`. A result is
   `pass`, `fail`, `flaky`, `weak` or `not run`. A pass against a mock or a
   simulation says so in the Actual cell.
4. A case that passes only on a retry is `flaky`. Run each failed case a
   second time to tell.
5. For every priority 1 test case, show the check fail once. Copy the
   collection into `<session>/evidence/postman/failing-once/`. Change the
   expected value in the copy, and run that request with `-i`. The run must
   exit non-zero, and the failing assertion must be the one changed. A check
   that still passes is `weak`. Delete nothing from the real collection. For a
   one-off assertion on a single request, `--script-post-request` is the
   documented alternative.
6. Run `postman spec lint <spec>` on `<be>/openapi.json` with
   `--report-events=false`. The CI guidance shows `--workspace-id` for
   governance rules. If the lint needs a workspace, report that case `not run`.

A check is wrong when it has a wrong variable, a missing wait for a slow
response or a missing setup step. Log the change in `results.md`. The
expected value never changes, and a test case is never skipped or disabled to
turn a run green.

## What this lane does not cover

Security testing beyond the access cases. The Postman plugin names no security
testing skill, so the `anthropic` lane takes it. The interface in a browser is
the `playwright` lane's. Stored data is the `sql` lane's. A walk by hand is
`/fde:smoke-test`.

These Postman skills never run, and the reason for each.

- `postman:api-engineer` would orchestrate, and `/fde:qa-session` does that.
- `postman:api-monitoring` creates scheduled monitors, which run in Postman's
  cloud.
- `postman:api-documentation` writes documentation, and QA publishes none.
- `postman:api-discovery` uses the Context Graph, which is a cloud service.
- `postman:ai-readiness` scores an API for agents, and no fact asks for that.
- `postman:flows` builds and deploys Postman Flows, which are no part of QA.
- `postman:webhook-testing` runs only if the application has webhooks.
- `postman:mcp-testing` runs only if the application is an MCP server.
- `postman:workspaces`, `postman:postman-mcp-server` and
  `postman:ci-integration` serve a workspace or CI. The lane has no workspace,
  and CI is the person's offer in phase 8.
- `postman:api-mocking` runs only inside `postman:api-simulation`.

When the core asks in phase 7, write the command that runs the kept checks
into `results.md` under `Regression: postman`. Name each request with `-i`,
and read `-h` for whether `-i` repeats.

## Reporting back

Report, and never write `notes.md`: the collections written, the test cases run by result,
the priority 1 checks shown failing once, the checks reported `weak` or
`flaky`, the optional parts that ran, and what was `not run` with the reason.
Then `/fde:qa-session` reads `results.md` and judges
the facts.

If the lane blocked, say which test case, what it waited on, and what you
tried. Report the one unblocking action.
