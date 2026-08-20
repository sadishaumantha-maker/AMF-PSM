"""Shared value types for the Anatomical Market Framework (AMF) toolkit.

This module defines the vocabulary used across every engine: the seven
anatomical :class:`SystemKind` members, the :class:`DependencyKind` of couplings
between them, the :class:`MarketBoundary` (AMF analytical Step 1), a
:class:`Severity` scale, and the frozen, serialisable result types returned by
the diagnostic and simulation engines.

Everything here is deliberately *structural*: there are no prices, orders, P&L,
or trade concepts anywhere in the type system. The toolkit models market
*anatomy and resilience*, not trading.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class SystemKind(StrEnum):
    """The seven anatomical systems of a market, per the AMF.

    Each member maps a biological system to its market counterpart.
    """

    SKELETON = "skeleton"
    """Market infrastructure: exchanges, clearing houses, settlement systems."""
    CIRCULATORY = "circulatory"
    """Capital flow: credit channels, liquidity facilities, payment rails."""
    NERVOUS = "nervous"
    """Information and signals: price discovery, data feeds, disclosures."""
    MUSCULATURE = "musculature"
    """Active participants: market makers, investors, algorithmic systems."""
    ORGANS = "organs"
    """Functional subsystems: primary/secondary, spot/derivatives segments."""
    IMMUNE = "immune"
    """Risk management and regulation: circuit breakers, margin, oversight."""
    METABOLISM = "metabolism"
    """Value creation and destruction: capital deployment and efficiency."""


class DependencyKind(StrEnum):
    """The nature of a directed coupling between two anatomical systems."""

    STRUCTURAL = "structural"
    """One system relies on another to exist or function at all."""
    INFORMATIONAL = "informational"
    """One system relies on signals or data produced by another."""
    CAPITAL = "capital"
    """One system relies on capital or liquidity supplied by another."""
    REGULATORY = "regulatory"
    """One system is constrained or protected by another's controls."""


class SystemMetric(StrEnum):
    """One of the four structural metrics carried by an anatomical system.

    Naming a metric as a value lets analyses iterate over the metrics
    generically -- perturbing each in turn -- instead of hard-coding four
    branches. Every member is the name of the corresponding
    :class:`~amf.systems.AnatomicalSystem` field.
    """

    INTEGRITY = "integrity"
    """How intact and robust the system is."""
    REDUNDANCY = "redundancy"
    """Availability of fallbacks or alternatives."""
    CRITICALITY = "criticality"
    """How load-bearing the system is for the market."""
    LOAD = "load"
    """Current stress level."""

    def improving_direction(self) -> int:
        """Return the sign of the change that *reduces* structural weakness.

        ``+1`` for metrics that help when raised (integrity, redundancy), ``-1``
        for metrics that help when lowered (load), and ``0`` for
        :attr:`CRITICALITY`, which describes how load-bearing a system is rather
        than a lever an operator can pull. Analyses use the zero to exclude
        criticality from intervention rankings while still reporting how
        sensitive the diagnosis is to it.
        """
        if self is SystemMetric.LOAD:
            return -1
        if self is SystemMetric.CRITICALITY:
            return 0
        return 1


class Severity(StrEnum):
    """An ordinal risk band used to summarise a normalised score in ``[0, 1]``."""

    LOW = "low"
    MODERATE = "moderate"
    ELEVATED = "elevated"
    CRITICAL = "critical"

    @classmethod
    def from_score(cls, score: float) -> Severity:
        """Map a normalised score in ``[0, 1]`` to a severity band.

        The bands are half-open and ordered from below, so the mapping is total:
        a score under ``0`` saturates at :attr:`LOW`, one above ``1`` saturates at
        :attr:`CRITICAL`, and ``NaN`` -- which compares false against every
        threshold -- falls through to :attr:`CRITICAL`. Saturating on the
        pessimistic side is deliberate: a score that has escaped ``[0, 1]``
        indicates a broken upstream computation, and under-reporting its severity
        would be the more dangerous failure.

        Args:
            score: A value where ``0`` is benign and ``1`` is the worst case.

        Returns:
            The corresponding :class:`Severity` band.
        """
        if score < 0.25:
            return cls.LOW
        if score < 0.50:
            return cls.MODERATE
        if score < 0.75:
            return cls.ELEVATED
        return cls.CRITICAL


