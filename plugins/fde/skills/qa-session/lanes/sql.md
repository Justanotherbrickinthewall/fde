# Lane: sql

This lane has not yet been run in a real session. It uses no outside skill.
Its method comes from the contract and the stack's own tooling.

The data lane. It checks that what the application stored matches what a test
case expects. It runs when a kept test case's expected result names stored
data: a record exists, fields match, a relationship holds or an audit row was
written.

| Job | Tool | Writes to | Produces |
|---|---|---|---|
| Propose (phase 2) | none, reads the schema | its report | `proposed` rows for stored data, with no id |
| Write (phase 5) | a subagent | `<session>/sql/<TC-id>.sql` | one saved query per test case |
| Run (phase 5) | the backend's own database command | `<session>/results.md` | result rows with counts and ids |

## Install check

There is nothing to install. The lane needs a way to reach the local stack's
database, or a test environment the person named, and nothing else. Find the
command in the backend's own tooling: its compose file, its justfile or its
README. Do not invent one. If you cannot find it, report blocked and say what
you looked at.

## What this lane overrides

**Read only.** The lane runs `SELECT` statements and nothing else. Where the
database offers a read-only transaction, every query runs inside one. It never
writes, never changes the schema and never runs a migration.

**The schema comes from the source.** Read the models, the migrations or the
database's own catalogue. Never guess a table or column name. A name you
cannot find is a gap to report.

Nothing else is overridden.

## Phase 2: propose test cases

Read the facts and pick those whose result would show up as stored data.
Return one `proposed` row for each in the report, with no id, and with Lane
`sql`. The core numbers them. Take Expected result from the fact. A
stored-data check no fact backs is `Fact: none`, Type `exploratory`.

## Phase 5: write and run the queries

Every query is authored by its own subagent. The lane never writes SQL
inline. Each brief names:

1. The tables and the columns, copied from the schema you read.
2. The relationship between the tables.
3. What must be true, taken from the test case's expected result.
4. The test data from `<session>/data/`, by id.
5. That the query is one `SELECT`, and that it never writes.
6. That it never runs `git stash`, `git checkout .` or `git reset --hard`.
7. That no credential appears in the file or the output.

Save each query as `<session>/sql/<TC-id>.sql`.

A valid query is not a right one. Review each query for five things before its
result counts.

1. The right table.
2. The right joins.
3. The business rule the fact states.
4. The data types.
5. The expected values.

Then run it. Show the failing-once proof for every priority 1 test case. The
same query must return nothing, or the wrong answer, for an id that does not
exist. A query that cannot be made to fail is `weak`.

Write one row per test case into `<session>/results.md`. Evidence holds counts
and ids, never a person's data. A query that cannot run is `not run` with the
reason. Several lanes write the file at once, so read it first and only append.

The queries merge nowhere, so the lane has no regression set. When the core
asks in phase 7, write `none, the queries stay in the session folder` under
`Regression: sql`.

## What this lane does not cover

1. Writes of any kind, and any change to the database.
2. Behaviour in the interface or the API. Other lanes own it.
3. Any database nobody named, and causes. Phase 6 judges.

It never adds or rewords a fact, never marks one and never names a root
cause. It does not open, switch or remove a branch or worktree. It does not
merge, edit product code or write to the engagement record. Nothing goes to a hosted service without the person's yes in chat.
The lane never asks the person itself. It reports what needs a yes, and the
orchestrator asks.

## Reporting back

The lane never writes `notes.md`. It reports, and the orchestrator writes
what the notes need. Report one of two things.

1. Done. Give the counts of each Result. Point at `<session>/sql/` and
   `<session>/results.md`. Name any table or column not found in the schema.
2. Blocked. Say what stopped the lane and what it needs.
