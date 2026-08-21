"""Value types shared by the drift detector.

Everything here is frozen and slotted, and every type serialises through ``to_dict`` --
matching the convention the ``amf`` package itself uses for result types, so a reader moving
between the two sees one house style.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Severity(StrEnum):
    """How badly a finding misleads a reader of ``CLAUDE.md``.

    The ordering is meaningful: :meth:`at_least` compares rank, and the CLI's
    ``--fail-on`` threshold uses it.
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    @property
    def rank(self) -> int:
        """Return the severity's ordinal, lowest first."""
        return _SEVERITY_ORDER.index(self)

    def at_least(self, floor: Severity) -> bool:
        """Report whether this severity is at or above ``floor``."""
        return self.rank >= floor.rank


_SEVERITY_ORDER: tuple[Severity, ...] = (Severity.LOW, Severity.MEDIUM, Severity.HIGH)


@dataclass(frozen=True, slots=True)
class Finding:
    """One disagreement between ``CLAUDE.md`` and the repository.

    Attributes:
        check: Identifier of the check that produced this, e.g. ``cli.flags``.
        severity: How badly the disagreement misleads a reader.
        message: One-line statement of what is wrong.
        detail: Optional elaboration, such as the two values that differ.
        location: Optional ``path`` or ``path:line`` the finding anchors to.
    """

    check: str
    severity: Severity
    message: str
    detail: str = ""
    location: str = ""

    @property
    def key(self) -> tuple[str, str, str, str]:
        """Return the canonical identity of this finding.

        ``detail`` is part of the identity on purpose. Several checks aggregate -- one
        finding lists every unmentioned document, say -- so a key built from the message
        alone would let a *newly* orphaned file hide inside a finding the baseline already
        knows about.
        """
        return (self.check, self.location, self.message, self.detail)

    def to_dict(self) -> dict[str, str]:
        """Return a JSON-ready mapping of this finding."""
        return {
            "check": self.check,
            "severity": self.severity.value,
            "message": self.message,
            "detail": self.detail,
            "location": self.location,
        }


@dataclass(frozen=True, slots=True)
class DriftReport:
    """The complete result of one scan.

    Attributes:
        findings: Every disagreement found, in canonical order.
        skipped: Check identifiers that could not run, mapped to why.
    """

    findings: tuple[Finding, ...] = ()
    skipped: dict[str, str] = field(default_factory=dict)

    @property
    def worst(self) -> Severity | None:
        """Return the highest severity present, or ``None`` when clean."""
        if not self.findings:
            return None
        return max((f.severity for f in self.findings), key=lambda s: s.rank)

    def at_or_above(self, floor: Severity) -> tuple[Finding, ...]:
        """Return the findings whose severity is at or above ``floor``."""
        return tuple(f for f in self.findings if f.severity.at_least(floor))

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready mapping of the whole report."""
        return {
            "findings": [f.to_dict() for f in self.findings],
            "skipped": dict(sorted(self.skipped.items())),
        }

    def to_json(self) -> str:
        """Return canonical JSON: sorted keys, fixed separators, trailing newline.

        Canonical form is what makes a checked-in baseline diffable and a repeated scan
        byte-identical.
        """
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"
