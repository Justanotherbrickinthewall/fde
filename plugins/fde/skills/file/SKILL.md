---
name: file
description: "The wiki machinery under one name. Files client material into raw/ with a ledger row and an authority tier, builds the page-anchored specimen store, and builds the knowledge graph from it. Takes a file, several files, a folder, or no argument at all, in which case it reconciles raw/ against raw/ledger.md and files what is missing. Runs the cheap layer for everything given, then asks once whether to run the expensive layer now or later. Use whenever material arrives or is sent, when a source file changes, or when the user says \"file this\", \"log this document\", \"extract this\", \"relint the wiki\", or invokes /fde:file. The --investigate flag walks one document with you and your corrections become permanent rules. Never alters what arrived; raw/ is immutable."
---

# file

One command for everything between a document arriving and the wiki knowing
what it says.

It does three jobs in order. It files the artefact into `$REC/raw/` with a ledger
row and an authority tier. It captures the artefact into a page-anchored
specimen store, losslessly and with no judgement. It turns that store into the
knowledge graph, which is where all the judgement lives.

The skill body is generic mechanism and the template owns it. This engagement's
judgement lives in `setup/filing-rules.md`, which also carries both version
keys. Read that file before starting; its rules override every step below.
The rules for `$REC/raw/` placement and naming sit elsewhere. They are in
`setup/scoping-rules.md` § "Intake rules". The interview discipline at the
head of that file governs every question asked here.

Guardrails always apply, and `setup/guardrails.md` holds them. Six of them
bind this skill hardest:

- 1, `$REC/raw/` is immutable.
- 3, do not invent domain facts.
- 4, nothing goes to the client without review.
- 5, client documents are private.
- 7, every claim carries its tier.
- 8, nothing is lost silently.

## Finding the engagement

The umbrella is the nearest ancestor of the current directory holding a
`.engagement` file. Read that file first. It carries plain `key=value` lines:
`slug`, `docs`, `be`, `fe`, `stack`, `plugin_version`, `plugin_root`, `apps`,
`record`, `merge_into`, `integration`, `release` and `worktree`. The `docs`,
`be` and `fe` values are folder names inside the umbrella, and `be` or `fe` is
empty when that side does not exist yet. The last six keys are empty for a
one-app engagement, and the skill then behaves as it did before they existed.
`apps` lists the apps; when it is set, resolve the app first. `record` is the
record's path inside `<docs>`, and empty means the `<docs>` root. `merge_into`
is where a milestone branch merges, and empty means `main`. `integration` is
the branch the app branch merges up into, and empty means there is no such step.
`release` is the branch that deploys, and nothing touches it in away mode.
`worktree` is the naming pattern for a worktree beside its repository.
`fde:init` writes the file, and it replaces the fixed repository names these
skills used to carry.

Below, `<docs>` means the docs folder that `.engagement` names, `<be>` the
backend folder and `<fe>` the frontend folder. In a shell command they are
`$DOCS`, `$BE` and `$FE`, each an absolute path. `<record>` is the `record`
value with the app filled in, and `$REC` is `$DOCS/<record>`; where `record` is
empty, `$REC` is `$DOCS`. Every engagement path is written relative to
`<docs>`, so a command run from the umbrella needs that prefix in front of it. A session path keeps its `my-sessions/` prefix.

`${CLAUDE_PLUGIN_ROOT}` is the plugin's own directory, and every plugin path
below hangs off it. Where the variable is unset, read `plugin_root` from
`.engagement` and use that. Where that is missing too, ask the user once for
the plugin's path and write it back as `plugin_root`.

## Invocation

```
/fde:file raw/docs/handbook.pdf                      one source
/fde:file raw/docs/handbook.pdf raw/docs/form.doc    several, in one run
/fde:file raw/docs/                                  everything in a folder
/fde:file ~/Downloads/new-report.pdf                 something outside the engagement
/fde:file                                            reconcile $REC/raw/ against the ledger
/fde:file --investigate raw/docs/handbook.pdf        walk one document with the user
/fde:file --app <app> raw/other/brief.pdf            name the app it serves (apps set only)
```

With no argument it reconciles `$REC/raw/` against `$REC/raw/ledger.md` and files what
is missing. That is the normal way to catch up after a folder was copied in by
hand.

