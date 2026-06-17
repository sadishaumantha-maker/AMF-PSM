"""Unit tests for the structural diagnostic engine."""

from __future__ import annotations

import pytest

from amf.diagnostics import DiagnosticConfig, DiagnosticEngine
from amf.market import Market
from amf.models import (
    Dependency,
    DependencyKind,
    MarketBoundary,
    Severity,
    SystemKind,
)
from amf.systems import (
    circulatory,
    immune,
    metabolism,
    musculature,
    nervous,
    organs,
    skeleton,
)


def _full(boundary: MarketBoundary, deps: list[Dependency]) -> Market:
    systems = [skeleton(), circulatory(), nervous(), musculature(), organs(), immune(), metabolism()]
    return Market.assemble(boundary, systems, deps)


def test_fragility_formula(boundary: MarketBoundary):
    systems = [
        skeleton(integrity=0.5, redundancy=0.2, criticality=0.9),
        circulatory(),
        nervous(),
        musculature(),
        organs(),
        immune(),
        metabolism(),
    ]
    market = Market.assemble(boundary, systems)
    fragility = DiagnosticEngine().fragility(market)
    # 0.9 * (1 - 0.5) * (1 - 0.2) = 0.36
    assert fragility[SystemKind.SKELETON] == pytest.approx(0.36)


def test_fragility_is_zero_for_healthy_or_redundant_system(boundary: MarketBoundary):
    systems = [
        skeleton(integrity=1.0, load=0.0, redundancy=0.0, criticality=0.9),  # full health -> 0
        circulatory(integrity=0.4, load=0.3, redundancy=1.0, criticality=0.9),  # full redundancy -> 0
        nervous(),
        musculature(),
        organs(),
        immune(),
        metabolism(),
    ]
    fragility = DiagnosticEngine().fragility(Market.assemble(boundary, systems))
    assert fragility[SystemKind.SKELETON] == pytest.approx(0.0)
    assert fragility[SystemKind.CIRCULATORY] == pytest.approx(0.0)


def test_concentration_hhi(boundary: MarketBoundary):
    # nervous depends on a single target => HHI 1.0
    single = _full(boundary, [Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, weight=0.5)])
    assert DiagnosticEngine().concentration(single)[SystemKind.NERVOUS] == pytest.approx(1.0)

    # nervous depends on two equally-weighted targets => HHI 0.5
    split = _full(
        boundary,
        [
            Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, weight=0.5),
            Dependency(SystemKind.NERVOUS, SystemKind.CIRCULATORY, weight=0.5),
        ],
    )
    assert DiagnosticEngine().concentration(split)[SystemKind.NERVOUS] == pytest.approx(0.5)

    # no dependencies => 0.0
    assert DiagnosticEngine().concentration(split)[SystemKind.METABOLISM] == 0.0

    # asymmetric split [0.6, 0.4] => 0.6^2 + 0.4^2 = 0.52
    asymmetric = _full(
        boundary,
        [
            Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, weight=0.6),
            Dependency(SystemKind.NERVOUS, SystemKind.CIRCULATORY, weight=0.4),
        ],
    )
    assert DiagnosticEngine().concentration(asymmetric)[SystemKind.NERVOUS] == pytest.approx(0.52)


def test_feedback_amplification_is_product_of_cycle_weights(boundary: MarketBoundary):
    deps = [
        Dependency(SystemKind.CIRCULATORY, SystemKind.NERVOUS, weight=0.5),
        Dependency(SystemKind.NERVOUS, SystemKind.MUSCULATURE, weight=0.5),
        Dependency(SystemKind.MUSCULATURE, SystemKind.CIRCULATORY, weight=0.4),
    ]
    market = _full(boundary, deps)
    feedback = DiagnosticEngine().feedback_amplification(market)
    expected = 0.5 * 0.5 * 0.4
    for kind in (SystemKind.CIRCULATORY, SystemKind.NERVOUS, SystemKind.MUSCULATURE):
        assert feedback[kind] == pytest.approx(expected)
    assert feedback[SystemKind.SKELETON] == 0.0


