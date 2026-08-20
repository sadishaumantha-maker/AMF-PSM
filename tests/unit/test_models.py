"""Unit tests for shared value types."""

from __future__ import annotations

import pytest

from amf.models import (
    Dependency,
    DependencyKind,
    MarketBoundary,
    Severity,
    Shock,
    SystemKind,
)


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
