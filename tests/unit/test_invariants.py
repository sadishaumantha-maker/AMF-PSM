"""Tests for the invariant guard the engines run over their own results.

Two halves. The first builds deliberately broken result objects and checks each
guard rejects them -- the result types are frozen dataclasses without validation,
so an invalid one is constructible even though no engine would ever produce it.
The second checks the guards are actually wired in, by running the real engines
and confirming a well-formed result passes through untouched.
"""

from __future__ import annotations

import math

import pytest

from amf.diagnostics import DiagnosticEngine
from amf.errors import AMFError, InvariantError
from amf.invariants import (
    check_centrality,
    check_diagnostic_report,
    check_resilience_score,
    check_sensitivity_report,
    check_simulation_trace,
    require_finite,
    require_non_negative,
    require_unit,
)
from amf.models import (
    DiagnosticReport,
    LeveragePoint,
    MarketBoundary,
    ResilienceScore,
    Sensitivity,
    SensitivityReport,
    Severity,
    Shock,
    SimulationTrace,
    SystemKind,
    SystemMetric,
    WeaknessFinding,
)
from amf.sensitivity import SensitivityAnalyzer
from amf.simulation import ShockSimulator

_BOUNDARY = MarketBoundary(asset_class="equities", geography="US", timeframe="intraday")


def _finding(**overrides) -> WeaknessFinding:
    fields = {
        "system": SystemKind.SKELETON,
        "score": 0.5,
        "severity": Severity.MODERATE,
        "fragility": 0.5,
        "concentration": 0.5,
        "feedback": 0.5,
        "is_single_point_of_failure": False,
    }
    fields.update(overrides)
    return WeaknessFinding(**fields)


def _report(**overrides) -> DiagnosticReport:
    fields = {
        "boundary": _BOUNDARY,
        "overall_index": 0.5,
        "overall_severity": Severity.MODERATE,
        "findings": (_finding(),),
        "single_points_of_failure": (),
        "feedback_loops": (),
    }
    fields.update(overrides)
    return DiagnosticReport(**fields)


def _score(**overrides) -> ResilienceScore:
    fields = {
        "target": SystemKind.CIRCULATORY,
        "value": 0.8,
        "severity": Severity.LOW,
        "peak_stress": 0.4,
        "settling_time": 3,
        "absorbed_fraction": 0.9,
        "amplification_factor": 1.2,
    }
    fields.update(overrides)
    return ResilienceScore(**fields)


# --- the primitives ---------------------------------------------------------


@pytest.mark.parametrize("bad", [-0.001, 1.001, math.nan, math.inf, -math.inf])
def test_require_unit_rejects_anything_outside_the_closed_unit_interval(bad):
    with pytest.raises(InvariantError):
        require_unit("thing", bad)


@pytest.mark.parametrize("good", [0.0, 1.0, 0.5])
def test_require_unit_accepts_the_bounds(good):
    assert require_unit("thing", good) is None


@pytest.mark.parametrize("bad", [-0.001, math.nan, math.inf])
def test_require_non_negative_rejects_negative_and_non_finite(bad):
    with pytest.raises(InvariantError):
        require_non_negative("thing", bad)


def test_require_non_negative_allows_values_above_one():
    # Amplification is unbounded above: doubling the injected load is a real
    # reading, not a broken one.
    assert require_non_negative("amplification", 7.5) is None


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
def test_require_finite_rejects_non_finite(bad):
    with pytest.raises(InvariantError):
        require_finite("gradient", bad)


def test_require_finite_allows_negative_values():
    assert require_finite("gradient", -3.25) is None


def test_violation_carries_the_property_the_value_and_the_interval():
    with pytest.raises(InvariantError) as excinfo:
        require_unit("findings[skeleton].score", 1.5)
    error = excinfo.value
    assert error.property_name == "findings[skeleton].score"
    assert error.value == 1.5
    assert (error.lower, error.upper) == (0.0, 1.0)
    assert "findings[skeleton].score" in str(error)
    # Catchable with the family clause, like every other failure in the package.
    assert isinstance(error, AMFError)


def test_violation_reports_an_unbounded_interval_for_non_negative_checks():
    with pytest.raises(InvariantError) as excinfo:
        require_non_negative("amplification", -1.0)
    assert excinfo.value.upper == math.inf


# --- the report guards ------------------------------------------------------


def test_diagnostic_guard_returns_a_valid_report_unchanged():
    report = _report()
    assert check_diagnostic_report(report) is report


def test_diagnostic_guard_rejects_an_out_of_range_overall_index():
    with pytest.raises(InvariantError, match="overall_index"):
        check_diagnostic_report(_report(overall_index=1.4))


@pytest.mark.parametrize("component", ["score", "fragility", "concentration", "feedback"])
def test_diagnostic_guard_rejects_an_out_of_range_component(component):
    with pytest.raises(InvariantError, match=component):
        check_diagnostic_report(_report(findings=(_finding(**{component: -0.2}),)))


def test_resilience_guard_returns_a_valid_score_unchanged():
    score = _score()
    assert check_resilience_score(score) is score


@pytest.mark.parametrize(
    ("field", "bad"),
    [("value", 1.2), ("peak_stress", -0.1), ("absorbed_fraction", math.nan), ("amplification_factor", -1.0)],
)
def test_resilience_guard_rejects_out_of_range_metrics(field, bad):
    with pytest.raises(InvariantError, match=field):
        check_resilience_score(_score(**{field: bad}))


def test_resilience_guard_accepts_the_never_settled_sentinel():
    assert check_resilience_score(_score(settling_time=-1)).settling_time == -1


