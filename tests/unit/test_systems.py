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


def test_factory_default_names_present():
    for factory in (skeleton, circulatory, nervous, musculature, organs, immune, metabolism):
        system = factory()
        assert system.name.strip()


def test_factory_overrides_metrics_and_components():
    system = skeleton(name="NYSE", components=["NYSE", "DTCC"], integrity=0.5, redundancy=0.2)
    assert system.name == "NYSE"
    assert system.components == ["NYSE", "DTCC"]
    assert system.integrity == pytest.approx(0.5)
    assert system.redundancy == pytest.approx(0.2)
