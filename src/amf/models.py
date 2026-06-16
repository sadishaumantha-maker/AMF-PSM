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


class Severity(StrEnum):
    """An ordinal risk band used to summarise a normalised score in ``[0, 1]``."""

    LOW = "low"
    MODERATE = "moderate"
    ELEVATED = "elevated"
    CRITICAL = "critical"

    @classmethod
    def from_score(cls, score: float) -> Severity:
        """Map a normalised score in ``[0, 1]`` to a severity band.

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
    """An initial structural stress injected into one system.

    Attributes:
        target: The system that receives the initial stress.
        magnitude: Initial stress in ``(0, 1]`` (a dimensionless load, not a price).
        label: Optional human-readable label for the scenario.
    """

    target: SystemKind
    magnitude: float = 0.8
    label: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the shock."""
        return {"target": self.target.value, "magnitude": self.magnitude, "label": self.label}


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
    """

    target: SystemKind
    value: float
    severity: Severity
    peak_stress: float
    settling_time: int
    absorbed_fraction: float
    amplification_factor: float

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
