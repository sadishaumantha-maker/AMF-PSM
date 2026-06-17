"""Rendering of diagnostic and simulation results to text, JSON, or Markdown.

These functions are pure formatting helpers: they take result objects produced by
the engines and return strings. They perform no I/O, which keeps the engines free
of presentation concerns and the renderers trivial to test.
"""

from __future__ import annotations

import json
from typing import Any

from amf.models import DiagnosticReport, ResilienceScore, SimulationTrace, SystemKind


def render_json(obj: DiagnosticReport | SimulationTrace | dict[SystemKind, ResilienceScore]) -> str:
    """Render any result object as pretty-printed JSON."""
    return json.dumps(_to_jsonable(obj), indent=2, sort_keys=True)


def _to_jsonable(obj: Any) -> Any:  # noqa: ANN401 - intentional dispatch over result types
    """Convert a result object into JSON-serialisable primitives."""
    if isinstance(obj, (DiagnosticReport, SimulationTrace, ResilienceScore)):
        return obj.to_dict()
    if isinstance(obj, dict):
        return {(k.value if isinstance(k, SystemKind) else str(k)): _to_jsonable(v) for k, v in obj.items()}
    return obj


def render_text(report: DiagnosticReport | SimulationTrace | dict[SystemKind, ResilienceScore]) -> str:
    """Render a diagnostic report, simulation trace, or stress-test profile as plain text."""
    if isinstance(report, DiagnosticReport):
        return _diagnostic_text(report)
    if isinstance(report, dict):
        return render_stress_test(report)
    return _simulation_text(report)


def render_markdown(report: DiagnosticReport | SimulationTrace | dict[SystemKind, ResilienceScore]) -> str:
    """Render a diagnostic report, simulation trace, or stress-test profile as Markdown."""
    if isinstance(report, DiagnosticReport):
        return _diagnostic_markdown(report)
    if isinstance(report, dict):
        return _stress_test_markdown(report)
    return _simulation_markdown(report)


def render_stress_test(profile: dict[SystemKind, ResilienceScore]) -> str:
    """Render a stress-test profile (system -> resilience) as plain text."""
    lines = ["Systemic stress test (shock each system in turn):", ""]
    ranked = sorted(profile.items(), key=lambda kv: kv[1].value)
    for kind, score in ranked:
        lines.append(
            f"  {kind.value:<12} resilience {score.value:.3f} [{score.severity.value:<8}] "
            f"peak {score.peak_stress:.3f}  absorbed {score.absorbed_fraction:.3f}  "
            f"amplification {score.amplification_factor:.3f}"
        )
    return "\n".join(lines)


def _stress_test_markdown(profile: dict[SystemKind, ResilienceScore]) -> str:
    """Render a stress-test profile (system -> resilience) as a Markdown table."""
    lines = [
        "# AMF Systemic Stress Test",
        "",
        "Shock each system in turn (weakest resilience first).",
        "",
        "| System | Resilience | Severity | Peak stress | Absorbed | Amplification |",
        "|--------|------------|----------|-------------|----------|---------------|",
    ]
    for kind, score in sorted(profile.items(), key=lambda kv: kv[1].value):
        lines.append(
            f"| {kind.value} | {score.value:.3f} | {score.severity.value} "
            f"| {score.peak_stress:.3f} | {score.absorbed_fraction:.3f} "
            f"| {score.amplification_factor:.3f} |"
        )
    return "\n".join(lines)


def _diagnostic_text(report: DiagnosticReport) -> str:
    b = report.boundary
    lines = [
        "Anatomical Market Framework - Structural Diagnosis",
        f"  Market: {b.asset_class} / {b.geography} / {b.timeframe}",
        f"  Overall weakness index: {report.overall_index:.3f} [{report.overall_severity.value}]",
        "",
        "  Per-system findings (weakest first):",
    ]
    for f in report.findings:
        marker = " *SPOF*" if f.is_single_point_of_failure else ""
        lines.append(
            f"    {f.system.value:<12} score {f.score:.3f} [{f.severity.value:<8}]"
            f"  fragility {f.fragility:.2f}  concentration {f.concentration:.2f}"
            f"  feedback {f.feedback:.2f}{marker}"
        )
        for driver in f.drivers:
            lines.append(f"        - {driver}")
    if report.single_points_of_failure:
        spofs = ", ".join(s.value for s in report.single_points_of_failure)
        lines += ["", f"  Single points of failure: {spofs}"]
    if report.feedback_loops:
        lines += ["", "  Feedback loops:"]
        for loop in report.feedback_loops:
            lines.append("    " + " -> ".join(s.value for s in loop) + f" -> {loop[0].value}")
    return "\n".join(lines)


def _simulation_text(trace: SimulationTrace) -> str:
    shocks = ", ".join(f"{s.target.value}={s.magnitude:.2f}" for s in trace.shocks)
    lines = [
        "Anatomical Market Framework - Shock Propagation",
        f"  Shocks: {shocks}",
        f"  Steps simulated: {len(trace.steps) - 1}  converged: {trace.converged}",
    ]
    if trace.resilience is not None:
        r = trace.resilience
        lines += [
            "",
            f"  Resilience: {r.value:.3f} [{r.severity.value}]",
            f"  Peak systemic stress: {r.peak_stress:.3f}",
            f"  Absorbed fraction:    {r.absorbed_fraction:.3f}",
            f"  Amplification factor: {r.amplification_factor:.3f}",
            f"  Settling time:        {r.settling_time} steps",
        ]
    return "\n".join(lines)


def _diagnostic_markdown(report: DiagnosticReport) -> str:
    b = report.boundary
    lines = [
        "# AMF Structural Diagnosis",
        "",
        f"**Market:** {b.asset_class} / {b.geography} / {b.timeframe}  ",
        f"**Overall weakness index:** {report.overall_index:.3f} (`{report.overall_severity.value}`)",
        "",
        "| System | Score | Severity | Fragility | Concentration | Feedback | SPOF |",
        "|--------|-------|----------|-----------|---------------|----------|------|",
    ]
    for f in report.findings:
        lines.append(
            f"| {f.system.value} | {f.score:.3f} | {f.severity.value} | {f.fragility:.2f} "
            f"| {f.concentration:.2f} | {f.feedback:.2f} | "
            f"{'yes' if f.is_single_point_of_failure else 'no'} |"
        )
    return "\n".join(lines)


def _simulation_markdown(trace: SimulationTrace) -> str:
    shocks = ", ".join(f"`{s.target.value}`={s.magnitude:.2f}" for s in trace.shocks)
    lines = ["# AMF Shock Propagation", "", f"**Shocks:** {shocks}  ", f"**Converged:** {trace.converged}"]
    if trace.resilience is not None:
        r = trace.resilience
        lines += [
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Resilience | {r.value:.3f} (`{r.severity.value}`) |",
            f"| Peak systemic stress | {r.peak_stress:.3f} |",
            f"| Absorbed fraction | {r.absorbed_fraction:.3f} |",
            f"| Amplification factor | {r.amplification_factor:.3f} |",
            f"| Settling time | {r.settling_time} steps |",
        ]
    return "\n".join(lines)
