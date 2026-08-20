"""Guard tests for repository invariants that are otherwise enforced by memory.

CLAUDE.md requires the package version to stay in sync with ``pyproject.toml``
and ``__all__`` to stay sorted. Both are mechanical, so both are asserted here.
"""

from __future__ import annotations

import importlib
import tomllib
from pathlib import Path

import pytest

import amf

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"


def _pyproject() -> dict:
    with PYPROJECT.open("rb") as handle:
        return tomllib.load(handle)


def test_package_version_matches_pyproject():
    assert amf.__version__ == _pyproject()["project"]["version"]


def test_console_script_points_at_the_cli():
    assert _pyproject()["project"]["scripts"]["amf"] == "amf.cli:main"


def test_all_is_sorted():
    assert list(amf.__all__) == sorted(amf.__all__)


def test_all_has_no_duplicates():
    assert len(amf.__all__) == len(set(amf.__all__))


@pytest.mark.parametrize("name", sorted(amf.__all__))
def test_every_exported_name_resolves(name: str):
    assert hasattr(amf, name), f"{name} is in __all__ but not importable from amf"


def test_every_public_module_is_importable():
    for module in ("cli", "diagnostics", "errors", "graph", "market", "models", "report", "simulation", "systems"):
        assert importlib.import_module(f"amf.{module}") is not None


def test_every_error_type_derives_from_amf_error():
    from amf import errors

    subclasses = [
        value
        for value in vars(errors).values()
        if isinstance(value, type) and issubclass(value, Exception) and value is not errors.AMFError
    ]
    assert subclasses, "the error module should define at least one subclass"
    for error in subclasses:
        assert issubclass(error, errors.AMFError), f"{error.__name__} escapes the AMFError hierarchy"
        assert error.__name__ in amf.__all__, f"{error.__name__} is not exported from amf"