A `raw/...` path in the examples above is relative to `$REC`, so with `apps`
set, `raw/docs/handbook.pdf` under the app folder means
`$REC/raw/docs/handbook.pdf`.

Pasted text counts as an argument. It is written to a file first, because a
ledger row must point at something.

## Which app the material serves

This section applies only when `apps` is set. With `apps` empty, skip it.

Every artefact serves one app, and the app decides where the wiki write
lands. There is one ledger per app, so the folder a ledger sits in is the
answer. Reconcile mode reads that folder rather than asking again.

`--app <app>` names the app when new material arrives and the material does
not say. Ask once, in one line, where neither the material nor the flag
settles it, and never guess. New material lands under that app's `raw/`.

## The two layers, and what each costs

| Layer | Does | Cost |
|---|---|---|
| Cheap | `$REC/raw/` to a page-anchored specimen store. Lossless, makes no claim about meaning | Mechanical, fast, idempotent. Batch several documents at once |
| Expensive | Specimen store to the knowledge graph: node identity, understanding, entities, registers, links, tiers | Slow, four checkpoints wanting attention. Not before a client call |

They cost different things and want different amounts of your attention, so
they run separately. The cheap layer runs for everything in the run. The
expensive layer runs when you say so.

The two layers keep the names `extract` and `lint` in `$REC/wiki/log.md`,
`$REC/wiki/.extract-state.json` and `$REC/wiki/.lint-state.json`. The names are cache
keys and log values, so renaming them would invalidate every row written
before 07-09-26.

## The one question

After the cheap layer finishes for everything in the run, ask once, and only
once: run the expensive layer now, or later?

| Answer | What happens |
|---|---|
| Now | The expensive layer runs over everything stale, with its checkpoints |
| Now, scoped | The expensive layer runs over one family or a named list of nodes |
| Later | The run closes. The ledger rows read `extracted (pending lint)` |

Later is the right answer for a batch of several documents. Now is the right
answer for one document that is small or urgent, and that case is why the
question exists at all.

Ask per run, not per document. Skip the question when the cheap layer staged
nothing new.

Scoping the expensive layer is an override for when you want a small run.
Unscoped is the default, because its job is to make the whole graph
consistent, and consistency is not a per-document property.

## Flags

| Flag | Applies to | Behaviour |
|---|---|---|
| `--afk` | the cheap layer | The default there. Run to completion, boundaries decided by rule, every decision logged |
| `--hitl` | the cheap layer | Stop once, after proposing section boundaries, before any file is written |
| `--afk` | the expensive layer | Run to completion. Every checkpoint decided by the rules and logged for later audit through `--investigate` |
| `--hitl` | the expensive layer | The default there. Stop at each checkpoint and wait |
| `--investigate` | the whole skill | Walk one document with the user. See the section below |

With no flag, the cheap layer runs `--afk`. There is nothing to judge there.
The expensive layer then runs `--hitl`, because there is everything to judge.
A flag given on the command line applies to both layers.

`--afk` follows the global away mode, in the user's `CLAUDE.md` under "Away
mode". That rule says how the run answers its own questions and what it logs.
This skill's own stop list below still applies in `--afk`.

Both modes make identical decisions in both layers. `--hitl` only surfaces
them first. Hard stops apply in both.

## Part 1 — File into `$REC/raw/`

`$REC/raw/` is what was exchanged, exactly as it was exchanged. This skill is the
only thing that writes there, and it writes nothing else.

### Step 0 — find the delta

`$REC/raw/` is gitignored, so a fresh clone has neither the folder nor the ledger.
Create them on the first run rather than reporting them missing. Make
`$REC/raw/`, `$REC/raw/docs/` and `$REC/raw/sent/`, then write `$REC/raw/ledger.md` with its
heading, one line saying it is the arrivals log, and the empty table below.
Say that you made them, and carry on.

```markdown
# Ledger

Every artefact exchanged with the client, in the order it arrived. This is
where a tier is assigned, and it is the only authority for one.

| Date | Path | Direction | Tier | What it is | Filed |
|---|---|---|---|---|---|
```

Compare files under `$REC/raw/` against rows in `$REC/raw/ledger.md`. Report three
sets: files with no row, rows with no file, rows not marked filed. With no
argument, the files with no row are the queue. With an argument, the argument
is the queue.

