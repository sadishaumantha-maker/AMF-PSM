"""In-process tests of the docsync command line, including exit codes and the baseline gate."""

from __future__ import annotations

import json

import pytest
from tools.docsync import cli


def run(capsys, *args):
    code = cli.main(list(args))
    return code, capsys.readouterr().out


def test_clean_repo_exits_zero(mini_repo, capsys):
    code, out = run(capsys, "--root", str(mini_repo), "--no-test-count")
    assert code == cli.EXIT_OK
    assert "no drift found" in out


def test_drift_exits_one(mini_repo, capsys):
    (mini_repo / "docs/orphan.md").write_text("# Orphan\n", encoding="utf-8")
    code, out = run(capsys, "--root", str(mini_repo), "--no-test-count")
    assert code == cli.EXIT_DRIFT
    assert "docs.mentioned" in out


def test_missing_guide_exits_two(tmp_path, capsys):
    code, out = run(capsys, "--root", str(tmp_path), "--no-test-count")
    assert code == cli.EXIT_ERROR
    assert "no CLAUDE.md" in out


def test_fail_on_threshold_suppresses_lower_severities(mini_repo, capsys):
    (mini_repo / "examples/lonely.py").write_text("print('x')\n", encoding="utf-8")  # LOW
    assert run(capsys, "--root", str(mini_repo), "--no-test-count")[0] == cli.EXIT_DRIFT
    assert run(capsys, "--root", str(mini_repo), "--no-test-count", "--fail-on", "medium")[0] == cli.EXIT_OK


@pytest.mark.parametrize("fmt", ["text", "json", "md"])
def test_every_format_renders(mini_repo, capsys, fmt):
    code, out = run(capsys, "--root", str(mini_repo), "--no-test-count", "--format", fmt)
    assert code == cli.EXIT_OK
    assert out.strip()


def test_json_output_is_parseable(mini_repo, capsys):
    (mini_repo / "docs/orphan.md").write_text("# Orphan\n", encoding="utf-8")
    _, out = run(capsys, "--root", str(mini_repo), "--no-test-count", "--format", "json")
    assert json.loads(out)["findings"][0]["check"] == "docs.mentioned"


def test_markdown_output_is_a_table(mini_repo, capsys):
    (mini_repo / "docs/orphan.md").write_text("# Orphan\n", encoding="utf-8")
    _, out = run(capsys, "--root", str(mini_repo), "--no-test-count", "--format", "md")
    assert "| Severity | Check | Where | Finding |" in out


def test_out_writes_the_report_to_a_file(mini_repo, tmp_path, capsys):
    target = tmp_path / "nested" / "report.json"
    run(capsys, "--root", str(mini_repo), "--no-test-count", "--format", "json", "--out", str(target))
    written = json.loads(target.read_text(encoding="utf-8"))
    assert written == {"findings": [], "skipped": {"docs.test-count": ANY_REASON}}


ANY_REASON = "the guide states no test total"


def test_baseline_suppresses_known_findings(mini_repo, tmp_path, capsys):
    (mini_repo / "docs/orphan.md").write_text("# Orphan\n", encoding="utf-8")
    baseline = tmp_path / "baseline.json"
    run(capsys, "--root", str(mini_repo), "--no-test-count", "--format", "json", "--out", str(baseline))
    code, _ = run(capsys, "--root", str(mini_repo), "--no-test-count", "--baseline", str(baseline))
    assert code == cli.EXIT_OK


def test_baseline_still_fails_on_a_new_finding(mini_repo, tmp_path, capsys):
    (mini_repo / "docs/orphan.md").write_text("# Orphan\n", encoding="utf-8")
    baseline = tmp_path / "baseline.json"
    run(capsys, "--root", str(mini_repo), "--no-test-count", "--format", "json", "--out", str(baseline))
    (mini_repo / "docs/second.md").write_text("# Second\n", encoding="utf-8")
    code, out = run(capsys, "--root", str(mini_repo), "--no-test-count", "--baseline", str(baseline))
    assert code == cli.EXIT_DRIFT
    assert "new since the baseline" in out


def test_absent_baseline_file_is_ignored(mini_repo, tmp_path, capsys):
    (mini_repo / "docs/orphan.md").write_text("# Orphan\n", encoding="utf-8")
    code, _ = run(capsys, "--root", str(mini_repo), "--no-test-count", "--baseline", str(tmp_path / "nope.json"))
    assert code == cli.EXIT_DRIFT


def test_repeated_scans_are_byte_identical(mini_repo, capsys):
    """Determinism is what lets a checked-in baseline work as a gate."""
    _, first = run(capsys, "--root", str(mini_repo), "--no-test-count", "--format", "json")
    _, second = run(capsys, "--root", str(mini_repo), "--no-test-count", "--format", "json")
    assert first == second
