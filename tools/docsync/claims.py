"""Parse ``CLAUDE.md`` into the mechanical claims it makes about the repository.

Only claims that can be checked *without ambiguity* are extracted. That restraint is
deliberate: a detector that cries wolf gets switched off. The clearest example is the CLI
synopsis block, which mixes real defaults with illustrative values -- ``--magnitude 0.8`` is
the default, while ``--cascade-threshold 0.2`` is an example of a knob whose default is
``None``. Flag *presence* is therefore checked from that block and defaults are taken only
from prose that states them as defaults.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

ClaimValue = str | int | float | bool | None
"""Any literal a claim can state: numbers, strings, booleans, or ``None``."""

PROG = "amf"
"""The console-script name, as declared by ``[project.scripts]`` in ``pyproject.toml``.

The CLI synopsis block is found and parsed by looking for lines that invoke it.
"""

_NUMBER_WORDS = {
    "no": 0,
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}


def _as_value(raw: str) -> ClaimValue:
    """Coerce a literal as written in prose to a Python value."""
    text = raw.strip().strip("`")
    for literal, value in (("None", None), ("True", True), ("False", False)):
        if text == literal:
            return value
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return text


@dataclass(frozen=True, slots=True)
class CliClaim:
    """The documented synopsis of one subcommand.

    Attributes:
        name: Subcommand name as written, e.g. ``stress-test``.
        flags: Every ``--flag`` the synopsis shows.
        line: 1-indexed line where the synopsis starts.
    """

    name: str
    flags: frozenset[str]
    line: int


@dataclass(frozen=True, slots=True)
class Claims:
    """Everything the detector believes ``CLAUDE.md`` asserts.

    Attributes:
        text: The full document, for membership tests such as "is this file mentioned".
        test_count: The test total stated in the *Developing* section, if any.
        module_rows: Module names appearing in the package architecture table.
        exception_names: Exception class names listed in the ``errors.py`` table row.
        cli: One entry per documented subcommand.
        subcommand_count: The subcommand count stated in prose, if any.
        codeql_directives: The stated number of yamllint disable-line directives.
        layout_paths: Paths listed in the repository layout block.
        config_defaults: Defaults stated as ``Name`` -> ``{field: value}``.
        named_constants: Constants stated inline, such as ``_LOW_REDUNDANCY``.
    """

    text: str
    test_count: int | None = None
    module_rows: tuple[str, ...] = ()
    exception_names: tuple[str, ...] = ()
    cli: tuple[CliClaim, ...] = ()
    subcommand_count: int | None = None
    codeql_directives: int | None = None
    layout_paths: tuple[str, ...] = ()
    config_defaults: dict[str, dict[str, Any]] = field(default_factory=dict)
    named_constants: dict[str, Any] = field(default_factory=dict)

    def mentions(self, needle: str) -> bool:
        """Report whether ``needle`` appears anywhere in the document."""
        return needle in self.text

    def mentions_path(self, needle: str) -> bool:
        """Report whether ``needle`` appears as a path, not merely as a substring.

        A plain substring test is wrong in both directions here. Matching the bare word
        ``tools`` is satisfied by prose like "those tools", and matching ``tools/`` is
        satisfied by an unrelated ``tests/tools/`` -- so an undocumented top-level directory
        would slip through on the strength of a different directory's name. Requiring a
        boundary before the match fixes both.
        """
        return re.search(rf"(?<![\w/.-]){re.escape(needle)}", self.text) is not None


def _fenced_blocks(text: str) -> list[tuple[str, str]]:
    """Return ``(info_string, body)`` for every fenced code block."""
    return [(m.group(1).strip(), m.group(2)) for m in re.finditer(r"```([^\n]*)\n(.*?)```", text, re.DOTALL)]


def _parse_cli_block(text: str) -> tuple[CliClaim, ...]:
    """Extract the documented subcommand synopses from the ``sh`` block."""
    for info, body in _fenced_blocks(text):
        if info != "sh" or f"{PROG} " not in body:
            continue
        offset = text[: text.index(body)].count("\n") + 1
        joined: list[tuple[int, str]] = []
        buffer = ""
        start = 0
        for index, line in enumerate(body.splitlines()):
            stripped = line.rstrip()
            if not buffer:
                start = index
            if stripped.endswith("\\"):
                buffer += stripped[:-1] + " "
                continue
            joined.append((start, buffer + stripped))
            buffer = ""
        claims: list[CliClaim] = []
        for index, line in joined:
            match = re.match(rf"\s*{re.escape(PROG)}\s+([a-z][a-z-]*)", line)
            if not match:
                continue
            claims.append(
                CliClaim(
                    name=match.group(1),
                    flags=frozenset(re.findall(r"(--[a-z][a-z-]*)", line)),
                    line=offset + index,
                )
            )
        return tuple(claims)
    return ()


def _parse_layout_block(text: str) -> tuple[str, ...]:
    """Extract the paths listed in the repository layout block."""
    for info, body in _fenced_blocks(text):
        if info or "src/amf/" not in body:
            continue
        paths: list[str] = []
        for line in body.splitlines():
            match = re.match(r"([A-Za-z0-9_./-]+)\s{2,}", line)
            if match:
                paths.append(match.group(1))
        return tuple(paths)
    return ()


def _parse_config_defaults(text: str) -> dict[str, dict[str, Any]]:
    """Extract ``X defaults: a=1, b=2`` statements into a mapping."""
    out: dict[str, dict[str, Any]] = {}
    for match in re.finditer(r"`(\w*Config)`\s+defaults:\s*(.+?)(?:\n\n|\. |;)", text, re.DOTALL):
        pairs = dict(re.findall(r"(\w+)=([A-Za-z0-9_.\-+]+)", match.group(2)))
        if pairs:
            out.setdefault(match.group(1), {}).update({k: _as_value(v) for k, v in pairs.items()})
    return out


def parse(path: Path) -> Claims:
    """Parse ``CLAUDE.md`` at ``path`` into a :class:`Claims`.

    Args:
        path: Path to the guide.

    Returns:
        The claims recovered from it; fields are left empty when a section is absent.
    """
    text = path.read_text(encoding="utf-8")

    test_match = re.search(r"currently\s+(\d[\d,]*)\s+tests", text)
    modules = tuple(m.group(1) for m in re.finditer(r"^\|\s*`(\w+)\.py`\s*\|", text, re.MULTILINE))
    errors_row = re.search(r"^\|\s*`errors\.py`\s*\|(.+)$", text, re.MULTILINE)
    exceptions = tuple(re.findall(r"`(\w*Error)`", errors_row.group(1))) if errors_row else ()

    count_match = re.search(r"offers\s+(\w+)\s+\n?\s*subcommands", text)
    subcommand_count = _NUMBER_WORDS.get(count_match.group(1).lower()) if count_match else None

    directives = re.search(r"carries\s+\**(\w+)\**\s+`#\s*yamllint disable-line", text)
    codeql = _NUMBER_WORDS.get(directives.group(1).lower()) if directives else None

    constants: dict[str, Any] = {}
    low_redundancy = re.search(r"`_LOW_REDUNDANCY`\s*\(([\d.]+)\)", text)
    if low_redundancy:
        constants["_LOW_REDUNDANCY"] = _as_value(low_redundancy.group(1))

    return Claims(
        text=text,
        test_count=int(test_match.group(1).replace(",", "")) if test_match else None,
        module_rows=modules,
        exception_names=exceptions,
        cli=_parse_cli_block(text),
        subcommand_count=subcommand_count,
        codeql_directives=codeql,
        layout_paths=_parse_layout_block(text),
        config_defaults=_parse_config_defaults(text),
        named_constants=constants,
    )