An empty queue means saying so and stopping.

### Step 1 — place each artefact

Ask the direction once per batch: did this arrive from the client, or did we
generate and send it? Incoming goes to `$REC/raw/docs/`, outgoing to `$REC/raw/sent/`.
The split exists so our own generations are never read later as client-stated
fact.

Copy, never move, when the source sits outside the engagement. Keep the
original filename. On a collision append `-2`, and never overwrite.

Pasted text is written to a file first, named `<subject>-DD-MM-YY.md`,
because a ledger row must point at something.

### Step 2 — assign the tier

Ask once per artefact, and never infer it:

- `statutory` — law, regulation or a regulator's published rule. Only in
  regulated domains.
- `artefact` — a document the client produced in the course of the work:
  a form, a report, an export, a screenshot of the real system.
- `stated` — what someone told us. Meeting notes, an email answer.
- `ours` — anything we produced, including our own summaries.

The tier travels with every claim later derived from this source, so a wrong
tier here is a wrong tier everywhere. Where the answer is genuinely unclear,
take the lower tier and note why in the ledger row.

### Step 3 — write the ledger row

Append to `$REC/raw/ledger.md`, in table order: date received or sent, path
relative to `$REC/raw/`, direction, tier, one line on what it is, and `no` in the
filed column. Filed means processed into the knowledge graph, which is the
expensive layer's job, so this step never writes `yes`.

### Step 4 — supersession

A document that replaces one already in `$REC/raw/` is the case that quietly
corrupts a wiki. The new file lands, nothing contradicts it, and every claim
built on the old version stays in place looking sourced.

Ask, for each artefact filed: does this replace something already in the
ledger? Offer the rows whose file names or subjects are close. "No" is the
common answer and the question is cheap, so ask it anyway.

Where it does replace one:

1. Name the superseded file in the new row's Supersedes column, and name the
   replacement in the superseded row, so the trail reads both ways.
2. Find the claims that cite the superseded file:
   `grep -rn "<superseded filename>" $REC/wiki/ $REC/project/`. The Sources tables in
   `$REC/wiki/process.md` and `$REC/wiki/data-sources.md` hold most of them.
3. Report every hit, and write a row in `$REC/project/open-questions.md` for each,
   naming the claim and what to re-check it against.

Do not edit the claims themselves. Whether the new version actually changes a
claim is the judgement of the page that owns it, and making it here would be
filing understanding from inside the filing step.

Nothing is deleted. The superseded file stays in `$REC/raw/` and keeps its ledger
row, because `$REC/raw/` is what was exchanged and the old version was exchanged.

### Step 5 — report and carry on

Say what was filed, what tier each took, and what is still unfiled. Name any
supersessions raised and the count of claims flagged for re-check.

Part 1 is done when every artefact has a row and a tier in `$REC/raw/ledger.md`.

Then carry straight into the cheap layer for everything just filed. There is
no handoff to another command, and no queue that waits for someone to
remember it.

## Part 2 — The cheap layer, the specimen store

Mechanical, lossless, idempotent. No judgement, no understanding, no links.

The contract: after this layer, the wiki holds everything the source held. If
`$REC/raw/` were archived tomorrow, nothing is lost.

This layer batches. Several documents in one sitting is the normal use, and
each source is independent, so one failing or blocking never stops the
others. The closing report covers every source in the run, one row each, and
the ledger records each one's own status.

Nothing here writes understanding. After it, the specimen store holds
everything the sources held, and no claim whatsoever about what any of it
means.

### Step 0 — detect the delta

1. `shasum -a 256` every file under `$REC/raw/` (skip `ledger.md`, `.DS_Store`).
2. Compare against `$REC/wiki/.extract-state.json`. Absent — including a `$REC/wiki/`
   that does not exist yet — means nothing has been captured and every source
   is delta. Create every path as needed. The work queue is files whose hash
   is absent or changed, plus files whose recorded `extract_version` is below
   the one in `setup/filing-rules.md`.
3. Any file with no `$REC/raw/ledger.md` row gets one through part 1. Tier is
   assigned once and travels with every claim downstream:

