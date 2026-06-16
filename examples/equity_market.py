"""Example: build a market in code and run the structural diagnosis.

Run with::

    python examples/equity_market.py
"""

from __future__ import annotations

from amf import (
    Dependency,
    DependencyKind,
    DiagnosticEngine,
    Market,
    MarketBoundary,
    SystemKind,
)
from amf.report import render_text
from amf.systems import (
    circulatory,
    immune,
    metabolism,
    musculature,
    nervous,
    organs,
    skeleton,
)


def build_market() -> Market:
    """Assemble an illustrative US equities market anatomy."""
    boundary = MarketBoundary(asset_class="equities", geography="US", timeframe="intraday")
    systems = [
        skeleton(name="Exchanges & settlement", integrity=0.7, redundancy=0.3),
        circulatory(name="Liquidity & capital flow", integrity=0.6, redundancy=0.4, load=0.2),
        nervous(name="Price discovery & data", integrity=0.8),
        musculature(name="Participants", redundancy=0.7),
        organs(name="Market segments"),
        immune(name="Risk controls & regulation", redundancy=0.6),
        metabolism(name="Value creation & destruction"),
    ]
    dependencies = [
        Dependency(SystemKind.CIRCULATORY, SystemKind.NERVOUS, DependencyKind.INFORMATIONAL, 0.5),
        Dependency(SystemKind.NERVOUS, SystemKind.MUSCULATURE, DependencyKind.INFORMATIONAL, 0.6),
        Dependency(SystemKind.MUSCULATURE, SystemKind.CIRCULATORY, DependencyKind.CAPITAL, 0.7),
        Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.8),
        Dependency(SystemKind.ORGANS, SystemKind.CIRCULATORY, DependencyKind.CAPITAL, 0.6),
        Dependency(SystemKind.IMMUNE, SystemKind.SKELETON, DependencyKind.REGULATORY, 0.3),
    ]
    return Market.assemble(boundary, systems, dependencies)


def main() -> None:
    """Diagnose the example market and print the report."""
    market = build_market()
    report = DiagnosticEngine().diagnose(market)
    print(render_text(report))


if __name__ == "__main__":
    main()
