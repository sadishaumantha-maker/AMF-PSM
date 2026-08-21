"""Unit tests for the static fact extractors."""

from __future__ import annotations

from tools.docsync import facts

CLI = '''\
"""Doc naming ``alpha`` and ``beta``."""

import argparse


def _add_format(parser):
    parser.add_argument("--format", choices=["text", "json"], default="text")


def _build_parser():
    sub = argparse.ArgumentParser().add_subparsers()
    a = sub.add_parser("alpha")
    a.add_argument("source")
    a.add_argument("--depth", type=int, default=3)
    _add_format(a)
    b = sub.add_parser("beta")
    b.add_argument("--target", choices=[k.value for k in SystemKind], required=True)
    b.add_argument("--out", "-o", default=None)
    return sub
'''

MODELS = """\
from enum import Enum


class SystemKind(str, Enum):
    ALPHA = "alpha"
    BETA = "beta"
"""


def test_subcommands_are_recovered_in_declaration_order():
    subs = facts.extract_subcommands(CLI, MODELS)
    assert [s.name for s in subs] == ["alpha", "beta"]


def test_helper_applied_arguments_are_inlined():
    """`--format` is added by `_add_format(parser)`, not inline; missing this yields false findings."""
    subs = facts.extract_subcommands(CLI, MODELS)
    assert "--format" in subs[0].flag_names


def test_helper_inlining_is_targeted_not_global():
    """`beta` never calls the helper, so it must not inherit `--format`."""
    subs = facts.extract_subcommands(CLI, MODELS)
    assert "--format" not in subs[1].flag_names


def test_helper_applied_defaults_and_choices_survive_inlining():
    fmt = facts.extract_subcommands(CLI, MODELS)[0].flag("--format")
    assert fmt.default == "text"
    assert fmt.choices == ("text", "json")


def test_symbolic_choices_are_resolved_against_the_enum():
    """`choices=[k.value for k in SystemKind]` must become real strings, not an AST dump."""
    target = facts.extract_subcommands(CLI, MODELS)[1].flag("--target")
    assert target.choices == ("alpha", "beta")
    assert target.required is True


def test_literal_defaults_are_recovered():
    depth = facts.extract_subcommands(CLI, MODELS)[0].flag("--depth")
    assert depth.default == 3
    assert depth.has_default is True


def test_positional_arguments_are_not_reported_as_flags():
    assert facts.extract_subcommands(CLI, MODELS)[0].flag_names == ("--depth", "--format")


def test_short_and_long_spellings_collapse_to_the_long_one():
    out = facts.extract_subcommands(CLI, MODELS)[1].flag("-o")
    assert out.primary == "--out"


def test_absent_default_is_distinguished_from_a_none_default():
    subs = facts.extract_subcommands(CLI, MODELS)
    assert subs[0].flag("source") is None or subs[0].flag("source").has_default is False
    assert subs[1].flag("--out").has_default is True
    assert subs[1].flag("--out").default is None


def test_unknown_subcommand_lookup_returns_none():
    assert facts.extract_subcommands(CLI, MODELS)[0].flag("--nope") is None


def test_exceptions_map_to_their_first_base():
    source = "class A(Exception):\n    pass\n\n\nclass B(A):\n    pass\n"
    assert facts.extract_exceptions(source) == {"A": "Exception", "B": "A"}


def test_dataclass_options_and_to_dict_are_detected():
    source = (
        "from dataclasses import dataclass\n\n\n"
        "@dataclass(frozen=True, slots=True)\n"
        "class Frozen:\n    ratio: float = 0.25\n\n    def to_dict(self):\n        return {}\n\n\n"
        "@dataclass\nclass Plain:\n    x: int = 1\n"
    )
    found = facts.extract_dataclasses(source)
    assert found["Frozen"] == {"frozen": True, "slots": True, "to_dict": True, "fields": {"ratio": 0.25}}
    assert found["Plain"]["frozen"] is False
    assert found["Plain"]["to_dict"] is False


def test_non_dataclasses_are_ignored():
    assert facts.extract_dataclasses("class Plain:\n    pass\n") == {}


def test_exports_are_returned_in_declaration_order():
    assert facts.extract_exports('__all__ = ["b", "a"]\n') == ("b", "a")


def test_missing_exports_yields_empty():
    assert facts.extract_exports("x = 1\n") == ()


def test_module_imports_capture_only_intra_package_edges():
    source = "import os\nfrom amf.errors import AMFError\nfrom amf import models\nimport amf.viz\n"
    module = facts.extract_module("m", source)
    assert module.imports == frozenset({"errors", "viz"})


def test_module_symbols_union_classes_functions_and_assignments():
    module = facts.extract_module("m", "X = 1\n\n\ndef f():\n    pass\n\n\nclass C:\n    pass\n")
    assert module.symbols == frozenset({"X", "f", "C"})


def test_constants_capture_module_level_literals_only():
    source = "TOP = 0.5\nNAME = 'x'\n\n\ndef f():\n    inner = 9\n    return inner\n"
    assert facts.extract_constants(source) == {"TOP": 0.5, "NAME": "x"}


def test_docstring_commands_are_extracted_from_double_backticks():
    assert facts.extract_module_docstring_commands(CLI) == ("alpha", "beta")


def test_non_literal_defaults_do_not_crash_extraction():
    source = (
        "import argparse\n\n\n"
        "def b():\n"
        "    s = argparse.ArgumentParser().add_subparsers()\n"
        '    a = s.add_parser("a")\n'
        '    a.add_argument("--x", default=compute())\n'
        "    return s\n"
    )
    assert facts.extract_subcommands(source, MODELS)[0].flag("--x").default is None