| Tier | Test |
|---|---|
| `statutory` | Law, regulation, published standard, or an authority's binding instrument. Regulated domains only |
| `artefact` | A document the client produced in their real process |
| `stated` | The client said it (transcript, email) |
| `ours` | We generated it (proposal, demos, hypotheses) |

4. Empty queue means saying so and stopping.

### Step 1 — classify the source

| Kind | Handling |
|---|---|
| Structured document (PDF/DOCX report, template, spec) | Full capture, steps 2 to 5. Belongs to a family under `$REC/wiki/documents/<family>/` |
| Transcript / correspondence (md, txt) | Steps 2 and 3 only, written to `$REC/wiki/sources/<id>.md`. No family, no decomposition |
| Data file (kml, csv, xlsx) | Copy verbatim to `$REC/wiki/sources/data/<id>/`, record schema. No prose extraction |
| Binary we cannot read (dwg, proprietary) | No capture. Ledger row marked `blocked — needs conversion`, logged as visible debt |

A family is a kind of document, not one document: every sample of that kind
shares the family's node spine. A new family means creating
`$REC/wiki/documents/<family>/` with an empty `outline.md` and `samples.md`.

### Step 2 — propose section boundaries

Boundaries come from the document, never from a model's sense of where
sections should fall:

1. Prefer the document's own contents page. Also harvest its list-of-tables
   and list-of-figures if present — those give the authoritative table and
   figure inventory to reconcile against in steps 4 and 5.
2. No contents page means a heading regex over `pdftotext -layout` output
   (numbered headings, case and font-size cues).
3. Produce a boundary table: ordinal, title as printed, page range.

Reconcile the count against the source's own claims. A document declaring 88
tables where capture finds 71 has lost 17 and must say so.

`--hitl` stops here and shows the boundary table. `--afk` logs it and
continues.

### Step 3 — text, page-anchored

Per section, into
`$REC/wiki/documents/<family>/_staging/<report-id>/<NN>-<title-slug>/text.md`:

```
pdftotext -layout -f <first> -l <last> $REC/raw/<file> -
```

- Front matter: `source`, `sha256`, `pages`, `ordinal`, `title`, `extraction`
  (a one-line note on what was stripped and why).
- Insert `<!-- p.N -->` at every page break, so any line is citable as
  `(handbook.pdf p.84)` without reopening the source.
- Strip the running header and page footer, once, and capture one instance
  verbatim in the family's `00-front-matter` staging folder. Nothing else is
  stripped.
- Body goes in a fenced block. Verbatim means verbatim: no rewrapping, no
  tidying, no correcting the source's typos.

Transcripts skip staging and go straight to `$REC/wiki/sources/<id>.md`, anchored
by timestamp instead of page.

### Step 4 — tables as data

Every table in the source's list-of-tables gets a file in the section's
`tables/`:

- Resolvable columns become `t<number>-<slug>.csv`, header row from the
  source, one row per source row.
- Not cleanly resolvable (wrapped columns, merged cells, multi-row headers)
  means keeping the ASCII block as `t<number>-<slug>.txt` and marking the
  table `unresolved` in the manifest.

Assume no table extractor is installed. This is column-splitting on
`pdftotext -layout` output, so expect a meaningful unresolved rate on wide
tables. That is acceptable. What is not acceptable is a table silently
becoming prose.

A `.doc` keeps its cell membership through `textutil -convert rtf`;
`${CLAUDE_PLUGIN_ROOT}/skills/file/scripts/rtfgrid.py` recovers the grid from
that. Try it before declaring a Word table unresolved. See "Scripts" below
where `CLAUDE_PLUGIN_ROOT` is unset.

Write `tables/manifest.md`: number, title, pages, `resolved` or `unresolved`,
column count.

### Step 5 — figures as assets

Every figure in the source's list-of-figures gets a rendered asset:

```
pdftoppm -f <page> -l <page> -r 150 -png $REC/raw/<file> <out>/fig-<number>-<slug>
```

Render the whole page the figure sits on. Framing is loose; information loss
is zero. Tighter cropping is later work, never a reason to skip this —
figures that exist only as captions are the most common hole in a wiki.

Reference each asset from `text.md` at the caption's position:
`![Figure 3.7 — Site Plan](assets/fig-3.7-site-plan.png)`.

Do not use `pdfimages`. Report figures are routinely composed of thousands of
tiled image objects, and object extraction returns fragments rather than the
figure.

