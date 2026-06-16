"""End-to-end test: build -> diagnose -> simulate -> report."""

from __future__ import annotations

import pytest

from amf import (
    DiagnosticEngine,
    Market,
    Shock,
    ShockSimulator,
    SystemKind,
)
from amf.report import render_json, render_text


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
def test_round_trip_then_analyse(stressed_market: Market):
    restored = Market.from_dict(stressed_market.to_dict())
    original_index = DiagnosticEngine().diagnose(stressed_market).overall_index
    restored_index = DiagnosticEngine().diagnose(restored).overall_index
    assert restored_index == pytest.approx(original_index)
