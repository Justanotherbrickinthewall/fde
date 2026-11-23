# The worked example

There is no built prototype in the template. This file describes the shape a
good one takes, so the first demonstrator on an engagement has something to
copy.

A demonstrator is one HTML file, a thousand lines or so, vanilla JavaScript,
no dependencies. It opens in a browser and plays a scripted session. Grey
chips speak the client's side and the screen responds. The person watching
sees the interaction rather than a description of it.

One demonstrator normally spans two milestones. The sign-in and the project
list come from one, the screen that does the real work from another. That is
fine, because a prototype attaches to a delivery.

## What it is grounded in

Five things, and a demonstrator grounded in fewer than these is decoration.

1. The wiki node for the document or the screen it shows. Its field table
   gives the type, the supplier, the formula and the timing.
2. The extracted grid from the specimen store, verbatim. That is what the
   client's own form looks like.
3. The record's behaviour, as the milestone settled it. Facts carry
   provenance and a tier. A field can hold several facts at once. A document
   is a view over facts, and a same-tier conflict is a human gate.
4. `setup/guardrails.md`, for the human gates. At least one of them shows on
   screen.
5. The rules that are still open, shown as visible gaps rather than hidden.

## The correction that matters most

An early version of a demonstrator rendered the field spec as the document
preview. The client rejected it. The preview must be the extracted grid,
exactly as the blank form prints, with the record's values dropped into the
right cells.

That is the single biggest lesson available here. A client recognises their
own form. They do not recognise your data model.

## How it is put together

One file, read top to bottom. Name each part so a reader can find it.

| Symbol | What it carries |
|---|---|
| `FIELDS` | The field model: id, section, label with the form's own numbering, supplier hint |
| `TIER_RANK` | Guardrail 7's order as numbers: statutory 3, artefact 2, stated 1, ours 0 |
| `makeRecord` | A per-project record. Every field starts `open` with no facts |
| `PROJECTS` | Two or three seeded projects: not started, in progress, signed |
| `agentRun` | The fake per-format parse. Every format emits the same fact shape |
| `addFact` | The record's rules in one function: rival detection, tier cascade, loser marking, same-tier conflict |
| `BADGES` | The field states and their colours, taken from `setup/design.md` |
| `renderField` | One field row, its badge, its facts and its provenance line |
| `cascade` | A computed field settles once every dependency settles |
| `bootChat` | The scripted walkthrough, one function per beat |
| `ROWS` | The document's rows, verbatim from the specimen |
| `PRE` | Cells the blank template pre-prints. Rendered grey until overridden |
| `VAL` | Record to row mapping. Returns the text for a cell, or null |
| `renderDoc` | The one renderer. The modal, the export and the print path all use it |

A mapping function returning null is the honest gap. The row is expected and
the record has nothing for it yet, so it renders as a visible hole.

## The chat asks by document first

Open by asking for the document that carries the most fields at once, not by
asking field by field. Field by field is slower and the client notices. Keep
the field-by-field path as the fallback for when no document exists.

## Known debt

State the debt in the file's own README or in the brief. Do not fix it
silently in a copy, and do not pretend a demonstrator is production code.

Typical items. A callback that reads a global at fire time and writes into
the wrong record. A panel that paints transiently into a hidden view. A
state with no edit affordance. Any invented figure is the dangerous one,
because the client may quote it back, so label it in its own cell.

## Verifying without a browser

Check the script parses, and check the row count matches the specimen.

```bash
sed -n '/<script>/,/<\/script>/p' project/prototypes/<name>.html \
  | sed '1d;$d' > /tmp/proto.js && node --check /tmp/proto.js
```

```bash
awk '/^const ROWS = \[/{f=1;next} f&&/^\];/{exit} f&&/^ \["/{c++} END{print c}' \
  project/prototypes/<name>.html
```

Bound the count to the array. A bare `grep -c` over the whole file counts
every other array of the same shape and reports the wrong number.

Then ask the user to open the file once. Do not drive a browser preview.
