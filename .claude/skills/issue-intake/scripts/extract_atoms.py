#!/usr/bin/env python3
"""Decompose a source document into a reviewable issue manifest.

Emits one record per addressable source unit: its verbatim heading, its verbatim atoms, a stable
id, a content hash for idempotency, and any guardrail conflict detected in the text.

The manifest is the approval gate. It is cheap to read, cheap to diff, and cheap to throw away —
unlike 43 published issues. Nothing reaches GitHub except by executing an approved manifest.

This uses **block splitting** on heading boundaries. The auditor's parser
(``.claude/skills/issue-audit/scripts/fidelity_check.py``) uses a line-oriented state machine over
the same document. That duplication is deliberate: two independent parsers agreeing on an atom
count is evidence of correctness, one parser agreeing with itself is not. See ADR-002.

Usage
-----
    python3 extract_atoms.py --source docs/RESEARCH_DISCUSSIONS.md \\
                             --out .claude/manifests/RESEARCH_DISCUSSIONS.manifest.yaml

    python3 extract_atoms.py --source docs/X.md --stats-only
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

# --------------------------------------------------------------------------------------
# Guardrail detection
# --------------------------------------------------------------------------------------

# Substrings forbidden in *identifiers* by tests/unit/test_non_trading_boundary.py. Their presence
# in source prose is not itself a violation, but a unit built around them usually needs a
# structural reframing, so the manifest flags it for a human.
FORBIDDEN = (
    "order",
    "buy",
    "sell",
    "price",
    "pnl",
    "broker",
    "backtest",
    "ticker",
    "trade",
    "portfolio",
    "candlestick",
    "returns",
    "signal",
)

# Phrases that claim, or invite, predictive capability. The package is explicitly
# illustrative-and-not-validated, so these always need an explicit reframing decision.
PREDICTIVE = (
    "predict",
    "forecast",
    "prediction",
    "forecasting",
    "leading indicator",
    "months ahead",
    "will reprice",
    "will reprrice",
)


def guardrail_flags(text: str) -> list[str]:
    """Return the guardrail concerns raised by a unit's text, most serious first."""
    low = text.lower()
    flags = []
    hits = sorted({w for w in PREDICTIVE if w in low})
    if hits:
        flags.append("predictive-framing: " + ", ".join(hits))
    hits = sorted({w for w in FORBIDDEN if w in low})
    if hits:
        flags.append("non-trading-vocabulary: " + ", ".join(hits))
    return flags


# --------------------------------------------------------------------------------------
# Block splitting
# --------------------------------------------------------------------------------------

HEADING = re.compile(r"^(#{2,4}) (.+)$", re.M)
TRACK = re.compile(r"^Track (\d+): (.+)$")
# Two numbering schemes in the wild: dotted (`Discussion 3.2:`, tracked under a Track heading) and
# prefixed (`Discussion Q1:`, standalone). Both are accepted; only the dotted form implies a parent.
DISCUSSION = re.compile(r"^Discussion (\d+\.\d+|[A-Z]\d+): (.+)$")
THEME = re.compile(r"^Theme ([A-D]): (.+)$")

# Any bold label followed by a value on the same line is a field atom. Deliberately generic: source
# documents invent their own labels (Concept, Mathematical Framework, Research Leaders Needed…) and a
# hardcoded list silently drops whatever it has not heard of. Labels that end a line with nothing
# after the colon — `**Key Questions**:` — are list headers, not fields, and do not match.
FIELD = re.compile(r"^\*\*([A-Za-z][A-Za-z /&-]*)\*\*: (.+)$", re.M)
BULLET_BLOCK = re.compile(r"^\*\*(Key Questions|Research Areas)\*\*:\n((?:- .+\n)+)", re.M)
NUMBERED = re.compile(r"^(\d+)\. (.+)$", re.M)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_blocks(text: str) -> list[tuple[str, str, str]]:
    """Yield (level, heading, body) per heading, where body includes the heading's whole subtree.

    A block runs to the next heading of the *same or shallower* depth, not merely the next heading.
    Documents differ in where they put a discussion: `docs/RESEARCH_DISCUSSIONS.md` makes each one a
    leaf `####`, while `docs/QUANTUM_NEURAL_RESEARCH.md` makes it a `###` containing several `####`
    sub-sections. Cutting at every heading orphaned those sub-sections and silently dropped most of
    the second document's content — 22 atoms out of 799 lines.
    """
    marks = list(HEADING.finditer(text))
    out = []
    for i, m in enumerate(marks):
        depth = len(m.group(1))
        end = len(text)
        for j in range(i + 1, len(marks)):
            if len(marks[j].group(1)) <= depth:
                end = marks[j].start()
                break
        out.append((m.group(1), m.group(2).strip(), text[m.end() : end]))
    return out