@dataclass(frozen=True, slots=True)
class MarketBoundary:
    """The scope of a market under analysis (AMF analytical Step 1).

    Attributes:
        asset_class: The asset class in scope (e.g. ``"equities"``).
        geography: The geographic scope (e.g. ``"US"``).
        timeframe: The analytical timeframe (e.g. ``"intraday"``).
        notes: Optional free-text clarification of the boundary.
    """

    asset_class: str
    geography: str
    timeframe: str
    notes: str = ""

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-serialisable representation of the boundary."""
        return {
            "asset_class": self.asset_class,
            "geography": self.geography,
            "timeframe": self.timeframe,
            "notes": self.notes,
        }


@dataclass(frozen=True, slots=True)
class Dependency:
    """A directed, weighted coupling: ``source`` depends on ``target``.

    The weight expresses how strongly ``source`` relies on ``target``. Stress, in
    a simulation, therefore flows in the *opposite* direction (from a stressed
    ``target`` toward the dependent ``source``).

    Attributes:
        source: The system that has the dependency.
        target: The system that is depended upon.
        kind: The nature of the coupling.
        weight: Strength of the coupling in ``(0, 1]``.
    """

    source: SystemKind
    target: SystemKind
    kind: DependencyKind = DependencyKind.STRUCTURAL
    weight: float = 0.5

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the dependency."""
        return {
            "source": self.source.value,
            "target": self.target.value,
            "kind": self.kind.value,
            "weight": self.weight,
        }


@dataclass(frozen=True, slots=True)
class WeaknessFinding:
    """A per-system structural weakness result from the diagnostic engine.

    Attributes:
        system: The system this finding describes.
        score: Composite weakness score in ``[0, 1]`` (higher is weaker).
        severity: The severity band derived from ``score``.
        fragility: Fragility component in ``[0, 1]``.
        concentration: Dependency-concentration component in ``[0, 1]``.
        feedback: Feedback-amplification component in ``[0, 1]``.
        is_single_point_of_failure: Whether the system is a structural SPOF.
        drivers: Human-readable explanations of what drives the score.
    """

    system: SystemKind
    score: float
    severity: Severity
    fragility: float
    concentration: float
    feedback: float
    is_single_point_of_failure: bool
    drivers: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the finding."""
        return {
            "system": self.system.value,
            "score": self.score,
            "severity": self.severity.value,
            "fragility": self.fragility,
            "concentration": self.concentration,
            "feedback": self.feedback,
            "is_single_point_of_failure": self.is_single_point_of_failure,
            "drivers": list(self.drivers),
        }


@dataclass(frozen=True, slots=True)
class DiagnosticReport:
    """The full output of the diagnostic engine (AMF analytical Steps 4-5).

    Attributes:
        boundary: The analysed market's boundary.
        overall_index: Criticality-weighted structural-weakness index in ``[0, 1]``.
        overall_severity: Severity band derived from ``overall_index``.
        findings: Per-system findings, ordered from weakest to strongest.
        single_points_of_failure: Systems flagged as structural SPOFs.
        feedback_loops: Risky feedback loops (each a tuple of systems in order).
    """

    boundary: MarketBoundary
    overall_index: float
    overall_severity: Severity
    findings: tuple[WeaknessFinding, ...]
    single_points_of_failure: tuple[SystemKind, ...]
    feedback_loops: tuple[tuple[SystemKind, ...], ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the report."""
        return {
            "boundary": self.boundary.to_dict(),
            "overall_index": self.overall_index,
            "overall_severity": self.overall_severity.value,
            "findings": [f.to_dict() for f in self.findings],
            "single_points_of_failure": [s.value for s in self.single_points_of_failure],
            "feedback_loops": [[s.value for s in loop] for loop in self.feedback_loops],
        }


