"""One test per check in `lint_record.py`, each against a temporary
repository fixture that carries a passing case and a failing case.

Run it either way:

    python3 -m pytest scripts/test_lint_record.py
    python3 scripts/test_lint_record.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lint_record


def _milestone(root: Path, name: str, front_matter: str, body: str = "") -> None:
    directory = root / "project" / "milestones"
    directory.mkdir(parents=True, exist_ok=True)
    (directory / name).write_text(f"---\n{front_matter}\n---\n{body}")


def test_status_first_word():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _milestone(root, "m01-good.md", "status: built 01-09-26\ndelivery: none")
        _milestone(root, "m11-bad.md", "status: blocked\ndelivery: none")

        findings = lint_record.check_status(root)

        assert len(findings) == 1, findings
        assert "m11-bad.md" in findings[0]
        assert "m01-good.md" not in "".join(findings)


def test_waits_on_resolves():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _milestone(root, "m01-a.md", "status: built\ndelivery: none\nwaits-on: none")
        _milestone(
            root,
            "m11-b.md",
            "status: built\ndelivery: none\nwaits-on: m01 — a reason",
        )
        _milestone(
            root,
            "m12-c.md",
            "status: draft\ndelivery: none\nwaits-on: m01, m11",
        )
        _milestone(
            root,
            "m13-d.md",
            "status: draft\ndelivery: none\nwaits-on: m99",
        )
        _milestone(
            root,
            "m14-e.md",
            "status: draft\ndelivery: none",
        )

        findings = lint_record.check_waits_on(root)

        assert len(findings) == 1, findings
        assert "m13-d.md" in findings[0]


def test_delivery_present():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _milestone(root, "m01-good.md", "status: built\ndelivery: none — shared capability")
        _milestone(root, "m11-also-good.md", "status: built\ndelivery: 1")
        _milestone(root, "m12-bad.md", "status: draft\ndelivery:")
        _milestone(root, "m13-missing.md", "status: draft")

        findings = lint_record.check_delivery(root)

        assert {f.split(":")[0] for f in findings} == {
            "project/milestones/m12-bad.md",
            "project/milestones/m13-missing.md",
        }, findings


def test_ready_parts():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        complete = """# Applications draft end to end

Why now: the wiki node changed.

## In scope

Everything.

## Out of scope

Nothing else.

## Guardrails

Guardrail 3.

## Rests on

The wiki.

## Walk this

1. Click it.
"""
        _milestone(root, "m01-complete.md", "status: ready\ndelivery: none", complete)

        thin = """# A thin one

## In scope