### Step 6 — close the cheap layer

1. Verify coverage before declaring done, with
   `${CLAUDE_PLUGIN_ROOT}/skills/file/scripts/coverage.py`. See "Scripts"
   below where `CLAUDE_PLUGIN_ROOT` is unset.
   Concatenate every staged `text.md`, normalise whitespace, and confirm
   every substantive source line (45 characters or more, running headers
   excluded) appears. Report the percentage. Below 100% names the missing
   lines.
2. Update `$REC/wiki/.extract-state.json`: per source, `sha256`,
   `extract_version`, date, sections produced, table resolved and unresolved
   counts, figure count.
3. Append one row to `$REC/wiki/log.md`, creating it with headers if absent: date,
   `extract`, mode, source, what was produced, decisions taken by rule,
   unresolved debt.
4. Ledger row becomes `extracted (pending lint)`. Only the expensive layer
   marks a row filed.
5. Report: sections staged, coverage percentage, tables resolved against
   unresolved, figures rendered, anything blocked.

Then ask the one question.

### Scripts

`${CLAUDE_PLUGIN_ROOT}/skills/file/scripts/` holds the shared machinery,
python3 standard library only. An engagement's own driver scripts add that
folder to `sys.path`. Where `CLAUDE_PLUGIN_ROOT` is unset, resolve it the way
"Finding the engagement" says, through `plugin_root` in `.engagement`.

- `pdfspec.py` — header and footer stripping, page anchoring, boundary
  lookup, table-block collection and CSV resolution, page rendering. Set
  `ROOT` from the engagement root before use.
- `rtfgrid.py` — table grid recovery from `textutil -convert rtf` output.
- `coverage.py` — the step-6 gate.
- `README.md` — what the machinery does and what it does not attempt.

Per-document driver scripts are engagement work, and they live in
`<docs>/scripts/`. Write them there, keep them runnable, and record in the
log that a run is reproducible by re-running one.

### Hard stops in the cheap layer — both modes

Stop and ask, even in `--afk`:

- Overwriting or deleting existing captured content where the new capture
  produces fewer sections, fewer tables, or lower coverage than the recorded
  state. Regression is never applied silently.
- Coverage below 95% after step 6. Something structural is wrong; do not
  stage a lossy specimen as if it were complete.

### Rules for the cheap layer

- Never modify `$REC/raw/`.
- Never interpret. No summarising, no classifying a block as fixed or slot,
  no linking, no entity creation. Those belong to the expensive layer and
  doing them here breaks idempotency.
- Silent loss is the only unrecoverable failure. Visible debt — `unresolved`,
  `blocked`, a named gap in the log — is fine and expected.
- This layer makes no claim about what a section is. Staging folders are
  named from the source's own ordinal and title. Canonical identity is
  assigned by the expensive layer.
- Re-running on unchanged input must produce byte-identical output. If it
  does not, the non-determinism is a bug to fix, not to work around.
- A correction to how something was captured goes in `setup/filing-rules.md`
  under the cheap layer section, never in this file.

## Part 3 — The expensive layer, the knowledge graph

All judgement lives here. This is the slow layer and the re-runnable one.

`lint_version` in `setup/filing-rules.md` is the cache key. Bumping it marks
every node stale in one line, and only this layer re-runs; capture stays
cold. That is what makes a doctrine change a re-run rather than a rebuild.

### It reads the specimen store, never `$REC/raw/`

This layer never re-reads a source document. By the time it runs, capture has
already moved every word, table and figure into the specimen store, and that
store is the only content input. Naming a PDF here is a category error: its
content is already in `$REC/wiki/`.

The one thing it reads outside `$REC/wiki/` is `$REC/raw/ledger.md`, and only for the
tier column. Tier is assigned once, at arrival, and is the authority for
resolving contradictions. It reads no artefact in `$REC/raw/` and writes nothing
there but a row's filing status.

### What this layer actually does

Everything left after capture is judgement:

1. Decide what each captured section is and put it in the right folder —
   canonical node identity, by concept rather than by the source's chapter
   number.
2. Write the understanding — one `index.md` per node, the single point of
   meaning.
3. Pull out what repeats — a record type read by more than one node becomes a
   register; a persona, standard, region or technology becomes an entity.
