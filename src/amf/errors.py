"""Typed exception hierarchy for the :mod:`amf` package.

All errors raised by the public API derive from :class:`AMFError`, so callers can
catch the whole family with a single ``except`` clause while still being able to
distinguish specific failure modes.
"""

from __future__ import annotations


class AMFError(Exception):
    """Base class for every error raised by the :mod:`amf` package."""


class InvalidSystemError(AMFError):
    """Raised when an :class:`~amf.systems.AnatomicalSystem` holds invalid state.

    For example, a structural metric outside the unit interval ``[0, 1]`` or an
    empty system name.
    """


class IncompleteMarketError(AMFError):
    """Raised when a :class:`~amf.market.Market` is missing one of the 7 systems.

    A complete market anatomy requires exactly one system of every
    :class:`~amf.models.SystemKind`.
    """


class InvalidDependencyError(AMFError):
    """Raised when a dependency references unknown systems or an invalid weight."""


class InvalidShockError(AMFError):
    """Raised when a simulation shock has an out-of-range magnitude or bad target."""


class MarketParseError(AMFError):
    """Raised when a market description (e.g. JSON) cannot be parsed into a model."""
