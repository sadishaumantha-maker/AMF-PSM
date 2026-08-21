"""Sensitivity and leverage analysis over a market's structural metrics.

Where :mod:`amf.diagnostics` answers *how weak is this market's anatomy*, this
module answers the two follow-up questions:

* **Sensitivity** -- which structural metric does the diagnosis respond to most
  strongly? Each of the four metrics on each of the seven systems is perturbed
  in turn and the market re-diagnosed, giving a finite-difference gradient of
  the overall weakness index.
* **Leverage** -- where would a feasible adjustment help most? The same sweep,
  restricted to changes in the improving direction and ranked by how far they
  move the index down. This is AMF analytical Step 5 (intervention points)
  applied to the model.

Both are *comparative statics on the supplied model*: they describe how this
toolkit's deterministic scoring responds to its own inputs. They are not
empirically validated, and say nothing about how any real market would respond
to any real intervention.

The analysis is deterministic and dependency-free; it re-uses
:class:`~amf.diagnostics.DiagnosticEngine` rather than reimplementing scoring,
so a change to the diagnostic weights is reflected here automatically.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from amf.diagnostics import DiagnosticEngine
from amf.errors import InvalidConfigError
from amf.invariants import check_sensitivity_report
from amf.models import (
    LeveragePoint,
    Sensitivity,
    SensitivityReport,
    Severity,
    SystemKind,
    SystemMetric,
)

if TYPE_CHECKING:
    from amf.market import Market

# Metrics are swept in declaration order so results are reproducible.
_METRICS: tuple[SystemMetric, ...] = tuple(SystemMetric)
_ORDER: tuple[SystemKind, ...] = tuple(SystemKind)


@dataclass(frozen=True, slots=True)
class SensitivityConfig:
    """Parameters controlling a sensitivity sweep.

    Attributes:
        step: How far to perturb each metric, in ``(0, 1]``. Smaller steps
            approximate a local derivative more closely; larger ones describe a
            more substantial intervention.
        include_criticality: Whether to report sensitivity to ``criticality``.
            It is always excluded from leverage points, because it describes how
            load-bearing a system *is* rather than something an operator tunes.
    """

    step: float = 0.05
    include_criticality: bool = True

    def __post_init__(self) -> None:
        """Validate the configuration.

        Raises:
            InvalidConfigError: If ``step`` is outside ``(0, 1]``.
        """
        if not 0.0 < self.step <= 1.0:
            msg = f"sensitivity step must be in (0, 1], got {self.step!r}"
            raise InvalidConfigError(msg)


class SensitivityAnalyzer:
    """Measures how a market's diagnosis responds to its structural metrics."""

    def __init__(self, engine: DiagnosticEngine | None = None, config: SensitivityConfig | None = None) -> None:
        """Initialise the analyser.

        Args:
            engine: The diagnostic engine whose index is differentiated; defaults
                to a :class:`~amf.diagnostics.DiagnosticEngine` with standard
                weights. Passing a custom-weighted engine analyses *that*
                scoring.
            config: Sweep parameters; defaults to :class:`SensitivityConfig`.
        """
        self.engine = engine or DiagnosticEngine()
        self.config = config or SensitivityConfig()

    def _index(self, market: Market) -> float:
        """Return the overall weakness index of a market."""
        return self.engine.diagnose(market).overall_index

    def _variant(self, market: Market, kind: SystemKind, metric: SystemMetric, value: float) -> Market:
        """Return ``market`` with one metric of one system replaced."""
        return market.with_system(market.system(kind).with_metric(metric, value))

    def sensitivity(self, market: Market, kind: SystemKind, metric: SystemMetric) -> Sensitivity:
        """Measure the response of the overall index to one metric of one system.

        A central difference is used where the metric has room on both sides of
        its current value; near ``0`` or ``1`` the difference becomes one-sided
        and ``span`` shrinks accordingly, so the reported gradient stays a slope
        over the interval actually explored.

        Args:
            market: The baseline market.
            kind: The system to perturb.
            metric: The metric to perturb.

        Returns:
            The measured :class:`~amf.models.Sensitivity`.
        """
        baseline = market.system(kind).metric(metric)
        # ``span`` is always positive, so the division below is safe: metrics are
        # confined to [0, 1] and SensitivityConfig confines the step to (0, 1],
        # which leaves at least ``min(step, 1)`` of room on one side or the other.
        low = max(0.0, baseline - self.config.step)
        high = min(1.0, baseline + self.config.step)
        span = high - low
        delta = self._index(self._variant(market, kind, metric, high)) - self._index(
            self._variant(market, kind, metric, low)
        )
        return Sensitivity(
            system=kind,
            metric=metric,
            baseline_value=baseline,
            span=span,
            index_delta=delta,
            gradient=delta / span,
        )

    def leverage_point(self, market: Market, kind: SystemKind, metric: SystemMetric) -> LeveragePoint | None:
        """Measure the improvement from adjusting one metric in its helping direction.

        Args:
            market: The baseline market.
            kind: The system to adjust.
            metric: The metric to adjust.

        Returns:
            The resulting :class:`~amf.models.LeveragePoint`, or ``None`` when no
            adjustment is available -- either the metric is not a lever
            (``criticality``) or it is already at the end of its range, leaving
            no headroom.
        """
        direction = metric.improving_direction()
        if direction == 0:
            return None
        baseline = market.system(kind).metric(metric)
        adjusted = min(1.0, max(0.0, baseline + direction * self.config.step))
        if adjusted == baseline:
            return None
        before = self._index(market)
        after = self._index(self._variant(market, kind, metric, adjusted))
        return LeveragePoint(
            system=kind,
            metric=metric,
            baseline_value=baseline,
            adjusted_value=adjusted,
            index_before=before,
            index_after=after,
            improvement=before - after,
        )

    def analyse(self, market: Market) -> SensitivityReport:
        """Sweep every system and metric, returning a full report.

        Args:
            market: The market to analyse (must be complete).

        Returns:
            A :class:`~amf.models.SensitivityReport` whose sensitivities are
            ordered by absolute gradient descending and whose leverage points are
            ordered by improvement descending. Both fall back to system and
            metric declaration order for ties, so the output is reproducible.
        """
        market.require_complete()
        baseline_index = self._index(market)

        metrics = [m for m in _METRICS if self.config.include_criticality or m is not SystemMetric.CRITICALITY]
        sensitivities = [self.sensitivity(market, kind, metric) for kind in _ORDER for metric in metrics]
        leverage = [
            point
            for kind in _ORDER
            for metric in _METRICS
            if (point := self.leverage_point(market, kind, metric)) is not None
        ]

        sensitivities.sort(key=lambda s: (-abs(s.gradient), _ORDER.index(s.system), _METRICS.index(s.metric)))
        leverage.sort(key=lambda p: (-p.improvement, _ORDER.index(p.system), _METRICS.index(p.metric)))
        return check_sensitivity_report(
            SensitivityReport(
                boundary=market.boundary,
                baseline_index=baseline_index,
                baseline_severity=Severity.from_score(baseline_index),
                step=self.config.step,
                sensitivities=tuple(sensitivities),
                leverage_points=tuple(leverage),
            )
        )
