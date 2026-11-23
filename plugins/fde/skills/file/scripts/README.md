# Extraction scripts

Shared layer-1 machinery, python3 stdlib only. Generic: no engagement
knows about these beyond importing them.

- `pdfspec.py` — the document model. Header and footer stripping, page
  anchoring, boundary lookup, table-block collection and CSV resolution,
  page rendering. `ROOT` defaults to the current working directory; set
  `ENGAGEMENT_ROOT` to override when running from elsewhere.
- `rtfgrid.py` — recovers a table grid from `textutil -convert rtf`
  output, which is how a `.doc` keeps its cell membership when
  `pdftotext`-style column splitting would lose it.
- `coverage.py` — the gate. Every substantive source line must appear in
  the staged specimen, or the run is not done.

## Driver scripts are engagement work

One driver per source document, written next to these, reading `raw/` and
writing that source's staging folder. They stay in the engagement because
they encode that document's quirks — where its front matter ends, which
headings are real, which pages carry the running furniture.

```
python3 extract_<source>.py     raw/docs/<file>  ->  wiki/documents/<family>/_staging/<id>/
```

Keep them runnable after the run. Re-running one on unchanged input must
produce byte-identical output; if it does not, the non-determinism is a
bug to fix rather than work around. Each driver rebuilds its own staging
folder from scratch and never writes to `raw/`.
