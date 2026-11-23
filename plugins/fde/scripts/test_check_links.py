"""One test for the link checker: it finds the dead link and leaves the good one.

Run it either way:

    python3 -m pytest scripts/test_check_links.py
    python3 scripts/test_check_links.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_links


def test_finds_only_the_dead_link():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "notes").mkdir()
        (root / "notes" / "target.md").write_text("# The file that exists\n")
        (root / "index.md").write_text(
            "[good](notes/target.md)\n"
            "[dead](notes/missing.md)\n"
            "[web](https://example.com/missing.md)\n"
            "[anchor](#section)\n"
        )

        checked, dead = check_links.check(root)

        assert checked == 2, checked
        assert dead == ["index.md:2: notes/missing.md"], dead


if __name__ == "__main__":
    test_finds_only_the_dead_link()
    print("ok")
