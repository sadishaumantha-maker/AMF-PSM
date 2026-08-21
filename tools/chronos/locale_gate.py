"""The hard-gated locale: Ratnapura, Sri Lanka.

These constants are the memory the rest of the system is not allowed to drift away from.
They are validated against the operating system's time zone database on import, and the
validation raises rather than warning: a run stamped with the wrong offset is worse than a
run that did not happen, because it looks usable.

Sri Lanka's offset has moved within living memory -- +05:30 until 1996, then +06:30, then
+06:00, then back to +05:30 on 15 April 2006 -- and the country has observed no daylight
saving since. :func:`verify_history` checks those transitions as a fingerprint of the tz
database, which catches a stub or truncated zoneinfo that would otherwise report a
plausible-looking constant offset.
"""

from __future__ import annotations

import datetime as dt
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from tools.chronos.errors import LocaleGateError

TZ_NAME = "Asia/Colombo"
"""IANA zone for all of Sri Lanka. There is only one."""

UTC_OFFSET_MINUTES = 330
"""+05:30. Fixed year-round."""

OBSERVES_DST = False
"""Sri Lanka has observed no daylight saving since the 2006 realignment."""

LOCATION = "Ratnapura, Sri Lanka"
"""The operating location this system is gated to."""

LATITUDE = 6.7056
"""Degrees north."""

LONGITUDE = 80.3847
"""Degrees east."""

_HISTORICAL_OFFSETS: tuple[tuple[dt.date, int], ...] = (
    (dt.date(1995, 1, 1), 330),
    (dt.date(1996, 6, 1), 390),
    (dt.date(1997, 1, 1), 360),
    (dt.date(2007, 1, 1), 330),
)
"""Known offsets, in minutes, used as a fingerprint of a real tz database."""


def zone() -> ZoneInfo:
    """Return the gated zone.

    Raises:
        LocaleGateError: If the system has no usable time zone database. On Windows this
            usually means the ``tzdata`` package is not installed.
    """
    try:
        return ZoneInfo(TZ_NAME)
    except ZoneInfoNotFoundError as exc:
        raise LocaleGateError(
            f"no time zone database entry for {TZ_NAME}; on Windows, install the `tzdata` package"
        ) from exc


def offset_minutes(moment: dt.datetime) -> int:
    """Return the zone's UTC offset in whole minutes at ``moment``."""
    offset = moment.astimezone(zone()).utcoffset()
    if offset is None:  # pragma: no cover - a tz-aware conversion always has an offset
        raise LocaleGateError(f"{TZ_NAME} reported no UTC offset")
    return int(offset.total_seconds() // 60)


def verify_history() -> None:
    """Check the zone's historical transitions against the recorded fingerprint.

    Raises:
        LocaleGateError: If a historical offset disagrees, which means the tz database is
            not the real Sri Lanka series and its present-day answer cannot be trusted
            either.
    """
    for day, expected in _HISTORICAL_OFFSETS:
        actual = offset_minutes(dt.datetime(day.year, day.month, day.day, 12, 0, tzinfo=dt.UTC))
        if actual != expected:
            raise LocaleGateError(
                f"{TZ_NAME} reports {actual} minutes on {day.isoformat()}, expected {expected}; "
                "the time zone database does not match the recorded history for Sri Lanka"
            )


def assert_locale(now: dt.datetime | None = None) -> None:
    """Enforce the gate.

    Args:
        now: Instant to validate against; defaults to the current time.

    Raises:
        LocaleGateError: If the present offset is not +05:30, if any daylight-saving
            transition occurs in the surrounding year, or if the historical fingerprint
            fails.
    """
    moment = now or dt.datetime.now(tz=dt.UTC)
    actual = offset_minutes(moment)
    if actual != UTC_OFFSET_MINUTES:
        raise LocaleGateError(
            f"{TZ_NAME} reports a UTC offset of {actual} minutes, but this system is gated to "
            f"{UTC_OFFSET_MINUTES} ({LOCATION})"
        )
    if not OBSERVES_DST:
        offsets = {offset_minutes(dt.datetime(moment.year, month, 15, 12, 0, tzinfo=dt.UTC)) for month in range(1, 13)}
        if offsets != {UTC_OFFSET_MINUTES}:
            raise LocaleGateError(
                f"{TZ_NAME} changes offset during {moment.year} ({sorted(offsets)} minutes), but this "
                "system is gated to a zone with no daylight saving"
            )
    verify_history()


def describe() -> dict[str, object]:
    """Return the gate's contents for embedding in an attestation."""
    return {
        "timezone": TZ_NAME,
        "utc_offset_minutes": UTC_OFFSET_MINUTES,
        "observes_dst": OBSERVES_DST,
        "location": LOCATION,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
    }
