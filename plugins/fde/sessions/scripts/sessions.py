#!/usr/bin/env python3
"""sessions.py: find the session root, make session folders, check notes, write INDEX.md.

  sessions.py root [--init] [--cwd D]
  sessions.py new --type T --slug S [--root R] [--title X] [--picks-up P] [--flat] [--triggers a,b]
  sessions.py check <folder>
  sessions.py index [--root R] [--write]

Stdlib only.
"""
from __future__ import annotations

import argparse
import datetime as dt
import getpass
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import memlib  # noqa: E402

TYPES = ["fdc", "aie", "hardening", "smoke", "qa", "prototype", "misc", "recurring"]
TYPE_DIR = {t: t for t in TYPES}
TYPE_DIR["prototype"] = "prototypes"
DIR_TYPE = {v: k for k, v in TYPE_DIR.items()}
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
REQUIRED = ["Folder", "Type", "Started", "Last updated", "Phase", "Status",
            "Summary", "Owes", "Picks up"]
DONE_WORDS = {"done", "complete", "closed", "finished", "built"}  # legacy free-text statuses
LINE_MAX, INDEX_LINES, INDEX_BYTES = 240, 200, 16 * 1024
TEMPLATE = Path(__file__).resolve().parent.parent / "templates" / "notes.md"


def _err(msg: str) -> None:
    print(f"sessions.py: {msg}", file=sys.stderr)


def long_date(d: dt.date) -> str:
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def short_date(d: dt.date) -> str:
    return f"{d.day:02d}{MONTHS[d.month - 1][:3].lower()}{d.year % 100:02d}"


def parse_date(text: str):
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    try:
        if m:
            return dt.date(*map(int, m.groups()))
        m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})[A-Za-z]*\s+(\d{4})", text)
        if m:
            mon = [x[:3].lower() for x in MONTHS].index(m.group(2).lower()) + 1
            return dt.date(int(m.group(3)), mon, int(m.group(1)))
    except ValueError:
        pass
    return None


# ---------------------------------------------------------------- root

def sessions_dir(root) -> Path:
    """The one place that says where a project keeps its sessions."""
    return Path(root) / "my-sessions"


def sessions_dir_for(arg) -> Path:
    """--root accepts the project root or the sessions folder itself."""
    if arg is None:
        return sessions_dir(memlib.find_root(os.getcwd()))
    p = Path(os.path.abspath(arg))
    return p if p.name == sessions_dir(p).name else sessions_dir(p)


def init_root(root: Path) -> Path:
    out = sessions_dir(root)
    if not out.exists():  # an existing folder may be engine-owned, so write nothing in it
        out.mkdir(parents=True)
        (out / ".gitignore").write_text("*\n")
        (out / "README.md").write_text(
            "# Session notes\n\nClaude Code session notes. The fde plugin's sessions/CONTRACT.md holds the rules, "
            "and git ignores this folder.\n")
        if not (root / "CLAUDE.md").exists() and not (root / ".engagement").exists():
            _err(f"warning: created {out} beside no CLAUDE.md or .engagement")
    if memlib._git(root, "ls-files", "--", out.name):
        _err(f"warning: git tracks files under {out}, and .gitignore cannot untrack them.")
    return out


def cmd_root(a) -> int:
    try:
        root = memlib.find_root(a.cwd or os.getcwd())
    except memlib.RootError as e:
        m = re.search(r"would be (.*?);", str(e))
        print(f"sessions.py: the root would be {m.group(1) if m else '?'}. "
              "Run this from a project folder.", file=sys.stderr)
        return 1
    print(init_root(root) if a.init else sessions_dir(root))
    return 0


# ---------------------------------------------------------------- new

def cmd_new(a) -> int:
    sdir = sessions_dir_for(a.root)
    init_root(sdir.parent)  # idempotent: safe when my-sessions/ already exists
    slug = re.sub(r"[^a-z0-9]+", "-", a.slug.lower()).strip("-")
    if not slug:
        _err("the slug is empty")
        return 2
    base = sdir if a.flat else sdir / TYPE_DIR[a.type]
    recurring = a.type == "recurring"
    name = slug if recurring else f"{short_date(memlib.today())}-{slug}"
    folder, n = base / name, 2
    if recurring and folder.exists():  # starting it again reuses the folder
        print(folder)
        return 0
    while folder.exists():
        folder, n = base / f"{name}-{n}", n + 1
    folder.mkdir(parents=True)
    title = a.title or slug.replace("-", " ").capitalize()
    text = TEMPLATE.read_text()
    triggers = [t.strip() for t in (a.triggers or "").split(",") if t.strip()]
    trig_line = "\n- Triggers: " + ", ".join(triggers) if recurring and triggers else ""
    for k, v in {"triggers_line": trig_line, "title": title, "folder": str(folder), "type": a.type,
                 "date": long_date(memlib.today()), "picks_up": a.picks_up or "none",
                 "owner": os.environ.get("SESSIONS_OWNER") or getpass.getuser()}.items():
        text = text.replace("{" + k + "}", v)
    (folder / "notes.md").write_text(text)
    print(folder)
    return 0


