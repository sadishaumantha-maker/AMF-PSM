"""Synthetic mini-repository builder for the docsync mutation corpus.

The detector is checked the way a mutation tester checks a test suite: build a repository
whose CLAUDE.md is *correct*, assert the scan is silent, then introduce exactly one defect
and assert exactly the matching check fires. A detector that cannot be shown to stay quiet
on a clean tree is a detector nobody will leave switched on.
"""

from __future__ import annotations

import textwrap

import pytest

CLI_SOURCE = '''\
"""Toolkit CLI.

Exposes ``alpha`` and ``beta`` subcommands.
"""

import argparse


def _add_format(parser):
    parser.add_argument("--format", choices=["text", "json"], default="text")


def _build_parser():
    parser = argparse.ArgumentParser(prog="amf")
    sub = parser.add_subparsers(dest="command")

    a = sub.add_parser("alpha")
    a.add_argument("source")
    a.add_argument("--depth", type=int, default=3)
    _add_format(a)

    b = sub.add_parser("beta")
    b.add_argument("--target", choices=[k.value for k in SystemKind], required=True)
    _add_format(b)

    return parser
'''

MODELS_SOURCE = '''\
"""Value types."""

from enum import Enum


class SystemKind(str, Enum):
    """Kinds."""

    ALPHA = "alpha"
    BETA = "beta"
'''

ERRORS_SOURCE = '''\
"""Errors."""


class AMFError(Exception):
    """Base."""


class InvalidSystemError(AMFError):
    """Bad system."""
'''

ENGINE_SOURCE = '''\
"""Engine."""

from amf.errors import AMFError

__all__ = ["AMFError"]
'''

GUIDE = textwrap.dedent("""\
    # CLAUDE.md — contributor guide

    ## Repository layout

    ```
    src/amf/            the package
    docs/               prose
    examples/           runnable scripts
    pyproject.toml      packaging
    ```

    ## Package architecture (`src/amf/`)

    | Module | Responsibility |
    |--------|----------------|
    | `errors.py` | Typed exceptions: `AMFError`, `InvalidSystemError`. |
    | `models.py` | Value types. |
    | `engine.py` | The engine. |
    | `cli.py` | The console script. |

    ## Using the CLI

    The console script offers two subcommands:

    ```sh
    amf alpha  source [--depth 3] [--format text|json]
    amf beta   --target alpha [--format text|json]
    ```

    ## Docs

    See `docs/guide.md`. Runnable scripts live in `examples/`: `demo.py`.

    ## CI

    Two workflows gate every push: `ci.yml` and `codeql.yml`.

    - **`codeql.yml` carries one `# yamllint disable-line rule:line-length`
      directive.**
    """)


def _write(root, relative, content):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


@pytest.fixture
def mini_repo(tmp_path):
    """Build a synthetic repository whose CLAUDE.md is entirely accurate.

    The repository lives in a subdirectory so that `tmp_path` itself stays free for test
    artifacts. Writing a report into the tree under scan would otherwise add a top-level
    entry and register as drift -- which is correct behaviour, but not what those tests are
    measuring.
    """
    root = tmp_path / "repo"
    _write(root, "src/amf/__init__.py", '"""Package."""\n\n__version__ = "0.1.0"\n\n__all__ = ["AMFError"]\n')
    _write(root, "src/amf/errors.py", ERRORS_SOURCE)
    _write(root, "src/amf/models.py", MODELS_SOURCE)
    _write(root, "src/amf/engine.py", ENGINE_SOURCE)
    _write(root, "src/amf/cli.py", CLI_SOURCE)
    _write(root, "pyproject.toml", '[project]\nname = "amf"\nversion = "0.1.0"\n')
    _write(root, "docs/guide.md", "# Guide\n")
    _write(root, "examples/demo.py", "print('hi')\n")
    _write(root, ".github/workflows/ci.yml", "name: CI\n")
    _write(root, ".github/workflows/codeql.yml", "# yamllint disable-line rule:line-length\nname: CodeQL\n")
    _write(root, "CLAUDE.md", GUIDE)
    return root


@pytest.fixture
def guide_editor(mini_repo):
    """Return a callable that rewrites one substring of the mini-repo's CLAUDE.md."""

    def edit(old, new):
        path = mini_repo / "CLAUDE.md"
        text = path.read_text(encoding="utf-8")
        assert old in text, f"anchor not present in guide: {old!r}"
        path.write_text(text.replace(old, new), encoding="utf-8")

    return edit
