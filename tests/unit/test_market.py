"""Unit tests for the Market aggregate root and JSON (de)serialisation."""

from __future__ import annotations

from collections import Counter

import pytest

from amf.errors import IncompleteMarketError, MarketParseError
from amf.market import Market
from amf.models import Dependency, DependencyKind, MarketBoundary, SystemKind
from amf.systems import SYSTEM_FACTORIES, skeleton


def _minimal_market_data(**system_bodies: dict[str, object]) -> dict[str, object]:
    """A schema-valid market whose systems carry only the given fields."""
    return {
        "boundary": {"asset_class": "equities", "geography": "US", "timeframe": "intraday"},
        "systems": {kind.value: system_bodies.get(kind.value, {}) for kind in SystemKind},
        "dependencies": [],
    }


def test_assemble_requires_all_seven_systems(boundary: MarketBoundary):
    with pytest.raises(IncompleteMarketError):
        Market.assemble(boundary, [skeleton()])


def test_assemble_rejects_duplicate_kind(boundary: MarketBoundary):
    with pytest.raises(IncompleteMarketError):
        Market.assemble(boundary, [skeleton(), skeleton()])


def test_system_lookup_and_missing(healthy_market: Market):
    assert healthy_market.system(SystemKind.SKELETON).kind is SystemKind.SKELETON
    # Build a separate market to remove the system from, so the shared fixture is
    # never mutated (which would corrupt it if it were ever scoped wider).
    without_skeleton = Market(
        boundary=healthy_market.boundary,
        systems={k: v for k, v in healthy_market.systems.items() if k is not SystemKind.SKELETON},
        graph=healthy_market.graph,
    )
    with pytest.raises(IncompleteMarketError):
        without_skeleton.system(SystemKind.SKELETON)


def test_round_trip_to_and_from_dict(stressed_market: Market):
    data = stressed_market.to_dict()
    restored = Market.from_dict(data)
    # Compare the restored graph against the ORIGINAL model, not against another
    # to_dict() output: a loss shared by both sides of that comparison is
    # invisible, which is exactly how the dropped dependency kind went unnoticed.
    assert restored.graph.dependencies() == stressed_market.graph.dependencies()
    assert restored.to_dict() == data


def test_to_dict_preserves_dependency_kinds(stressed_market: Market):
    # The fixture carries informational x2, capital x2, regulatory x1 and
    # structural x3; every edge used to be exported as "structural".
    exported = Counter(d["kind"] for d in stressed_market.to_dict()["dependencies"])
    assert exported == Counter({"structural": 3, "informational": 2, "capital": 2, "regulatory": 1})


def test_round_trip_preserves_two_kinds_on_one_pair(market_factory):
    deps = [
        Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.3),
        Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.2),
    ]
    market = market_factory(deps)
    data = market.to_dict()
    assert len(data["dependencies"]) == 2

    restored = Market.from_dict(data)
    assert restored.graph.dependencies() == market.graph.dependencies()
    assert restored.graph.edge_weight(SystemKind.NERVOUS, SystemKind.SKELETON) == pytest.approx(0.5)


def test_to_dict_dependency_order_is_independent_of_construction_order(market_factory):
    deps = [
        Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.2),
        Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.4),
    ]
    forward = market_factory(deps).to_dict()["dependencies"]
    backward = market_factory(list(reversed(deps))).to_dict()["dependencies"]
    assert forward == backward


def test_from_dict_missing_key_raises():
    with pytest.raises(MarketParseError):
        Market.from_dict({"systems": {}})


def test_from_dict_unknown_system_kind_raises(stressed_market: Market):
    data = stressed_market.to_dict()
    data["systems"]["bones"] = data["systems"].pop("skeleton")
    with pytest.raises(MarketParseError):
        Market.from_dict(data)


def test_from_dict_unknown_dependency_kind_raises(stressed_market: Market):
    data = stressed_market.to_dict()
    data["dependencies"][0]["kind"] = "telepathic"
    with pytest.raises(MarketParseError):
        Market.from_dict(data)


