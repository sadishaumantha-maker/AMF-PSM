"""Mathematical invariants checked at the public engine boundary.

Every engine validates its own result before handing it back, so a computation
that has gone wrong fails loudly at its source instead of flowing onward into a
report, an SVG, or a JSON document that looks perfectly well-formed. The
properties enforced here are exactly the ones the result types *document* and
that downstream code relies on:

* every score, stress level, and index lies in ``[0, 1]`` and is finite, which is
  the precondition :meth:`~amf.models.Severity.from_score` is written against;
* an amplification factor is finite and non-negative (it may exceed ``1`` -- that
  is what amplification means);
* a settling time is a step index or the ``-1`` sentinel;
* a sensitivity span is strictly positive, since the gradient divides by it;
* a centrality vector is max-normalised, so its largest entry is exactly ``1``
  unless the graph is empty.

Each ``check_*`` function returns its argument unchanged, so an engine adopts it
by wrapping its return value -- ``return check_diagnostic_report(report)`` --
with no other change to the call site. The cost is a handful of comparisons per
result, so the checks are always on: there is no "strict" flag to forget to set.

Failures raise :class:`~amf.errors.InvariantError`, never ``assert``.
Assertions vanish under ``python -O``, which would disable the guard precisely
where it matters most.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from amf.errors import InvariantError

if TYPE_CHECKING:
    from collections.abc import Mapping

    from amf.models import (
        DiagnosticReport,
        ResilienceScore,
        SensitivityReport,
        SimulationTrace,
        SystemKind,
    )


def require_unit(name: str, value: float) -> None:
    """Raise :class:`~amf.errors.InvariantError` unless ``value`` is a finite number in ``[0, 1]``.

    ``NaN`` fails: it compares false against both bounds, and a ``NaN`` score
    would band as :attr:`~amf.models.Severity.CRITICAL` while telling the reader
    nothing about the market.

    Args:
        name: Dotted name of the property, used in the error message.
        value: The value to check.

    Raises:
        InvariantError: If ``value`` is not finite or lies outside ``[0, 1]``.
    """
    if not math.isfinite(value) or not 0.0 <= value <= 1.0:
        raise InvariantError(name, value)


def require_non_negative(name: str, value: float) -> None:
    """Raise :class:`~amf.errors.InvariantError` unless ``value`` is finite and at least ``0``.

    Used for quantities with no upper bound, such as an amplification factor.

    Args:
        name: Dotted name of the property, used in the error message.
        value: The value to check.

    Raises:
        InvariantError: If ``value`` is not finite or is negative.
    """
    if not math.isfinite(value) or value < 0.0:
        raise InvariantError(name, value, 0.0, math.inf)


def require_finite(name: str, value: float) -> None:
    """Raise :class:`~amf.errors.InvariantError` unless ``value`` is finite.

    Used for signed quantities such as a gradient, where only the infinities and
    ``NaN`` are meaningless.

    Args:
        name: Dotted name of the property, used in the error message.
        value: The value to check.

    Raises:
        InvariantError: If ``value`` is infinite or ``NaN``.
    """
    if not math.isfinite(value):
        raise InvariantError(name, value, -math.inf, math.inf)


def check_diagnostic_report(report: DiagnosticReport) -> DiagnosticReport:
    """Verify a diagnostic report's numeric invariants and return it unchanged.

    Args:
        report: The report to check.

    Returns:
        ``report``, unmodified.

    Raises:
        InvariantError: If the overall index or any per-system component
            escapes ``[0, 1]``.
    """
    require_unit("overall_index", report.overall_index)
    for finding in report.findings:
        system = finding.system.value
        require_unit(f"findings[{system}].score", finding.score)
        require_unit(f"findings[{system}].fragility", finding.fragility)
        require_unit(f"findings[{system}].concentration", finding.concentration)
        require_unit(f"findings[{system}].feedback", finding.feedback)
    return report


def check_resilience_score(score: ResilienceScore) -> ResilienceScore:
    """Verify a resilience score's numeric invariants and return it unchanged.

    Args:
        score: The score to check.

    Returns:
        ``score``, unmodified.

    Raises:
        InvariantError: If any metric escapes its documented range.
    """
    require_unit("resilience.value", score.value)
    require_unit("resilience.peak_stress", score.peak_stress)
    require_unit("resilience.absorbed_fraction", score.absorbed_fraction)
    require_non_negative("resilience.amplification_factor", score.amplification_factor)
    if score.settling_time < -1:
        raise InvariantError("resilience.settling_time", score.settling_time, -1.0, math.inf)
    return score


def check_simulation_trace(trace: SimulationTrace) -> SimulationTrace:
    """Verify every step of a trajectory stays in ``[0, 1]`` and return it unchanged.

    Args:
        trace: The trace to check.

    Returns:
        ``trace``, unmodified.

    Raises:
        InvariantError: If any per-system stress or resilience metric escapes
            its documented range.
    """
    for index, step in enumerate(trace.steps):
        for kind, stress in step.items():
            require_unit(f"steps[{index}][{kind.value}]", stress)
    if trace.resilience is not None:
        check_resilience_score(trace.resilience)
    return trace


def check_sensitivity_report(report: SensitivityReport) -> SensitivityReport:
    """Verify a sensitivity report's numeric invariants and return it unchanged.

    Args:
        report: The report to check.

    Returns:
        ``report``, unmodified.

    Raises:
        InvariantError: If the baseline index or any leverage index escapes
            ``[0, 1]``, a span is not strictly positive, or a gradient is not
            finite.
    """
    require_unit("baseline_index", report.baseline_index)
    for sensitivity in report.sensitivities:
        label = f"sensitivities[{sensitivity.system.value}.{sensitivity.metric.value}]"
        if not math.isfinite(sensitivity.span) or not 0.0 < sensitivity.span <= 1.0:
            raise InvariantError(f"{label}.span", sensitivity.span)
        require_finite(f"{label}.gradient", sensitivity.gradient)
    for point in report.leverage_points:
        label = f"leverage_points[{point.system.value}.{point.metric.value}]"
        require_unit(f"{label}.index_before", point.index_before)
        require_unit(f"{label}.index_after", point.index_after)
    return report


def check_centrality(centrality: Mapping[SystemKind, float]) -> dict[SystemKind, float]:
    """Verify a centrality vector is max-normalised and return it as a plain dict.

    Every entry must lie in ``[0, 1]``, and because the vector is max-normalised
    the largest entry must be exactly ``1`` whenever any entry is positive. An
    empty or fully isolated graph yields all zeros, which is allowed.

    Args:
        centrality: The system-to-centrality mapping to check.

    Returns:
        The same mapping as a ``dict``.

    Raises:
        InvariantError: If an entry escapes ``[0, 1]`` or the vector carries a
            positive entry without being normalised to a maximum of ``1``.
    """
    result = dict(centrality)
    for kind, value in result.items():
        require_unit(f"centrality[{kind.value}]", value)
    if result:
        peak = max(result.values())
        if peak > 0.0 and peak != 1.0:
            raise InvariantError("centrality.max", peak, 1.0, 1.0)
    return result
