"""The attestation record and its VERIFIED / UNVERIFIED / FAILED verdict."""

from __future__ import annotations

import json

import pytest
from chronos_fakes import Broken, Fixed, agreeing
from tools.chronos import locale_gate
from tools.chronos.attest import SCHEMA, Status, attest, significant_digits

# --- verdicts -----------------------------------------------------------------------


def test_three_agreeing_sources_inside_budget_are_verified():
    result = attest(agreeing(), budget_seconds=0.050)
    assert result.status is Status.VERIFIED
    assert result.reason == ""


def test_a_bound_wider_than_the_budget_is_unverified():
    result = attest(agreeing(error=1.0), budget_seconds=0.050)
    assert result.status is Status.UNVERIFIED
    assert "exceeds" in result.reason


def test_too_few_sources_is_unverified():
    result = attest([Fixed("only", 0.0, 0.001)])
    assert result.status is Status.UNVERIFIED
    assert "required" in result.reason


def test_no_reachable_source_is_unverified_not_silently_accepted():
    """This is the state inside a sandbox with no egress; it must never look like success."""
    result = attest([Broken("a"), Broken("b"), Broken("c")])
    assert result.status is Status.UNVERIFIED
    assert set(result.unreachable) == {"a", "b", "c"}


def test_a_locale_gate_failure_fails_the_whole_attestation(monkeypatch):
    """A wrong offset makes every rendered timestamp wrong, so measuring is pointless."""
    monkeypatch.setattr(locale_gate, "UTC_OFFSET_MINUTES", 0)
    result = attest(agreeing())
    assert result.status is Status.FAILED
    assert "gated to" in result.reason


def test_a_failed_attestation_still_records_a_time(monkeypatch):
    """Silence after the fact is indistinguishable from success; always leave a record."""
    monkeypatch.setattr(locale_gate, "UTC_OFFSET_MINUTES", 0)
    result = attest(agreeing())
    assert result.realtime_ns > 0
    assert result.monotonic_ns > 0


def test_an_unreachable_source_does_not_prevent_consensus_among_the_rest():
    result = attest([*agreeing(), Broken("dead")])
    assert result.status is Status.VERIFIED
    assert "dead" in result.unreachable


def test_a_falseticker_is_recorded_as_rejected():
    result = attest([*agreeing(), Fixed("liar", 100.0, 0.001)])
    assert result.status is Status.VERIFIED
    assert result.consensus.falsetickers == ("liar",)


# --- the record ---------------------------------------------------------------------


def test_true_time_applies_the_measured_offset():
    result = attest(agreeing(offset=2.0, error=0.001), budget_seconds=1.0)
    assert result.true_time_ns - result.realtime_ns == pytest.approx(2e9, rel=1e-6)


def test_true_time_falls_back_to_the_raw_clock_when_nothing_was_established():
    result = attest([Broken("a")])
    assert result.true_time_ns == result.realtime_ns
    assert result.uncertainty_seconds is None


def test_monotonic_is_recorded_so_a_reader_can_detect_a_stepped_clock():
    assert attest(agreeing()).monotonic_ns > 0


def test_local_time_is_rendered_in_the_gated_zone():
    assert attest(agreeing()).local().utcoffset().total_seconds() == 330 * 60


def test_the_record_carries_the_schema_and_the_locale_gate():
    payload = attest(agreeing()).to_dict()
    assert payload["schema"] == SCHEMA
    assert payload["locale"]["location"] == "Ratnapura, Sri Lanka"
    assert payload["locale"]["utc_offset_minutes"] == 330


def test_every_sample_is_recorded_including_rejected_ones():
    payload = attest([*agreeing(), Fixed("liar", 100.0, 0.001)]).to_dict()
    assert [s["source"] for s in payload["samples"]] == ["liar", "s0", "s1", "s2"]


def test_json_is_canonical_and_parseable():
    text = attest(agreeing()).to_json()
    assert text.endswith("\n")
    assert json.loads(text)["status"] == "VERIFIED"


def test_unreachable_reasons_are_preserved_for_forensics():
    payload = attest([Broken("gnss", "needs a receiver")]).to_dict()
    assert payload["unreachable"]["gnss"] == "needs a receiver"


# --- honest precision ---------------------------------------------------------------


@pytest.mark.parametrize(
    ("uncertainty", "expected"),
    [(0.1, 2), (0.01, 3), (0.001, 4), (1.0, 1), (10.0, 0)],
)
def test_digits_track_the_measured_bound(uncertainty, expected):
    assert significant_digits(uncertainty) == expected


@pytest.mark.parametrize("bad", [0.0, -1.0, float("nan"), float("inf")])
def test_a_meaningless_bound_justifies_no_digits(bad):
    assert significant_digits(bad) == 0


def test_digits_are_capped_at_nanoseconds():
    assert significant_digits(1e-30) == 9


def test_rendering_a_verified_attestation_shows_the_bound():
    assert "±" in attest(agreeing()).render()


def test_rendering_an_unverified_attestation_shows_why_instead():
    rendered = attest([Broken("a")]).render()
    assert "UNVERIFIED" in rendered
    assert "±" not in rendered