def extract(text: str) -> tuple[list[dict], dict[str, int]]:
    """Return (units, atom counts by type)."""
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n"))
    units: list[dict] = []
    counts: dict[str, int] = {}

    def bump(kind: str, n: int = 1) -> None:
        counts[kind] = counts.get(kind, 0) + n

    for level, heading, body in split_blocks(text):
        atoms: list[dict] = []
        uid = kind = None
        parent = None

        m = DISCUSSION.match(heading)
        if m and level in ("###", "####"):
            ident = m.group(1)
            uid = f"discussion-{ident.lower()}"
            kind = "discussion"
            parent = f"track-{ident.split('.')[0]}" if "." in ident else None
            for fm in FIELD.finditer(body):
                label = fm.group(1).strip().lower().replace(" ", "-")
                atoms.append({"type": label, "text": fm.group(2).strip()})
                bump(label)
            for bm in BULLET_BLOCK.finditer(body):
                label = "key-question" if bm.group(1) == "Key Questions" else "research-area"
                for line in bm.group(2).strip().split("\n"):
                    atoms.append({"type": label, "text": line[2:].strip()})
                    bump(label)

        elif THEME.match(heading) and level == "###":
            tm = THEME.match(heading)
            uid = f"theme-{tm.group(1).lower()}"  # type: ignore[union-attr]
            kind = "theme"
            parent = "cross-cutting"
            for line in body.split("\n"):
                if line.startswith("- "):
                    atoms.append({"type": "theme-bullet", "text": line[2:].strip()})
                    bump("theme-bullet")

        elif TRACK.match(heading) and level == "###":
            tm = TRACK.match(heading)
            uid = f"track-{tm.group(1)}"  # type: ignore[union-attr]
            kind = "track"

        elif heading.startswith("🚀"):
            for nm in NUMBERED.finditer(body):
                units.append(
                    {
                        "uid": f"next-step-{nm.group(1)}",
                        "kind": "next-step",
                        "title": None,
                        "parent": "program",
                        "atoms": [{"type": "process-step", "text": nm.group(2).strip()}],
                        "flags": guardrail_flags(nm.group(2)),
                    }
                )
                bump("process-step")
            continue

        if uid is None:
            continue

        # Flags are computed over the unit's ENTIRE source body, not just the atoms extracted from
        # it. A safety check that only sees what the parser understood inherits the parser's blind
        # spots — and a guardrail conflict sitting in a paragraph the extractor skipped is exactly
        # the one nobody would catch downstream.
        units.append(
            {
                "uid": uid,
                "kind": kind,
                "title": heading,
                "parent": parent,
                "atoms": atoms,
                "flags": guardrail_flags(heading + "\n" + body),
            }
        )

    # Synthesised containers. They have no heading of their own, but they are real issues and must
    # appear in the manifest or they are published — and audited — by nobody. Their atoms are their
    # children's, so a change to any child changes the container hash and triggers a re-publish.
    def container(uid: str, child_kind: str) -> None:
        children = [a for u in units if u["kind"] == child_kind for a in u["atoms"]]
        if children:
            units.append(
                {
                    "uid": uid,
                    "kind": "container",
                    "title": None,
                    "parent": None,
                    "atoms": children,
                    "flags": guardrail_flags("\n".join(a["text"] for a in children)),
                }
            )

    container("cross-cutting", "theme")
    container("program", "next-step")

    return units, counts


# --------------------------------------------------------------------------------------
# YAML emission (stdlib only — block scalars sidestep every quoting hazard)
# --------------------------------------------------------------------------------------


def yaml_block(text: str, indent: int) -> str:
    pad = " " * indent
    return "|-\n" + "\n".join(pad + line for line in text.split("\n"))


def emit(source: Path, digest: str, units: list[dict], counts: dict[str, int]) -> str:
    out: list[str] = []
    out.append("# Decomposition manifest — REVIEW BEFORE PUBLISHING")
    out.append("#")
    out.append("# Generated by .claude/skills/issue-intake/scripts/extract_atoms.py")
    out.append("# Nothing here has been written to GitHub. A human approves this file first.")
    out.append("")
    out.append(f"source: {source.as_posix()}")
    out.append(f"source_sha256: {digest}")
    out.append(f"unit_count: {len(units)}")
    out.append("atom_counts:")
    for k in sorted(counts):
        out.append(f"  {k}: {counts[k]}")
    out.append(f"  TOTAL: {sum(counts.values())}")
    out.append("")
    flagged = [u for u in units if u["flags"]]
    out.append(f"guardrail_flagged: {len(flagged)}")
    out.append("")
    out.append("units:")
    for u in units:
        out.append(f"  - uid: {u['uid']}")
        out.append(f"    kind: {u['kind']}")
        out.append(f"    parent: {u['parent'] or '~'}")
        if u["title"] is not None:
            out.append(f"    title: {yaml_block(u['title'], 8)}")
        body_text = "\n".join(a["text"] for a in u["atoms"])
        out.append(f"    title_sha256: {sha(u['title'] or u['uid'])[:16]}")
        out.append(f"    body_sha256: {sha(body_text)[:16]}")
        if u["flags"]:
            out.append("    guardrail_flags:")
            for f in u["flags"]:
                out.append(f'      - "{f}"')
        out.append(f"    atom_count: {len(u['atoms'])}")
        if u["atoms"]:
            out.append("    atoms:")
            for a in u["atoms"]:
                out.append(f"      - type: {a['type']}")
                out.append(f"        text: {yaml_block(a['text'], 12)}")
        out.append("")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--stats-only", action="store_true")
    args = ap.parse_args(argv)

    try:
        raw = args.source.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    digest = sha(raw)
    units, counts = extract(raw)

    print(f"source : {args.source}")
    print(f"sha256 : {digest[:16]}")
    print(f"units  : {len(units)}")
    for k in sorted(counts):
        print(f"  {k:<16} {counts[k]}")
    print(f"  {'TOTAL':<16} {sum(counts.values())}")

    flagged = [u for u in units if u["flags"]]
    if flagged:
        print(f"\nguardrail-flagged units: {len(flagged)}")
        for u in flagged:
            print(f"  {u['uid']:<20} {'; '.join(u['flags'])}")

    if args.stats_only:
        return 0
    if args.out is None:
        print("\nerror: --out required unless --stats-only", file=sys.stderr)
        return 2

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(emit(args.source, digest, units, counts), encoding="utf-8")
    print(f"\nmanifest written: {args.out}")
    print("REVIEW IT before running issue-publisher.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
