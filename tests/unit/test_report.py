"""Unit tests for the result renderers."""

from __future__ import annotations

import json
import re
from typing import get_args

from amf.diagnostics import DiagnosticEngine
from amf.market import Market
from amf.models import (
    DiagnosticReport,
    MarketBoundary,
    ResilienceScore,
    Severity,
    Shock,
    SimulationTrace,
    SystemKind,
    WeaknessFinding,
)
from amf.report import (
    Renderable,
    _to_jsonable,
    render_distribution,
    render_json,
    render_markdown,
    render_stress_test,
    render_text,
)
from amf.simulation import ShockSimulator, SimulationConfig


def _score(target: SystemKind, value: float) -> ResilienceScore:
    """A resilience score with hand-chosen, exactly-representable values."""
    return ResilienceScore(
        target=target,
        value=value,
        severity=Severity.from_score(1.0 - value),
        peak_stress=0.25,
        settling_time=4,
        absorbed_fraction=0.125,
        amplification_factor=1.5,
    )


def _finding(system: SystemKind, score: float, *, spof: bool = False) -> WeaknessFinding:
    return WeaknessFinding(
        system=system,
        score=score,
        severity=Severity.from_score(score),
        fragility=0.25,
        concentration=0.5,
        feedback=0.125,
        is_single_point_of_failure=spof,
    )


def _report(findings: tuple[WeaknessFinding, ...], **kwargs) -> DiagnosticReport:
    return DiagnosticReport(
        boundary=MarketBoundary("equities", "US", "intraday"),
        overall_index=kwargs.get("overall_index", 0.5),
        overall_severity=Severity.ELEVATED,
        findings=findings,
        single_points_of_failure=kwargs.get("spofs", ()),
        feedback_loops=kwargs.get("loops", ()),
    )


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


def test_stress_test_orders_weakest_resilience_first():
    # Values are assigned in an order that differs from SystemKind declaration
    # order, so the test fails if the sort is dropped.
    profile = {
        SystemKind.SKELETON: _score(SystemKind.SKELETON, 0.9),
        SystemKind.CIRCULATORY: _score(SystemKind.CIRCULATORY, 0.1),
        SystemKind.NERVOUS: _score(SystemKind.NERVOUS, 0.5),
    }
    rendered = render_stress_test(profile)
    order = [line.split()[0] for line in rendered.splitlines() if line.startswith("  ")]
    assert order == ["circulatory", "nervous", "skeleton"]
    assert order != [kind.value for kind in profile]


def test_stress_test_line_format_is_exact():
    # Pins column widths, field order, and 3-decimal formatting in one assertion.
    # severity is from_score(1 - value), so value 0.5 renders as "elevated".
    profile = {SystemKind.CIRCULATORY: _score(SystemKind.CIRCULATORY, 0.5)}
    line = render_stress_test(profile).splitlines()[-1]
    assert line == "  circulatory  resilience 0.500 [elevated] peak 0.250  absorbed 0.125  amplification 1.500"


def test_stress_test_markdown_orders_weakest_first():
    profile = {
        SystemKind.SKELETON: _score(SystemKind.SKELETON, 0.9),
        SystemKind.CIRCULATORY: _score(SystemKind.CIRCULATORY, 0.1),
    }
    rows = [line for line in render_markdown(profile).splitlines() if line.startswith("| ") and "---" not in line]
    assert [row.split(" | ")[0].removeprefix("| ") for row in rows[1:]] == ["circulatory", "skeleton"]


def test_spof_marker_appears_only_on_spof_rows():
    report = _report(
        (
            _finding(SystemKind.SKELETON, 0.6, spof=True),
            _finding(SystemKind.NERVOUS, 0.4),
        ),
        spofs=(SystemKind.SKELETON,),
    )
    text = render_text(report)
    skeleton_line = next(line for line in text.splitlines() if "skeleton" in line and "score" in line)
    nervous_line = next(line for line in text.splitlines() if "nervous" in line and "score" in line)
    assert skeleton_line.endswith("*SPOF*")
    assert "*SPOF*" not in nervous_line
    assert text.count("*SPOF*") == 1


