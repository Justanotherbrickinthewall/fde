"""The part of a larger library that the session script needs.
Stdlib only.
"""
from __future__ import annotations

import datetime as _dt
import os
import re
import subprocess
from pathlib import Path


class RootError(Exception):
    """The session root would be $HOME or /."""


def _home() -> str:
    return os.path.expanduser("~")


def today() -> _dt.date:
    env = os.environ.get("MEMORY_TODAY")
    if env:
        return _dt.date.fromisoformat(env)
    return _dt.date.today()


def _git(path, *args: str) -> str | None:
    try:
        r = subprocess.run(["git", "-C", str(path), *args], capture_output=True,
                           text=True, timeout=10, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.SubprocessError):
        return None
    out = r.stdout.strip()
    return out if r.returncode == 0 and out else None


def git_main_root(path) -> Path | None:
    out = _git(path, "rev-parse", "--path-format=absolute", "--git-common-dir")
    return Path(out).resolve().parent if out else None


def find_root(cwd, home=None) -> Path:
    here = Path(os.path.abspath(cwd))
    home_p = Path(home if home is not None else _home()).resolve()
    root = None
    d = here
    while d != d.parent and d != home_p:
        if (d / "my-sessions").is_dir() and (
                d == here or (d / "CLAUDE.md").exists() or (d / ".engagement").exists()):
            root = d
            break
        d = d.parent
    if root is None:
        root = git_main_root(here) or here
    if root == home_p or root == Path("/"):
        raise RootError(f"the root would be {root}; run this from a project folder")
    return root


def parse_notes(text: str) -> dict:
    title, front, sections = "", {}, {}
    cur = None
    buf: list = []
    for ln in text.split("\n"):
        if ln.startswith("## "):
            if cur is not None:
                sections[cur] = "\n".join(buf).strip()
            cur, buf = ln[3:].strip(), []
        elif cur is not None:
            buf.append(ln)
        elif ln.startswith("# ") and not title:
            title = ln[2:].strip()
        else:
            m = re.match(r"^[-*]\s+\*{0,2}([A-Za-z][A-Za-z ]*?):\*{0,2}\s*(.*?)\s*$", ln)
            if m:
                front[m.group(1)] = m.group(2)
    if cur is not None:
        sections[cur] = "\n".join(buf).strip()
    return {"title": title, "front": front, "sections": sections}


_MARKERS = [
    (re.compile(r"Graduated:\s*\S.*$", re.I), "graduated"),
    (re.compile(r"Stays local\b\.?$", re.I), "stays-local"),
    (re.compile(r"To wiki\b\.?$", re.I), "to-wiki"),
]


def notes_decisions(text: str) -> list:
    sec = parse_notes(text)["sections"].get("Decisions", "")
    bullets: list = []
    for ln in sec.split("\n"):
        if re.match(r"^[-*]\s", ln):
            bullets.append(ln[2:].strip())
        elif bullets and ln.strip():
            bullets[-1] += " " + ln.strip()
    res = []
    for b in bullets:
        marker = next((name for rx, name in _MARKERS if rx.search(b)), None)
        res.append({"text": b, "marker": marker})
    return res


_MONTHS = {m: i + 1 for i, m in enumerate(
    "jan feb mar apr may jun jul aug sep oct nov dec".split())}


def folder_date(name: str):
    name = Path(name).name
    try:
        m = re.match(r"^(\d{4})-(\d{2})-(\d{2})(?!\d)", name)
        if m:
            return _dt.date(*map(int, m.groups()))
        m = re.match(r"^(\d{1,2})([A-Za-z]{3})(\d{4}|\d{2})(?!\d)", name)
        if m and m.group(2).lower() in _MONTHS:
            y = int(m.group(3))
            return _dt.date(y + 2000 if y < 100 else y, _MONTHS[m.group(2).lower()], int(m.group(1)))
    except ValueError:
        pass
    return None
