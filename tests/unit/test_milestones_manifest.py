"""Offline validation of the delivery-milestone manifest and its reconciler.

The manifest drives what appears in the repository's Milestones section, so a
malformed entry would be discovered only after it had been pushed to GitHub.
These tests check it here instead. Nothing touches the network.
"""

from __future__ import annotations

import datetime
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / ".github" / "milestones.json"
SCRIPT_PATH = ROOT / "tools" / "sync_milestones.py"

EXPECTED_DAYS = 20


def _load_script():
    """Import tools/sync_milestones.py by path; it is a script, not a package module."""
    spec = importlib.util.spec_from_file_location("sync_milestones", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def milestones(manifest) -> list[dict]:
    return manifest["milestones"]


def test_manifest_declares_one_milestone_per_working_day(milestones):
    assert len(milestones) == EXPECTED_DAYS


def test_titles_are_unique_and_day_numbered_in_order(milestones):
    titles = [m["title"] for m in milestones]
    assert len(set(titles)) == len(titles)
    for index, title in enumerate(titles, start=1):
        assert title.startswith(f"D{index:02d} - "), title


def test_due_dates_are_strictly_ascending_working_days(milestones):
    previous = None
    for entry in milestones:
        due = datetime.datetime.strptime(entry["due_on"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.UTC)
        # Saturday is 5, Sunday is 6: the programme is scheduled on working days.
        assert due.weekday() < 5, f"{entry['title']} falls on a weekend"
        if previous is not None:
            assert due > previous, f"{entry['title']} does not follow its predecessor"
        previous = due


def test_window_matches_the_first_and_last_milestone(manifest, milestones):
    assert manifest["window"]["day_one"] == milestones[0]["due_on"][:10]
    assert manifest["window"]["day_twenty"] == milestones[-1]["due_on"][:10]


def test_every_milestone_carries_tasks_acceptance_and_the_guardrails(milestones):
    for entry in milestones:
        body = entry["description"]
        assert "**Tasks**" in body, entry["title"]
        assert "**Acceptance criteria**" in body, entry["title"]
        # The guardrails travel with each milestone so a reader of one page in the
        # Milestones section cannot miss the constraints the work inherits.
        assert "Guardrails inherited from CLAUDE.md" in body, entry["title"]
        assert "- [ ] " in body, entry["title"]


def test_every_milestone_starts_open(milestones):
    assert {entry["state"] for entry in milestones} == {"open"}


def test_no_milestone_description_uses_trading_vocabulary(milestones):
    # The non-trading boundary constrains the package's names; the delivery plan
    # published alongside it should not undercut that in prose either.
    forbidden = ("buy ", "sell ", " pnl", "backtest", "ticker", "portfolio", "candlestick")
    for entry in milestones:
        lowered = f"{entry['title']} {entry['description']}".lower()
        for term in forbidden:
            assert term not in lowered, f"{entry['title']} mentions {term!r}"


def test_reconciler_creates_everything_against_an_empty_repository():
    module = _load_script()
    desired = module.load_manifest()
    to_create, to_update = module.plan_changes([], desired)
    assert len(to_create) == EXPECTED_DAYS
    assert to_update == []


def test_reconciler_is_idempotent_once_the_section_matches():
    # Second run must be a no-op, including when GitHub has normalised the
    # time-of-day it stores against each due date.
    module = _load_script()
    desired = module.load_manifest()
    existing = [
        {
            "number": index,
            "title": entry["title"],
            "description": entry["description"],
            "due_on": f"{entry['due_on'][:10]}T07:00:00Z",
            "state": entry["state"],
        }
        for index, entry in enumerate(desired, start=1)
    ]
    to_create, to_update = module.plan_changes(existing, desired)
    assert to_create == []
    assert to_update == []


@pytest.mark.parametrize(
    ("field", "value"),
    [("description", "stale text"), ("due_on", "2020-01-01T12:00:00Z"), ("state", "closed")],
)
def test_reconciler_updates_a_drifted_milestone(field, value):
    module = _load_script()
    desired = module.load_manifest()
    existing = [
        {
            "number": 7,
            "title": desired[0]["title"],
            "description": desired[0]["description"],
            "due_on": desired[0]["due_on"],
            "state": desired[0]["state"],
        }
    ]
    existing[0][field] = value
    to_create, to_update = module.plan_changes(existing, desired[:1])
    assert to_create == []
    assert to_update == [(7, desired[0])]


def test_reconciler_never_plans_a_deletion():
    # A milestone somebody added by hand must survive a sync untouched: the
    # planner has no delete channel at all, by design.
    module = _load_script()
    desired = module.load_manifest()
    handmade = {"number": 99, "title": "Ad-hoc milestone", "description": "", "due_on": None, "state": "open"}
    to_create, to_update = module.plan_changes([handmade], desired)
    assert all(entry["title"] != "Ad-hoc milestone" for entry in to_create)
    assert all(number != 99 for number, _ in to_update)
