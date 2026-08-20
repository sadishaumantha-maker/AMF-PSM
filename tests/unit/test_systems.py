"""Unit tests for the anatomical systems domain model."""

from __future__ import annotations

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


def test_default_criticality_table_is_exact():
    # The seven defaults are a design decision, not incidental: pin all of them.
    factories = (skeleton, circulatory, nervous, musculature, organs, immune, metabolism)
    assert {f().kind: f().criticality for f in factories} == {
        SystemKind.SKELETON: pytest.approx(0.90),
        SystemKind.CIRCULATORY: pytest.approx(0.85),
        SystemKind.IMMUNE: pytest.approx(0.75),
        SystemKind.NERVOUS: pytest.approx(0.70),
        SystemKind.ORGANS: pytest.approx(0.65),
        SystemKind.MUSCULATURE: pytest.approx(0.60),
        SystemKind.METABOLISM: pytest.approx(0.60),
    }


def test_default_criticality_ordering_reflects_load_bearing_rank():
    # The ordering is the claim the table encodes: infrastructure and capital flow
    # are the most load-bearing, participants and metabolism the least.
    ranked = [skeleton(), circulatory(), immune(), nervous(), organs()]
    scores = [s.criticality for s in ranked]
    assert scores == sorted(scores, reverse=True)
    assert organs().criticality > musculature().criticality
    assert musculature().criticality == pytest.approx(metabolism().criticality)


def test_absorptive_capacity_weights_sum_to_one():
    # A fully redundant, fully intact, unloaded system absorbs everything; the
    # blend can therefore never exceed the unit interval.
    best = AnatomicalSystem(SystemKind.SKELETON, "s", integrity=1.0, redundancy=1.0, load=0.0)
    worst = AnatomicalSystem(SystemKind.SKELETON, "s", integrity=0.0, redundancy=0.0, load=1.0)
    assert best.absorptive_capacity() == pytest.approx(1.0)
    assert worst.absorptive_capacity() == pytest.approx(0.0)