4. Connect it all with links, inline, so a human can read one page start to
   finish and an agent can reach the right page in one hop. Every link target
   must exist.
5. Reconcile — tiers, contradictions, absences, new questions.

Moving things into the right place and wiring them together is the work.
Nothing here re-reads a source, and nothing here edits a specimen.

### The four checkpoints

In order: canonical identity mapping, then entity and register promotions,
then tier conflicts, then new open questions. `--hitl` stops at each one and
waits. `--afk` decides each by the rules and logs it for audit through
`--investigate`.

### Step 0 — detect stale nodes

1. Read `$REC/wiki/.lint-state.json`. Absent means nothing has been filed yet and
   every staged node is new. A node is stale if any of these hold: its
   specimen hash changed, its recorded `lint_version` is below the one in
   `setup/filing-rules.md`, it is newly staged, or the user named it.
2. The work queue is the stale nodes. Empty means saying so and stopping.
3. Never touch a node that is not stale. Delta only.

### Step 1 — assign canonical identity

Staged sections carry the source's own ordinal and title. They carry no claim
about what they are. Resolve that here.

For each staged section, decide: does it match an existing canonical node in
`$REC/wiki/documents/<family>/outline.md`?

On a cold start there is no `outline.md` and no `$REC/wiki/` at all. That is
normal, not an error: every staged section is then a new node, and the
family's spine is written from scratch. Create every path as needed.

| Case | Action |
|---|---|
| Matches an existing node | Move the staged folder to `<node>/specimens/<report-id>/`. Add a column to `outline.md` recording this report's chapter number and pages |
| No match | New node. The slug is the concept, never the number — `payment-terms`, not `ch04-...` |
| Existing node absent from this report | `absent_in` gains the report. Candidate optional — resolved in step 4, never here |
| One staged section spans two canonical nodes, or two staged sections collapse into one | Split or merge. `outline.md` records the relationship |

This layer places specimens; it never rewrites their content. Moving a folder
is placement. Editing a `text.md` is a bug.

`outline.md` is the family's spine: canonical node order down the rows, one
column per sample giving that sample's chapter number and pages. A sample
with more chapters adds a column, never a rename.

A node is a folder:

```
$REC/wiki/documents/<family>/
  outline.md              canonical order × each sample's position
  samples.md              per-sample attributes that explain divergence
  <node-slug>/
    index.md              the understanding, written by the expensive layer
    specimens/<id>/
      text.md             verbatim, page-anchored, written by the cheap layer
      tables/*.csv
      assets/*.png
```

Checkpoint: show the mapping table before moving anything.

### Step 2 — write the node index

`<node>/index.md` is the single point of understanding, built from every
specimen, read by default. One home per fact: a fact lives on this page or on
the entity it belongs to, never on both. In order:

1. Front matter — facts about the node only: `node`, `title`, `tags`,
   `automatability`, `seen_in`, `absent_in`, `mandatory`, `lint_version`.
   Never relationships.
2. Essence — what the section is, who drafts it.
3. Blocks classified: `fixed`, `slot`, `computed`, `specialist`, `derived`.
4. Inputs table — what must exist before drafting, from whom, what it gates.
5. Structure — the findings that matter, each naming its evidence.
6. Template with `{variables}` marked.
7. Variables table — type, supplier, example value from each sample,
   labelled as instance data.
8. Assertions — the checkable constraints.
9. Questions raised.
10. Divergence across samples.

Raw text never enters the index. Analysis never enters a specimen.

The block classification is what makes the graph buildable, so it carries
weight. `fixed` becomes standing content, `slot` becomes an intake field with
a named supplier, `computed` becomes deterministic code, `specialist` becomes
a human approval gate, and `derived` becomes a generation spec over other
nodes.

### Step 3 — promote entities and registers

Read the node for things that are not prose:

- A repeating record type read by more than one node becomes
  `$REC/wiki/entities/registers/<name>.md` with a field table.
- Standing text fixed by a chosen option becomes
  `$REC/wiki/entities/technologies/<option>.md`.
- Content identical for any project in a geography becomes
  `$REC/wiki/entities/regions/<region>.md`.
- A persona, source, standard or format named anywhere gets its entity file,
  created before the node is filed.

