"""In-process tests of the chronos command line and its exit-code contract."""

from __future__ import annotations

import json

import pytest
from chronos_fakes import Broken, Fixed, agreeing
from tools.chronos import cli, locale_gate
from tools.chronos.sources import ChronySource, LocalClockSource, NtpSource, PpsSource, PtpSource


@pytest.fixture
def offline(monkeypatch):
    """Replace the real source set with three agreeing fakes; nothing touches the network."""

    def fake_build(_servers, **_kwargs):
        return agreeing()

    monkeypatch.setattr(cli, "build_sources", fake_build)


@pytest.fixture
def unreachable(monkeypatch):
    monkeypatch.setattr(cli, "build_sources", lambda _servers, **_kwargs: [Broken("a"), Broken("b")])


def run(capsys, *args):
    code = cli.main(list(args))
    return code, capsys.readouterr().out


def test_verified_exits_zero(offline, capsys):
    code, out = run(capsys, "attest")
    assert code == cli.EXIT_VERIFIED
    assert "VERIFIED" in out


def test_unverified_exits_three_not_one(unreachable, capsys):
    """Distinct from a tool failure, so a caller can tell the two apart."""
    code, _ = run(capsys, "attest")
    assert code == cli.EXIT_UNVERIFIED


def test_a_locale_gate_failure_exits_four(offline, capsys, monkeypatch):
    monkeypatch.setattr(locale_gate, "UTC_OFFSET_MINUTES", 0)
    code, out = run(capsys, "attest")
    assert code == cli.EXIT_FAILED
    assert "FAILED" in out


@pytest.mark.parametrize("bad", ["0", "-5"])
def test_a_non_positive_budget_is_a_usage_error(offline, capsys, bad):
    code, out = run(capsys, "attest", "--budget-ms", bad)
    assert code == cli.EXIT_USAGE
    assert "budget" in out


def test_a_zero_minimum_is_a_usage_error(offline, capsys):
    code, out = run(capsys, "attest", "--min-sources", "0")
    assert code == cli.EXIT_USAGE
    assert "min-sources" in out


def test_a_tight_budget_downgrades_a_wide_measurement(monkeypatch, capsys):
    monkeypatch.setattr(cli, "build_sources", lambda _s, **_k: agreeing(error=0.5))
    assert run(capsys, "attest", "--budget-ms", "1")[0] == cli.EXIT_UNVERIFIED


def test_relaxing_the_minimum_lets_a_single_source_verify(monkeypatch, capsys):
    monkeypatch.setattr(cli, "build_sources", lambda _s, **_k: [Fixed("solo", 0.0, 0.001)])
    assert run(capsys, "attest", "--min-sources", "1")[0] == cli.EXIT_VERIFIED


def test_check_is_silent_in_text_mode(offline, capsys):
    code, out = run(capsys, "check")
    assert code == cli.EXIT_VERIFIED
    assert out == ""


def test_check_still_emits_json_when_asked(offline, capsys):
    _, out = run(capsys, "check", "--format", "json")
    assert json.loads(out)["status"] == "VERIFIED"


def test_now_prints_a_single_line(offline, capsys):
    _, out = run(capsys, "now")
    assert len(out.strip().splitlines()) == 1
    assert "+05:30" in out


def test_attest_reports_the_agreeing_sources(offline, capsys):
    _, out = run(capsys, "attest")
    assert "agreed by" in out


def test_a_falseticker_is_named_in_the_report(monkeypatch, capsys):
    monkeypatch.setattr(cli, "build_sources", lambda _s, **_k: [*agreeing(), Fixed("liar", 99.0, 0.001)])
    _, out = run(capsys, "attest")
    assert "rejected" in out
    assert "liar" in out


def test_unreachable_sources_are_listed(unreachable, capsys):
    _, out = run(capsys, "attest")
    assert out.count("unreachable") == 2


def test_out_writes_canonical_json(offline, tmp_path, capsys):
    target = tmp_path / "nested" / "attestation.json"
    run(capsys, "attest", "--out", str(target))
    assert json.loads(target.read_text(encoding="utf-8"))["status"] == "VERIFIED"


def test_json_output_is_parseable(offline, capsys):
    _, out = run(capsys, "attest", "--format", "json")
    payload = json.loads(out)
    assert payload["locale"]["timezone"] == "Asia/Colombo"
    assert payload["uncertainty_seconds"] is not None


# --- source assembly ----------------------------------------------------------------


def test_the_default_source_set_spans_every_kind():
    sources = cli.build_sources(["a", "b"])
    kinds = {type(s) for s in sources}
    assert {NtpSource, ChronySource, PpsSource, PtpSource, LocalClockSource} == kinds


def test_hardware_sources_are_listed_so_their_absence_is_visible():
    """Omitting them silently would hide the only paths to sub-microsecond accuracy."""
    names = [s.name for s in cli.build_sources([])]
    assert "gnss-pps" in names
    assert "ptp" in names


def test_optional_sources_can_be_switched_off():
    names = [s.name for s in cli.build_sources(["a"], use_chrony=False, use_hardware=False)]
    assert names == ["a", "local-clock"]
