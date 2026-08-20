"""Typed failures for the time layer.

Mirrors the ``amf`` package's convention: every failure crossing this package's public
surface derives from one base, so a caller can catch the family without catching the world.
"""

from __future__ import annotations


class ChronosError(Exception):
    """Base class for every failure raised by :mod:`tools.chronos`."""


class LocaleGateError(ChronosError):
    """The hard-gated locale does not match the system's time zone database.

    Raised when the recorded constants for Ratnapura disagree with what ``zoneinfo``
    reports -- a wrong offset, an unexpected daylight-saving transition, or a missing tz
    database. Continuing past this would silently mis-stamp every subsequent record.
    """


class SourceUnavailableError(ChronosError):
    """A time source could not be reached or is not configured on this machine."""


class NoConsensusError(ChronosError):
    """No set of sources large enough to be trusted agreed on an interval."""
