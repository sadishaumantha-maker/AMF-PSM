"""Structural weakness diagnostics (AMF analytical Steps 4-5).

The :class:`DiagnosticEngine` is pure, deterministic graph analysis: given a
:class:`~amf.market.Market` it scores each system's structural weakness from
three interpretable components and rolls them up into a market-wide index. No
randomness, no simulation, and nothing about prices or trading.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from amf.errors import InvalidConfigError
from amf.models import (
    DiagnosticReport,
    Severity,
    SystemKind,
    WeaknessFinding,
)

if TYPE_CHECKING:
    from amf.graph import DependencyGraph
    from amf.market import Market
    from amf.systems import AnatomicalSystem

# A system is considered short of fallbacks (a flag for single-point-of-failure
# status) when its redundancy is below this level.
_LOW_REDUNDANCY = 0.5

# Declaration order of the seven systems, used to break ranking ties so that two
# markets with equal content rank identically however they were assembled. The
# annotated tuple comes first because mypy types the members of a bare
# ``enumerate(SystemKind)`` as ``str`` (the StrEnum's own base) rather than as
# ``SystemKind``; graph.py and simulation.py hold the same constant the same way.
_ORDER: tuple[SystemKind, ...] = tuple(SystemKind)
_INDEX: dict[SystemKind, int] = {kind: i for i, kind in enumerate(_ORDER)}


@dataclass(frozen=True, slots=True)
class DiagnosticConfig:
    """Weights blending the three weakness components into one score.

    The three weights conventionally sum to one but need not: they are divided by
    their own sum, so any non-negative triple yields a score in ``[0, 1]``. An
    all-zero triple is allowed and yields a score of zero for every system.

    Each weight must be finite and non-negative. A negative weight is rejected
    rather than normalised, because it would push scores outside the ``[0, 1]``
    interval that :class:`~amf.models.WeaknessFinding` and
    :meth:`~amf.models.Severity.from_score` both document and rely on.

    Attributes:
        fragility_weight: Weight on intrinsic fragility.
        concentration_weight: Weight on dependency concentration.
        feedback_weight: Weight on feedback amplification.
        scale_concentration_by_reliance: Opt in to scaling the concentration
            component by how much reliance a system actually carries. Off by
            default, because it changes every published concentration score; see
            :meth:`DiagnosticEngine.concentration` for what it fixes.
    """

    fragility_weight: float = 0.4
    concentration_weight: float = 0.3
    feedback_weight: float = 0.3
    scale_concentration_by_reliance: bool = False

    def __post_init__(self) -> None:
        """Validate the blend weights on construction.

        Raises:
            InvalidConfigError: If any weight is negative or not finite. A negative
                weight would push per-system scores outside ``[0, 1]``, which every
                consumer of a score -- :meth:`~amf.models.Severity.from_score` above
                all -- assumes it can rely on.
        """
        for name in ("fragility_weight", "concentration_weight", "feedback_weight"):
            value: float = getattr(self, name)
            if not math.isfinite(value) or value < 0.0:
                msg = f"{name} must be a finite, non-negative number, got {value!r}"
                raise InvalidConfigError(msg)


class DiagnosticEngine:
    """Scores structural weaknesses of a market's anatomy."""

    def __init__(self, config: DiagnosticConfig | None = None) -> None:
        """Initialise the engine.

        Args:
            config: Blend weights; defaults to :class:`DiagnosticConfig`.
        """
        self.config = config or DiagnosticConfig()

    def fragility(self, market: Market) -> dict[SystemKind, float]:
        """Return per-system fragility in ``[0, 1]``.

        Fragility is high when a system is load-bearing, already degraded, and
        lacking fallbacks: ``criticality * (1 - health) * (1 - redundancy)``.
        """
        result: dict[SystemKind, float] = {}
        for kind, system in market.systems.items():
            result[kind] = system.criticality * (1.0 - system.health()) * (1.0 - system.redundancy)
        return result

    def concentration(self, market: Market) -> dict[SystemKind, float]:
        """Return per-system dependency concentration in ``[0, 1]``.

        Uses a Herfindahl-Hirschman-style index over the weights of a system's
        *outgoing* dependencies (the things it relies on). A system that spreads
        its reliance across many balanced couplings scores low (diversified); one
        whose reliance sits in a single coupling scores ``1``.

        HHI measures the *shape* of a system's reliance, not how much of it there
        is: it is computed from each coupling's share of the total, so it is
        invariant to the total. A system with one coupling therefore scores
        exactly ``1.0`` whatever that coupling weighs -- a system leaning on a
        single ``0.01`` coupling scores the same as one wholly dependent on a
        ``1.0`` coupling. A system with no dependencies at all scores ``0``, so
        adding one trivial coupling to an isolated system moves it from the best
        score to the worst. That discontinuity is inherent to a share-based index.

        Setting :attr:`DiagnosticConfig.scale_concentration_by_reliance` multiplies
        the index by ``min(1, total outgoing weight)`` so the score reflects how
        much reliance is concentrated as well as how unevenly it is spread. That
        makes the measure continuous at zero, and is off by default because it
        changes every concentration score the engine reports.
        """
        graph = market.graph
        result: dict[SystemKind, float] = {}
        for kind in market.systems:
            weights = [graph.edge_weight(kind, t) for t in graph.dependencies_of(kind)]
            total = sum(weights)
            if total <= 0.0:
                result[kind] = 0.0
                continue
            index = sum((w / total) ** 2 for w in weights)
            if self.config.scale_concentration_by_reliance:
                index *= min(1.0, total)
            result[kind] = index
        return result

    def feedback_amplification(self, market: Market) -> dict[SystemKind, float]:
        """Return per-system feedback amplification in ``[0, 1]``.

        For each feedback loop, the product of its edge weights measures how
        strongly it re-circulates stress. Each system's score is the sum of those
        products over the loops it participates in, clipped to ``[0, 1]``.
        """
        graph = market.graph
        result: dict[SystemKind, float] = dict.fromkeys(market.systems, 0.0)
        for loop in graph.feedback_loops():
            product = _loop_weight_product(graph, loop)
            for kind in loop:
                result[kind] = min(1.0, result[kind] + product)
        return result

    def single_points_of_failure(self, market: Market) -> list[SystemKind]:
        """Return systems that are structural cut vertices with few fallbacks.

        A system qualifies when removing it disconnects the dependency graph
        (an articulation point) *and* its redundancy is below
        :data:`_LOW_REDUNDANCY`.

        Returns:
            The qualifying systems, most load-bearing first, with equal
            criticalities broken by :class:`~amf.models.SystemKind` declaration
            order so the ranking is reproducible.
        """
        articulation = market.graph.articulation_points()
        spofs = [
            kind
            for kind in market.systems
            if kind in articulation and market.systems[kind].redundancy < _LOW_REDUNDANCY
        ]
        return sorted(spofs, key=lambda k: (-market.systems[k].criticality, _INDEX[k]))

    def diagnose(self, market: Market) -> DiagnosticReport:
        """Run the full diagnosis and return a :class:`DiagnosticReport`.

        Args:
            market: The market to diagnose (must be complete).

        Returns:
            A report with per-system findings ordered weakest first (ties broken
            by :class:`~amf.models.SystemKind` declaration order), a
            criticality-weighted overall index, ranked single points of failure,
            and risky feedback loops.
        """
        market.require_complete()
        fragility = self.fragility(market)
        concentration = self.concentration(market)
        feedback = self.feedback_amplification(market)
        ranked_spofs = self.single_points_of_failure(market)
        spofs = set(ranked_spofs)
        reliance = _reliance(market)

        w_total = self.config.fragility_weight + self.config.concentration_weight + self.config.feedback_weight
        if w_total <= 0.0:
            w_total = 1.0

        findings: list[WeaknessFinding] = []
        weighted_sum = 0.0
        criticality_sum = 0.0
        for kind, system in market.systems.items():
            score = (
                self.config.fragility_weight * fragility[kind]
                + self.config.concentration_weight * concentration[kind]
                + self.config.feedback_weight * feedback[kind]
            ) / w_total
            findings.append(
                WeaknessFinding(
                    system=kind,
                    score=score,
                    severity=Severity.from_score(score),
                    fragility=fragility[kind],
                    concentration=concentration[kind],
                    feedback=feedback[kind],
                    is_single_point_of_failure=kind in spofs,
                    drivers=_drivers(
                        system,
                        fragility[kind],
                        concentration[kind],
                        feedback[kind],
                        kind in spofs,
                        reliance[kind],
                    ),
                )
            )
            weighted_sum += score * system.criticality
            criticality_sum += system.criticality

        overall = weighted_sum / criticality_sum if criticality_sum > 0.0 else 0.0
        # Weakest first, with equally weak systems ordered by declaration rather
        # than by however the market happened to be assembled.
        findings.sort(key=lambda f: (-f.score, _INDEX[f.system]))
        return DiagnosticReport(
            boundary=market.boundary,
            overall_index=overall,
            overall_severity=Severity.from_score(overall),
            findings=tuple(findings),
            single_points_of_failure=tuple(ranked_spofs),
            feedback_loops=tuple(market.graph.feedback_loops()),
        )


