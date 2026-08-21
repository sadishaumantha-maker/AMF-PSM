"""Value-type behaviour: severity ordering, canonical serialisation, report queries."""

from __future__ import annotations

import json

import pytest
from tools.docsync.model import DriftReport, Finding, Severity


def finding(check="a.b", severity=Severity.LOW, message="m", detail="", location="L"):
    return Finding(check=check, severity=severity, message=message, detail=detail, location=location)


@pytest.mark.parametrize(
    ("lower", "higher"),
    [(Severity.LOW, Severity.MEDIUM), (Severity.MEDIUM, Severity.HIGH), (Severity.LOW, Severity.HIGH)],
)
def test_severity_is_ordered(lower, higher):
    assert higher.at_least(lower)
    assert not lower.at_least(higher)


def test_severity_is_at_least_itself():
    assert Severity.MEDIUM.at_least(Severity.MEDIUM)


def test_empty_report_has_no_worst_severity():
    assert DriftReport().worst is None


def test_worst_reports_the_highest_present():
    report = DriftReport(findings=(finding(severity=Severity.LOW), finding(severity=Severity.HIGH)))
    assert report.worst is Severity.HIGH


def test_at_or_above_filters_by_threshold():
    report = DriftReport(
        findings=(
            finding(check="low", severity=Severity.LOW),
            finding(check="med", severity=Severity.MEDIUM),
            finding(check="high", severity=Severity.HIGH),
        )
    )
    assert [f.check for f in report.at_or_above(Severity.MEDIUM)] == ["med", "high"]
    assert len(report.at_or_above(Severity.LOW)) == 3
    assert [f.check for f in report.at_or_above(Severity.HIGH)] == ["high"]


def test_canonical_json_is_stable_under_field_insertion_order():
    """A baseline is only usable as a gate if identical content serialises identically."""
    a = DriftReport(findings=(finding(),), skipped={"z": "1", "a": "2"})
    b = DriftReport(findings=(finding(),), skipped={"a": "2", "z": "1"})
    assert a.to_json() == b.to_json()


def test_canonical_json_ends_with_a_newline():
    assert DriftReport().to_json().endswith("\n")


def test_json_round_trips():
    report = DriftReport(findings=(finding(detail="d"),), skipped={"x": "why"})
    parsed = json.loads(report.to_json())
    assert parsed["findings"][0]["check"] == "a.b"
    assert parsed["findings"][0]["severity"] == "low"
    assert parsed["skipped"] == {"x": "why"}


def test_finding_key_orders_by_check_then_location_then_message():
    findings = [
        finding(check="b", location="1"),
        finding(check="a", location="2"),
        finding(check="a", location="1", message="z"),
        finding(check="a", location="1", message="a"),
    ]
    assert [f.key for f in sorted(findings, key=lambda f: f.key)] == [
        ("a", "1", "a", ""),
        ("a", "1", "z", ""),
        ("a", "2", "m", ""),
        ("b", "1", "m", ""),
    ]


def test_detail_is_part_of_a_findings_identity():
    """An aggregated finding whose contents change must not match the baseline entry."""
    assert finding(detail="one").key != finding(detail="one, two").key


def test_findings_are_immutable():
    with pytest.raises((AttributeError, TypeError)):
        finding().check = "other"


def test_severity_serialises_as_its_string_value():
    assert finding(severity=Severity.HIGH).to_dict()["severity"] == "high"