def test_diagnostic_text_renders_one_row_per_system():
    findings = tuple(_finding(kind, 0.5) for kind in SystemKind)
    text = render_text(_report(findings))
    rows = [line for line in text.splitlines() if "score" in line and "fragility" in line]
    assert len(rows) == 7
    assert [row.split()[0] for row in rows] == [kind.value for kind in SystemKind]
    # Three-decimal score, two-decimal components.
    assert "score 0.500" in rows[0]
    assert "fragility 0.25" in rows[0]


def test_diagnostic_markdown_row_order_matches_findings_order():
    findings = (
        _finding(SystemKind.NERVOUS, 0.9),
        _finding(SystemKind.SKELETON, 0.5),
        _finding(SystemKind.IMMUNE, 0.1),
    )
    # The separator row starts "|-", so filtering on "| " already drops it.
    rows = [line for line in render_markdown(_report(findings)).splitlines() if line.startswith("| ")]
    data_rows = rows[1:]  # skip the header
    assert [row.split(" | ")[0].removeprefix("| ") for row in data_rows] == ["nervous", "skeleton", "immune"]
    assert data_rows[0].split(" | ")[6] == "no |"


def test_diagnostic_markdown_flags_spof_rows():
    report = _report((_finding(SystemKind.SKELETON, 0.5, spof=True),))
    row = next(line for line in render_markdown(report).splitlines() if line.startswith("| skeleton"))
    assert row.endswith("| yes |")


def test_render_json_is_indented_and_key_sorted():
    payload = render_json(_report((_finding(SystemKind.SKELETON, 0.5),)))
    top_level = re.findall(r'^  "(\w+)":', payload, re.MULTILINE)
    assert top_level == sorted(top_level), "render_json promises sort_keys=True"
    assert top_level  # indent=2 puts top-level keys at exactly two spaces


def test_render_json_of_primitive_passes_it_through():
    # _to_jsonable's fall-through branch for values that are not result objects.
    assert json.loads(render_json({SystemKind.SKELETON: 0.5})) == {"skeleton": 0.5}


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


def test_renderable_alias_covers_every_renderer_input(healthy_market: Market):
    # The `Renderable` alias is what types the CLI's `_format`. If a new result
    # type joins the renderers' dispatch without being added to the alias, the
    # CLI stops type-checking against reality -- so pin the alias to the set of
    # things all three renderers actually accept.
    engine_report = DiagnosticEngine().diagnose(healthy_market)
    simulator = ShockSimulator(healthy_market)
    trace = simulator.propagate(Shock(target=SystemKind.CIRCULATORY, magnitude=0.6))
    profile = simulator.stress_test(magnitude=0.6)

    members = get_args(Renderable)
    assert set(members) == {DiagnosticReport, SimulationTrace, dict[SystemKind, ResilienceScore]}

    for result in (engine_report, trace, profile):
        assert render_text(result)
        assert render_markdown(result)
        assert json.loads(render_json(result))


def test_render_cascade_trace_shows_tipped_systems(stressed_market: Market):
    config = SimulationConfig(cascade_threshold=0.2, cascade_gain=1.0)
    trace = ShockSimulator(stressed_market, config).propagate(Shock(SystemKind.CIRCULATORY, 0.9))
    assert "Tipped (cascade)" in render_text(trace)
    assert "Tipped (cascade)" in render_markdown(trace)


def test_render_distribution_text_and_json(stressed_market: Market):
    dist = ShockSimulator(stressed_market).ensemble(Shock(SystemKind.CIRCULATORY, 0.8), runs=20, base_seed=1)
    text = render_distribution(dist)
    assert "Resilience Ensemble" in text
    assert "runs: 20" in text
    payload = json.loads(render_json(dist))
    assert payload["runs"] == 20
    assert set(payload["value"]) == {"mean", "minimum", "maximum", "p10", "p50", "p90"}