@dataclass(frozen=True, slots=True)
class Shock:
    """A structural stress injected into one system.

    Attributes:
        target: The system that receives the stress.
        magnitude: Injected stress in ``(0, 1]`` (a dimensionless load, not a price).
        label: Optional human-readable label for the scenario.
        at_step: Timestep at which the shock is injected (``0`` = the start). Use a
            later step to model a second wave hitting a still-stressed market.
    """

    target: SystemKind
    magnitude: float = 0.8
    label: str = ""
    at_step: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the shock."""
        return {
            "target": self.target.value,
            "magnitude": self.magnitude,
            "label": self.label,
            "at_step": self.at_step,
        }


@dataclass(frozen=True, slots=True)
class Intervention:
    """A containment measure that boosts one system's absorptive capacity.

    From ``at_step`` onward, the target system dampens more of the incoming stress,
    modelling a structural intervention (e.g. a backstop or circuit breaker).

    Attributes:
        target: The system whose absorptive capacity is boosted.
        absorptive_boost: Amount added to the target's absorption, in ``[0, 1]``
            (the effective capacity is clipped to ``1``).
        at_step: Timestep from which the intervention is active (``0`` = the start).
    """

    target: SystemKind
    absorptive_boost: float = 0.3
    at_step: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the intervention."""
        return {
            "target": self.target.value,
            "absorptive_boost": self.absorptive_boost,
            "at_step": self.at_step,
        }


