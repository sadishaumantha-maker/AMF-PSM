"""Shared pytest fixtures for the AMF test suite."""

from __future__ import annotations

import pytest

from amf.market import Market
from amf.models import Dependency, DependencyKind, MarketBoundary, SystemKind
from amf.systems import (
    circulatory,
    immune,
    metabolism,
    musculature,
    nervous,
    organs,
    skeleton,
)


@pytest.fixture
def boundary() -> MarketBoundary:
    """A simple equities market boundary."""
    return MarketBoundary(asset_class="equities", geography="US", timeframe="intraday")


@pytest.fixture
def healthy_market(boundary: MarketBoundary) -> Market:
    """A complete market with strong, redundant systems and no couplings."""
    systems = [
        skeleton(integrity=1.0, redundancy=0.8),
        circulatory(integrity=1.0, redundancy=0.8),
        nervous(integrity=1.0, redundancy=0.8),
        musculature(integrity=1.0, redundancy=0.8),
        organs(integrity=1.0, redundancy=0.8),
        immune(integrity=1.0, redundancy=0.8),
        metabolism(integrity=1.0, redundancy=0.8),
    ]
    return Market.assemble(boundary, systems)


@pytest.fixture
def stressed_market(boundary: MarketBoundary) -> Market:
    """A market with a feedback loop and two structural single points of failure.

    The dependency edges induce the cycle ``circulatory -> nervous ->
    musculature -> circulatory`` and make ``skeleton`` and ``circulatory``
    low-redundancy articulation points.
    """
    systems = [
        skeleton(integrity=0.7, redundancy=0.3),
        circulatory(integrity=0.6, redundancy=0.4, load=0.2),
        nervous(integrity=0.8, redundancy=0.5),
        musculature(integrity=0.9, redundancy=0.7),
        organs(integrity=0.9, redundancy=0.5),
        immune(integrity=0.9, redundancy=0.6),
        metabolism(integrity=0.9, redundancy=0.5),
    ]
    deps = [
        Dependency(SystemKind.CIRCULATORY, SystemKind.NERVOUS, DependencyKind.INFORMATIONAL, 0.5),
        Dependency(SystemKind.NERVOUS, SystemKind.MUSCULATURE, DependencyKind.INFORMATIONAL, 0.6),
        Dependency(SystemKind.MUSCULATURE, SystemKind.CIRCULATORY, DependencyKind.CAPITAL, 0.7),
        Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.8),
        Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.5),
        Dependency(SystemKind.ORGANS, SystemKind.CIRCULATORY, DependencyKind.CAPITAL, 0.6),
        Dependency(SystemKind.METABOLISM, SystemKind.ORGANS, DependencyKind.STRUCTURAL, 0.4),
        Dependency(SystemKind.IMMUNE, SystemKind.SKELETON, DependencyKind.REGULATORY, 0.3),
    ]
    return Market.assemble(boundary, systems, deps)