def _loop_weight_product(graph: DependencyGraph, loop: tuple[SystemKind, ...]) -> float:
    """Return the product of edge weights around a feedback loop."""
    product = 1.0
    count = len(loop)
    for i in range(count):
        source = loop[i]
        target = loop[(i + 1) % count]
        product *= graph.edge_weight(source, target)
    return product


def _reliance(market: Market) -> dict[SystemKind, tuple[int, float]]:
    """Return each system's ``(coupling count, total outgoing weight)``.

    The concentration index is share-based and so says nothing about how much
    reliance a system actually carries; the drivers quote both so a reader can
    tell a genuine concentration risk from a single trivial coupling.
    """
    graph = market.graph
    result: dict[SystemKind, tuple[int, float]] = {}
    for kind in market.systems:
        targets = graph.dependencies_of(kind)
        result[kind] = (len(targets), sum(graph.edge_weight(kind, t) for t in targets))
    return result


def _drivers(
    system: AnatomicalSystem,
    fragility: float,
    concentration: float,
    feedback: float,
    is_spof: bool,
    reliance: tuple[int, float] = (0, 0.0),
) -> tuple[str, ...]:
    """Return human-readable explanations of a system's weakness drivers."""
    drivers: list[str] = []
    if fragility >= 0.25:
        drivers.append(
            f"fragile: criticality {system.criticality:.2f}, health {system.health():.2f}, "
            f"redundancy {system.redundancy:.2f}"
        )
    if concentration >= 0.5:
        couplings, total = reliance
        drivers.append(
            f"reliance concentrated in {couplings} coupling(s) (HHI {concentration:.2f}, total reliance {total:.2f})"
        )
    if feedback >= 0.25:
        drivers.append(f"participates in amplifying feedback loops (score {feedback:.2f})")
    if is_spof:
        drivers.append("single point of failure: removal disconnects the market")
    return tuple(drivers)