Registers are the product's data model in draft. Treat them with that weight.
The tell is one record type printed several ways: a price list appearing in
three chapters as three tables is one register with three views, not three
tables.

Checkpoint: list the proposed promotions with the evidence for each.

### Step 4 — reconcile

1. Tiers. Every claim inherits its source's tier from that source's row in
   `$REC/raw/ledger.md`, which is where the tier is assigned and the only
   authority for it. `$REC/wiki/sources/index.md` is a view over those rows,
   written in step 5 and never read as the source of truth. Precedence:
   `statutory` > `artefact` > `stated` > `ours` (guardrail 7). On
   contradiction the higher tier wins and the loser takes a dated correction
   note. A same-tier contradiction cannot be resolved mechanically — it is an
   open question, and a hard stop.
2. Promotion. A claim confirmed by a higher-tier source records the move:
   `tier: ours → stated (M1 2:03:59)`. Promotion history shows which
   pre-sales assumptions have survived contact.
3. Absence. A node absent from a sample is read against `samples.md`
   attributes. Absent means optional only when the samples are otherwise
   comparable; otherwise conditional, and naming the condition is the
   finding. With one sample nothing is known to be mandatory.
4. Questions. New uncertainty goes to the node's own "Questions raised". This
   layer never writes to `$REC/project/`.
5. Links. Every entity, persona, source, standard or sibling node mentioned
   for the first time becomes an inline link. Verify every target exists.

Checkpoint: tier conflicts and new questions, before writing.

### Step 5 — close the expensive layer

1. Refresh the family `index.md`, `outline.md`, `samples.md`, and
   `$REC/wiki/sources/index.md`.
2. Verify no dead links: every `](` target under `$REC/wiki/` resolves.
3. Update `$REC/wiki/.lint-state.json`: per node, specimen hashes, `lint_version`,
   date, what was produced.
4. Append one row to `$REC/wiki/log.md`, creating it with headers if absent: date,
   `lint`, mode, nodes touched, promotions, tier corrections, questions
   raised, decisions taken by rule.
5. Mark the ledger row `filed → <nodes>`.
6. Report what changed and what it raises. Next steps and milestones belong
   to `/fde:fdc-session`, built from the nodes.

### Hard stops in the expensive layer — both modes

Stop and ask, even in `--afk`:

- Deleting or superseding an existing node, or dropping content a previous
  run produced.
- A same-tier contradiction. The cascade cannot rank them, and a guess
  fabricates a fact (guardrail 3).

### Three rules that are mechanism, not judgement

The filing rules are not in this file. `setup/filing-rules.md` holds them,
they override everything above, and they are the reason two engagements
running the same skill produce different wikis. An empty section there means
this engagement has not formed an opinion yet, which `--investigate` is how
you fix.

These three are mechanism rather than judgement, so they live here and are
not negotiable per client:

- Link inline, never hand-write backlinks. The first mention of a persona,
  source, term, node or question becomes a link. Reverse lookup is
  `grep -rl`. A stored second copy of a relationship has nothing keeping it
  honest, and a stale backlink sends an agent down exactly the wrong path.
- A link target must exist before the page is filed. Naming a persona with no
  file means creating it first. This is how the entity folders fill up, by
  construction. Dead links are the one failure this structure cannot absorb.
- Front matter holds facts about the page, never relationships. Anything
  expressible as a link is a link. The exception is a checkable assertion,
  which is recorded explicitly because it is a test rather than a
  relationship.

## `--investigate` — the tuning loop

Two purposes: you verify filing instead of trusting it, and your corrections
permanently improve the pipeline. It is not a bulk processor.

It is also the audit path for `--afk` runs. Anything an unattended run
decided by rule is reviewable here, because both modes make the same
decisions and log them the same way.

Corrections are written to `setup/filing-rules.md`, never to a skill body.
The skill body is generic mechanism and the template owns it; what you learn about
this client's documents belongs to this engagement.

`--investigate` runs `--hitl` by default, meaning an interactive walkthrough
that stops after each section and absorbs corrections as they come. With
`--afk` it produces the full findings report in one pass, no stops, writing
nothing to the wiki and adding no rule. You read the report and decide what
to act on.

### Step 0 — orient

1. Identify the target: a raw document, a wiki node, a family, or a run-log
   entry. Ask only if it is genuinely ambiguous.
