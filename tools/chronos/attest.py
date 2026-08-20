"""The attestation: what was measured, how well, and whether it may be relied on.

An attestation is always produced, even when nothing could be measured. A run that could not
establish the time still needs a record saying so -- silence is indistinguishable from
success after the fact. What varies is the :class:`Status`, and only ``VERIFIED`` authorises
downstream work.
"""

from __future__ import annotations

import datetime as dt
import json
import math
import time
from dataclasses import dataclass, field
from enum import StrEnum
from typing import TYPE_CHECKING, Any

from tools.chronos import locale_gate
from tools.chronos.consensus import Consensus, intersect
from tools.chronos.errors import ChronosError, NoConsensusError, SourceUnavailableError

if TYPE_CHECKING:
    from collections.abc import Sequence

    from tools.chronos.sources import Sample, TimeSource

SCHEMA = "amf.chronos.attestation/1"
"""Schema identifier, so a consumer can tell which shape it is reading."""

DEFAULT_BUDGET_SECONDS = 0.050
"""50 ms. Comfortably achievable over WAN NTP, and tight enough to be worth asserting."""


class Status(StrEnum):
    """Whether an attestation may be relied on."""

    VERIFIED = "VERIFIED"
    """Enough independent sources agreed, and the bound is inside the budget."""

    UNVERIFIED = "UNVERIFIED"
    """A time was recorded but not established: too few sources, or too wide a bound."""

    FAILED = "FAILED"
    """The attestation could not be produced at all, most often a locale-gate failure."""


def significant_digits(uncertainty: float) -> int:
    """Return how many decimal places an uncertainty of this size justifies.

    Printing a timestamp to microseconds when the bound is ten milliseconds invents four
    digits of precision that were never measured. This keeps the rendering honest.
    """
    if uncertainty <= 0 or not math.isfinite(uncertainty):
        return 0
    return max(0, min(9, math.ceil(-math.log10(uncertainty)) + 1))


@dataclass(frozen=True, slots=True)
class TimeAttestation:
    """A signed-off statement about this machine's clock at one instant.

    Attributes:
        status: Whether the attestation may be relied on.
        realtime_ns: The local wall clock at the moment of attestation.
        monotonic_ns: The monotonic clock at the same moment, so a later reader can tell
            whether the wall clock was stepped in between.
        samples: Every measurement gathered, including the ones discarded.
        consensus: The agreed interval, when one was reached.
        budget_seconds: The uncertainty the caller was willing to accept.
        unreachable: Sources that could not be reached, mapped to why.
        reason: Why the status is not VERIFIED, when it is not.
    """

    status: Status
    realtime_ns: int
    monotonic_ns: int
    samples: tuple[Sample, ...] = ()
    consensus: Consensus | None = None
    budget_seconds: float = DEFAULT_BUDGET_SECONDS
    unreachable: dict[str, str] = field(default_factory=dict)
    reason: str = ""

    @property
    def true_time_ns(self) -> int:
        """Return the best estimate of true time, in nanoseconds since the Unix epoch.

        Falls back to the raw local clock when no consensus was reached -- which is exactly
        why such an attestation is stamped UNVERIFIED rather than trusted.
        """
        if self.consensus is None:
            return self.realtime_ns
        return self.realtime_ns + int(self.consensus.offset * 1e9)

    @property
    def uncertainty_seconds(self) -> float | None:
        """Return the proven bound, or ``None`` when nothing was established."""
        return None if self.consensus is None else self.consensus.uncertainty

    def utc(self) -> dt.datetime:
        """Return the attested instant as an aware UTC datetime."""
        return dt.datetime.fromtimestamp(self.true_time_ns / 1e9, tz=dt.UTC)

    def local(self) -> dt.datetime:
        """Return the attested instant in the gated zone, Asia/Colombo."""
        return self.utc().astimezone(locale_gate.zone())

    def render(self) -> str:
        """Return a one-line human summary, truncated to the precision actually measured."""
        bound = self.uncertainty_seconds
        digits = significant_digits(bound) if bound is not None else 0
        stamp = self.local().isoformat(timespec="microseconds" if digits > 3 else "milliseconds")
        if bound is None:
            return f"{stamp}  [{self.status.value}: {self.reason or 'no bound established'}]"
        return f"{stamp}  ±{bound * 1000:.{max(0, digits - 3)}f} ms  [{self.status.value}]"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-ready mapping of the whole attestation."""
        return {
            "schema": SCHEMA,
            "status": self.status.value,
            "reason": self.reason,
            "locale": locale_gate.describe(),
            "clock": {
                "realtime_ns": self.realtime_ns,
                "monotonic_ns": self.monotonic_ns,
                "true_time_ns": self.true_time_ns,
                "utc": self.utc().isoformat(),
                "local": self.local().isoformat(),
            },
            "budget_seconds": self.budget_seconds,
            "uncertainty_seconds": self.uncertainty_seconds,
            "consensus": None if self.consensus is None else self.consensus.to_dict(),
            "samples": [
                {
                    "source": s.source,
                    "offset_seconds": s.offset,
                    "delay_seconds": s.delay,
                    "error_seconds": s.error,
                    "stratum": s.stratum,
                }
                for s in sorted(self.samples, key=lambda s: s.source)
            ],
            "unreachable": dict(sorted(self.unreachable.items())),
        }

    def to_json(self) -> str:
        """Return canonical JSON with a trailing newline."""
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


def attest(
    sources: Sequence[TimeSource],
    *,
    budget_seconds: float = DEFAULT_BUDGET_SECONDS,
    minimum_sources: int = 3,
) -> TimeAttestation:
    """Measure the clock against every source and decide whether the result may be relied on.

    The locale gate is enforced first. If the machine's notion of Asia/Colombo is wrong there
    is no point measuring anything, because every rendered timestamp would be wrong in a way
    no amount of clock accuracy would fix.

    Args:
        sources: Sources to query, in any order.
        budget_seconds: The widest uncertainty that still counts as verified.
        minimum_sources: How many independent sources must agree.

    Returns:
        An attestation. Never raises for a measurement failure -- the failure is the result.
    """
    monotonic_ns = time.monotonic_ns()
    realtime_ns = time.time_ns()

    try:
        locale_gate.assert_locale()
    except ChronosError as exc:
        return TimeAttestation(
            status=Status.FAILED,
            realtime_ns=realtime_ns,
            monotonic_ns=monotonic_ns,
            budget_seconds=budget_seconds,
            reason=str(exc),
        )

    samples: list[Sample] = []
    unreachable: dict[str, str] = {}
    for source in sources:
        try:
            samples.append(source.sample())
        except SourceUnavailableError as exc:
            unreachable[source.name] = str(exc)

    consensus: Consensus | None = None
    reason = ""
    try:
        consensus = intersect(samples, minimum=minimum_sources)
    except NoConsensusError as exc:
        reason = str(exc)

    if consensus is None:
        status = Status.UNVERIFIED
    elif consensus.uncertainty > budget_seconds:
        status = Status.UNVERIFIED
        reason = (
            f"uncertainty ±{consensus.uncertainty * 1000:.3f} ms exceeds the ±{budget_seconds * 1000:.3f} ms budget"
        )
    else:
        status = Status.VERIFIED

    return TimeAttestation(
        status=status,
        realtime_ns=realtime_ns,
        monotonic_ns=monotonic_ns,
        samples=tuple(samples),
        consensus=consensus,
        budget_seconds=budget_seconds,
        unreachable=unreachable,
        reason=reason,
    )
