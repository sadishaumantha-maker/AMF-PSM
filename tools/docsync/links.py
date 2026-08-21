"""Offline detection of Markdown links that point at files which do not exist.

CI checks Markdown links with ``markdown-link-check``, which needs Node and the network and
runs behind ``yamllint`` in the ``validate`` job -- so a YAML error hides it entirely. That
combination is exactly how eleven dead links in ``docs/discussions/README.md`` sat on
``main`` failing every build.

This module answers the same question for *relative* targets with nothing but the standard
library, fast enough to run in a pre-commit hook.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_EXTERNAL = ("http://", "https://", "mailto:", "tel:", "#")
_SKIP_DIRS = frozenset({".git", "node_modules", ".venv", "venv", "__pycache__"})


@dataclass(frozen=True, slots=True)
class DeadLink:
    """A relative Markdown link whose target is missing.

    Attributes:
        source: Repository-relative path of the file containing the link.
        target: The link target exactly as written.
        line: 1-indexed line number of the link.
    """

    source: str
    target: str
    line: int


def _markdown_files(root: Path) -> list[Path]:
    """Return every Markdown file under ``root``, skipping vendored directories."""
    return sorted(p for p in root.rglob("*.md") if not _SKIP_DIRS & set(p.relative_to(root).parts))


def find_dead_links(root: Path) -> list[DeadLink]:
    """Return every relative Markdown link in the tree whose target does not exist.

    External schemes and pure in-page anchors are ignored; a target's ``#fragment`` is
    stripped before the existence test, since a fragment addresses a heading rather than a
    file.

    Args:
        root: Repository root.

    Returns:
        Dead links in a canonical order: by source path, then line, then target.
    """
    dead: list[DeadLink] = []
    for path in _markdown_files(root):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for lineno, line in enumerate(text.splitlines(), start=1):
            for match in _LINK.finditer(line):
                raw = match.group(1).strip()
                if not raw or raw.startswith(_EXTERNAL):
                    continue
                target = raw.split("#", 1)[0].strip()
                if not target:
                    continue
                if not (path.parent / target).exists():
                    dead.append(
                        DeadLink(
                            source=str(path.relative_to(root)).replace("\\", "/"),
                            target=target,
                            line=lineno,
                        )
                    )
    return sorted(dead, key=lambda d: (d.source, d.line, d.target))