def test_feedback_amplification_clips_overlapping_loops_at_one(boundary: MarketBoundary):
    # Circulatory sits in two strong 2-cycles, each with product 1.0; its summed
    # feedback (2.0) must clip to 1.0 rather than overflow the unit interval.
    deps = [
        Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, weight=1.0),
        Dependency(SystemKind.SKELETON, SystemKind.CIRCULATORY, weight=1.0),
        Dependency(SystemKind.CIRCULATORY, SystemKind.NERVOUS, weight=1.0),
        Dependency(SystemKind.NERVOUS, SystemKind.CIRCULATORY, weight=1.0),
    ]
    feedback = DiagnosticEngine().feedback_amplification(_full(boundary, deps))
    assert feedback[SystemKind.CIRCULATORY] == pytest.approx(1.0)


def test_single_points_of_failure(stressed_market: Market):
    spofs = DiagnosticEngine().single_points_of_failure(stressed_market)
    assert set(spofs) == {SystemKind.SKELETON, SystemKind.CIRCULATORY}


def test_single_points_of_failure_ranked_by_criticality(stressed_market: Market):
    # skeleton (criticality 0.90) must rank ahead of circulatory (0.85).
    spofs = DiagnosticEngine().single_points_of_failure(stressed_market)
    assert spofs == [SystemKind.SKELETON, SystemKind.CIRCULATORY]


def test_diagnose_report_structure_and_ordering(stressed_market: Market):
    report = DiagnosticEngine().diagnose(stressed_market)
    assert 0.0 <= report.overall_index <= 1.0
    assert isinstance(report.overall_severity, Severity)
    assert len(report.findings) == 7
    scores = [f.score for f in report.findings]
    assert scores == sorted(scores, reverse=True)
    # the feedback loop is surfaced
    assert (SystemKind.CIRCULATORY, SystemKind.NERVOUS, SystemKind.MUSCULATURE) in report.feedback_loops
    # at least one finding has explanatory drivers
    assert any(f.drivers for f in report.findings)


def test_healthy_market_scores_low(healthy_market: Market):
    report = DiagnosticEngine().diagnose(healthy_market)
    assert report.overall_index < 0.1
    assert report.overall_severity is Severity.LOW
    assert report.single_points_of_failure == ()


def test_zero_weight_config_falls_back(stressed_market: Market):
    engine = DiagnosticEngine(DiagnosticConfig(0.0, 0.0, 0.0))
    report = engine.diagnose(stressed_market)
    # All component weights zero => every score is zero, not a division error.
    assert report.overall_index == pytest.approx(0.0)


def _skeleton_drivers(boundary: MarketBoundary, redundancy: float) -> tuple[str, ...]:
    # No dependencies => no concentration, feedback, or SPOF drivers, so the
    # skeleton finding's drivers are governed purely by the fragility threshold.
    systems = [
        skeleton(integrity=0.5, load=0.0, redundancy=redundancy, criticality=0.5),
        circulatory(),
        nervous(),
        musculature(),
        organs(),
        immune(),
        metabolism(),
    ]
    report = DiagnosticEngine().diagnose(Market.assemble(boundary, systems))
    finding = next(f for f in report.findings if f.system is SystemKind.SKELETON)
    return finding.drivers


def test_fragility_driver_appears_at_threshold(boundary: MarketBoundary):
    # fragility = 0.5 * (1 - 0.5) * (1 - 0.0) = 0.25, exactly at the >= 0.25 cutoff.
    drivers = _skeleton_drivers(boundary, redundancy=0.0)
    assert any(d.startswith("fragile:") for d in drivers)


def test_fragility_driver_absent_just_below_threshold(boundary: MarketBoundary):
    # fragility = 0.5 * 0.5 * (1 - 0.02) = 0.245, just under the cutoff.
    drivers = _skeleton_drivers(boundary, redundancy=0.02)
    assert not any(d.startswith("fragile:") for d in drivers)


def test_dependency_kinds_do_not_affect_scoring(boundary: MarketBoundary):
    structural = _full(boundary, [Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.5)])
    capital = _full(boundary, [Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.5)])
    a = DiagnosticEngine().diagnose(structural).overall_index
    b = DiagnosticEngine().diagnose(capital).overall_index
    assert a == pytest.approx(b)