2. Pick the mode from the target's state:

| Target state | Mode | What is shown |
|---|---|---|
| Not yet captured | dry-run | What the cheap layer would stage and what the expensive layer would do with it. Nothing written until the end |
| Captured, not filed | pre-lint | Staged sections and the proposed canonical mapping |
| Filed | audit | What was produced, quoting the actual wiki lines |
| A run-log entry | review | Every decision that run took by rule, with its uncertainty |

3. Say how many sections the walkthrough covers before starting.

### Step 1 — walk

One section, or a small coherent batch, at a time. Per item:

| Field | Content |
|---|---|
| Source | Section, table or figure, with page anchor |
| Layer | Cheap (content) or expensive (judgement) — which layer owns this decision |
| Verdict | place, transform, promote (to entity or register), or discard |
| Destination | Exact path plus the section within it. Dry-run: proposed. Audit: actual, quoted |
| Why | The rule driving it, named, with the file it came from |
| Tier | The claim's authority tier and where it came from |

Discards are always shown, never silent. You must see what would be dropped
and why.

Pause after each section: correct, or continue. Never dump the whole document
at once.

### Step 2 — absorb corrections

When you correct a mapping:

1. Apply it to the current walkthrough. In audit mode, fix the wiki now.
2. Decide which layer the correction belongs to. A correction about what was
   captured is the cheap layer. A correction about what it means or where it
   goes is the expensive layer. Getting this wrong puts a judgement rule in
   the deterministic layer and breaks idempotency.
3. Generalise it into a rule and confirm the wording with you before writing
   it.
4. Append it to the right section of `setup/filing-rules.md`, dated with
   provenance: `— 18-08-26, from investigate on handbook.pdf`. Amend rather
   than delete when it modifies an existing rule; the original reading stays
   visible.

| Correction about | Section of `setup/filing-rules.md` | Then |
|---|---|---|
| What was captured or dropped | Cheap layer | bump `extract_version` in its front matter |
| What a section is, or where it goes | Expensive layer | bump `lint_version` in its front matter |

5. Bumping the version is not optional. It is what marks the affected work
   stale, so the correction actually reaches the wiki on the next run. A rule
   written without a bump changes nothing.
6. If the correction reveals a structural gap — a missing folder, a page type
   that does not exist — propose the change and, on approval, say plainly
   that it is a mechanism gap. Mechanism belongs to the template and goes back by
   pull request; do not patch a skill body in place.
7. If the correction is not client-specific at all — it would hold on any
   engagement — record it in `$REC/project/findings.md` as a candidate mechanism
   fix, then still write the client-specific version to the rules file so
   this engagement gets it today.

### Step 3 — close the walk

- Dry-run: on final approval, run the two layers for the agreed filing.
- Audit: summarise the corrections applied.
- Always report: rules added, to which section, whether a version moved, and
  anything logged as a mechanism gap.

### Rules for `--investigate`

- Never write to the wiki during a dry-run walkthrough until the user
  approves that section.
- Every verdict names its rule. Where no existing rule covers an item, say so
  plainly — that item is exactly where a new rule should be born.
- Never edit a skill body. Rules go to `setup/filing-rules.md`; mechanism
  fixes go back to the template by pull request.
- `$REC/raw/` stays untouched.
- A correction given once becomes a rule. Applying it to this document only
  and moving on wastes the walkthrough, which is the most expensive thing we
  do.

## Rules for every run

- One home per fact. A fact lives on exactly one page and every other page
  links to it. A second copy has nothing keeping it honest.
- Delta only. A filed row is settled; re-open it only when a newer artefact
  contradicts it.
- Partial work is recorded, never hidden.
- Unknown is an open question, not a guess (guardrail 3).
- Nothing client-facing is sent. Flag it for the user's review (guardrail 4).
- Outside `$REC/raw/`, this skill writes only to `$REC/wiki/`, plus the
  `$REC/project/open-questions.md` rows a supersession raises. Milestones and next
  steps belong to `/fde:fdc-session`, built from the nodes.
- `$REC/wiki/process.md` and `$REC/wiki/data-sources.md` are nodes like any other. The
  expensive layer may supersede their `ours`-tier content with `artefact`
  material under the normal tier rules, and the losing claim takes a dated
  correction note.

