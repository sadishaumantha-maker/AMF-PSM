"""Run every check and assemble a canonical report."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tools.docsync import claims as claims_module
from tools.docsync import facts as facts_module
from tools.docsync.checks import CHECKS
from tools.docsync.model import DriftReport, Severity

if TYPE_CHECKING:
    from pathlib import Path

    from tools.docsync.model import Finding


def scan(root: Path, *, with_test_count: bool = True) -> DriftReport:
    """Scan the repository at ``root`` for drift between it and ``CLAUDE.md``.

    Args:
        root: Repository root.
        with_test_count: Whether to ask pytest for an authoritative test total. When
            disabled, the test-count check is reported as skipped rather than guessed.

    Returns:
        A report whose findings are in canonical order.
    """
    repo_facts = facts_module.collect(root, with_test_count=with_test_count)
    guide = root / "CLAUDE.md"
    if not guide.is_file():
        return DriftReport(skipped={"*": "CLAUDE.md not found"})
    parsed = claims_module.parse(guide)

    findings: list[Finding] = []
    for check in CHECKS:
        findings.extend(check(repo_facts, parsed))

    skipped: dict[str, str] = {}
    if repo_facts.test_count is None:
        skipped["docs.test-count"] = "pytest could not be run to collect an authoritative count"
    if parsed.test_count is None:
        skipped["docs.test-count"] = "the guide states no test total"

    return DriftReport(findings=tuple(sorted(findings, key=lambda f: f.key)), skipped=skipped)


def render_markdown(report: DriftReport) -> str:
    """Render a report as Markdown suitable for a PR body or an issue."""
    if not report.findings:
        lines = ["# CLAUDE.md drift report", "", "No drift found. The guide matches the repository."]
    else:
        by_severity: dict[Severity, int] = {}
        for finding in report.findings:
            by_severity[finding.severity] = by_severity.get(finding.severity, 0) + 1
        ordered = sorted(by_severity.items(), key=lambda kv: -kv[0].rank)
        summary = ", ".join(f"{count} {sev.value}" for sev, count in ordered)
        lines = [
            "# CLAUDE.md drift report",
            "",
            f"**{len(report.findings)} finding(s)** — {summary}.",
            "",
            "| Severity | Check | Where | Finding |",
            "|----------|-------|-------|---------|",
        ]
        lines.extend(
            f"| {f.severity.value} | `{f.check}` | `{f.location or '-'}` | {f.message}"
            + (f"<br><sub>{f.detail}</sub>" if f.detail else "")
            + " |"
            for f in report.findings
        )
    if report.skipped:
        lines.extend(["", "## Skipped checks", ""])
        lines.extend(f"- `{name}` — {reason}" for name, reason in sorted(report.skipped.items()))
    return "\n".join(lines) + "\n"