def test_resilience_guard_rejects_a_settling_time_below_the_sentinel():
    with pytest.raises(InvariantError, match="settling_time"):
        check_resilience_score(_score(settling_time=-2))


def test_trace_guard_rejects_a_stress_level_outside_the_unit_interval():
    trace = SimulationTrace(
        shocks=(Shock(target=SystemKind.SKELETON),),
        steps=({SystemKind.SKELETON: 0.5}, {SystemKind.SKELETON: 1.7}),
    )
    with pytest.raises(InvariantError, match=r"steps\[1\]\[skeleton\]"):
        check_simulation_trace(trace)


def test_trace_guard_accepts_a_trace_with_no_resilience_attached():
    # `propagate` always attaches one, but the field is optional on the type and
    # the guard must not assume otherwise.
    trace = SimulationTrace(shocks=(Shock(target=SystemKind.SKELETON),), steps=({SystemKind.SKELETON: 0.5},))
    assert check_simulation_trace(trace) is trace


def test_trace_guard_reaches_the_attached_resilience_score():
    trace = SimulationTrace(
        shocks=(Shock(target=SystemKind.SKELETON),),
        steps=({SystemKind.SKELETON: 0.5},),
        resilience=_score(value=2.0),
    )
    with pytest.raises(InvariantError, match=r"resilience\.value"):
        check_simulation_trace(trace)


def _sensitivity_report(**overrides) -> SensitivityReport:
    fields = {
        "boundary": _BOUNDARY,
        "baseline_index": 0.3,
        "baseline_severity": Severity.MODERATE,
        "step": 0.05,
        "sensitivities": (
            Sensitivity(
                system=SystemKind.SKELETON,
                metric=SystemMetric.INTEGRITY,
                baseline_value=0.5,
                span=0.1,
                index_delta=0.02,
                gradient=0.2,
            ),
        ),
        "leverage_points": (),
    }
    fields.update(overrides)
    return SensitivityReport(**fields)


def test_sensitivity_guard_returns_a_valid_report_unchanged():
    report = _sensitivity_report()
    assert check_sensitivity_report(report) is report


def test_sensitivity_guard_rejects_an_out_of_range_baseline():
    with pytest.raises(InvariantError, match="baseline_index"):
        check_sensitivity_report(_sensitivity_report(baseline_index=-0.5))


@pytest.mark.parametrize("bad_span", [0.0, -0.1, 1.5, math.nan])
def test_sensitivity_guard_rejects_a_non_positive_span(bad_span):
    # The gradient divides by the span, so a zero span is a division by zero
    # waiting to be reported as a number.
    sensitivity = Sensitivity(
        system=SystemKind.NERVOUS,
        metric=SystemMetric.LOAD,
        baseline_value=0.5,
        span=bad_span,
        index_delta=0.0,
        gradient=0.0,
    )
    with pytest.raises(InvariantError, match="span"):
        check_sensitivity_report(_sensitivity_report(sensitivities=(sensitivity,)))


def test_sensitivity_guard_rejects_a_non_finite_gradient():
    sensitivity = Sensitivity(
        system=SystemKind.NERVOUS,
        metric=SystemMetric.LOAD,
        baseline_value=0.5,
        span=0.1,
        index_delta=math.inf,
        gradient=math.inf,
    )
    with pytest.raises(InvariantError, match="gradient"):
        check_sensitivity_report(_sensitivity_report(sensitivities=(sensitivity,)))


@pytest.mark.parametrize("field", ["index_before", "index_after"])
def test_sensitivity_guard_rejects_an_out_of_range_leverage_index(field):
    fields = {
        "system": SystemKind.IMMUNE,
        "metric": SystemMetric.REDUNDANCY,
        "baseline_value": 0.5,
        "adjusted_value": 0.55,
        "index_before": 0.3,
        "index_after": 0.2,
        "improvement": 0.1,
    }
    fields[field] = 1.9
    with pytest.raises(InvariantError, match=field):
        check_sensitivity_report(_sensitivity_report(leverage_points=(LeveragePoint(**fields),)))


# --- centrality -------------------------------------------------------------


def test_centrality_guard_accepts_an_all_zero_vector():
    # An isolated market has no influence to normalise; all zeros is correct.
    zeros = dict.fromkeys(SystemKind, 0.0)
    assert check_centrality(zeros) == zeros


def test_centrality_guard_accepts_an_empty_mapping():
    assert check_centrality({}) == {}


def test_centrality_guard_rejects_an_entry_outside_the_unit_interval():
    with pytest.raises(InvariantError, match="centrality"):
        check_centrality({SystemKind.SKELETON: 1.0, SystemKind.NERVOUS: -0.1})


def test_centrality_guard_rejects_a_vector_that_is_not_max_normalised():
    # Every positive centrality vector is divided through by its own maximum, so
    # a peak below 1 means the normalisation step was skipped or corrupted.
    with pytest.raises(InvariantError, match=r"centrality\.max"):
        check_centrality({SystemKind.SKELETON: 0.5, SystemKind.NERVOUS: 0.25})


# --- wiring: the real engines run their own guards ---------------------------


def test_the_engines_pass_their_own_guards(stressed_market):
    report = DiagnosticEngine().diagnose(stressed_market)
    assert check_diagnostic_report(report) is report

    trace = ShockSimulator(stressed_market).propagate(Shock(target=SystemKind.CIRCULATORY))
    assert check_simulation_trace(trace) is trace

    sensitivity = SensitivityAnalyzer().analyse(stressed_market)
    assert check_sensitivity_report(sensitivity) is sensitivity

    centrality = stressed_market.graph.centrality()
    assert check_centrality(centrality) == centrality
    assert max(centrality.values()) == 1.0
