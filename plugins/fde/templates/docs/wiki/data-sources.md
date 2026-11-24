# Data sources

Purpose: the information landscape the solution will depend on, and who
owns each part of it.
Done when: every field the solution depends on has an authoritative source
with a named owner and a working access path.

This node is `tier: ours` — our understanding of the landscape. A claim
traced to a raw artefact carries that artefact's tier in the Sources table
below instead.

Filled by `/fde:fdc-session`'s data-sources check. One block per source. A
source with no named owner is not a source, it is a hope.

## Inventory

Derive the sources from the System column of [`process.md`](process.md),
then extend them by asking. One block each.

An access path is not proven until someone has pulled a real record
through it. Until then the block describes how the work is done today, and
it carries an assumption in
[`../project/assumptions.md`](../project/assumptions.md).

Owner means a named person who can grant access, never a department.

### <source name>

Feeds steps <numbers>.

| Field | Value |
|---|---|
| Purpose | |
| Data held | |
| Format | |
| Access | |
| Owner | |
| Auth | |
| Updates | |
| Quality | |

## Architecture questions

These four decide the architecture, and none of them is a detail.

1. Which source is authoritative for each field the solution depends on?
2. Which source wins when two disagree, and who decided that?
3. How fresh must the data be for the process to work?
4. Can production data be used? If not, what is the synthetic
   alternative, and who signs it off?

Answer each one below, and say plainly where the answer is still open. A
precedence rule is the client's to state, not ours to invent, under
guardrail 10.

## Field ownership

One row per field the solution depends on. Gate 1 reads this table, and a
field with no proven access path fails it.

| Field the solution depends on | Authoritative source | Owner | Access proven |
|---|---|---|---|
| | | | |

## Sources

| Claim | Source | Tier |
|---|---|---|
| | | |
