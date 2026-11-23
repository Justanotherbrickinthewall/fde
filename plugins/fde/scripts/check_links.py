#!/usr/bin/env python3
"""Fail on any relative link in the record that points at a file we do not have.

Walks every .md and .html from the repository root, pulls out the relative link
targets, resolves each one against the file that holds it, and prints the ones
that do not exist.

What it deliberately does not do:

- It does not check that a #fragment resolves to a heading. That is a different
  job and this record does not ask for it.
- It does not read code. A fenced block, an inline code span, and the body of a
  <script> or <style> element are all masked out before the link patterns run,
  because a path inside them is a sample rather than a link. Without that mask
  the session plans fail on their own Jinja templates.

What it does read from code is one thing: a url(...) inside a <style> element
or a .css file. A prototype that loads a font from a path is a link like any
other, and the split broke exactly one of those. data: and absolute URLs are
skipped, as they are everywhere else.

Run it from the docs repository root, or pass that root as an argument
(this script ships in the fde plugin, so it no longer sits inside the
repository it checks):

    python3 scripts/check_links.py
    python3 scripts/check_links.py /path/to/some-docs
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

# raw/ is 23 MB of client documents and is not part of the record's link graph.
# fixtures/ holds test data, which may carry broken links on purpose.
# The rest are directories no link should ever point into.
SKIP_DIRS = {".git", "raw", "fixtures", "__pycache__", ".pytest_cache", "node_modules"}

SUFFIXES = {".md", ".html", ".css"}

# ](target) and ](target "title"). The target may be wrapped in angle brackets.
MD_INLINE = re.compile(r"\]\(\s*<?([^)<>\s]+)>?(?:\s+[\"'(][^)]*)?\s*\)")
# [label]: target, at the head of a line.
MD_REFDEF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?([^\s<>]+)>?", re.MULTILINE)
# href="target", src='target'.
HTML_ATTR = re.compile(r"(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)

# Anything with a URI scheme: http:, https:, mailto:, tel:, data:, and the rest.
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.\-]*:")

FENCE = re.compile(r"^ {0,3}(?P<f>```+|~~~+)[^\n]*$.*?^ {0,3}(?P=f)[^\n]*$", re.MULTILINE | re.DOTALL)
UNCLOSED_FENCE = re.compile(r"^ {0,3}(?P<f>```+|~~~+)[^\n]*$.*\Z", re.MULTILINE | re.DOTALL)
CODE_SPAN = re.compile(r"(?P<t>`+)(?:(?!(?P=t))[^\n])*(?P=t)")
SCRIPT_OR_STYLE = re.compile(r"<(script|style)\b.*?</\1\s*>", re.IGNORECASE | re.DOTALL)
STYLE_BLOCK = re.compile(r"<style\b[^>]*>(.*?)</style\s*>", re.IGNORECASE | re.DOTALL)
# url(target), url('target'), url("target"), inside CSS.
CSS_URL = re.compile(r"url\(\s*(['\"]?)([^'\")\s]+)\1\s*\)", re.IGNORECASE)


def _blank(match: re.Match) -> str:
    """Replace a span with newlines only, so every later line keeps its number."""
    return "\n" * match.group(0).count("\n")


def mask_code(text: str, is_html: bool) -> str:
    if is_html:
        return SCRIPT_OR_STYLE.sub(_blank, text)
    text = FENCE.sub(_blank, text)
    text = UNCLOSED_FENCE.sub(_blank, text)
    return CODE_SPAN.sub(_blank, text)


def candidate_files(root: Path) -> list[Path]:
    found = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            path = Path(dirpath) / name
            if path.suffix.lower() in SUFFIXES:
                found.append(path)
    return sorted(found)


def drop_ignored(root: Path, files: list[Path]) -> list[Path]:
    """Ask git which of these it ignores. If git cannot answer, keep them all."""
    if not files:
        return files
    payload = "\n".join(str(p.relative_to(root)) for p in files)
    try:
        result = subprocess.run(
            ["git", "check-ignore", "--stdin"],
            cwd=root,
            input=payload,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return files
    if result.returncode not in (0, 1):
        return files
    ignored = {line.strip() for line in result.stdout.splitlines() if line.strip()}
    return [p for p in files if str(p.relative_to(root)) not in ignored]


def targets_in(text: str):
    """Yield (line number, raw target) for every link the file declares."""
    for pattern in (MD_INLINE, MD_REFDEF, HTML_ATTR):
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            yield line, match.group(1)


def css_targets_in(text: str, offset: int = 0):
    """Yield (line number, raw target) for every url(...) in a run of CSS."""
    for match in CSS_URL.finditer(text):
        line = offset + text.count("\n", 0, match.start()) + 1
        yield line, match.group(2)


def style_targets_in(html: str):
    """Yield (line number, raw target) for every url(...) in a <style> block."""
    for block in STYLE_BLOCK.finditer(html):
        offset = html.count("\n", 0, block.start(1))
        yield from css_targets_in(block.group(1), offset)


def resolve(root: Path, source: Path, target: str) -> Path | None:
    """Return the path a target names, or None when it is not ours to check."""
    if not target or target.startswith("#"):
        return None
    if target.startswith("//") or SCHEME.match(target):
        return None
    cleaned = unquote(target.split("#", 1)[0])
    if not cleaned:
        return None
    if cleaned.startswith("/"):
        return root / cleaned.lstrip("/")
    return source.parent / cleaned


def check(root: Path) -> tuple[int, list[str]]:
    checked = 0
    dead: list[str] = []
    for path in sorted(drop_ignored(root, candidate_files(root))):
        raw = path.read_text(encoding="utf-8", errors="replace")
        suffix = path.suffix.lower()
        if suffix == ".css":
            found = css_targets_in(raw)
        elif suffix == ".html":
            found = list(targets_in(mask_code(raw, True))) + list(style_targets_in(raw))
        else:
            found = targets_in(mask_code(raw, False))
        seen = set()
        for line, target in found:
            if (line, target) in seen:
                continue
            seen.add((line, target))
            resolved = resolve(root, path, target)
            if resolved is None:
                continue
            checked += 1
            wants_dir = target.split("#", 1)[0].endswith("/")
            ok = resolved.is_dir() if wants_dir else resolved.exists()
            if not ok:
                dead.append(f"{path.relative_to(root)}:{line}: {target}")
    return checked, sorted(dead)


def main() -> int:
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    checked, dead = check(root)
    for line in dead:
        print(line)
    print(f"{checked} relative links checked, {len(dead)} dead.")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())
