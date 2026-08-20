#!/usr/bin/env python3
r"""Reconcile ``.github/milestones.json`` with the repository's Milestones section.

The delivery schedule is kept as code so the Milestones section is reproducible
and reviewable rather than hand-maintained in the GitHub UI. This script is the
reconciler: it creates milestones the manifest describes but the repository does
not have, updates the ones that have drifted, and **never deletes anything** --
a milestone someone added by hand is left alone, so an accidental run cannot
destroy work.

Running it twice in a row makes no second round of changes.

Usage::

    GITHUB_TOKEN=<token with issues:write> \\
    GITHUB_REPOSITORY=owner/repo \\
    python tools/sync_milestones.py [--dry-run]

Standard library only, matching the package's zero-dependency policy.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_ROOT = "https://api.github.com"
MANIFEST = Path(__file__).resolve().parent.parent / ".github" / "milestones.json"
TIMEOUT_SECONDS = 30


def load_manifest(path: Path = MANIFEST) -> list[dict[str, Any]]:
    """Return the milestone entries declared in the manifest.

    Args:
        path: Location of the manifest file.

    Returns:
        The list under the manifest's ``milestones`` key.
    """
    document = json.loads(path.read_text(encoding="utf-8"))
    milestones: list[dict[str, Any]] = document["milestones"]
    return milestones


def plan_changes(
    existing: list[dict[str, Any]],
    desired: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[tuple[int, dict[str, Any]]]]:
    """Work out which milestones to create and which to update.

    Matching is by title, which is the manifest's stable identity for an entry.
    ``due_on`` is compared on its date only: GitHub normalises the time-of-day it
    stores, so comparing the full timestamp would report drift on every run and
    the script would never reach a fixed point.

    Args:
        existing: Milestones already present, as returned by the REST API.
        desired: Milestones declared in the manifest.

    Returns:
        A ``(to_create, to_update)`` pair, where each update is the existing
        milestone's number paired with the manifest entry.
    """
    by_title = {milestone["title"]: milestone for milestone in existing}
    to_create: list[dict[str, Any]] = []
    to_update: list[tuple[int, dict[str, Any]]] = []
    for entry in desired:
        current = by_title.get(entry["title"])
        if current is None:
            to_create.append(entry)
            continue
        drifted = (
            (current.get("description") or "").strip() != entry["description"].strip()
            or (current.get("due_on") or "")[:10] != entry["due_on"][:10]
            or current.get("state") != entry["state"]
        )
        if drifted:
            to_update.append((current["number"], entry))
    return to_create, to_update


def _request(method: str, url: str, token: str, payload: dict[str, Any] | None = None) -> Any:  # noqa: ANN401
    """Perform one authenticated GitHub REST call and return the decoded body."""
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, method=method)
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_existing(repository: str, token: str) -> list[dict[str, Any]]:
    """Return every milestone on the repository, open or closed, following pagination."""
    milestones: list[dict[str, Any]] = []
    page = 1
    while True:
        url = f"{API_ROOT}/repos/{repository}/milestones?state=all&per_page=100&page={page}"
        batch = _request("GET", url, token)
        if not batch:
            return milestones
        milestones.extend(batch)
        page += 1


def main(argv: list[str] | None = None) -> int:
    """Run the reconciliation and return a process exit code."""
    args = sys.argv[1:] if argv is None else argv
    dry_run = "--dry-run" in args

    repository = os.environ.get("GITHUB_REPOSITORY", "")
    token = os.environ.get("GITHUB_TOKEN", "")
    if not repository:
        print("error: GITHUB_REPOSITORY is not set (expected 'owner/repo')", file=sys.stderr)
        return 1
    if not token and not dry_run:
        print("error: GITHUB_TOKEN is not set; a token with issues:write is required", file=sys.stderr)
        return 1

    desired = load_manifest()
    existing = [] if dry_run and not token else fetch_existing(repository, token)
    to_create, to_update = plan_changes(existing, desired)

    print(
        f"manifest: {len(desired)} milestones | repository: {len(existing)} "
        f"| create: {len(to_create)} | update: {len(to_update)}"
    )
    if dry_run:
        for entry in to_create:
            print(f"  would create  {entry['title']}")
        for number, entry in to_update:
            print(f"  would update  #{number} {entry['title']}")
        return 0

    for entry in to_create:
        payload = {k: entry[k] for k in ("title", "state", "description", "due_on")}
        try:
            created = _request("POST", f"{API_ROOT}/repos/{repository}/milestones", token, payload)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            print(f"error: could not create {entry['title']!r}: HTTP {exc.code} {detail}", file=sys.stderr)
            return 1
        print(f"  created  #{created['number']}  {created['title']}")

    for number, entry in to_update:
        payload = {k: entry[k] for k in ("title", "state", "description", "due_on")}
        _request("PATCH", f"{API_ROOT}/repos/{repository}/milestones/{number}", token, payload)
        print(f"  updated  #{number}  {entry['title']}")

    print("milestones section is in sync with the manifest")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
