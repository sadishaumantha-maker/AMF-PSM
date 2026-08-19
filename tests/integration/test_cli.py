"""Integration tests driving the CLI end to end via ``main``."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from amf import __version__
from amf.cli import _load_market, main
from amf.errors import MarketParseError
from amf.market import Market

SAMPLE = Path(__file__).resolve().parents[2] / "examples" / "sample_market.json"


def test_version(capsys: pytest.CaptureFixture[str]):
    assert main(["version"]) == 0
    assert capsys.readouterr().out.strip() == __version__


def test_describe_lists_seven_systems(capsys: pytest.CaptureFixture[str]):
    assert main(["describe"]) == 0
    out = capsys.readouterr().out
    assert "seven systems" in out
    assert out.count("\n") >= 7


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


def test_missing_file_raises_typed_parse_error():
    # _load_market wraps I/O failures in MarketParseError, not a bare AMFError.
    with pytest.raises(MarketParseError):
        _load_market(Path("does-not-exist.json"))


def test_invalid_json_raises_typed_parse_error(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text("{ not json", encoding="utf-8")
    with pytest.raises(MarketParseError):
        _load_market(bad)


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


def test_sample_market_is_loadable():
    market = Market.from_dict(json.loads(SAMPLE.read_text(encoding="utf-8")))
    market.require_complete()
