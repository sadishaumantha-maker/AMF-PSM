"""Guard test: the public API must contain no trading-system concepts.

The Anatomical Market Framework toolkit models market *structure and resilience*,
never trading. This test asserts that no public symbol, class member, or dataclass
field name uses trading vocabulary, so the constraint is enforced mechanically and
a future change introducing, say, an ``order`` or ``price`` field fails CI.

The scan walks every public class reachable from ``amf.__all__`` rather than a
hand-maintained list, because a hand-maintained list drifts: the previous version
of this file checked seven dataclasses and missed five others, along with every
method and property name in the package.
"""

from __future__ import annotations

import dataclasses
from enum import Enum

import pytest

import amf
from amf.errors import InvalidSystemError

# Substrings that would indicate trading concepts leaking into the model. Chosen
# to avoid collisions with the toolkit's structural vocabulary; these are matched
# as substrings of lowercased identifiers only, never against prose.
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
    "returns",
    "signal",
)

# ``(class, member)`` pairs that contain a forbidden substring but are provably
# not trading concepts. Keyed by class so a future ``order`` elsewhere is still
# caught. Every entry is checked for existence by the meta-test below.
ALLOWLIST: frozenset[tuple[str, str]] = frozenset(
    {
        # CouplingMatrix.order is the row/column ordering of the 7x7 matrix, not
        # a trade order. The API name is kept deliberately; see graph.py.
        ("CouplingMatrix", "order"),
    }
)

# Bases whose members are inherited machinery, not part of the AMF surface.
_STOP_BASES = (object, str, Enum, Exception, BaseException)


def _public_members(klass: type) -> set[str]:
    """Return the public members a class itself defines, across its own bases.

    Uses ``vars()`` rather than ``dir()`` for two reasons: on Python 3.11
    ``dir()`` on a ``StrEnum`` omits methods defined in the enum body (the
    metaclass filters them, so ``Severity.from_score`` would be missed), and it
    adds ~47 inherited ``str`` methods that are pure noise.
    """
    names: set[str] = set()
    for base in klass.__mro__:
        if base in _STOP_BASES or base.__module__ in {"builtins", "enum"}:
            continue
        names |= {name for name in vars(base) if not name.startswith("_")}
    return names


def _public_classes() -> list[tuple[str, type]]:
    """Return every class exported from ``amf.__all__``."""
    classes = []
    for name in amf.__all__:
        obj = getattr(amf, name)
        if isinstance(obj, type):
            classes.append((name, obj))
    return classes


def _offending(name: str) -> list[str]:
    lowered = name.lower()
    return [bad for bad in FORBIDDEN if bad in lowered]


def test_public_names_have_no_trading_vocabulary():
    assert "SystemKind" in amf.__all__, "__all__ is populated (else this test is vacuous)"
    for name in amf.__all__:
        assert not _offending(name), f"trading term in public name: {name}"


def test_public_members_have_no_trading_vocabulary():
    classes = _public_classes()
    assert len(classes) > 10, "the walk found classes (else this test is vacuous)"

    checked = 0
    for class_name, klass in classes:
        for member in _public_members(klass):
            checked += 1
            if (class_name, member) in ALLOWLIST:
                continue
            assert not _offending(member), f"trading term in member: {class_name}.{member}"
    # Anchor on a member we know exists, so a walker that silently returns
    # nothing cannot pass. dir() would miss this one on Python 3.11.
    assert "from_score" in _public_members(amf.Severity)
    assert "integrity" in _public_members(amf.AnatomicalSystem)
    assert checked > 50


def test_public_dataclass_fields_have_no_trading_vocabulary():
    dataclass_names = [name for name, klass in _public_classes() if dataclasses.is_dataclass(klass)]
    # The previous hand-maintained list held seven; discovery finds all of them,
    # including AnatomicalSystem, Market, CouplingMatrix and the two configs.
    assert len(dataclass_names) >= 12, dataclass_names

    for class_name, klass in _public_classes():
        if not dataclasses.is_dataclass(klass):
            continue
        for field in dataclasses.fields(klass):
            if (class_name, field.name) in ALLOWLIST:
                continue
            assert not _offending(field.name), f"trading term in field: {class_name}.{field.name}"


def test_allowlist_entries_still_exist():
    # Without this, a rename would leave a permanent silent hole in the guard.
    for class_name, member in ALLOWLIST:
        klass = getattr(amf, class_name, None)
        assert klass is not None, f"allowlisted class no longer exported: {class_name}"
        assert member in _public_members(klass), f"allowlisted member no longer exists: {class_name}.{member}"
        assert _offending(member), f"allowlist entry {class_name}.{member} is no longer needed"


def test_no_trading_modules_exposed():
    assert amf.__all__
    for name in amf.__all__:
        assert "trad" not in name.lower()
        assert "exchange" not in name.lower()


def test_system_factories_reject_trading_metrics_at_runtime():
    # The name scan cannot see keyword arguments, and the factories accept
    # arbitrary **metrics; without the unknown-metric check `skeleton(price=3.0)`
    # would be silently accepted.
    for term in ("price", "pnl", "trade"):
        with pytest.raises(InvalidSystemError, match=term):
            amf.skeleton(**{term: 1.0})
