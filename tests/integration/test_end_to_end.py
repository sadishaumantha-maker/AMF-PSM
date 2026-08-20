"""End-to-end test: build -> diagnose -> simulate -> report."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from amf import (
    DiagnosticConfig,
    DiagnosticEngine,
    Market,
    Shock,
    ShockSimulator,
    SystemKind,
)
from amf.report import render_json, render_text

SAMPLE = Path(__file__).resolve().parents[2] / "examples" / "sample_market.json"


@pytest.mark.integration
def test_full_workflow(stressed_market: Market):
    # Diagnose
    report = DiagnosticEngine().diagnose(stressed_market)
    assert report.findings
    assert render_text(report)

    # Simulate the weakest system being shocked
    weakest = report.findings[0].system
    simulator = ShockSimulator(stressed_market)
    trace = simulator.propagate(Shock(weakest, 0.9))
    assert trace.converged
    assert trace.resilience is not None

    # Systemic stress test and serialisation
    profile = simulator.stress_test()
    assert set(profile) == set(SystemKind)
    assert render_json(profile)


@pytest.mark.integration
def test_construction_path_does_not_change_the_score(boundary, market_factory):
    # The same market described two ways -- built from the factories, and parsed
    # from JSON that omits every optional metric -- must diagnose identically.
    from_factories = market_factory()
    from_json = Market.from_dict(
        {
            "boundary": boundary.to_dict(),
            "systems": {kind.value: {} for kind in SystemKind},
            "dependencies": [],
        }
    )
    engine = DiagnosticEngine()
    assert engine.diagnose(from_json).overall_index == pytest.approx(engine.diagnose(from_factories).overall_index)
    for kind in SystemKind:
        assert from_json.system(kind).criticality == pytest.approx(from_factories.system(kind).criticality)


@pytest.mark.integration
def test_round_trip_then_analyse(stressed_market: Market):
    restored = Market.from_dict(stressed_market.to_dict())
    original_index = DiagnosticEngine().diagnose(stressed_market).overall_index
    restored_index = DiagnosticEngine().diagnose(restored).overall_index
    assert restored_index == pytest.approx(original_index)


def test_shipped_sample_market_scores_are_pinned():
    """Guard the published numbers for `examples/sample_market.json`.

    These are the scores the framework's own example reports. They are not
    arbitrary fixtures: any change to the diagnostic maths moves them, so this
    test is what makes such a change a deliberate decision rather than a silent
    side effect. Four of the seven systems have exactly one outgoing coupling and
    so score the maximum concentration of 1.00 whatever that coupling weighs --
    see `DiagnosticEngine.concentration` and the opt-in that rescales it.
    """
    market = Market.from_dict(json.loads(SAMPLE.read_text(encoding="utf-8")))
    report = DiagnosticEngine().diagnose(market)

    assert report.overall_index == pytest.approx(0.27964, abs=5e-5)
    concentration = {f.system: f.concentration for f in report.findings}
    assert concentration == {
        SystemKind.SKELETON: pytest.approx(0.00),
        SystemKind.CIRCULATORY: pytest.approx(0.52663, abs=5e-5),
        SystemKind.NERVOUS: pytest.approx(0.50413, abs=5e-5),
        SystemKind.MUSCULATURE: pytest.approx(1.00),
        SystemKind.ORGANS: pytest.approx(1.00),
        SystemKind.IMMUNE: pytest.approx(1.00),
        SystemKind.METABOLISM: pytest.approx(1.00),
    }


def test_reliance_scaling_separates_the_systems_the_index_ties():
    """The opt-in ranks the four tied systems by how much reliance they carry."""
    market = Market.from_dict(json.loads(SAMPLE.read_text(encoding="utf-8")))
    engine = DiagnosticEngine(DiagnosticConfig(scale_concentration_by_reliance=True))
    scaled = engine.concentration(market)
    assert scaled[SystemKind.MUSCULATURE] == pytest.approx(0.70)
    assert scaled[SystemKind.ORGANS] == pytest.approx(0.60)
    assert scaled[SystemKind.METABOLISM] == pytest.approx(0.40)
    assert scaled[SystemKind.IMMUNE] == pytest.approx(0.30)
