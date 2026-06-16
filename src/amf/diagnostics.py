"""Structural weakness diagnostics (AMF analytical Steps 4-5).

The :class:`DiagnosticEngine` is pure, deterministic graph analysis: given a
:class:`~amf.market.Market` it scores each system's structural weakness from
three interpretable components and rolls them up into a market-wide index. No
randomness, no simulation, and nothing about prices or trading.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

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


@dataclass(frozen=True, slots=True)
class DiagnosticConfig:
    """Weights blending the three weakness components into one score.

    The three weights should sum to one; they are normalised defensively so any
    positive triple yields a score in ``[0, 1]``.

    Attributes:
        fragility_weight: Weight on intrinsic fragility.
        concentration_weight: Weight on dependency concentration.
        feedback_weight: Weight on feedback amplification.
    """

    fragility_weight: float = 0.4
    concentration_weight: float = 0.3
    feedback_weight: float = 0.3


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
        *outgoing* dependencies (the things it relies on). A system that leans on
        one strong coupling scores near ``1`` (brittle); one that spreads its
        reliance across many balanced couplings scores low (diversified). A system
        with no dependencies scores ``0``.
        """
        graph = market.graph
        result: dict[SystemKind, float] = {}
        for kind in market.systems:
            weights = [graph.edge_weight(kind, t) for t in graph.dependencies_of(kind)]
            total = sum(weights)
            if total <= 0.0:
                result[kind] = 0.0
                continue
            result[kind] = sum((w / total) ** 2 for w in weights)
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
        """
        articulation = market.graph.articulation_points()
        spofs = [
            kind
            for kind in market.systems
            if kind in articulation and market.systems[kind].redundancy < _LOW_REDUNDANCY
        ]
        return sorted(spofs, key=lambda k: market.systems[k].criticality, reverse=True)

    def diagnose(self, market: Market) -> DiagnosticReport:
        """Run the full diagnosis and return a :class:`DiagnosticReport`.

        Args:
            market: The market to diagnose (must be complete).

        Returns:
            A report with per-system findings, a criticality-weighted overall
            index, ranked single points of failure, and risky feedback loops.
        """
        market.require_complete()
        fragility = self.fragility(market)
        concentration = self.concentration(market)
        feedback = self.feedback_amplification(market)
        spofs = set(self.single_points_of_failure(market))

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
                    drivers=_drivers(system, fragility[kind], concentration[kind], feedback[kind], kind in spofs),
                )
            )
            weighted_sum += score * system.criticality
            criticality_sum += system.criticality

        overall = weighted_sum / criticality_sum if criticality_sum > 0.0 else 0.0
        findings.sort(key=lambda f: f.score, reverse=True)
        return DiagnosticReport(
            boundary=market.boundary,
            overall_index=overall,
            overall_severity=Severity.from_score(overall),
            findings=tuple(findings),
            single_points_of_failure=tuple(self.single_points_of_failure(market)),
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


def _drivers(
    system: AnatomicalSystem,
    fragility: float,
    concentration: float,
    feedback: float,
    is_spof: bool,
) -> tuple[str, ...]:
    """Return human-readable explanations of a system's weakness drivers."""
    drivers: list[str] = []
    if fragility >= 0.25:
        drivers.append(
            f"fragile: criticality {system.criticality:.2f}, health {system.health():.2f}, "
            f"redundancy {system.redundancy:.2f}"
        )
    if concentration >= 0.5:
        drivers.append(f"reliance concentrated in few couplings (HHI {concentration:.2f})")
    if feedback >= 0.25:
        drivers.append(f"participates in amplifying feedback loops (score {feedback:.2f})")
    if is_spof:
        drivers.append("single point of failure: removal disconnects the market")
    return tuple(drivers)
