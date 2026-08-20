"""Unit tests for shared value types."""

from __future__ import annotations

import pytest

from amf.models import (
    Dependency,
    DependencyKind,
    LeveragePoint,
    MarketBoundary,
    Sensitivity,
    SensitivityReport,
    Severity,
    Shock,
    SystemKind,
    SystemMetric,
)
from amf.systems import skeleton


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (0.0, Severity.LOW),
        (0.24, Severity.LOW),
        (0.25, Severity.MODERATE),
        (0.49, Severity.MODERATE),
        (0.5, Severity.ELEVATED),
        (0.74, Severity.ELEVATED),
        (0.75, Severity.CRITICAL),
        (1.0, Severity.CRITICAL),
    ],
)
def test_severity_bands(score: float, expected: Severity):
    assert Severity.from_score(score) is expected


def test_str_enums_serialise_to_their_value():
    assert SystemKind.SKELETON.value == "skeleton"
    assert str(SystemKind.SKELETON) == "skeleton"
    assert DependencyKind.CAPITAL == "capital"


def test_value_types_round_trip_to_dict():
    boundary = MarketBoundary("equities", "US", "intraday", notes="n")
    assert boundary.to_dict()["asset_class"] == "equities"

    dep = Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.5)
    assert dep.to_dict() == {
        "source": "nervous",
        "target": "skeleton",
        "kind": "structural",
        "weight": 0.5,
    }

    shock = Shock(SystemKind.CIRCULATORY, 0.8, label="x")
    assert shock.to_dict()["target"] == "circulatory"


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (-5.0, Severity.LOW),
        (-0.0001, Severity.LOW),
        (1.0001, Severity.CRITICAL),
        (99.0, Severity.CRITICAL),
        (float("inf"), Severity.CRITICAL),
        (float("-inf"), Severity.LOW),
        (float("nan"), Severity.CRITICAL),
    ],
)
def test_severity_saturates_outside_the_unit_interval(score: float, expected: Severity):
    # from_score is total: out-of-range input saturates at the nearest end band and
    # NaN -- false against every threshold -- falls through to CRITICAL. Saturating
    # pessimistically is deliberate; under-reporting a broken score would be worse.
    assert Severity.from_score(score) is expected


def test_severity_bands_are_ordered_and_exhaustive():
    seen = [Severity.from_score(i / 100) for i in range(101)]
    assert set(seen) == set(Severity)
    # Bands never go backwards as the score rises.
    order = list(Severity)
    assert [order.index(s) for s in seen] == sorted(order.index(s) for s in seen)


@pytest.mark.parametrize(
    ("metric", "expected"),
    [
        (SystemMetric.INTEGRITY, 1),
        (SystemMetric.REDUNDANCY, 1),
        (SystemMetric.LOAD, -1),
        (SystemMetric.CRITICALITY, 0),
    ],
)
def test_improving_direction(metric, expected):
    assert metric.improving_direction() == expected


def test_system_metric_values_name_anatomical_system_fields():
    system = skeleton()
    for metric in SystemMetric:
        assert hasattr(system, metric.value)


def test_sensitivity_to_dict_round_trips():
    sensitivity = Sensitivity(
        system=SystemKind.SKELETON,
        metric=SystemMetric.INTEGRITY,
        baseline_value=0.7,
        span=0.1,
        index_delta=-0.02,
        gradient=-0.2,
    )
    assert sensitivity.to_dict() == {
        "system": "skeleton",
        "metric": "integrity",
        "baseline_value": 0.7,
        "span": 0.1,
        "index_delta": -0.02,
        "gradient": -0.2,
    }


def test_leverage_point_to_dict_round_trips():
    point = LeveragePoint(
        system=SystemKind.CIRCULATORY,
        metric=SystemMetric.LOAD,
        baseline_value=0.2,
        adjusted_value=0.15,
        index_before=0.4,
        index_after=0.38,
        improvement=0.02,
    )
    assert point.to_dict()["system"] == "circulatory"
    assert point.to_dict()["metric"] == "load"
    assert point.to_dict()["improvement"] == 0.02


def test_sensitivity_report_to_dict_nests_children():
    report = SensitivityReport(
        boundary=MarketBoundary(asset_class="equities", geography="US", timeframe="intraday"),
        baseline_index=0.4,
        baseline_severity=Severity.MODERATE,
        step=0.05,
        sensitivities=(),
        leverage_points=(),
    )
    payload = report.to_dict()
    assert payload["baseline_severity"] == "moderate"
    assert payload["boundary"]["asset_class"] == "equities"
    assert payload["sensitivities"] == []
    assert payload["leverage_points"] == []
