"""Integration tests driving the CLI end to end via ``main``."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from amf import __version__
from amf.cli import _METHOD_STEPS, _SYSTEM_SUMMARY, main
from amf.diagnostics import DiagnosticEngine
from amf.market import Market
from amf.models import DependencyKind, SystemKind

SAMPLE = Path(__file__).resolve().parents[2] / "examples" / "sample_market.json"


def test_version(capsys: pytest.CaptureFixture[str]):
    assert main(["version"]) == 0
    assert capsys.readouterr().out.strip() == __version__


def test_describe_lists_seven_systems(capsys: pytest.CaptureFixture[str]):
    assert main(["describe"]) == 0
    out = capsys.readouterr().out
    assert "seven systems" in out
    # Name every system and number every method step, rather than counting lines:
    # `describe` prints ~15 of them, so a ">= 7" bound tolerated dropping several.
    for kind in SystemKind:
        assert kind.value in out, f"describe omits {kind.value}"
    for summary in _SYSTEM_SUMMARY.values():
        assert summary in out
    for index, step in enumerate(_METHOD_STEPS, start=1):
        assert f"{index}. {step}" in out


def test_no_command_prints_help(capsys: pytest.CaptureFixture[str]):
    assert main([]) == 1
    assert "usage" in capsys.readouterr().out.lower()


def test_diagnose_text(capsys: pytest.CaptureFixture[str]):
    assert main(["diagnose", str(SAMPLE)]) == 0
    assert "Structural Diagnosis" in capsys.readouterr().out


def test_diagnose_json_is_valid(capsys: pytest.CaptureFixture[str]):
    assert main(["diagnose", str(SAMPLE), "--format", "json"]) == 0
    captured = capsys.readouterr()
    # stdout must remain pure JSON; the disclaimer goes to stderr.
    payload = json.loads(captured.out)
    assert "overall_index" in payload
    assert "illustrative" in captured.err.lower()


def test_disclaimer_printed_to_stderr(capsys: pytest.CaptureFixture[str]):
    for argv in (
        ["diagnose", str(SAMPLE)],
        ["simulate", str(SAMPLE), "--target", "circulatory"],
        ["stress-test", str(SAMPLE)],
        ["describe"],
    ):
        assert main(argv) == 0
        err = capsys.readouterr().err.lower()
        assert "not financial advice" in err
        assert "not a diagnosis or forecast" in err


def test_diagnose_markdown(capsys: pytest.CaptureFixture[str]):
    assert main(["diagnose", str(SAMPLE), "--format", "md"]) == 0
    assert capsys.readouterr().out.startswith("# AMF Structural Diagnosis")


def test_simulate(capsys: pytest.CaptureFixture[str]):
    assert main(["simulate", str(SAMPLE), "--target", "circulatory", "--magnitude", "0.8"]) == 0
    assert "Shock Propagation" in capsys.readouterr().out


def test_simulate_json_is_valid(capsys: pytest.CaptureFixture[str]):
    assert main(["simulate", str(SAMPLE), "--target", "circulatory", "--format", "json"]) == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["converged"] is True
    assert payload["shocks"][0]["target"] == "circulatory"
    assert "illustrative" in captured.err.lower()


def test_simulate_markdown(capsys: pytest.CaptureFixture[str]):
    assert main(["simulate", str(SAMPLE), "--target", "circulatory", "--format", "md"]) == 0
    assert capsys.readouterr().out.startswith("# AMF Shock Propagation")


def test_diagnose_json_matches_the_engine(capsys: pytest.CaptureFixture[str]):
    # Ties the CLI's output to the engine, rather than only checking it parses.
    assert main(["diagnose", str(SAMPLE), "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    market = Market.from_dict(json.loads(SAMPLE.read_text(encoding="utf-8")))
    assert payload == DiagnosticEngine().diagnose(market).to_dict()


def test_version_does_not_print_the_disclaimer(capsys: pytest.CaptureFixture[str]):
    # The negative case for test_disclaimer_printed_to_stderr: `version` is not
    # an analytical command, so it stays silent on stderr.
    assert main(["version"]) == 0
    assert capsys.readouterr().err == ""


def test_invalid_target_exits_with_a_usage_error(capsys: pytest.CaptureFixture[str]):
    # argparse raises SystemExit for a bad choice; main never sees it, so this
    # path returns no exit code of its own.
    with pytest.raises(SystemExit) as exc:
        main(["simulate", str(SAMPLE), "--target", "bogus"])
    assert exc.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


def test_missing_required_argument_exits_with_a_usage_error():
    with pytest.raises(SystemExit) as exc:
        main(["diagnose"])
    assert exc.value.code == 2


def test_stress_test(capsys: pytest.CaptureFixture[str]):
    assert main(["stress-test", str(SAMPLE)]) == 0
    assert "stress test" in capsys.readouterr().out.lower()


def test_stress_test_json_is_valid(capsys: pytest.CaptureFixture[str]):
    assert main(["stress-test", str(SAMPLE), "--format", "json"]) == 0
    captured = capsys.readouterr()
    # stdout must remain pure JSON; the disclaimer goes to stderr.
    payload = json.loads(captured.out)
    assert payload  # one entry per shocked system
    assert "illustrative" in captured.err.lower()


def test_stress_test_markdown(capsys: pytest.CaptureFixture[str]):
    assert main(["stress-test", str(SAMPLE), "--format", "md"]) == 0
    assert capsys.readouterr().out.startswith("# AMF Systemic Stress Test")


def test_missing_file_returns_error_code(capsys: pytest.CaptureFixture[str]):
    assert main(["diagnose", "does-not-exist.json"]) == 2
    assert "error:" in capsys.readouterr().err


def test_invalid_json_returns_error_code(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    bad = tmp_path / "bad.json"
    bad.write_text("{ not json", encoding="utf-8")
    assert main(["diagnose", str(bad)]) == 2
    assert "invalid JSON" in capsys.readouterr().err


def test_non_numeric_metric_returns_error_code(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    # Schema-shaped but with a non-numeric metric: this must be a handled error with
    # exit code 2, not an unhandled ValueError traceback out of the CLI.
    data = json.loads(SAMPLE.read_text(encoding="utf-8"))
    data["systems"]["skeleton"]["integrity"] = "abc"
    bad = tmp_path / "bad_metric.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    assert main(["diagnose", str(bad)]) == 2
    assert "error:" in capsys.readouterr().err


def test_simulate_bad_magnitude_returns_error_code(capsys: pytest.CaptureFixture[str]):
    assert main(["simulate", str(SAMPLE), "--target", "skeleton", "--magnitude", "5"]) == 2
    assert "magnitude" in capsys.readouterr().err


def test_simulate_requires_target():
    # --target is required; argparse rejects its absence with exit code 2.
    with pytest.raises(SystemExit) as exc:
        main(["simulate", str(SAMPLE)])
    assert exc.value.code == 2


def test_simulate_rejects_unknown_target():
    # --target is constrained to the seven system kinds.
    with pytest.raises(SystemExit) as exc:
        main(["simulate", str(SAMPLE), "--target", "bogus"])
    assert exc.value.code == 2


def test_rejects_unknown_format():
    # --format is constrained to text/json/md.
    with pytest.raises(SystemExit) as exc:
        main(["diagnose", str(SAMPLE), "--format", "xml"])
    assert exc.value.code == 2


def test_diagnose_requires_market_path():
    # The positional market path is required.
    with pytest.raises(SystemExit) as exc:
        main(["diagnose"])
    assert exc.value.code == 2


def test_sample_market_round_trip_preserves_all_dependency_kinds():
    market = Market.from_dict(json.loads(SAMPLE.read_text(encoding="utf-8")))
    market.require_complete()
    assert len(market.systems) == 7

    expected = Counter(
        {
            DependencyKind.STRUCTURAL: 3,
            DependencyKind.INFORMATIONAL: 2,
            DependencyKind.CAPITAL: 2,
            DependencyKind.REGULATORY: 1,
        }
    )
    assert Counter(d.kind for d in market.graph.dependencies()) == expected

    # The shipped sample survives a full export/import cycle unchanged.
    restored = Market.from_dict(market.to_dict())
    assert restored.graph.dependencies() == market.graph.dependencies()
    assert Counter(d.kind for d in restored.graph.dependencies()) == expected
