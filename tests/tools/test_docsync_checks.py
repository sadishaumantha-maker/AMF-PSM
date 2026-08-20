"""Direct tests of individual checks, for branches the mutation corpus cannot reach."""

from __future__ import annotations

import sys

from tools.docsync import facts as facts_module
from tools.docsync.checks import (
    check_cli_docstring,
    check_config_defaults,
    check_examples_mentioned,
    check_named_constants,
    check_subcommands,
    check_test_count,
    check_version_sync,
)
from tools.docsync.claims import Claims
from tools.docsync.facts import RepoFacts, Subcommand
from tools.docsync.model import Severity


def make_facts(**kwargs):
    return RepoFacts(root=kwargs.pop("root", None) or facts_module.Path("."), **kwargs)


def make_claims(text="", **kwargs):
    return Claims(text=text, **kwargs)


# --- docs.test-count ---------------------------------------------------------------


def test_matching_test_counts_produce_no_finding():
    assert check_test_count(make_facts(test_count=520), make_claims(test_count=520)) == []


def test_mismatched_test_counts_are_high_severity():
    findings = check_test_count(make_facts(test_count=520), make_claims(test_count=513))
    assert len(findings) == 1
    assert findings[0].severity is Severity.HIGH
    assert "513" in findings[0].message
    assert "520" in findings[0].message


def test_unknown_real_count_yields_nothing_rather_than_guessing():
    assert check_test_count(make_facts(test_count=None), make_claims(test_count=513)) == []


def test_unstated_claim_count_yields_nothing():
    assert check_test_count(make_facts(test_count=520), make_claims(test_count=None)) == []


# --- cli.subcommand-set ------------------------------------------------------------


def test_documented_subcommand_that_does_not_exist_is_reported():
    findings = check_subcommands(
        make_facts(subcommands=(Subcommand(name="alpha"),)),
        make_claims(cli=()),
    )
    assert [f.check for f in findings] == ["cli.subcommand-set"]
    assert "does not document" in findings[0].message


def test_subcommand_count_of_zero_is_not_confused_with_absent():
    findings = check_subcommands(make_facts(subcommands=()), make_claims(cli=(), subcommand_count=0))
    assert findings == []


# --- cli.docstring-commands --------------------------------------------------------


def test_docstring_check_is_skipped_when_there_is_no_docstring():
    facts = make_facts(subcommands=(Subcommand(name="alpha"),), cli_docstring_commands=())
    assert check_cli_docstring(facts, make_claims()) == []


def test_docstring_naming_every_subcommand_passes():
    facts = make_facts(subcommands=(Subcommand(name="alpha"),), cli_docstring_commands=("alpha", "main"))
    assert check_cli_docstring(facts, make_claims()) == []


# --- version.sync ------------------------------------------------------------------


def test_version_check_is_skipped_when_either_version_is_unknown():
    assert check_version_sync(make_facts(package_version="", pyproject_version="1.0"), make_claims()) == []
    assert check_version_sync(make_facts(package_version="1.0", pyproject_version=""), make_claims()) == []


def test_matching_versions_pass():
    assert check_version_sync(make_facts(package_version="1.0", pyproject_version="1.0"), make_claims()) == []


# --- config.defaults ---------------------------------------------------------------


def test_documented_field_that_does_not_exist_is_reported():
    facts = make_facts(dataclasses={"DemoConfig": {"fields": {"other": 1}}})
    findings = check_config_defaults(facts, make_claims(config_defaults={"DemoConfig": {"ratio": 0.5}}))
    assert [f.severity for f in findings] == [Severity.MEDIUM]
    assert "no such field default" in findings[0].message


def test_documented_config_that_does_not_exist_is_ignored():
    findings = check_config_defaults(make_facts(), make_claims(config_defaults={"Ghost": {"x": 1}}))
    assert findings == []


# --- constants.named ---------------------------------------------------------------


def test_named_constant_mismatch_is_reported_with_its_module():
    facts = make_facts(constants={"diagnostics._LOW_REDUNDANCY": 0.4})
    findings = check_named_constants(facts, make_claims(named_constants={"_LOW_REDUNDANCY": 0.5}))
    assert findings[0].location == "src/amf/diagnostics.py"
    assert findings[0].severity is Severity.HIGH


def test_named_constant_that_matches_passes():
    facts = make_facts(constants={"diagnostics._LOW_REDUNDANCY": 0.5})
    assert check_named_constants(facts, make_claims(named_constants={"_LOW_REDUNDANCY": 0.5})) == []


# --- examples.mentioned ------------------------------------------------------------


def test_mentioned_example_passes():
    facts = make_facts(examples=("demo.py",))
    assert check_examples_mentioned(facts, make_claims(text="see `demo.py`")) == []


# --- facts.collect_test_count ------------------------------------------------------


def test_collect_test_count_returns_none_when_pytest_reports_nothing(tmp_path):
    """An empty tree collects no tests, so there is no count to parse -- and none is invented."""
    assert facts_module.collect_test_count(tmp_path) in (None, 0)


def test_collect_test_count_parses_a_real_collection(tmp_path):
    (tmp_path / "test_sample.py").write_text("def test_a():\n    pass\n\n\ndef test_b():\n    pass\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[tool.pytest.ini_options]\ntestpaths = ['.']\n", encoding="utf-8")
    assert facts_module.collect_test_count(tmp_path) == 2


def test_collect_test_count_returns_none_when_pytest_cannot_run(tmp_path, monkeypatch):
    monkeypatch.setattr(facts_module.subprocess, "run", _raise_oserror)
    assert facts_module.collect_test_count(tmp_path) is None


def _raise_oserror(*_args, **_kwargs):
    raise OSError("no interpreter")


def test_module_entry_point_runs(tmp_path):
    """`python -m tools.docsync` must be a working entry point, not just an importable module."""
    import os
    import subprocess

    env = {k: v for k, v in os.environ.items() if not k.startswith(("COV_CORE_", "COVERAGE_"))}
    completed = subprocess.run(
        [sys.executable, "-m", "tools.docsync", "--root", str(tmp_path), "--no-test-count"],
        check=False,
        capture_output=True,
        text=True,
        cwd=facts_module.Path(__file__).resolve().parents[2],
        env=env,
    )
    assert completed.returncode == 2
    assert "no CLAUDE.md" in completed.stdout
