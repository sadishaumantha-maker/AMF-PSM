"""Unit tests for the anatomical systems domain model."""

from __future__ import annotations

import dataclasses

import pytest

from amf.errors import InvalidSystemError
from amf.models import SystemKind
from amf.systems import (
    AnatomicalSystem,
    circulatory,
    immune,
    metabolism,
    musculature,
    nervous,
    organs,
    skeleton,
)

_FACTORIES = (skeleton, circulatory, nervous, musculature, organs, immune, metabolism)


def test_health_combines_integrity_and_load():
    system = AnatomicalSystem(SystemKind.SKELETON, "infra", integrity=0.8, load=0.5)
    assert system.health() == pytest.approx(0.4)


def test_absorptive_capacity_blend():
    system = AnatomicalSystem(SystemKind.SKELETON, "infra", integrity=0.8, redundancy=0.5, load=0.0)
    # 0.5*0.5 + 0.3*0.8 + 0.2*1.0
    assert system.absorptive_capacity() == pytest.approx(0.69)


@pytest.mark.parametrize("field", ["integrity", "redundancy", "criticality", "load"])
def test_out_of_range_metric_raises(field: str):
    with pytest.raises(InvalidSystemError):
        AnatomicalSystem(SystemKind.NERVOUS, "n", **{field: 1.5})


def test_empty_name_raises():
    with pytest.raises(InvalidSystemError):
        AnatomicalSystem(SystemKind.NERVOUS, "   ")


def test_factories_set_kind_and_default_criticality():
    assert skeleton().kind is SystemKind.SKELETON
    assert skeleton().criticality == pytest.approx(0.90)
    assert circulatory().criticality == pytest.approx(0.85)
    assert metabolism().criticality == pytest.approx(0.60)


@pytest.mark.parametrize(
    ("factory", "kind", "name", "criticality"),
    [
        (skeleton, SystemKind.SKELETON, "Market infrastructure", 0.90),
        (circulatory, SystemKind.CIRCULATORY, "Capital flow", 0.85),
        (nervous, SystemKind.NERVOUS, "Information & signals", 0.70),
        (musculature, SystemKind.MUSCULATURE, "Active participants", 0.60),
        (organs, SystemKind.ORGANS, "Functional subsystems", 0.65),
        (immune, SystemKind.IMMUNE, "Risk management & regulation", 0.75),
        (metabolism, SystemKind.METABOLISM, "Value creation & destruction", 0.60),
    ],
)
def test_factory_defaults_are_exact(factory, kind: SystemKind, name: str, criticality: float):
    # Replaces a `assert system.name.strip()` check that would pass even if every
    # factory's default name were swapped with another's.
    system = factory()
    assert system.kind is kind
    assert system.name == name
    assert system.criticality == pytest.approx(criticality)
    assert system.integrity == pytest.approx(1.0)
    assert system.redundancy == pytest.approx(0.5)
    assert system.load == pytest.approx(0.0)
    assert system.components == []


def test_factory_default_names_are_distinct():
    assert len({factory().name for factory in _FACTORIES}) == len(_FACTORIES)


@pytest.mark.parametrize("factory", _FACTORIES)
def test_factory_rejects_unknown_metric(factory):
    # A misspelled metric must not be silently discarded.
    with pytest.raises(InvalidSystemError, match="integritty"):
        factory(integritty=0.1)


def test_factory_rejects_trading_vocabulary_kwarg():
    # The non-trading boundary has to hold at runtime too, not just in name scans.
    with pytest.raises(InvalidSystemError, match="price"):
        skeleton(price=3.0)


def test_factory_error_lists_every_unknown_metric_sorted():
    with pytest.raises(InvalidSystemError, match="alpha, zeta"):
        skeleton(zeta=1.0, alpha=1.0)


@pytest.mark.parametrize("field", ["integrity", "redundancy", "criticality", "load"])
def test_system_is_immutable(field: str):
    system = skeleton()
    with pytest.raises(dataclasses.FrozenInstanceError):
        setattr(system, field, 0.5)


def test_health_cannot_be_driven_out_of_range_after_construction():
    # Previously `s.load = 5.0` was accepted and made health() == -4.0.
    system = skeleton(integrity=1.0, load=0.0)
    assert system.health() == pytest.approx(1.0)
    with pytest.raises(dataclasses.FrozenInstanceError):
        system.load = 5.0
    assert 0.0 <= system.health() <= 1.0
    assert 0.0 <= system.absorptive_capacity() <= 1.0


def test_factory_overrides_metrics_and_components():
    system = skeleton(name="NYSE", components=["NYSE", "DTCC"], integrity=0.5, redundancy=0.2)
    assert system.name == "NYSE"
    assert system.components == ["NYSE", "DTCC"]
    assert system.integrity == pytest.approx(0.5)
    assert system.redundancy == pytest.approx(0.2)
