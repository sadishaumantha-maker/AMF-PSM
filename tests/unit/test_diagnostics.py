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


def test_single_points_of_failure(stressed_market: Market):
    spofs = DiagnosticEngine().single_points_of_failure(stressed_market)
    assert set(spofs) == {SystemKind.SKELETON, SystemKind.CIRCULATORY}


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


def test_dependency_kinds_do_not_affect_scoring(boundary: MarketBoundary):
    structural = _full(boundary, [Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.5)])
    capital = _full(boundary, [Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.5)])
    a = DiagnosticEngine().diagnose(structural).overall_index
    b = DiagnosticEngine().diagnose(capital).overall_index
    assert a == pytest.approx(b)
