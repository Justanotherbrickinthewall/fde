#!/usr/bin/env python3
"""The record lint: everything `check_links.py` does not catch.

Calls `check_links.check()` for dead relative links and adds the checks the
spec asks for on top of it:

- every milestone's `status:` first word is one of the five the method
  defines
- every milestone's `waits-on:` is `none` or a list of milestone ids that
  exist as files
- every milestone's `delivery:` is present
- a `ready` milestone holds its required parts: one H1, and headings for
  why now, in scope, out of scope, guardrails, rests on and walk this.
  `draft`, `building`, `built` and `dropped` are not checked for parts —
  only `ready` is a promise the AIE can start on.
- every open question in `project/open-questions.md` has an owner in its
  "Who can answer" cell
- every live guardrail in `setup/guardrails.md` carries a `Source:` line. A
  guardrail whose heading or body says withdrawn or removed is not live.
- no page under `project/` or `wiki/` is unlinked: every `.md` there is the
  target of a markdown link from some other `.md` in the repository

The unlinked check excludes the specimen store under `wiki/documents/`: it
is `/file-fde`'s cheap-layer output, page-anchored and lossless, and nobody
links to a page of it by hand. The rule for "specimen leaf", read off the
layout `/file-fde` writes: a file named `outline.md` or
`samples.md` (family-level bookkeeping, one pair per family), or a file
anywhere under a `specimens/`, `specimen-meta/` or `_staging/` directory
(the per-node and per-specimen mechanical layer, and the pre-lint holding
pen). An `index.md` is never a specimen leaf — it is the written
understanding of a node from `/file-fde`'s expensive layer, and it stays in
the check.

The same exclusion covers one more mechanical shape: `text.md` or
`schema.md` sitting directly under a `wiki/sources/data/<source>/` folder.
That is `/file-fde`'s cheap-layer specimen for a data file, the same
page-anchored, lossless output as a `wiki/documents/` leaf, and nobody
links to it by hand either. `wiki/sources/index.md` and `wiki/sources/m2.md`
are not under `data/` and stay in the check, and so does everything else
under `project/` and `wiki/`.

One line per finding: the path, then what is wrong. Run it from the docs
repository root, or pass that root as an argument (this script ships in
the fde plugin, so it no longer sits inside the repository it checks).
The root it resolves is the same one it passes to `check_links`. An optional
second argument is the record root, for an engagement with `record=apps/<app>`:
the project and wiki checks read it, while links and guardrails stay on the
docs root. It defaults to the docs root.

    python3 scripts/lint_record.py
    python3 scripts/lint_record.py /path/to/some-docs
    python3 scripts/lint_record.py /path/to/some-docs /path/to/some-docs/apps/<app>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_links

STATUSES = ("draft", "ready", "building", "built", "dropped")

MILESTONE_ID = re.compile(r"^(m\d+)-")
MILESTONE_ID_ONLY = re.compile(r"^m\d+$")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)\s*$", re.MULTILINE)
GUARDRAIL_HEADING = re.compile(r"^### +(\d+)\.\s*(.*?)\s*$", re.MULTILINE)
TABLE_ROW = re.compile(r"^\|(.*)\|\s*$")
SEPARATOR_CELL = re.compile(r"^:?-+:?$")

# "Why now" is prose under the title in the milestone template, not a
# heading like the rest, so a part counts as present if a heading contains
# it or a line of body text opens with it.
READY_PARTS = (
    ("why now", "Why now"),
    ("in scope", "In scope"),
    ("out of scope", "Out of scope"),
    ("guardrails", "Guardrails"),
    ("rests on", "Rests on"),
    ("walk", "Walk this"),
)


def parse_front_matter(text: str) -> dict[str, str]:
    match = FRONT_MATTER.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def milestone_files(root: Path) -> list[Path]:
    directory = root / "project" / "milestones"
    if not directory.is_dir():
        return []
    return sorted(p for p in directory.glob("m*.md") if MILESTONE_ID.match(p.name))


def check_status(root: Path) -> list[str]:
    findings = []
    for path in milestone_files(root):
        fields = parse_front_matter(path.read_text(encoding="utf-8"))
        status = fields.get("status", "")
        first_word = status.split()[0] if status.split() else ""
        if first_word not in STATUSES:
            findings.append(
                f"{path.relative_to(root)}: status is {status!r}, "
                f"not one of {', '.join(STATUSES)}"
            )
    return findings


def check_waits_on(root: Path) -> list[str]:
    files = milestone_files(root)
    ids = {MILESTONE_ID.match(p.name).group(1) for p in files}
    findings = []
    for path in files:
        fields = parse_front_matter(path.read_text(encoding="utf-8"))
        if "waits-on" not in fields:
            continue
        value = fields["waits-on"]
        head = value.partition(" — ")[0].strip()
        if head == "none":
            continue
        candidates = [c.strip() for c in head.split(",")]
        bad = not candidates or any(
            not MILESTONE_ID_ONLY.match(c) or c not in ids for c in candidates
        )
        if bad:
            findings.append(
                f"{path.relative_to(root)}: waits-on {value!r} is not 'none' "
                "or a comma-separated list of milestone ids that exist"
            )
    return findings


def check_delivery(root: Path) -> list[str]:
    findings = []
    for path in milestone_files(root):
        fields = parse_front_matter(path.read_text(encoding="utf-8"))
        if not fields.get("delivery", "").strip():
            findings.append(f"{path.relative_to(root)}: delivery is missing")
    return findings


def check_ready_parts(root: Path) -> list[str]:
    findings = []
    for path in milestone_files(root):
        text = path.read_text(encoding="utf-8")
        fields = parse_front_matter(text)
        status_words = fields.get("status", "").split()
        if not status_words or status_words[0] != "ready":
            continue
        headings = [(len(level), title.lower()) for level, title in HEADING.findall(text)]
        lines_lower = [line.strip().lower() for line in text.splitlines()]
        missing = []
        if sum(1 for level, _ in headings if level == 1) != 1:
            missing.append("H1")
        for needle, label in READY_PARTS:
            in_heading = any(needle in title for _, title in headings)
            in_prose = any(line.startswith(needle) for line in lines_lower)
            if not (in_heading or in_prose):
                missing.append(label)
        if missing:
            findings.append(
                f"{path.relative_to(root)}: ready milestone is missing "
                + ", ".join(missing)
            )
    return findings


def check_open_questions(root: Path) -> list[str]:
    path = root / "project" / "open-questions.md"
    if not path.is_file():
        return [f"{path.relative_to(root)}: file is missing"]
    findings = []
    owner_col: int | None = None
    for line in path.read_text(encoding="utf-8").splitlines():
        match = TABLE_ROW.match(line.strip())
        if not match:
            owner_col = None
            continue
        cells = [c.strip() for c in match.group(1).split("|")]
        if all(SEPARATOR_CELL.match(c) for c in cells):
            continue
        header_hit = next((i for i, c in enumerate(cells) if c.lower() == "who can answer"), None)
        if header_hit is not None:
            owner_col = header_hit
            continue
        if owner_col is None or not re.fullmatch(r"Q\d+", cells[0]):
            owner_col = None
            continue
        owner = cells[owner_col] if owner_col < len(cells) else ""
        if not owner.strip():
            findings.append(f"{path.relative_to(root)}: {cells[0]} has no owner in 'Who can answer'")
    return findings


def check_guardrails(root: Path) -> list[str]:
    path = root / "setup" / "guardrails.md"
    if not path.is_file():
        return [f"{path.relative_to(root)}: file is missing"]
    text = path.read_text(encoding="utf-8")
    matches = list(GUARDRAIL_HEADING.finditer(text))
    findings = []
    for i, match in enumerate(matches):
        number, title = match.group(1), match.group(2)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[match.end():end]
        combined = f"{title}\n{body}".lower()
        if "withdrawn" in combined or "removed" in combined:
            continue
        if not re.search(r"^source:", body, re.MULTILINE | re.IGNORECASE):
            findings.append(f"{path.relative_to(root)}: guardrail {number} ({title}) has no Source line")
    return findings


SPECIMEN_LEAF_NAMES = {"outline.md", "samples.md"}
SPECIMEN_LEAF_DIRS = {"specimens", "specimen-meta", "_staging"}
DATA_SPECIMEN_LEAF_NAMES = {"text.md", "schema.md"}


def is_specimen_leaf(root: Path, path: Path) -> bool:
    """A mechanical leaf of a specimen store: `wiki/documents/` or
    `wiki/sources/data/`.

    Under `wiki/documents/`, true for `outline.md` and `samples.md` (family
    bookkeeping) and for anything under a `specimens/`, `specimen-meta/` or
    `_staging/` directory (the per-node and per-specimen mechanical layer).
    `index.md` is never a specimen leaf there — it is the page `/file-fde`'s
    expensive layer writes, and the one file per node a person actually
    links to.

    Under `wiki/sources/data/`, true for `text.md` or `schema.md` sitting
    directly in a `<source>/` folder — the same mechanical, page-anchored
    output for a data source specimen. Not true one level up: `wiki/sources/
    index.md` and `wiki/sources/m2.md` stay in the check.
    """
    try:
        parts = path.relative_to(root / "wiki" / "documents").parts
    except ValueError:
        pass
    else:
        if path.name in SPECIMEN_LEAF_NAMES:
            return True
        if any(part in SPECIMEN_LEAF_DIRS for part in parts[:-1]):
            return True

    try:
        data_parts = path.relative_to(root / "wiki" / "sources" / "data").parts
    except ValueError:
        return False
    return len(data_parts) == 2 and path.name in DATA_SPECIMEN_LEAF_NAMES


def check_unlinked(root: Path, record: Path | None = None) -> list[str]:
    # Links are read and resolved from the docs root; the pages checked sit under the record.
    record = record or root
    candidates = check_links.drop_ignored(root, check_links.candidate_files(root))
    linked: set[Path] = set()
    for path in candidates:
        raw = path.read_text(encoding="utf-8", errors="replace")
        suffix = path.suffix.lower()
        if suffix == ".html":
            found = list(check_links.targets_in(check_links.mask_code(raw, True)))
            found += list(check_links.style_targets_in(raw))
        elif suffix == ".css":
            found = list(check_links.css_targets_in(raw))
        else:
            found = list(check_links.targets_in(check_links.mask_code(raw, False)))
        for _line, target in found:
            resolved = check_links.resolve(root, path, target)
            if resolved is None or not resolved.exists():
                continue
            linked.add(resolved.resolve())

    findings = []
    for base in ("project", "wiki"):
        directory = record / base
        if not directory.is_dir():
            continue
        for path in sorted(directory.rglob("*.md")):
            if is_specimen_leaf(record, path):
                continue
            if path.resolve() not in linked:
                findings.append(f"{path.relative_to(record)}: not linked from any other page")
    return findings


def check(root: Path, record: Path | None = None) -> list[str]:
    record = record or root
    findings: list[str] = []
    _checked, dead = check_links.check(root)
    findings.extend(dead)
    scoped: list[str] = []
    for fn in (check_status, check_waits_on, check_delivery, check_ready_parts, check_open_questions):
        scoped.extend(fn(record))
    scoped.extend(check_unlinked(root, record))
    # Record findings print relative to the docs root, so a per-app path reads apps/<app>/project/...
    prefix = record.relative_to(root).as_posix() + "/" if record != root else ""
    findings.extend(prefix + f for f in scoped)
    findings.extend(check_guardrails(root))
    return findings


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    record = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else root
    findings = check(root, record)
    for line in findings:
        print(line)
    print(f"{len(findings)} finding(s).")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
