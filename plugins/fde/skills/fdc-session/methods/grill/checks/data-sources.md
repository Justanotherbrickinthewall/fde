# Check: the data sources

Covers `wiki/data-sources.md`.

*Lifted from the `map-data` skill on 07-09-26, when the six scoping skills
folded into `/fde:fdc-session`.*

This engagement's corrections live in `setup/scoping-rules.md` § "Data
rules". Read them first; they override what is below. Guardrails always
apply, especially 2 (no unsourced facts in the wiki), 3 (unknown is an open
question) and 5 (client data never leaves without per-instance approval).

Understand the information landscape before designing an integration.

## Complete looks like

Every field the solution depends on has an authoritative source, with a named
owner and a working access path.

A source with no named owner is not a source, it is a hope. Owner means a
named person who can grant access, never a department.

## Read state first

Read the System column of `wiki/process.md` § "Steps". Every distinct system
there is a candidate source, and the list starts as that set.

Ask what is missing from it. The systems people describe are the ones they
touch, not the ones the data came from.

Report sources already inventoried and ask only about the rest.

## The eleven rows per source

Ten fields, asked in order, one source at a time. Then the eleventh, which is
the one that catches the problems.

| Row | What it asks |
|---|---|
| Purpose | what this source is for, in the process |
| Data held | what is actually in it |
| Format | the file type, the schema, the specimen we hold |
| Access | how it is reached today |
| Owner | the named person who can grant access |
| Auth | how it authenticates |
| Updates | how often it changes |
| Quality | how good the data is, in the owner's own words |
| Sensitivity | personal, financial, commercial or public |
| Known limitations | what we already know is wrong with it |
| Access proven | has anyone actually pulled a record? |

An access path nobody has exercised is an assumption. It goes to
`project/assumptions.md` with the validation named and who can perform it.

Ask where each answer came from, and record it in the Sources table with its
tier.

## The sensitivity check

Where a source holds personal, financial or otherwise sensitive data, ask two
things. Where will that data sit once the solution runs? Does that cross the
boundary agreed with the client?

Where it does, say plainly in the session that this is a security posture
exception, and one of the five things that leave the engagement. It escalates
to whoever owns the engagement commercially. Record it in
`project/risks.md` and name it in the report.

Do not file it quietly, and do not design around it.

## The four architecture questions

They decide the architecture, and they are answered against the field list
rather than in general.

1. Which source is authoritative for each field?
2. Who wins a disagreement, and who decided that?
3. What freshness does each field require?
4. Can production data be used, and if not, what is the synthetic
   alternative?

Fill the Field ownership table as they resolve, one row per field the
solution depends on.

## Template

```markdown
# Data sources

Purpose: the information landscape the solution will depend on, and who owns
each part of it.
Done when: every field the solution depends on has an authoritative source
with a named owner and a working access path.

## Inventory

### <Source name>

Feeds steps <ids>.

| Field | Value |
|---|---|
| Purpose | |
| Data held | |
| Format | |
| Access | |
| Owner | <a named person> |
| Auth | |
| Updates | |
| Quality | |
| Sensitivity | |
| Known limitations | |
| Access proven | <Yes, with what was pulled and when — or **No**, with the assumption id> |

## Field ownership

| Field the solution depends on | Authoritative source | Owner | Access proven |
|---|---|---|---|

## Sources

| Claim | Source | Tier |
|---|---|---|
```

A field where several sources disagree and no rule picks reads `**none**` in
the authoritative column, with an open question against it. That is a real
answer and it is more useful than a chosen favourite.

## What to report

Sources inventoried, access paths proven versus assumed, fields still without
an authoritative source, and any escalation raised.
