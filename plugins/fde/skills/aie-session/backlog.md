# Backlog tasks

Every session's plan is extracted into task files in `$REC/backlog/tasks/`.
This file is the one place the format lives, and `SKILL.md` points here from
phases 4, 5, 7 and 8.

The plan stays in the session folder in `my-sessions`, and it is still the
plan. A task file is the record-side extract of one plan task. So a task file
never links to or cites `my-sessions`, and it never repeats the plan's detail.
It says what the task does and why, in words a person reading the board can
follow.

The orchestrator writes these files, never the pack. A pack does not write to
the engagement record, and `methods/README.md` says why.

When `.engagement` sets `apps`, a task's app is the app the session resolved
in phase 0, and `$REC` already points at its folder. The app is never written
on the task.

## When the files are written and changed

1. After the plan check in phase 4, write one file per plan task, all at
   `To Do`. Commit and push them with the plan's status change.
2. During phase 5, move a task to `In Progress` when its subagent is
   dispatched and to `Done` when it reports and commits. Write them at the
   track boundary, in the same pass as the full suite, the same rule the
   findings file follows. Commit and push them there too.
3. In phase 7, every finding routed to "fix here" becomes a task of its own,
   numbered after the last plan task. It moves the same way.
4. At close in phase 8, every task reads `Done` or `To Do`. A task left at
   `To Do` gets one sentence under its description saying why, and where the
   work went if it went somewhere.

Bump `updated_date` on every change. Never renumber a task once it is
written, because the board and the commits cite the id.

## The format

The file name is `<id>-<short-slug>.md`, for example
`m11-03-override-columns.md`. The id is the session's key, then a two-digit
task number. The key is the milestone id when there is a milestone, and the
session slug when there is none. Where `apps` is set, the milestone id already
carries its app.

```yaml
---
id: m11-03                  # session key, then task number in plan order, zero-padded
title: Add override columns to the facts table
status: To Do               # To Do | In Progress | Done
milestone: m11              # the milestone id; omit when the session has none
delivery: D1                # copied from the milestone file's `delivery:` front matter; omit with no milestone
due_date: 15-09-26          # DD-MM-YY, from that delivery's row in the deliveries file; omit if none or several
labels: [backend]           # backend | frontend | docs | infra | test
dependencies: []            # task ids in the same shape, such as [m11-01]
created_date: 11-09-26
updated_date: 11-09-26
---

## Description
Two to four plain sentences: what and why.

## Acceptance criteria
- [ ] ...

## Files
- `<be>/...`

## Tests
- `<be>/.../test_x.py::test_name`
```

`Files` lists the paths the plan task creates or changes, one per line, with
the repository name first. `Tests` lists the tests that prove the acceptance
criteria, in the form the test runner prints. Both come from the plan task,
and neither carries steps or code. They let a reader check a task against the
code without opening the plan.

A task with no test, such as a docs or infra task, says so in one line under
`Tests` instead of leaving it empty. A task made from a finding fills both
sections once its fix commits.

`delivery:` in a milestone file is not always written one way. Write `D` and
the number, or `none`. Where the milestone serves several deliveries, list
them as `D1, D2` and leave out `due_date`.

`dependencies:` lists task ids, taken from what the plan says a task consumes
from earlier tasks.

A task made from a finding says so in its description, with the finding's
number, for example "Finding 12 from the walk." It does not link to the
findings file.
