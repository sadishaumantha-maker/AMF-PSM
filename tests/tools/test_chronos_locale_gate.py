"""The hard gate: Ratnapura, Asia/Colombo, +05:30, no daylight saving."""

from __future__ import annotations

import datetime as dt

import pytest
from tools.chronos import locale_gate
from tools.chronos.errors import LocaleGateError


def test_the_recorded_constants_are_the_ones_we_are_gated_to():
    assert locale_gate.TZ_NAME == "Asia/Colombo"
    assert locale_gate.UTC_OFFSET_MINUTES == 330
    assert locale_gate.OBSERVES_DST is False
    assert locale_gate.LOCATION == "Ratnapura, Sri Lanka"


def test_the_live_zone_agrees_with_the_recorded_offset():
    assert locale_gate.offset_minutes(dt.datetime.now(tz=dt.UTC)) == 330


def test_the_gate_passes_on_this_machine():
    locale_gate.assert_locale()


@pytest.mark.parametrize("month", range(1, 13))
def test_no_month_of_the_current_year_changes_the_offset(month):
    """Sri Lanka observes no daylight saving; any transition would silently mis-stamp records."""
    moment = dt.datetime(dt.datetime.now(tz=dt.UTC).year, month, 15, 12, 0, tzinfo=dt.UTC)
    assert locale_gate.offset_minutes(moment) == 330


@pytest.mark.parametrize(
    ("year", "month", "day", "expected"),
    [(1995, 1, 1, 330), (1996, 6, 1, 390), (1997, 1, 1, 360), (2007, 1, 1, 330)],
)
def test_historical_transitions_match_the_recorded_fingerprint(year, month, day, expected):
    """+05:30 -> +06:30 -> +06:00 -> +05:30. A stub tzdata would not reproduce this."""
    assert locale_gate.offset_minutes(dt.datetime(year, month, day, 12, 0, tzinfo=dt.UTC)) == expected


def test_verify_history_passes_against_the_real_database():
    locale_gate.verify_history()


def test_a_tampered_offset_constant_is_rejected(monkeypatch):
    """The gate must fail loudly if the recorded memory is edited to disagree with reality."""
    monkeypatch.setattr(locale_gate, "UTC_OFFSET_MINUTES", 0)
    with pytest.raises(LocaleGateError, match="gated to"):
        locale_gate.assert_locale()


def test_a_wrong_timezone_name_is_rejected(monkeypatch):
    monkeypatch.setattr(locale_gate, "TZ_NAME", "Europe/London")
    with pytest.raises(LocaleGateError):
        locale_gate.assert_locale()


def test_a_missing_time_zone_database_is_reported_clearly(monkeypatch):
    monkeypatch.setattr(locale_gate, "TZ_NAME", "Not/AZone")
    with pytest.raises(LocaleGateError, match="tzdata"):
        locale_gate.zone()


def test_a_tampered_history_fingerprint_is_rejected(monkeypatch):
    monkeypatch.setattr(locale_gate, "_HISTORICAL_OFFSETS", ((dt.date(1995, 1, 1), 999),))
    with pytest.raises(LocaleGateError, match="does not match the recorded history"):
        locale_gate.verify_history()


def test_claiming_dst_is_observed_changes_nothing_because_none_occurs(monkeypatch):
    monkeypatch.setattr(locale_gate, "OBSERVES_DST", True)
    locale_gate.assert_locale()


def test_describe_carries_the_full_gate_for_the_attestation():
    described = locale_gate.describe()
    assert described["timezone"] == "Asia/Colombo"
    assert described["utc_offset_minutes"] == 330
    assert described["location"] == "Ratnapura, Sri Lanka"
    assert described["latitude"] == pytest.approx(6.7056)
    assert described["longitude"] == pytest.approx(80.3847)
