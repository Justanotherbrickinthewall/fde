"""rtfgrid keeps vertical merges: \\clvmgf starts a block, \\clvmrg continues it.

Runs under plain python3 and needs no document on disk:
    python3 test_rtfgrid.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rtfgrid import parse  # noqa: E402

RTF = (
    r"{\rtf1\ansi"
    r"\trowd\cellx1000\cellx2000\intbl A1\cell B1\cell\row"
    r"\trowd\clvmgf\cellx1000\cellx2000\intbl Block\cell B2\cell\row"
    r"\trowd\clvmrg\cellx1000\cellx2000\intbl \cell B3\cell\row"
    r"\trowd\cellx1000\cellx2000\intbl A4\cell B4\cell\row"
    r"}"
)


def rows():
    return [d["cells"] for kind, d in parse(RTF) if kind == "row"]


def test_row_count():
    assert len(rows()) == 4


def test_vertical_merge_start_and_continuation():
    r = rows()
    assert r[1][0] == ("Block", (False, True, False))
    assert r[2][0] == ("", (False, False, True))
    assert r[0][0][1] == (False, False, False)
    assert r[3][0][1] == (False, False, False)


if __name__ == "__main__":
    test_row_count()
    test_vertical_merge_start_and_continuation()
    print("ok: 2 tests passed")
