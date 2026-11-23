# Building the prototype

This file is for the build subagent, and for the subagent that makes each
round of changes. The orchestrator hands it over and does not read it
again. Read it whole before writing a line, then read `brief.md` and
`context.md` in the session folder. Read `reference/exemplar.md` before
writing the first line of a new prototype.

This engagement's corrections live in `setup/planning-rules.md` §
"Prototype rules". Those rules override the steps below. Guardrails apply
throughout, especially 3 (an unknown is an open question, never a plausible
guess), 5 (client data stays local) and 9 (no product code during scoping).

## Ground it

`context.md` summarises the ground, and it names the files behind each
point. Open a named file when the brief needs its detail. Use real field
names and real row labels. A prototype the client does not recognise is
wasted work.

The prototype follows the existing UI patterns that `context.md` names:
the frontend screens and components (read-only), the tokens in
`setup/design.md` and `styles/app.css`, and any prototype already in
`project/prototypes/`. A client who sees one look in the prototype and
another in the product learns that neither is real.

## Where the prototype fills a form

Where this one fills a form, do the five steps below in order. Where it
reworks a screen that fills no form, use the steps that apply, and say in
your report which ones you skipped.

1. Build the field model first. Give one entry per field: id, section,
   label carrying the form's own numbering, supplier hint, formula and
   dependencies. Sections come from the form's own block ranges, not from
   a grouping you find tidy.
2. Give the record its shape. Every field holds facts, never a value. A
   fact carries its value, its source, that source's tier and its date.
   Two conflicting facts live on one field at once, and the loser stays
   visible. A higher tier wins and records the rule. A same-tier conflict
   is a human decision, and the system never picks.
3. Use six states for the whole interaction: open, inferred, provisional,
   conflict, awaiting and settled. Colour them consistently and badge them
   in plain words.
4. Script one walkthrough as beats. Each beat is a chip the user clicks,
   and branches converge back to the spine. The script contains at least a
   document upload, an inferred block needing confirmation, a computed
   cascade, one human gate from the guardrails, one same-tier conflict,
   one round trip awaiting a named person, a confirm sweep, the
   stragglers, the preview, sign-off and reopen. Seed three records: one
   empty that runs the script, one partial, and one signed where reopen
   voids the signature without deleting it.
5. Render the document as the document. The preview is the extracted grid,
   exactly, and never the field list. Map fields into rows. A row with no
   fact renders as a visible gap, not as blank space. Template pre-prints
   render differently from record values. Exports reuse the same renderer.

## Write it and check it

Write the file to `project/prototypes/<slug>.html` inside the record, as the
brief names it.

1. It is one self-contained file. No fragments, no build step and no
   dependencies.
2. Client data stays local. No external service, no CDN and no font fetch.
3. A footer says the file is a scoping prototype under guardrail 9, not
   product code, and that its figures are demo data. Any invented number
   is labelled in its own cell.
4. An unknown is shown as a gap, never filled with a plausible number.
5. Extract the script block and run `node --check` on it.
6. Where a document preview renders, assert its row count equals the
   specimen CSV's row count.
7. Drive a browser only if the brief to you says so. Otherwise stop at the
   two checks above.

## A round of changes

Before changing the file, copy it to
`<session>/versions/<slug>-v<N>.html`, where N is the version being
replaced. Make only the change the round asks for. Never rebuild a file
wholesale when a change was asked for.

## Report back

Keep the report to about ten lines. Say what the walkthrough now covers,
every `Must show` row the file does not yet reach, every gap it
deliberately shows, and every invented figure by name. Say whether both
checks passed. Name any open question the build raised.

Never write `wiki/` or a milestone body. Never commit. The orchestrator
commits.

Follow the global rule for subagent models, name the model on any subagent
you dispatch, and tell it the same rule.
