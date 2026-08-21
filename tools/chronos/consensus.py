"""Marzullo interval intersection over independent time sources.

Averaging offsets is the wrong thing to do. One misconfigured server drags the mean, and the
result carries no statement about how wrong it might be. NTP instead treats each source as
asserting a closed interval that must contain the true offset, and looks for the interval
the largest number of sources agree on. Sources whose interval misses that consensus are
*falsetickers* and are discarded rather than averaged in.

What comes out is not an estimate with a confidence level attached after the fact. It is an
interval that every surviving source vouches for, so its half-width is a bound that can be
compared against a budget and acted on.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from tools.chronos.errors import NoConsensusError

if TYPE_CHECKING:
    from collections.abc import Sequence

    from tools.chronos.sources import Sample

_LOWER = -1
"""Endpoint type marker for the start of a correctness interval."""

_UPPER = 1
"""Endpoint type marker for the end of a correctness interval."""


@dataclass(frozen=True, slots=True)
class Consensus:
    """The agreed interval and who agreed on it.

    Attributes:
        low: Lower bound of the intersection, in seconds.
        high: Upper bound of the intersection, in seconds.
        truechimers: Names of the sources whose intervals contain the intersection.
        falsetickers: Names of the sources discarded as disagreeing.
    """

    low: float
    high: float
    truechimers: tuple[str, ...] = ()
    falsetickers: tuple[str, ...] = field(default=())

    @property
    def offset(self) -> float:
        """Return the midpoint of the agreed interval, in seconds."""
        return (self.low + self.high) / 2.0

    @property
    def uncertainty(self) -> float:
        """Return the half-width of the agreed interval, in seconds.

        This is the proven bound: the true offset lies within ``offset ± uncertainty``
        unless more than the tolerated number of sources are lying in the same direction.
        """
        return (self.high - self.low) / 2.0

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-ready mapping."""
        return {
            "offset_seconds": self.offset,
            "uncertainty_seconds": self.uncertainty,
            "low_seconds": self.low,
            "high_seconds": self.high,
            "truechimers": list(self.truechimers),
            "falsetickers": list(self.falsetickers),
            "method": "marzullo",
        }


def intersect(samples: Sequence[Sample], *, minimum: int = 3) -> Consensus:
    """Find the interval the largest number of sources agree on.

    Args:
        samples: Independent measurements. Order does not affect the result.
        minimum: How many agreeing sources are required. Three is the smallest number that
            lets one falseticker be outvoted rather than merely noticed, which is why NTP
            treats it as the floor for a trustworthy answer.

    Returns:
        The agreed interval, with the sources sorted into truechimers and falsetickers.

    Raises:
        NoConsensusError: If fewer than ``minimum`` sources overlap anywhere.
    """
    if not samples:
        raise NoConsensusError("no samples were collected")

    endpoints: list[tuple[float, int]] = []
    for sample in samples:
        low, high = sample.interval
        endpoints.append((low, _LOWER))
        endpoints.append((high, _UPPER))
    # Sort by position, and at equal positions place lower bounds first so that intervals
    # meeting exactly at a point still count as overlapping.
    endpoints.sort(key=lambda item: (item[0], item[1]))

    best = 0
    count = 0
    low = high = 0.0
    for index, (position, kind) in enumerate(endpoints):
        count -= kind
        if count > best and index + 1 < len(endpoints):
            best = count
            low = position
            high = endpoints[index + 1][0]

    if best < minimum:
        raise NoConsensusError(f"only {best} of {len(samples)} source(s) agree on any interval; {minimum} are required")

    midpoint = (low + high) / 2.0
    truechimers = tuple(sorted(s.source for s in samples if s.interval[0] <= midpoint <= s.interval[1]))
    falsetickers = tuple(sorted(s.source for s in samples if not s.interval[0] <= midpoint <= s.interval[1]))
    return Consensus(low=low, high=high, truechimers=truechimers, falsetickers=falsetickers)
