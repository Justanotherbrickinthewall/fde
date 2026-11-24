from __future__ import annotations

import io
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

SK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SK / "scripts"))
import sessions  # noqa: E402


def run(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        rc = sessions.main(list(argv))
    return rc, out.getvalue(), err.getvalue()


def note(front: dict, extra: str = "") -> str:
    base = {"Folder": "/x", "Type": "aie", "Started": "7 November 2026",
            "Last updated": "7 November 2026", "Phase": "done", "Status": "done",
            "Summary": "Did the thing.", "Owes": "none", "Picks up": "none"}
    base.update(front)
    lines = "\n".join(f"- {k}: {v}" for k, v in base.items())
    return f"# T\n\n{lines}\n\n## Resume here\n\nok\n\n## Decisions\n\n{extra}\n"


class Base(unittest.TestCase):
    def setUp(self):
        self.td = tempfile.TemporaryDirectory()
        self.t = Path(self.td.name).resolve()
        os.environ["MEMORY_TODAY"] = "2026-11-07"
        os.environ["SESSIONS_OWNER"] = "Ada"
        self.addCleanup(self.td.cleanup)
        for k in ("MEMORY_TODAY", "SESSIONS_OWNER"):
            self.addCleanup(os.environ.pop, k, None)


class SymlinkRoot(Base):
    def test_sessions_dir_for_keeps_symlink_path(self):
        rec = self.t / "records" / "p"
        rec.mkdir(parents=True)
        (self.t / "p").mkdir()
        (self.t / "p" / "my-sessions").symlink_to(rec)
        self.assertEqual(sessions.sessions_dir_for(str(self.t / "p")), self.t / "p" / "my-sessions")
        self.assertEqual(sessions.sessions_dir_for(str(self.t / "p" / "my-sessions")),
                         self.t / "p" / "my-sessions")


class NewCheck(Base):
    def test_new_then_check(self):
        root = self.t / "proj"
        root.mkdir()
        rc, out, _ = run("new", "--type", "prototype", "--slug", "My Idea", "--root", str(root))
        folder = Path(out.strip())
        self.assertEqual(folder, root / "my-sessions" / "prototypes" / "07nov26-my-idea")
        text = (folder / "notes.md").read_text()
        self.assertIn(f"- Folder: {folder}", text)
        self.assertIn("- Started: 7 November 2026", text)
        self.assertIn("- Last updated: 7 November 2026", text)
        self.assertIn("## For Ada", text)
        self.assertNotIn("{", text)
        # the unfilled template fails: Summary still reads "Not yet written."
        rc, out, _ = run("check", str(folder))
        self.assertEqual(rc, 1)
        self.assertIn("template default", out)
        (folder / "notes.md").write_text(note({}, "- Chose A. Stays local"))
        self.assertEqual(run("check", str(folder))[0], 0)
        (folder / "notes.md").write_text(note({}, "- Chose A."))
        rc, out, _ = run("check", str(folder))
        self.assertEqual(rc, 1)
        self.assertIn("no marker", out)

    def test_new_types_flat_and_clash(self):
        root = self.t / "proj"
        for typ in ("aie", "fdc", "smoke", "misc"):
            _, out, _ = run("new", "--type", typ, "--slug", "x", "--root", str(root))
            self.assertEqual(Path(out.strip()).parent.name, typ)
        _, a, _ = run("new", "--type", "aie", "--slug", "x", "--root", str(root))
        self.assertTrue(a.strip().endswith("07nov26-x-2"))
        _, f, _ = run("new", "--type", "aie", "--slug", "y", "--flat", "--root", str(root),
                      "--picks-up", "aie/07nov26-x")
        self.assertEqual(Path(f.strip()).parent, root / "my-sessions")
        self.assertIn("- Picks up: aie/07nov26-x", (Path(f.strip()) / "notes.md").read_text())

    def test_check_other_problems(self):
        d = self.t / "n"
        d.mkdir()
        (d / "notes.md").write_text(note({"Summary": "x" * 201, "Owes": ""}))
        _, out, _ = run("check", str(d))
        self.assertIn("missing front field: Owes", out)
        self.assertIn("over 200", out)
        long_resume = note({}).replace("\nok\n", "\n" + "\n".join(f"l{i}" for i in range(11)) + "\n")
        (d / "notes.md").write_text(long_resume)
        self.assertIn("over 10", run("check", str(d))[1])


class Recurring(Base):
    def test_recurring_reuse_triggers_done_and_dir(self):
        root = self.t / "proj"
        _, a, _ = run("new", "--type", "recurring", "--slug", "x", "--triggers", "a,b", "--root", str(root))
        folder = Path(a.strip())
        self.assertEqual(folder, root / "my-sessions" / "recurring" / "x")
        text = (folder / "notes.md").read_text()
        self.assertIn("- Type: recurring\n- Triggers: a, b\n", text)
        self.assertIn("- Flags:\n", text)
        self.assertNotIn("Triggers", (Path(run("new", "--type", "aie", "--slug", "y", "--root", str(root))[1].strip()) / "notes.md").read_text())
        rc, b, _ = run("new", "--type", "recurring", "--slug", "x", "--root", str(root))
        self.assertEqual((rc, b.strip()), (0, str(folder)))
        self.assertEqual(sessions.read_session(folder, folder.parents[1])["triggers"], ["a", "b"])
        (folder / "notes.md").write_text(note({"Type": "recurring", "Status": "done"}))
        self.assertIn("recurring", run("check", str(folder))[1])
        (folder / "notes.md").write_text(note({"Type": "recurring", "Status": "paused", "Flags": ""}))
        self.assertEqual(run("check", str(folder))[0], 0)
        (folder / "notes.md").write_text(note({"Type": "recurring", "Status": "active"}))
        self.assertEqual(run("check", str(folder))[0], 0)

    def test_changed_sessions_dir_moves_new(self):
        root = self.t / "proj2"
        orig = sessions.sessions_dir
        sessions.sessions_dir = lambda r: Path(r) / "elsewhere"
        self.addCleanup(setattr, sessions, "sessions_dir", orig)
        _, out, _ = run("new", "--type", "aie", "--slug", "x", "--root", str(root))
        self.assertEqual(Path(out.strip()).parent, root / "elsewhere" / "aie")


class Index(Base):
    def mk(self, rel, text=None, yaml=None):
        d = self.t / "my-sessions" / rel
        d.mkdir(parents=True)
        if text:
            (d / "notes.md").write_text(text)
        if yaml:
            (d / "state.yaml").write_text(yaml)

    def test_four_naming_schemes(self):
        self.mk("aie/07nov26-a", note({"Started": "7 November 2026"}))
        self.mk("2026-11-05-b", note({"Started": "", "Status": "active", "Type": ""}))
        self.mk("06nov26-c", note({"Status": "active", "Started": ""}))
        self.mk("16Oct2026-1942-hunt", yaml="phase: closed\n")
        self.mk("16Oct2026-2000-hunt2", yaml="phase: running\n")
        rc, out, _ = run("index", "--root", str(self.t / "my-sessions"))
        self.assertEqual(rc, 0)
        self.assertIn("from 5 folders", out)
        lines = {ln.split(" | ")[3]: ln for ln in out.splitlines() if ln.startswith("- ")}
        self.assertEqual(len(lines), 5)
        self.assertIn("| aie | done | aie/07nov26-a |", lines["aie/07nov26-a"])
        self.assertTrue(lines["2026-11-05-b"].startswith("- 2026-11-05 | misc | active"))
        self.assertTrue(lines["06nov26-c"].startswith("- 2026-11-06 |"))
        self.assertTrue(lines["16Oct2026-1942-hunt"].startswith("- 2026-10-16 | misc | done"))
        self.assertIn("| active |", lines["16Oct2026-2000-hunt2"])
        self.assertLessEqual(max(len(x) for x in lines.values()), 240)

    def test_legacy_without_status_is_not_active(self):
        legacy = "# Old build\n\n- **Started:** 01-10-26\n- **Phase:** 8 close\n\n## Log\n\nx\n"
        self.mk("01oct26-old", legacy)
        self.mk("02oct26-old2", legacy.replace("- **Phase:**", "- **Status:** done 01-10-26\n- **Phase:**"))
        self.mk("aie/07nov26-new", note({"Status": "active"}))
        out = run("index", "--root", str(self.t))[1]
        self.assertIn("## Active (1)", out)
        self.assertIn("## Done (1)", out)
        self.assertIn("## No status (1)", out)
        self.assertIn("| no status | 01oct26-old | Old build", out)

    def test_open_handoff(self):
        self.mk("aie/07nov26-a", note({"Owes": "smoke test"}))
        out = run("index", "--root", str(self.t))[1]
        self.assertIn("## Open hand-offs (1)", out)
        self.mk("smoke/08nov26-s", note({"Picks up": "aie/07nov26-a"}))
        out = run("index", "--root", str(self.t))[1]
        self.assertIn("## Open hand-offs (0)", out)

    def test_write_and_size_bound(self):
        for i in range(250):
            self.mk(f"aie/{i:03d}-s{i}", note({"Started": f"{1 + i % 28} March 2026"}))
        self.assertEqual(run("index", "--root", str(self.t), "--write")[0], 0)
        text = (self.t / "my-sessions" / "INDEX.md").read_text()
        self.assertLessEqual(text.count("\n"), 200)
        self.assertLessEqual(len(text.encode()), 16 * 1024)
        self.assertIn("older sessions not listed", text)


class RootInit(Base):
    def test_init_existing_folder_writes_nothing(self):
        root = self.t / "jh"
        (root / "my-sessions").mkdir(parents=True)
        rc, out, _ = run("root", "--init", "--cwd", str(root))
        self.assertEqual(out.strip(), str(root / "my-sessions"))
        self.assertEqual(list((root / "my-sessions").iterdir()), [])

    def test_init_creates_files(self):
        root = self.t / "p"
        root.mkdir()
        run("root", "--init", "--cwd", str(root))
        self.assertEqual((root / "my-sessions" / ".gitignore").read_text(), "*\n")

    def test_home_fails(self):
        home = self.t / "home"
        home.mkdir()
        old = os.environ.get("HOME")
        os.environ["HOME"] = str(home)
        try:
            rc, out, _ = run("root", "--init", "--cwd", str(home))
        finally:
            os.environ["HOME"] = old
        self.assertEqual((rc, out), (1, ""))
        self.assertFalse((home / "my-sessions").exists())


class Isolation(Base):
    def test_hands_over_to_the_full_skill(self):
        home = self.t / "home"
        full = home / ".claude" / "skills" / "sessions" / "scripts"
        full.mkdir(parents=True)
        (full / "sessions.py").write_text('print("FULL-SKILL-MARKER")\n')
        (full / "memlib.py").write_text("")
        r = subprocess.run([sys.executable, str(SK / "scripts" / "sessions.py"), "index"],
                           capture_output=True, text=True, env={**os.environ, "HOME": str(home)})
        self.assertIn("FULL-SKILL-MARKER", r.stdout)

    def test_ignores_an_unrelated_skill_of_the_same_name(self):
        home = self.t / "home"
        other = home / ".claude" / "skills" / "sessions" / "scripts"
        other.mkdir(parents=True)
        (other / "sessions.py").write_text('print("OTHER-SKILL-MARKER")\n')
        root = self.t / "proj"
        root.mkdir()
        r = subprocess.run([sys.executable, str(SK / "scripts" / "sessions.py"),
                            "root", "--cwd", str(root)],
                           capture_output=True, text=True, env={**os.environ, "HOME": str(home)})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("OTHER-SKILL-MARKER", r.stdout)

    def test_new_writes_nothing_in_home(self):
        home = self.t / "home"
        home.mkdir()
        root = self.t / "proj"
        root.mkdir()
        r = subprocess.run([sys.executable, str(SK / "scripts" / "sessions.py"), "new",
                            "--type", "qa", "--slug", "x", "--root", str(root)],
                           capture_output=True, text=True, env={**os.environ, "HOME": str(home)})
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(list(home.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
