"""Unit tests for the Market aggregate root and JSON (de)serialisation."""

from __future__ import annotations

import pytest

from amf.errors import IncompleteMarketError, MarketParseError
from amf.market import Market
from amf.models import MarketBoundary, SystemKind
from amf.systems import skeleton


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
