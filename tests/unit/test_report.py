"""Unit tests for the result renderers."""

from __future__ import annotations

import json

from amf.diagnostics import DiagnosticEngine
from amf.market import Market
from amf.models import Shock, SimulationTrace, SystemKind
from amf.report import (
    _to_jsonable,
    render_json,
    render_markdown,
    render_stress_test,
    render_text,
)
from amf.simulation import ShockSimulator


def test_to_jsonable_passes_primitives_through():
    # The serialiser dispatches result types and dicts; anything else (a JSON
    # primitive) is returned unchanged, including as a nested dict value.
    assert _to_jsonable(42) == 42
    assert _to_jsonable("x") == "x"
    assert _to_jsonable({SystemKind.SKELETON: 0.5}) == {"skeleton": 0.5}


def test_render_diagnostic_text_and_markdown(stressed_market: Market):
    report = DiagnosticEngine().diagnose(stressed_market)
    text = render_text(report)
    assert "Structural Diagnosis" in text
    assert "Feedback loops" in text
    md = render_markdown(report)
    assert md.startswith("# AMF Structural Diagnosis")
    assert "| System |" in md


def test_render_diagnostic_json_round_trips(stressed_market: Market):
    report = DiagnosticEngine().diagnose(stressed_market)
    payload = json.loads(render_json(report))
    assert payload == report.to_dict()


def test_render_simulation_text_and_markdown(stressed_market: Market):
    trace = ShockSimulator(stressed_market).propagate(Shock(SystemKind.CIRCULATORY, 0.8))
    text = render_text(trace)
    assert "Shock Propagation" in text
    assert "Resilience" in text
    md = render_markdown(trace)
    assert md.startswith("# AMF Shock Propagation")


def test_render_simulation_json(stressed_market: Market):
    trace = ShockSimulator(stressed_market).propagate(Shock(SystemKind.CIRCULATORY, 0.8))
    payload = json.loads(render_json(trace))
    assert payload["converged"] is True


def test_render_stress_test(stressed_market: Market):
    profile = ShockSimulator(stressed_market).stress_test()
    rendered = render_stress_test(profile)
    assert "Systemic stress test" in rendered
    for kind in SystemKind:
        assert kind.value in rendered


def test_render_json_of_stress_test_profile(stressed_market: Market):
    profile = ShockSimulator(stressed_market).stress_test()
    payload = json.loads(render_json(profile))
    assert set(payload) == {k.value for k in SystemKind}


def test_render_stress_test_via_render_text(stressed_market: Market):
    # render_text dispatches the stress-test profile to the text renderer.
    profile = ShockSimulator(stressed_market).stress_test()
    assert render_text(profile) == render_stress_test(profile)


def test_render_stress_test_markdown(stressed_market: Market):
    profile = ShockSimulator(stressed_market).stress_test()
    md = render_markdown(profile)
    assert md.startswith("# AMF Systemic Stress Test")
    assert "| System | Resilience |" in md
    for kind in SystemKind:
        assert kind.value in md


def test_render_healthy_market_omits_empty_sections(healthy_market: Market):
    report = DiagnosticEngine().diagnose(healthy_market)
    text = render_text(report)
    # A healthy market has no SPOFs and no feedback loops, so those sections are
    # absent from the rendered text.
    assert "Single points of failure" not in text
    assert "Feedback loops" not in text


def test_render_trace_without_resilience():
    # A trace with no resilience score still renders both formats without error.
    trace = SimulationTrace(shocks=(Shock(SystemKind.SKELETON, 0.5),))
    assert "Shock Propagation" in render_text(trace)
    assert "Resilience" not in render_text(trace)
    assert render_markdown(trace).startswith("# AMF Shock Propagation")


def test_to_jsonable_stringifies_non_system_keys():
    # The str(k) fallback is a conditional expression, which branch coverage does
    # not measure -- so this path read as covered while no test exercised it.
    assert _to_jsonable({"already-a-string": 1, 2: "two"}) == {"already-a-string": 1, "2": "two"}


def test_render_json_is_sorted_and_stable(stressed_market: Market):
    # Renderers are pure: the same input must produce byte-identical output.
    report = DiagnosticEngine().diagnose(stressed_market)
    assert render_json(report) == render_json(report)
    payload = json.loads(render_json(report))
    assert list(payload) == sorted(payload)


def test_stress_test_renderers_rank_weakest_first(stressed_market: Market):
    profile = ShockSimulator(stressed_market).stress_test()
    ranked = [k.value for k, _ in sorted(profile.items(), key=lambda kv: kv[1].value)]
    text_order = [line.split()[0] for line in render_stress_test(profile).splitlines()[2:] if line.strip()]
    assert text_order == ranked
