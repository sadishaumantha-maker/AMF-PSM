#!/usr/bin/env python3
"""Deterministic fidelity checker: published GitHub issues vs. their source document.

Answers one question mechanically: does every atomic unit of the source document appear,
verbatim, in the issue that claims to carry it — in the **title** as well as the body?

Why this exists: a hand review of 43 issues found every body verbatim-correct and missed a
one-character title defect (issue #62, `Feedback Loops: Markets ↔ Policy` published as
`Feedback Loops — Markets ↔ Policy`). Titles were simply never checked. See ADR-001.

This parser is deliberately an INDEPENDENT implementation from
``.claude/skills/issue-intake/scripts/extract_atoms.py``. Two parsers agreeing on a count is
evidence; one parser agreeing with itself is not. See ADR-002 — do not refactor them together.

Usage
-----
    python3 fidelity_check.py --source docs/RESEARCH_DISCUSSIONS.md \\
                              --issues issues.json \\
                              --index .claude/memory/issue-index.md

``issues.json`` is a JSON array of ``{"number": int, "title": str, "body": str}`` produced by the
calling agent from ``mcp__github__issue_read``. Network access lives in the agent; determinism
lives here.

Exit codes: 0 = no defects, 1 = defects found, 2 = usage/parse error.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

# --------------------------------------------------------------------------------------
# Normalisation
# --------------------------------------------------------------------------------------

# The GitHub MCP server HTML-escapes text on read: & -> &amp;, " -> &#34;, ' -> &#39;, > -> &gt;.
# Exactly ONE unescape pass is applied. Unescaping repeatedly would silently repair a genuine
# double-escape (&amp;amp;), which is a real defect we want to see. See ADR-004.


def normalise(text: str) -> str:
    """Undo transport escaping and cosmetic whitespace, preserving every meaningful character."""
    out = html.unescape(text)
    out = unicodedata.normalize("NFC", out)
    out = out.replace("\r\n", "\n").replace("\r", "\n")
    # Collapse runs of spaces/tabs but never touch newlines: Markdown line breaks are two
    # trailing spaces, and those are stripped per-line below rather than mangled here.
    out = "\n".join(re.sub(r"[ \t]+", " ", line).strip() for line in out.split("\n"))
    return out


# --------------------------------------------------------------------------------------
# Source parsing (line-oriented, independent of extract_atoms.py)
# --------------------------------------------------------------------------------------

DISCUSSION_RE = re.compile(r"^#### (Discussion (\d+)\.(\d+): .+)$")
THEME_RE = re.compile(r"^### (Theme ([A-D]): .+)$")
TRACK_RE = re.compile(r"^### (Track (\d+): (.+))$")
FIELD_RE = re.compile(r"^\*\*(Theme|Deliverable)\*\*: (.+)$")
LIST_HEAD_RE = re.compile(r"^\*\*(Key Questions|Research Areas)\*\*:$")
NUMBERED_RE = re.compile(r"^(\d+)\. (.+)$")


class Unit:
    """One addressable piece of the source document."""

    def __init__(self, uid: str, kind: str, heading: str | None) -> None:
        self.uid = uid
        self.kind = kind
        self.heading = heading
        self.atoms: list[str] = []

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"Unit({self.uid}, {len(self.atoms)} atoms)"


def parse_source(text: str) -> dict[str, Unit]:
    """Walk the document once, emitting a unit per addressable section."""
    lines = normalise(text).split("\n")
    units: dict[str, Unit] = {}
    current: Unit | None = None
    collecting: str | None = None
    section: str | None = None  # which top-level '## ' section we are inside

    for raw in lines:
        line = raw

        if line.startswith("## "):
            section = line[3:].strip()
            collecting = None
            if not line.startswith("## 📚"):
                current = None

        m = TRACK_RE.match(line)
        if m:
            uid = f"track-{m.group(2)}"
            current = units.setdefault(uid, Unit(uid, "track", m.group(1)))
            current.heading = m.group(1)
            collecting = None
            continue

        m = DISCUSSION_RE.match(line)
        if m:
            uid = f"discussion-{m.group(2)}.{m.group(3)}"
            current = Unit(uid, "discussion", m.group(1))
            units[uid] = current
            collecting = None
            continue

        m = THEME_RE.match(line)
        if m:
            uid = f"theme-{m.group(2).lower()}"
            current = Unit(uid, "theme", m.group(1))
            units[uid] = current
            collecting = None
            continue

        if current is not None and current.kind == "discussion":
            m = FIELD_RE.match(line)
            if m:
                current.atoms.append(m.group(2))
                collecting = None
                continue
            if LIST_HEAD_RE.match(line):
                collecting = "bullets"
                continue

        if collecting == "bullets":
            if line.startswith("- "):
                current.atoms.append(line[2:])  # type: ignore[union-attr]
                continue
            if line:
                collecting = None

        if current is not None and current.kind == "theme" and line.startswith("- "):
            current.atoms.append(line[2:])
            continue

        # Numbered items in the two process sections become their own units.
        m = NUMBERED_RE.match(line)
        if m and section:
            if section.startswith("🚀"):
                uid = f"next-step-{m.group(1)}"
                units.setdefault(uid, Unit(uid, "next-step", None)).atoms.append(m.group(2))
            elif section.startswith("📌"):
                uid = "program"
                units.setdefault(uid, Unit(uid, "program", None)).atoms.append(m.group(2))

    # A track issue must carry each child discussion's theme and deliverable.
    for uid, unit in list(units.items()):
        if unit.kind != "discussion":
            continue
        track = f"track-{uid.split('-')[1].split('.')[0]}"
        if track in units and unit.atoms:
            units[track].atoms.append(unit.atoms[0])  # theme
            units[track].atoms.append(unit.atoms[-1])  # deliverable

    # The cross-cutting container issue carries every theme's bullets. Without this the unit is
    # indexed but never parsed, so its fidelity goes silently unverified — a blind spot found by
    # the first live run of this checker.
    theme_bullets = [a for u in units.values() if u.kind == "theme" for a in u.atoms]
    if theme_bullets:
        cc = Unit("cross-cutting", "container", None)
        cc.atoms = theme_bullets
        units["cross-cutting"] = cc

    # The program issue must also carry every next-step item verbatim.
    if "program" in units:
        for n in range(1, 99):
            step = units.get(f"next-step-{n}")
            if step is None:
                break
            units["program"].atoms.extend(step.atoms)

    return units


# --------------------------------------------------------------------------------------
# Index parsing
# --------------------------------------------------------------------------------------

INDEX_ROW_RE = re.compile(r"^\|\s*([a-z0-9.\-]+)\s*\|\s*#(\d+)\s*\|")


def parse_index(text: str) -> dict[str, int]:
    """Map unit id -> issue number from the markdown table in issue-index.md."""
    mapping: dict[str, int] = {}
    for line in text.split("\n"):
        m = INDEX_ROW_RE.match(line.strip())
        if m:
            mapping[m.group(1)] = int(m.group(2))
    return mapping


# --------------------------------------------------------------------------------------
# Title rules
# --------------------------------------------------------------------------------------


def expected_titles(unit: Unit) -> list[str] | None:
    """Acceptable titles for a unit, or None when the title is synthesised and unchecked.

    ADR-001: a source heading is an atom. The only permitted restyling is a bracketed prefix
    for track issues; the heading text itself is never edited.
    """
    if unit.heading is None:
        return None
    if unit.kind in ("discussion", "theme"):
        return [unit.heading]
    if unit.kind == "track":
        m = TRACK_RE.match(f"### {unit.heading}")
        if m:
            return [unit.heading, f"[Track {m.group(2)}] {m.group(3)}"]
    return [unit.heading]


# --------------------------------------------------------------------------------------
# Checking
# --------------------------------------------------------------------------------------


def check(units: dict[str, Unit], index: dict[str, int], issues: dict[int, dict]) -> list[dict]:
    defects: list[dict] = []
    for uid in sorted(units):
        unit = units[uid]
        number = index.get(uid)
        if number is None:
            defects.append({"unit": uid, "kind": "unmapped", "detail": "no issue in index"})
            continue
        issue = issues.get(number)
        if issue is None:
            defects.append({"unit": uid, "issue": number, "kind": "missing", "detail": "not in issues.json"})
            continue

        title = normalise(issue.get("title", ""))
        body = normalise(issue.get("body", ""))

        allowed = expected_titles(unit)
        if allowed is not None and title not in allowed:
            defects.append(
                {
                    "unit": uid,
                    "issue": number,
                    "kind": "title",
                    "source": allowed[0],
                    "published": title,
                }
            )

        for atom in unit.atoms:
            if atom and atom not in body:
                defects.append({"unit": uid, "issue": number, "kind": "atom", "source": atom})

    # Reverse direction: an indexed unit the parser never produced is a hole in this checker, not a
    # clean bill of health. Name it loudly — an unverified issue that looks verified is the worst
    # possible audit outcome.
    for uid, number in sorted(index.items()):
        if uid not in units:
            defects.append(
                {
                    "unit": uid,
                    "issue": number,
                    "kind": "unparsed",
                    "detail": "indexed but the source parser emits no such unit — NOT VERIFIED",
                }
            )
    return defects


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--issues", required=True, type=Path)
    ap.add_argument("--index", required=True, type=Path)
    ap.add_argument("--expect-atoms", type=int, default=None, help="fail if the atom count differs")
    args = ap.parse_args(argv)

    try:
        units = parse_source(args.source.read_text(encoding="utf-8"))
        index = parse_index(args.index.read_text(encoding="utf-8"))
        raw = json.loads(args.issues.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    issues = {int(i["number"]): i for i in raw}

    # Atom total counts each source atom once, before track/program units re-reference them.
    primary = sum(len(u.atoms) for u in units.values() if u.kind in ("discussion", "theme", "next-step"))

    print(f"source   : {args.source}")
    print(f"units    : {len(units)}  (checked against {len(issues)} fetched issues)")
    print(f"atoms    : {primary} primary")
    print()

    defects = check(units, index, issues)

    by_unit: dict[str, list[dict]] = {}
    for d in defects:
        by_unit.setdefault(d["unit"], []).append(d)

    for uid in sorted(units):
        marks = by_unit.get(uid, [])
        status = "PASS" if not marks else "FAIL"
        num = index.get(uid)
        label = f"#{num}" if num else "unmapped"
        print(f"  {status}  {uid:<20} {label:<8} atoms={len(units[uid].atoms)}")

    print()
    if not defects:
        print("ZERO DEFECTS")
    else:
        print(f"{len(defects)} DEFECT(S)")
        for d in defects:
            print()
            print(f"  unit    : {d['unit']}  issue #{d.get('issue', '?')}")
            print(f"  kind    : {d['kind']}")
            if d["kind"] == "title":
                print(f"  source  : {d['source']!r}")
                print(f"  publishd: {d['published']!r}")
            elif "source" in d:
                print(f"  missing : {d['source']!r}")
            else:
                print(f"  detail  : {d['detail']}")

    if args.expect_atoms is not None and primary != args.expect_atoms:
        print(f"\nATOM COUNT MISMATCH: expected {args.expect_atoms}, parsed {primary}", file=sys.stderr)
        return 1

    return 1 if defects else 0


if __name__ == "__main__":
    raise SystemExit(main())
