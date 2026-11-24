# Plan ledger

Purpose: one row per wiki node, and whether the plan has taken account of it.
Done when: never. The delta between this file and `wiki/` is what
`/fde:fdc-session` reads on its next run.

Last sync: never.

This file's own modification time is the watermark. A `wiki/` file newer
than it re-pends its node. Written last in a run, after the diffs are
applied.

A node carrying placement only holds extracted specimens and no written
index, so the plan cannot rest on it. `/fde:file`'s expensive layer is
what clears one.

Statuses: pending, folded `<date>`, no-impact `<date>` with a reason.

| Node | Kind | Wiki state | Status |
|---|---|---|---|
| | | | |
