"""Unit tests for the anatomical systems domain model."""

from __future__ import annotations

import dataclasses

import pytest

from amf.errors import InvalidSystemError
from amf.models import SystemKind, SystemMetric
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


class TestMetricAccess:
    @pytest.mark.parametrize(
        ("metric", "expected"),
        [
            (SystemMetric.INTEGRITY, 0.7),
            (SystemMetric.REDUNDANCY, 0.3),
            (SystemMetric.CRITICALITY, 0.9),
            (SystemMetric.LOAD, 0.1),
        ],
    )
    def test_metric_reads_each_field(self, metric, expected):
        system = skeleton(integrity=0.7, redundancy=0.3, criticality=0.9, load=0.1)
        assert system.metric(metric) == pytest.approx(expected)

    @pytest.mark.parametrize("metric", list(SystemMetric))
    def test_with_metric_replaces_only_that_metric(self, metric):
        system = skeleton(integrity=0.7, redundancy=0.3, criticality=0.9, load=0.1)
        variant = system.with_metric(metric, 0.5)
        assert variant.metric(metric) == pytest.approx(0.5)
        for other in SystemMetric:
            if other is not metric:
                assert variant.metric(other) == system.metric(other)

    def test_with_metric_leaves_the_original_untouched(self):
        system = skeleton(integrity=0.7)
        system.with_metric(SystemMetric.INTEGRITY, 0.2)
        assert system.integrity == pytest.approx(0.7)

    def test_with_metric_preserves_identity_fields(self):
        system = skeleton(name="NYSE + DTCC", components=["clearing"])
        variant = system.with_metric(SystemMetric.LOAD, 0.4)
        assert variant.kind is system.kind
        assert variant.name == system.name
        assert variant.components == system.components

    def test_with_metric_copies_components_rather_than_aliasing(self):
        system = skeleton(components=["clearing"])
        variant = system.with_metric(SystemMetric.LOAD, 0.4)
        variant.components.append("settlement")
        assert system.components == ["clearing"]

    @pytest.mark.parametrize("value", [-0.1, 1.5])
    def test_with_metric_validates_the_new_value(self, value):
        with pytest.raises(InvalidSystemError):
            skeleton().with_metric(SystemMetric.INTEGRITY, value)