@dataclass(frozen=True, slots=True)
class ResilienceScore:
    """Resilience metrics derived from a shock-propagation simulation.

    All quantities are dimensionless and structural.

    Attributes:
        target: The shocked system.
        value: Composite resilience in ``[0, 1]`` (higher is more resilient).
        severity: Severity band derived from ``1 - value``.
        peak_stress: Peak criticality-weighted aggregate stress in ``[0, 1]``.
        settling_time: Steps until the trajectory settled (``-1`` if it never did).
        absorbed_fraction: Fraction of injected stress dissipated, in ``[0, 1]``.
        amplification_factor: Peak aggregate stress divided by injected stress.
        tipped_systems: Systems that crossed the cascade threshold during the run
            (empty unless nonlinear cascade dynamics were enabled).
    """

    target: SystemKind
    value: float
    severity: Severity
    peak_stress: float
    settling_time: int
    absorbed_fraction: float
    amplification_factor: float
    tipped_systems: tuple[SystemKind, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the score."""
        return {
            "target": self.target.value,
            "value": self.value,
            "severity": self.severity.value,
            "peak_stress": self.peak_stress,
            "settling_time": self.settling_time,
            "absorbed_fraction": self.absorbed_fraction,
            "amplification_factor": self.amplification_factor,
            "tipped_systems": [s.value for s in self.tipped_systems],
        }


@dataclass(frozen=True, slots=True)
class MetricStats:
    """Summary statistics for one metric across an ensemble of runs.

    Attributes:
        mean: Arithmetic mean across runs.
        minimum: Smallest observed value.
        maximum: Largest observed value.
        p10: 10th percentile.
        p50: Median (50th percentile).
        p90: 90th percentile.
    """

    mean: float
    minimum: float
    maximum: float
    p10: float
    p50: float
    p90: float

    def to_dict(self) -> dict[str, float]:
        """Return a JSON-serialisable representation of the statistics."""
        return {
            "mean": self.mean,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "p10": self.p10,
            "p50": self.p50,
            "p90": self.p90,
        }


@dataclass(frozen=True, slots=True)
class ResilienceDistribution:
    """Distribution of resilience metrics over a Monte Carlo ensemble.

    Attributes:
        target: The shocked system.
        runs: Number of stochastic replications summarised.
        value: Statistics of the composite resilience value.
        amplification_factor: Statistics of the amplification factor.
        peak_stress: Statistics of the peak systemic stress.
        absorbed_fraction: Statistics of the absorbed fraction.
    """

    target: SystemKind
    runs: int
    value: MetricStats
    amplification_factor: MetricStats
    peak_stress: MetricStats
    absorbed_fraction: MetricStats

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the distribution."""
        return {
            "target": self.target.value,
            "runs": self.runs,
            "value": self.value.to_dict(),
            "amplification_factor": self.amplification_factor.to_dict(),
            "peak_stress": self.peak_stress.to_dict(),
            "absorbed_fraction": self.absorbed_fraction.to_dict(),
        }


@dataclass(frozen=True, slots=True)
class SimulationTrace:
    """The full record of a shock-propagation run.

    Attributes:
        shocks: The shocks applied at ``t = 0``.
        steps: The stress vector at each timestep, keyed by system.
        converged: Whether the trajectory reached its fixed point within budget.
        resilience: The derived resilience metrics.
    """

    shocks: tuple[Shock, ...]
    steps: tuple[dict[SystemKind, float], ...] = field(default_factory=tuple)
    converged: bool = False
    resilience: ResilienceScore | None = None

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the trace."""
        return {
            "shocks": [s.to_dict() for s in self.shocks],
            "steps": [{k.value: v for k, v in step.items()} for step in self.steps],
            "converged": self.converged,
            "resilience": self.resilience.to_dict() if self.resilience else None,
        }


@dataclass(frozen=True, slots=True)
class Sensitivity:
    """How strongly the overall weakness index responds to one structural metric.

    Estimated by perturbing a single metric of a single system and re-running the
    diagnosis. The gradient is a finite-difference slope, not an analytic
    derivative, so it describes the model's local behaviour around the market as
    supplied -- it is not a prediction about any real market.

    Attributes:
        system: The system whose metric was perturbed.
        metric: The metric that was perturbed.
        baseline_value: The metric's value in the unperturbed market.
        span: The distance actually traversed, which shrinks near ``0`` or ``1``.
        index_delta: Change in the overall weakness index across ``span``.
        gradient: ``index_delta / span``; positive means raising the metric
            raises structural weakness.
    """

    system: SystemKind
    metric: SystemMetric
    baseline_value: float
    span: float
    index_delta: float
    gradient: float

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the sensitivity."""
        return {
            "system": self.system.value,
            "metric": self.metric.value,
            "baseline_value": self.baseline_value,
            "span": self.span,
            "index_delta": self.index_delta,
            "gradient": self.gradient,
        }


@dataclass(frozen=True, slots=True)
class LeveragePoint:
    """A single structural adjustment and the improvement it would yield.

    Leverage points answer AMF analytical Step 5 -- where to intervene -- by
    reporting, for one feasible adjustment to one system, how far the overall
    weakness index falls. They rank candidate interventions within the supplied
    model; they are not recommendations about any real market.

    Attributes:
        system: The system to adjust.
        metric: The metric to adjust.
        baseline_value: The metric's current value.
        adjusted_value: The value after the adjustment.
        index_before: Overall weakness index before the adjustment.
        index_after: Overall weakness index after the adjustment.
        improvement: ``index_before - index_after``; positive means the
            adjustment reduces structural weakness.
    """

    system: SystemKind
    metric: SystemMetric
    baseline_value: float
    adjusted_value: float
    index_before: float
    index_after: float
    improvement: float

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the leverage point."""
        return {
            "system": self.system.value,
            "metric": self.metric.value,
            "baseline_value": self.baseline_value,
            "adjusted_value": self.adjusted_value,
            "index_before": self.index_before,
            "index_after": self.index_after,
            "improvement": self.improvement,
        }


@dataclass(frozen=True, slots=True)
class SensitivityReport:
    """The full output of a sensitivity and leverage analysis.

    Attributes:
        boundary: The analysed market's boundary.
        baseline_index: The unperturbed overall weakness index.
        baseline_severity: Severity band derived from ``baseline_index``.
        step: The requested perturbation size.
        sensitivities: Per metric, ordered by absolute gradient descending.
        leverage_points: Feasible adjustments, ordered by improvement descending.
    """

    boundary: MarketBoundary
    baseline_index: float
    baseline_severity: Severity
    step: float
    sensitivities: tuple[Sensitivity, ...]
    leverage_points: tuple[LeveragePoint, ...]

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the report."""
        return {
            "boundary": self.boundary.to_dict(),
            "baseline_index": self.baseline_index,
            "baseline_severity": self.baseline_severity.value,
            "step": self.step,
            "sensitivities": [s.to_dict() for s in self.sensitivities],
            "leverage_points": [p.to_dict() for p in self.leverage_points],
        }
