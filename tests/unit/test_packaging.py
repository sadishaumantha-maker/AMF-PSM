"""Guard tests for repository invariants that are otherwise enforced by memory.

CLAUDE.md requires the package version to stay in sync with ``pyproject.toml``,
``__all__`` to stay resolvable, and the distribution to remain private. All are
mechanical, so all are asserted here.
"""

from __future__ import annotations

import importlib
import tomllib
from importlib import metadata
from pathlib import Path

import pytest

import amf

PYPROJECT = Path(__file__).resolve().parents[2] / "pyproject.toml"

# PyPI refuses any upload carrying this classifier. It is what keeps this
# proprietary, all-rights-reserved package off public indexes.
PRIVATE_CLASSIFIER = "Private :: Do Not Upload"


def _pyproject() -> dict:
    with PYPROJECT.open("rb") as handle:
        return tomllib.load(handle)


def test_package_version_matches_pyproject():
    assert amf.__version__ == _pyproject()["project"]["version"]


def test_console_script_points_at_the_cli():
    assert _pyproject()["project"]["scripts"]["amf"] == "amf.cli:main"


# __all__ ordering is enforced by ruff's RUF022, which uses an isort-style natural
# sort (SCREAMING_CASE constants first) rather than plain str ordering. Asserting it
# here would duplicate the linter and encode the wrong convention.


def test_all_has_no_duplicates():
    assert len(amf.__all__) == len(set(amf.__all__))


@pytest.mark.parametrize("name", sorted(amf.__all__))
def test_every_exported_name_resolves(name: str):
    assert hasattr(amf, name), f"{name} is in __all__ but not importable from amf"


def test_every_public_module_is_importable():
    for module in (
        "cli",
        "diagnostics",
        "errors",
        "graph",
        "market",
        "models",
        "report",
        "sensitivity",
        "simulation",
        "systems",
        "viz",
    ):
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


def test_pyproject_declares_the_private_classifier():
    # Without this, `twine upload` would be accepted by PyPI rather than refused.
    assert PRIVATE_CLASSIFIER in _pyproject()["project"]["classifiers"]


def test_built_metadata_carries_the_private_classifier():
    # The classifier must survive the build, not merely sit in the source config:
    # an index reads the metadata from the distribution, not from pyproject.toml.
    assert PRIVATE_CLASSIFIER in metadata.metadata("amf").get_all("Classifier", [])


def test_licence_is_declared_proprietary():
    assert "Proprietary" in _pyproject()["project"]["license"]["text"]


def test_no_public_index_is_configured():
    # A project URL pointing at a public index would contradict the
    # private-only distribution policy recorded in RELEASING.md.
    urls = " ".join(_pyproject()["project"].get("urls", {}).values()).lower()
    assert "pypi.org" not in urls
