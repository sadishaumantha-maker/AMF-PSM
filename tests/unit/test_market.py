"""Unit tests for the Market aggregate root and JSON (de)serialisation."""

from __future__ import annotations

import pytest

from amf.diagnostics import DiagnosticEngine
from amf.errors import IncompleteMarketError, InvalidSystemError, MarketParseError
from amf.market import Market
from amf.models import Dependency, DependencyKind, MarketBoundary, SystemKind
from amf.simulation import ShockSimulator
from amf.systems import (
    circulatory,
    immune,
    metabolism,
    musculature,
    nervous,
    organs,
    skeleton,
)


def test_assemble_requires_all_seven_systems(boundary: MarketBoundary):
    with pytest.raises(IncompleteMarketError):
        Market.assemble(boundary, [skeleton()])


def test_assemble_rejects_duplicate_kind(boundary: MarketBoundary):
    with pytest.raises(IncompleteMarketError):
        Market.assemble(boundary, [skeleton(), skeleton()])


def test_system_lookup_and_missing(healthy_market: Market):
    assert healthy_market.system(SystemKind.SKELETON).kind is SystemKind.SKELETON
    del healthy_market.systems[SystemKind.SKELETON]
    with pytest.raises(IncompleteMarketError):
        healthy_market.system(SystemKind.SKELETON)


def test_round_trip_to_and_from_dict(stressed_market: Market):
    data = stressed_market.to_dict()
    restored = Market.from_dict(data)
    assert restored.to_dict() == data


def test_to_dict_preserves_dependency_kind(stressed_market: Market):
    # The fixture couples immune -> skeleton with a regulatory dependency; the
    # serialised entry must carry that kind, not the structural default.
    deps = {(d["source"], d["target"]): d["kind"] for d in stressed_market.to_dict()["dependencies"]}
    assert deps[("immune", "skeleton")] == "regulatory"
    assert deps[("circulatory", "nervous")] == "informational"
    assert deps[("musculature", "circulatory")] == "capital"
    assert deps[("circulatory", "skeleton")] == "structural"


def test_round_trip_preserves_dependency_kinds(stressed_market: Market):
    restored = Market.from_dict(stressed_market.to_dict())
    assert restored.graph.edge_kinds(SystemKind.IMMUNE, SystemKind.SKELETON) == (DependencyKind.REGULATORY,)
    assert restored.graph.edge_kinds(SystemKind.ORGANS, SystemKind.CIRCULATORY) == (DependencyKind.CAPITAL,)


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


def test_from_dict_self_loop_dependency_raises_market_parse_error(stressed_market: Market):
    data = stressed_market.to_dict()
    dep = data["dependencies"][0]
    dep["target"] = dep["source"]
    with pytest.raises(MarketParseError):
        Market.from_dict(data)


@pytest.mark.parametrize("field", ["integrity", "redundancy", "criticality", "load"])
def test_from_dict_non_numeric_metric_raises_market_parse_error(stressed_market: Market, field: str):
    # A wrong-typed value is as malformed as an out-of-range one. Before this was
    # fixed, float() raised a bare ValueError that escaped from_dict entirely.
    data = stressed_market.to_dict()
    data["systems"]["skeleton"][field] = "very high"
    with pytest.raises(MarketParseError, match=field):
        Market.from_dict(data)


def test_from_dict_non_numeric_dependency_weight_raises_market_parse_error(stressed_market: Market):
    data = stressed_market.to_dict()
    data["dependencies"][0]["weight"] = "heavy"
    with pytest.raises(MarketParseError, match="weight"):
        Market.from_dict(data)


@pytest.mark.parametrize("value", ["abc", 5, {"a": 1}])
def test_from_dict_non_list_components_raises_market_parse_error(stressed_market: Market, value):
    # A bare string is iterable, so accepting one would split "abc" into three
    # single-character components instead of reporting malformed input.
    data = stressed_market.to_dict()
    data["systems"]["skeleton"]["components"] = value
    with pytest.raises(MarketParseError, match="components"):
        Market.from_dict(data)


def test_round_trip_preserves_every_edge_weight_and_kind(stressed_market: Market):
    # Stronger than comparing the two dicts: that comparison also passes when
    # from_dict loses information, as long as the loss is stable on re-serialising.
    restored = Market.from_dict(stressed_market.to_dict())
    for source in SystemKind:
        for target in SystemKind:
            assert restored.graph.edge_weight(source, target) == pytest.approx(
                stressed_market.graph.edge_weight(source, target)
            )
            assert restored.graph.edge_kinds(source, target) == stressed_market.graph.edge_kinds(source, target)


def test_round_trip_preserves_system_metrics(stressed_market: Market):
    restored = Market.from_dict(stressed_market.to_dict())
    for kind, system in stressed_market.systems.items():
        other = restored.system(kind)
        assert other.name == system.name
        assert other.components == system.components
        assert (other.integrity, other.redundancy, other.criticality, other.load) == pytest.approx(
            (system.integrity, system.redundancy, system.criticality, system.load)
        )


def test_multi_kind_edge_is_a_documented_round_trip_limitation(boundary: MarketBoundary):
    # The JSON schema carries one kind per entry, so an edge aggregated from two
    # kinds serialises under the first only. This asserts the known lossiness so a
    # future schema change that fixes it has to update this test deliberately.
    systems = [skeleton(), circulatory(), nervous(), musculature(), organs(), immune(), metabolism()]
    deps = [
        Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.REGULATORY, 0.3),
        Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.INFORMATIONAL, 0.4),
    ]
    market = Market.assemble(boundary, systems, deps)
    assert market.graph.edge_kinds(SystemKind.NERVOUS, SystemKind.SKELETON) == (
        DependencyKind.INFORMATIONAL,
        DependencyKind.REGULATORY,
    )
    restored = Market.from_dict(market.to_dict())
    assert restored.graph.edge_kinds(SystemKind.NERVOUS, SystemKind.SKELETON) == (DependencyKind.INFORMATIONAL,)
    # The aggregated weight does survive, and the dict form is stable.
    assert restored.graph.edge_weight(SystemKind.NERVOUS, SystemKind.SKELETON) == pytest.approx(0.7)
    assert restored.to_dict() == market.to_dict()


@pytest.mark.parametrize("field", ["integrity", "redundancy", "criticality", "load"])
def test_require_complete_rejects_a_system_mutated_out_of_range(healthy_market: Market, field: str):
    # Systems are mutable, so validation at construction is not enough. Every
    # engine calls require_complete first, which makes it the catch point.
    setattr(healthy_market.system(SystemKind.SKELETON), field, 1.5)
    with pytest.raises(InvalidSystemError, match=field):
        healthy_market.require_complete()


def test_engines_reject_a_market_mutated_out_of_range(healthy_market: Market):
    healthy_market.system(SystemKind.CIRCULATORY).integrity = 7.5
    with pytest.raises(InvalidSystemError):
        DiagnosticEngine().diagnose(healthy_market)
    with pytest.raises(InvalidSystemError):
        ShockSimulator(healthy_market)
