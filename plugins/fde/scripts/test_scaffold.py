"""Two tests for scaffold.sh: the bundled docs template works with no --org,
and an owner/repo template without --org fails before gh is called.

Every run uses a scratch HOME and a scratch umbrella, with --be none --fe none.

Run it either way:

    python3 -m pytest scripts/test_scaffold.py
    python3 scripts/test_scaffold.py
"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCAFFOLD = HERE / "scaffold.sh"

sys.path.insert(0, str(HERE))

import check_links
import lint_record


def _run(tmp: Path, *extra: str) -> subprocess.CompletedProcess:
    home = tmp / "home"
    home.mkdir()
    env = {**os.environ, "HOME": str(home)}
    return subprocess.run(
        ["bash", str(SCAFFOLD), "--slug", "demo", "--umbrella", str(tmp / "umbrella"),
         "--be", "none", "--fe", "none", *extra],
        capture_output=True, text=True, env=env,
    )


def test_bundled_template_with_no_org():
    with tempfile.TemporaryDirectory() as tmp:
        result = _run(Path(tmp))
        assert result.returncode == 0, result.stderr
        docs = Path(tmp) / "umbrella" / "demo-docs"
        assert (docs / "setup" / "guardrails.md").is_file()
        assert (docs / ".gitignore").is_file()
        for path in docs.rglob("*"):
            if path.is_file() and ".git" not in path.relative_to(docs).parts:
                assert b"fde-docs" not in path.read_bytes(), path
        saved = sys.argv
        sys.argv = ["lint_record.py", str(docs)]
        try:
            assert lint_record.main() == 0
            sys.argv = ["check_links.py", str(docs)]
            assert check_links.main() == 0
        finally:
            sys.argv = saved


def test_owner_repo_template_needs_org():
    with tempfile.TemporaryDirectory() as tmp:
        result = _run(Path(tmp), "--docs-template", "some-owner/some-repo")
        assert result.returncode != 0
        assert "--org is required when --docs-template is owner/repo" in result.stderr
        assert "gh is not signed in" not in result.stderr


if __name__ == "__main__":
    test_bundled_template_with_no_org()
    test_owner_repo_template_needs_org()
    print("ok")
