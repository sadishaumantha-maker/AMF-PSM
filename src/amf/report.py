"""Rendering of diagnostic, simulation, and sensitivity results to text, JSON, or Markdown.

These functions are pure formatting helpers: they take result objects produced by
the engines and return strings. They perform no I/O, which keeps the engines free
of presentation concerns and the renderers trivial to test.
"""

from __future__ import annotations

import json
from typing import Any, TypeAlias

from amf.models import (
    DiagnosticReport,
    ResilienceDistribution,
    ResilienceScore,
    SensitivityReport,
    SimulationTrace,
    SystemKind,
)

Renderable: TypeAlias = DiagnosticReport | SimulationTrace | SensitivityReport | dict[SystemKind, ResilienceScore]
"""Any result object the renderers accept.

A :class:`~amf.models.DiagnosticReport` from the diagnostic engine, a
:class:`~amf.models.SimulationTrace` from a single shock, a
:class:`~amf.models.SensitivityReport` from a sensitivity sweep, or the
system-to-:class:`~amf.models.ResilienceScore` mapping a stress test returns.

A :class:`~amf.models.ResilienceDistribution` is deliberately excluded: only
:func:`render_json` serialises one, while the text and Markdown renderers use
the dedicated :func:`render_distribution`.
"""


def render_json(obj: Renderable | ResilienceDistribution) -> str:
    """Render any result object as pretty-printed JSON."""
    return json.dumps(_to_jsonable(obj), indent=2, sort_keys=True)


def _to_jsonable(obj: Any) -> Any:  # noqa: ANN401 - intentional dispatch over result types
    """Convert a result object into JSON-serialisable primitives."""
    if isinstance(obj, (DiagnosticReport, SimulationTrace, SensitivityReport, ResilienceScore, ResilienceDistribution)):
        return obj.to_dict()
    if isinstance(obj, dict):
        return {(k.value if isinstance(k, SystemKind) else str(k)): _to_jsonable(v) for k, v in obj.items()}
    return obj


def render_text(report: Renderable) -> str:
    """Render a diagnostic report, simulation trace, sensitivity report, or stress-test profile as text."""
    if isinstance(report, DiagnosticReport):
        return _diagnostic_text(report)
    if isinstance(report, SensitivityReport):
        return _sensitivity_text(report)
    if isinstance(report, dict):
        return render_stress_test(report)
    return _simulation_text(report)


def render_markdown(report: Renderable) -> str:
    """Render a diagnostic report, simulation trace, sensitivity report, or stress-test profile as Markdown."""
    if isinstance(report, DiagnosticReport):
        return _diagnostic_markdown(report)
    if isinstance(report, SensitivityReport):
        return _sensitivity_markdown(report)
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
        if r.tipped_systems:
            tipped = ", ".join(s.value for s in r.tipped_systems)
            lines.append(f"  Tipped (cascade):     {tipped}")
    return "\n".join(lines)


def render_distribution(dist: ResilienceDistribution) -> str:
    """Render a Monte Carlo resilience distribution as plain text."""
    lines = [
        "Anatomical Market Framework - Resilience Ensemble",
        f"  Shocked system: {dist.target.value}   runs: {dist.runs}",
        "",
        "  metric                mean    p10    p50    p90    min    max",
    ]
    rows = (
        ("resilience", dist.value),
        ("amplification", dist.amplification_factor),
        ("peak stress", dist.peak_stress),
        ("absorbed", dist.absorbed_fraction),
    )
    for name, s in rows:
        lines.append(
            f"  {name:<18} {s.mean:6.3f} {s.p10:6.3f} {s.p50:6.3f} {s.p90:6.3f} {s.minimum:6.3f} {s.maximum:6.3f}"
        )
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
        if r.tipped_systems:
            tipped = ", ".join(s.value for s in r.tipped_systems)
            lines.append(f"| Tipped (cascade) | {tipped} |")
    return "\n".join(lines)


def _sensitivity_text(report: SensitivityReport) -> str:
    """Render a sensitivity report as plain text."""
    b = report.boundary
    lines = [
        "Anatomical Market Framework - Sensitivity & Leverage",
        f"  Market: {b.asset_class} / {b.geography} / {b.timeframe}",
        f"  Baseline weakness index: {report.baseline_index:.3f} [{report.baseline_severity.value}]",
        f"  Perturbation step: {report.step:.3f}",
        "",
        "  Most influential metrics (steepest response first):",
    ]
    for s in report.sensitivities:
        direction = "raises" if s.gradient > 0 else "lowers" if s.gradient < 0 else "does not move"
        lines.append(
            f"    {s.system.value:<12} {s.metric.value:<12} gradient {s.gradient:+.3f}"
            f"  (raising it {direction} weakness)"
        )
    if report.leverage_points:
        lines += ["", "  Leverage points (largest improvement first):"]
        for p in report.leverage_points:
            lines.append(
                f"    {p.system.value:<12} {p.metric.value:<12} "
                f"{p.baseline_value:.2f} -> {p.adjusted_value:.2f}  "
                f"index {p.index_before:.3f} -> {p.index_after:.3f}  "
                f"improvement {p.improvement:+.3f}"
            )
    else:
        lines += ["", "  No adjustable metric has headroom at this step size."]
    return "\n".join(lines)


def _sensitivity_markdown(report: SensitivityReport) -> str:
    """Render a sensitivity report as Markdown."""
    b = report.boundary
    lines = [
        "# AMF Sensitivity & Leverage",
        "",
        f"**Market:** {b.asset_class} / {b.geography} / {b.timeframe}  ",
        f"**Baseline weakness index:** {report.baseline_index:.3f} (`{report.baseline_severity.value}`)  ",
        f"**Perturbation step:** {report.step:.3f}",
        "",
        "## Metric sensitivity",
        "",
        "| System | Metric | Baseline | Span | Index delta | Gradient |",
        "|--------|--------|----------|------|-------------|----------|",
    ]
    for s in report.sensitivities:
        lines.append(
            f"| {s.system.value} | {s.metric.value} | {s.baseline_value:.2f} "
            f"| {s.span:.2f} | {s.index_delta:+.3f} | {s.gradient:+.3f} |"
        )
    lines += ["", "## Leverage points", ""]
    if report.leverage_points:
        lines += [
            "| System | Metric | Adjustment | Index before | Index after | Improvement |",
            "|--------|--------|------------|--------------|-------------|-------------|",
        ]
        for p in report.leverage_points:
            lines.append(
                f"| {p.system.value} | {p.metric.value} "
                f"| {p.baseline_value:.2f} → {p.adjusted_value:.2f} "
                f"| {p.index_before:.3f} | {p.index_after:.3f} | {p.improvement:+.3f} |"
            )
    else:
        lines.append("No adjustable metric has headroom at this step size.")
    return "\n".join(lines)