Only this.
"""
        _milestone(root, "m11-thin.md", "status: ready\ndelivery: none", thin)

        # A built milestone this thin is history, not a promise, so it is
        # never checked for parts.
        _milestone(root, "m12-built-thin.md", "status: built\ndelivery: none", thin)

        findings = lint_record.check_ready_parts(root)

        assert len(findings) == 1, findings
        assert "m11-thin.md" in findings[0]
        for part in ("Why now", "Out of scope", "Guardrails", "Rests on", "Walk this"):
            assert part in findings[0], findings[0]
        assert "m12-built-thin.md" not in findings[0]


def test_open_questions_owner():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        directory = root / "project"
        directory.mkdir(parents=True)
        (directory / "open-questions.md").write_text(
            "# Open questions\n\n"
            "| ID | Question | Raised | Blocks | Who can answer | Status |\n"
            "|---|---|---|---|---|---|\n"
            "| Q1 | Has an owner? | 01-09-26 | nothing | Alex Rivera | open |\n"
            "| Q2 | Has an unnamed role as owner? | 01-09-26 | nothing | Client IT (unnamed) | open |\n"
            "| Q3 | Has no owner? | 01-09-26 | nothing |  | open |\n"
            "\n"
            "| ID | Node |\n"
            "|---|---|\n"
            "| Q1 | some/node.md |\n"
        )

        findings = lint_record.check_open_questions(root)

        assert len(findings) == 1, findings
        assert "Q3" in findings[0]


def test_guardrails_source():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        directory = root / "setup"
        directory.mkdir(parents=True)
        (directory / "guardrails.md").write_text(
            "# Guardrails\n\n"
            "### 1. Has a source\n\n"
            "Some rule.\n\n"
            "Source: ours. Inferred 07-09-26.\n\n"
            "### 2. Has no source\n\n"
            "Some other rule with nothing saying where it came from.\n\n"
            "### 3. Withdrawn, and never had a source\n\n"
            "**Withdrawn 04-09-26.** This guardrail no longer binds anything.\n"
        )

        findings = lint_record.check_guardrails(root)

        assert len(findings) == 1, findings
        assert "guardrail 2" in findings[0]


def test_unlinked_pages_excludes_specimen_leaves():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        family = root / "wiki" / "documents" / "main-report"
        (family / "study-area" / "specimens" / "r1" / "tables").mkdir(parents=True)
        (family / "specimen-meta" / "r1").mkdir(parents=True)
        (family / "_staging" / "r2" / "01-intro").mkdir(parents=True)
        node = family / "impact-assessment"
        node.mkdir(parents=True)

        # Specimen-store leaves: nobody links to these by hand.
        (family / "outline.md").write_text("# Outline\n")
        (family / "samples.md").write_text("# Samples\n")
        (family / "study-area" / "specimens" / "r1" / "text.md").write_text("body\n")
        (family / "study-area" / "specimens" / "r1" / "tables" / "manifest.md").write_text("t1\n")
        (family / "specimen-meta" / "r1" / "boundaries.md").write_text("bounds\n")
        (family / "_staging" / "r2" / "01-intro" / "text.md").write_text("staged\n")

        # A written node page: not a specimen leaf, stays checked.
        (node / "index.md").write_text("# Impact assessment\n")

        # wiki/sources/data/<source>/text.md and schema.md are specimen
        # leaves too: /file-fde's cheap-layer output, page-anchored and
        # nobody links to it by hand.
        electrical = root / "wiki" / "sources" / "data" / "electrical-calculations"
        electrical.mkdir(parents=True)
        (electrical / "text.md").write_text("data\n")
        kml = root / "wiki" / "sources" / "data" / "site-boundary-kml"
        kml.mkdir(parents=True)
        (kml / "schema.md").write_text("schema\n")

        # A file one level deeper, and index.md at the data/ level itself,
        # are not "directly under a <source>/ folder": both stay checked.
        nested = electrical / "extra" / "text.md"
        nested.parent.mkdir(parents=True)
        nested.write_text("nested\n")
        (root / "wiki" / "sources" / "data" / "index.md").write_text("# Data\n")

        findings = lint_record.check_unlinked(root)

        flagged = {f.split(":")[0] for f in findings}
        assert flagged == {
            "wiki/documents/main-report/impact-assessment/index.md",
            "wiki/sources/data/electrical-calculations/extra/text.md",
            "wiki/sources/data/index.md",
        }, flagged


def test_unlinked_pages():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        project = root / "project"
        wiki = root / "wiki"
        project.mkdir(parents=True)
        wiki.mkdir(parents=True)

        (project / "index.md").write_text("[linked](linked.md)\n")
        (project / "linked.md").write_text("# Linked\n\n[back](index.md)\n")
        (wiki / "orphan.md").write_text("# Nobody points here\n")

        findings = lint_record.check_unlinked(root)

        assert len(findings) == 1, findings
        assert "orphan.md" in findings[0]


def test_per_app_record_root():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        rec = root / "apps" / "acme"
        _milestone(rec, "m01-bad.md", "status: blocked\ndelivery: none")
        (root / "setup").mkdir()
        (root / "setup" / "guardrails.md").write_text("### 1. No sourceless rule\nBody.\n")

        findings = lint_record.check(root, rec)

        assert any(f.startswith("apps/acme/project/milestones/m01-bad.md: status") for f in findings), findings
        assert any(f.startswith("setup/guardrails.md: guardrail 1") for f in findings), findings


if __name__ == "__main__":
    test_status_first_word()
    test_waits_on_resolves()
    test_delivery_present()
    test_ready_parts()
    test_open_questions_owner()
    test_guardrails_source()
    test_unlinked_pages_excludes_specimen_leaves()
    test_unlinked_pages()
    test_per_app_record_root()
    print("ok")
