"""The layering rule, asserted rather than trusted.

`core/` is authentication and RBAC. A domain may import it; it may never
import a domain. That is what keeps a domain removable: delete
`src/domains/<name>/`, drop its line from INSTALLED_APPS and its line
from `config/urls.py`, and nothing in `core/` breaks.

`core/rbac.py` is the one place that needs a domain's models, and it
reaches them by label through `settings.RBAC_PROJECT_MODEL` rather than
by import. That is the pattern a second domain follows.

Every check reads the source with `ast` rather than importing the
module. An import test only catches what a module does at import time; a
`from domains.projects.models import Project` inside a function would
pass it and still break the layering. Reading the tree catches both.
"""

import ast
import pathlib

import pytest

# `parents[2]` counts up from `tests/domains/`. Fix the number on copy if
# this file lands at a different depth, or the test silently checks nothing.
SRC = pathlib.Path(__file__).resolve().parents[2] / "src"
CORE = SRC / "core"

# Nothing under `core/` may import these. `domains` is the rule this file
# exists for. `sqlalchemy` is here because nothing in this repository uses
# it and an import would mean a second ORM arrived without a decision.
BANNED_ROOTS = ("domains", "sqlalchemy")


def _modules() -> list[pathlib.Path]:
    paths = sorted(CORE.rglob("*.py"))
    assert paths, "nothing under core/ -- the test is looking in the wrong place"
    return paths


def _imported_roots(path: pathlib.Path) -> set[str]:
    roots: set[str] = set()
    tree = ast.parse(path.read_text(), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            # `level > 0` is a relative import, which can only reach
            # inside `core/` and is therefore never a violation.
            if node.level == 0 and node.module:
                roots.add(node.module.split(".")[0])
    return roots


def test_no_module_under_core_imports_a_domain():
    """The rule, stated exactly. Named separately from the parametrised
    test below so a failure says which rule broke."""
    offenders = []
    for path in _modules():
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.level == 0:
                names = [node.module or ""]
            for name in names:
                if name == "domains" or name.startswith("domains."):
                    offenders.append(f"{path.name}:{node.lineno} imports {name}")
    assert offenders == []


@pytest.mark.parametrize("root", BANNED_ROOTS)
def test_no_module_under_core_imports_a_banned_package(root):
    offenders = [
        str(path.relative_to(CORE))
        for path in _modules()
        if root in _imported_roots(path)
    ]
    assert offenders == []


def test_core_names_a_domain_model_by_label_and_never_by_import():
    """`core/rbac.py` reads two settings and calls `apps.get_model`.

    That indirection is the whole reason `core/` survives a domain being
    removed, so it is asserted rather than left as a comment.
    """
    source = (CORE / "rbac.py").read_text()
    assert "settings.RBAC_PROJECT_MODEL" in source
    assert "settings.RBAC_PROJECT_MEMBER_MODEL" in source
    assert "apps.get_model" in source


def test_every_domain_is_a_sibling_package_under_domains():
    """A domain is a directory under `src/domains/`, and nothing else.

    A module dropped straight into `src/domains/` would be shared code
    with no owner, which is the state this layout exists to prevent.
    """
    stray = [
        path.name
        for path in (SRC / "domains").iterdir()
        if path.is_file() and path.name != "__init__.py"
    ]
    assert stray == []