# ---------------------------------------------------------------- check

def check_notes(path: Path) -> list:
    if not path.is_file():
        return [f"{path} does not exist"]
    text = path.read_text(errors="replace")
    notes = memlib.parse_notes(text)
    front, probs = notes["front"], []
    for k in REQUIRED:
        if not front.get(k, "").strip():
            probs.append(f"missing front field: {k}")
    summary = front.get("Summary", "").strip()
    if summary and re.fullmatch(r"not yet written\.?", summary, re.I):
        probs.append("Summary is still the template default")
    if len(summary) > 200:
        probs.append(f"Summary is {len(summary)} characters, over 200")
    status = front.get("Status", "").strip().lower()
    if status == "done" and front.get("Type", "").strip().lower() == "recurring":
        probs.append("a recurring record is never done, so set Status to active or paused")
    elif status and status not in ("active", "paused", "done"):
        probs.append(f"Status is '{status}', not active, paused or done")
    for d in memlib.notes_decisions(text):
        if d["marker"] is None:
            probs.append(f"Decision has no marker: {d['text'][:60]}")
    resume = [x for x in notes["sections"].get("Resume here", "").split("\n") if x.strip()]
    if len(resume) > 10:
        probs.append(f"Resume here is {len(resume)} lines, over 10")
    return probs


def cmd_check(a) -> int:
    p = Path(a.folder)
    probs = check_notes(p if p.suffix == ".md" else p / "notes.md")
    for x in probs:
        print(x)
    return 1 if probs else 0


# ---------------------------------------------------------------- index

def _norm(v: str) -> str:
    return re.sub(r"^(\./|my-sessions/)+", "", v.strip().strip("`").rstrip("/"))


def read_session(d: Path, sdir: Path):
    rel = d.relative_to(sdir).as_posix()
    kind = DIR_TYPE.get(d.parent.name) or (d.parent.name if d.parent != sdir else "misc")
    notes = d / "notes.md"
    if notes.is_file():
        n = memlib.parse_notes(notes.read_text(errors="replace"))
        f = n["front"]
        typ = (f.get("Type", "").split() or [kind])[0].lower()
        raw = f.get("Status", "").strip().lower()
        word = (re.split(r"\W+", raw) or [""])[0]
        # A missing Status means a legacy folder, so it is not claimed as active.
        status = ("no status" if not raw else "done" if word in DONE_WORDS
                  else "paused" if word == "paused" else "active")
        owes = f.get("Owes", "").strip()
        return {
            "rel": rel, "type": typ, "status": status,
            "date": parse_date(f.get("Started", "")) or memlib.folder_date(d.name),
            "summary": " ".join((f.get("Summary") or n["title"]).split()),
            "owes": "" if re.fullmatch(r"none\.?|-|", owes, re.I) else " ".join(owes.split()),
            "picks": [_norm(x) for x in re.split(r"[,;]", f.get("Picks up", "")) if _norm(x)],
            "triggers": [x.strip() for x in f.get("Triggers", "").split(",") if x.strip()],
        }
    for y in sorted(list(d.glob("*.yaml")) + list(d.glob("*.yml"))):
        m = re.search(r"^phase:\s*['\"]?(running|closed)", y.read_text(errors="replace"), re.M)
        if m:
            return {"rel": rel, "type": kind, "date": memlib.folder_date(d.name),
                    "status": "active" if m.group(1) == "running" else "done",
                    "summary": d.name, "owes": "", "picks": [], "triggers": []}
    return None


def collect(sdir: Path) -> list:
    out = []
    for d1 in sorted(sdir.iterdir()):
        if d1.name.startswith(".") or not d1.is_dir():
            continue
        for d in [d1] + sorted(x for x in d1.iterdir()
                               if x.is_dir() and not x.name.startswith(".")):
            s = read_session(d, sdir)
            if s:
                out.append(s)
    return out


