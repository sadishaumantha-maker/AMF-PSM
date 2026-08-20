"""Command-line interface for the drift detector.

Exit codes follow the repository's own convention of returning a code rather than calling
``sys.exit`` deep inside, so ``main`` stays unit-testable in process:

* ``0`` -- clean, or drift below the ``--fail-on`` threshold.
* ``1`` -- drift at or above the threshold.
* ``2`` -- the scan could not run.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.docsync.drift import render_markdown, scan
from tools.docsync.model import DriftReport, Severity

EXIT_OK = 0
"""No drift at or above the failure threshold."""

EXIT_DRIFT = 1
"""Drift found at or above the failure threshold."""

EXIT_ERROR = 2
"""The scan itself could not run."""


def _build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser."""
    parser = argparse.ArgumentParser(
        prog="docsync",
        description="Detect drift between CLAUDE.md and the repository it documents.",
    )
    parser.add_argument("--root", type=Path, default=Path(), help="Repository root (default: cwd).")
    parser.add_argument(
        "--format",
        choices=["text", "json", "md"],
        default="text",
        help="Output format.",
    )
    parser.add_argument(
        "--fail-on",
        choices=[s.value for s in Severity],
        default="low",
        help="Lowest severity that should fail the run (default: low).",
    )
    parser.add_argument("--out", type=Path, default=None, help="Write the report to a file as well as stdout.")
    parser.add_argument(
        "--no-test-count",
        action="store_true",
        help="Skip the pytest collection used for the authoritative test total.",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=None,
        help="Compare against a checked-in baseline; only findings absent from it fail the run.",
    )
    return parser


def _render(report_format: str, report: DriftReport) -> str:
    """Render the report in the requested format."""
    if report_format == "json":
        return report.to_json()
    if report_format == "md":
        return render_markdown(report)
    if not report.findings:
        body = "docsync: no drift found.\n"
    else:
        body = "".join(
            f"{f.severity.value:>6}  {f.check:<28} {f.location or '-'}\n        {f.message}\n"
            + (f"        {f.detail}\n" if f.detail else "")
            for f in report.findings
        )
        body += f"\n{len(report.findings)} finding(s).\n"
    for name, reason in sorted(report.skipped.items()):
        body += f"skipped {name}: {reason}\n"
    return body


def main(argv: list[str] | None = None) -> int:
    """Run a scan and print the report.

    Args:
        argv: Argument vector; ``None`` reads ``sys.argv``.

    Returns:
        A process exit code.
    """
    args = _build_parser().parse_args(argv)
    root: Path = args.root.resolve()
    if not (root / "CLAUDE.md").is_file():
        print(f"docsync: no CLAUDE.md under {root}")
        return EXIT_ERROR

    report = scan(root, with_test_count=not args.no_test_count)
    rendered = _render(args.format, report)
    print(rendered, end="")
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")

    failing = report.at_or_above(Severity(args.fail_on))
    if args.baseline is not None and args.baseline.is_file():
        known = {
            (f["check"], f["location"], f["message"], f.get("detail", ""))
            for f in json.loads(args.baseline.read_text(encoding="utf-8")).get("findings", [])
        }
        failing = tuple(f for f in failing if f.key not in known)
        if failing:
            print(f"\n{len(failing)} finding(s) are new since the baseline.")
    return EXIT_DRIFT if failing else EXIT_OK
