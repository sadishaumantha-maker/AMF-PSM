"""Guard test: the public API must contain no trading-system concepts.

The Anatomical Market Framework toolkit models market *structure and resilience*,
never trading. This test asserts that no public symbol name or dataclass field
name uses trading vocabulary, so the constraint is enforced mechanically and a
future change introducing, say, an ``order`` or ``price`` field fails CI.
"""

from __future__ import annotations

import dataclasses

import amf
from amf import models

# Substrings that would indicate trading concepts leaking into the model. Chosen
# to avoid collisions with the toolkit's structural vocabulary (e.g. "ordering"
# is not used as a public name; these are matched as substrings of lowercased
# identifiers only, never against prose).
FORBIDDEN = (
    "order",
    "buy",
    "sell",
    "price",
    "pnl",
    "broker",
    "backtest",
    "ticker",
    "trade",
    "portfolio",
    "candlestick",
)

# Every public dataclass whose field names form part of the API surface.
_PUBLIC_DATACLASSES = (
    models.MarketBoundary,
    models.Dependency,
    models.WeaknessFinding,
    models.DiagnosticReport,
    models.Shock,
    models.ResilienceScore,
    models.SimulationTrace,
)


def test_public_names_have_no_trading_vocabulary():
    for name in amf.__all__:
        lowered = name.lower()
        assert not any(bad in lowered for bad in FORBIDDEN), f"trading term in public name: {name}"


def test_public_dataclass_fields_have_no_trading_vocabulary():
    for klass in _PUBLIC_DATACLASSES:
        for field in dataclasses.fields(klass):
            lowered = field.name.lower()
            assert not any(bad in lowered for bad in FORBIDDEN), f"trading term in field: {klass.__name__}.{field.name}"


def test_no_trading_modules_exposed():
    for name in amf.__all__:
        lowered = name.lower()
        assert "trad" not in lowered
        assert "exchange" not in lowered or name == "exchange"  # no trading-exchange concept