def fmt_line(s: dict) -> str:
    def build(summary):
        parts = [str(s["date"] or "unknown"), s["type"], s["status"], s["rel"], summary]
        if s["owes"]:
            parts.append("owes: " + s["owes"])
        return "- " + " | ".join(parts)
    line = build(s["summary"])
    if len(line) > LINE_MAX:
        cut = max(0, len(s["summary"]) - (len(line) - LINE_MAX) - 3)
        line = build(s["summary"][:cut] + "...")
    return line if len(line) <= LINE_MAX else line[:LINE_MAX - 3] + "..."


def render_index(sdir: Path) -> str:
    sess = collect(sdir)
    picked = {p for s in sess for p in s["picks"] if p != s["rel"]}
    key = lambda s: (str(s["date"] or ""), s["rel"])  # noqa: E731
    sess.sort(key=key, reverse=True)
    hand = [s for s in sess if s["owes"] and s["rel"] not in picked]
    rest = [s for s in sess if s not in hand]
    active = [s for s in rest if s["status"] not in ("done", "no status")]
    done = [s for s in rest if s["status"] == "done"]
    nostat = [s for s in rest if s["status"] == "no status"]
    stamp = f"{memlib.today()} {dt.datetime.now():%H:%M}"
    head = ["# Sessions index", "",
            f"Generated by sessions.py on {stamp} from {len(sess)} folders. Do not edit.", ""]

    def body(n_dropped: int) -> str:
        # Trim the oldest No status lines first, then the oldest Done lines.
        cut_ns = min(n_dropped, len(nostat))
        cut_done = n_dropped - cut_ns
        lines = list(head)
        for title, items, cut in (("Open hand-offs", hand, 0), ("Active", active, 0),
                                  ("Done", done, cut_done), ("No status", nostat, cut_ns)):
            lines += [f"## {title} ({len(items)})"] + [fmt_line(s) for s in items[:len(items) - cut]]
            if cut:
                lines.append(f"- ... and {cut} older sessions not listed")
            lines.append("")
        return "\n".join(lines)

    # shortcut: only No status and Done are trimmed, so a huge Active list can still pass 200 lines.
    n = 0
    text = body(n)
    while n < len(done) + len(nostat) and (text.count("\n") > INDEX_LINES or len(text.encode()) > INDEX_BYTES):
        n += 1
        text = body(n)
    return text


def cmd_index(a) -> int:
    try:
        sdir = sessions_dir_for(a.root)
    except memlib.RootError as e:
        _err(str(e))
        return 1
    if not sdir.is_dir():
        _err(f"{sdir} does not exist")
        return 1
    text = render_index(sdir)
    if a.write:
        tmp = sdir / ".INDEX.md.tmp"
        tmp.write_text(text)
        os.replace(tmp, sdir / "INDEX.md")
    else:
        sys.stdout.write(text)
    return 0


# ---------------------------------------------------------------- cli

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="sessions.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("root")
    r.add_argument("--init", action="store_true")
    r.add_argument("--cwd")
    n = sub.add_parser("new")
    n.add_argument("--type", required=True, choices=TYPES)
    n.add_argument("--slug", required=True)
    n.add_argument("--root")
    n.add_argument("--title")
    n.add_argument("--picks-up", dest="picks_up")
    n.add_argument("--flat", action="store_true")
    n.add_argument("--triggers", help='comma list for a recurring record, e.g. "hunt,retro"')
    c = sub.add_parser("check")
    c.add_argument("folder")
    i = sub.add_parser("index")
    i.add_argument("--root")
    i.add_argument("--write", action="store_true")
    a = ap.parse_args(argv)
    try:
        return {"root": cmd_root, "new": cmd_new, "check": cmd_check, "index": cmd_index}[a.cmd](a)
    except memlib.RootError as e:
        _err(str(e))
        return 1


if __name__ == "__main__":
    # A machine with the full sessions skill keeps that skill's extra bookkeeping.
    # memlib.py beside it tells that skill apart from an unrelated one of the same name.
    full = Path.home() / ".claude" / "skills" / "sessions" / "scripts" / "sessions.py"
    if (full.is_file() and (full.parent / "memlib.py").is_file()
            and full.resolve() != Path(__file__).resolve()):
        os.execv(sys.executable, [sys.executable, str(full), *sys.argv[1:]])
    sys.exit(main())