def test_from_dict_incomplete_after_parse_raises(stressed_market: Market):
    data = stressed_market.to_dict()
    data["systems"].pop("metabolism")
    with pytest.raises(MarketParseError):
        Market.from_dict(data)


@pytest.mark.parametrize("field", ["integrity", "redundancy", "criticality", "load"])
def test_from_dict_out_of_range_metric_raises_market_parse_error(stressed_market: Market, field: str):
    # An out-of-range metric is a malformed value: from_dict must surface it as a
    # MarketParseError, not leak the underlying InvalidSystemError.
    data = stressed_market.to_dict()
    data["systems"]["skeleton"][field] = 1.5
    with pytest.raises(MarketParseError):
        Market.from_dict(data)


def test_from_dict_empty_system_name_raises_market_parse_error(stressed_market: Market):
    data = stressed_market.to_dict()
    data["systems"]["skeleton"]["name"] = "   "
    with pytest.raises(MarketParseError):
        Market.from_dict(data)


@pytest.mark.parametrize("weight", [0.0, -0.1, 1.5])
def test_from_dict_invalid_dependency_weight_raises_market_parse_error(stressed_market: Market, weight: float):
    # A bad dependency weight is rejected by the graph; from_dict must wrap the
    # resulting InvalidDependencyError as a MarketParseError.
    data = stressed_market.to_dict()
    data["dependencies"][0]["weight"] = weight
    with pytest.raises(MarketParseError):
        Market.from_dict(data)


@pytest.mark.parametrize("kind", list(SystemKind))
def test_from_dict_omitted_metrics_match_the_factory_defaults(kind: SystemKind):
    # A market built from JSON must not differ from the equivalent factory-built
    # market just because the JSON left a field out.
    parsed = Market.from_dict(_minimal_market_data()).system(kind)
    expected = SYSTEM_FACTORIES[kind]()
    assert parsed.criticality == pytest.approx(expected.criticality)
    assert parsed.name == expected.name
    assert parsed.integrity == pytest.approx(expected.integrity)
    assert parsed.redundancy == pytest.approx(expected.redundancy)
    assert parsed.load == pytest.approx(expected.load)


def test_from_dict_explicit_values_override_the_factory_defaults():
    # Negative control: the fix must not be "always use the factory default".
    data = _minimal_market_data(skeleton={"name": "NYSE", "criticality": 0.1, "integrity": 0.2})
    parsed = Market.from_dict(data).system(SystemKind.SKELETON)
    assert parsed.name == "NYSE"
    assert parsed.criticality == pytest.approx(0.1)
    assert parsed.integrity == pytest.approx(0.2)


def test_from_dict_rejects_unknown_system_field():
    # Unknown metrics are rejected by the factories, and from_dict surfaces that
    # as a parse error rather than silently ignoring the field.
    data = _minimal_market_data(skeleton={"integritty": 0.5})
    with pytest.raises(MarketParseError):
        Market.from_dict(data)


@pytest.mark.parametrize("field", ["integrity", "redundancy", "criticality", "load"])
def test_from_dict_non_numeric_metric_raises_market_parse_error(stressed_market: Market, field: str):
    # float("abc") raises ValueError, which was not in from_dict's caught tuple and
    # escaped the documented MarketParseError contract.
    data = stressed_market.to_dict()
    data["systems"]["skeleton"][field] = "abc"
    with pytest.raises(MarketParseError, match="malformed market description"):
        Market.from_dict(data)


def test_from_dict_non_numeric_dependency_weight_raises_market_parse_error(stressed_market: Market):
    data = stressed_market.to_dict()
    data["dependencies"][0]["weight"] = "heavy"
    with pytest.raises(MarketParseError, match="malformed market description"):
        Market.from_dict(data)


def test_from_dict_self_loop_dependency_raises_market_parse_error(stressed_market: Market):
    data = stressed_market.to_dict()
    dep = data["dependencies"][0]
    dep["target"] = dep["source"]
    with pytest.raises(MarketParseError):
        Market.from_dict(data)
