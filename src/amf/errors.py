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
    """Raised when the dependency structure itself is unusable.

    Covers a dependency with an invalid weight or a self-loop, and a graph whose
    shape admits no well-defined answer -- notably
    :meth:`~amf.graph.DependencyGraph.centrality` on a graph with no single
    dominant mode, where the ranking cycles instead of settling.
    """


class InvalidShockError(AMFError):
    """Raised when a simulation shock has an out-of-range magnitude or bad target."""


class InvalidConfigError(AMFError):
    """Raised when an engine or algorithm parameter is outside its documented range.

    Covers :class:`~amf.diagnostics.DiagnosticConfig`,
    :class:`~amf.simulation.SimulationConfig`,
    :class:`~amf.sensitivity.SensitivityConfig`, and the tuning arguments of
    :meth:`~amf.graph.DependencyGraph.centrality`. Validating these up front keeps
    an out-of-range knob from silently producing scores outside their documented
    interval instead of failing.
    """


class MarketParseError(AMFError):
    """Raised when a market description (e.g. JSON) cannot be parsed into a model."""


class InvariantError(AMFError):
    """Raised when a computed result breaks a property the type documents.

    Every engine validates its own output before returning it (see
    :mod:`amf.invariants`), so a score outside ``[0, 1]``, a ``NaN`` that escaped
    a clip, or a severity band inconsistent with the score it was derived from
    surfaces here as a typed failure rather than flowing onward into a report.

    This is deliberately an exception and not an ``assert``: assertions are
    stripped under ``python -O``, which would silently disable the guard exactly
    where a deployment is most likely to want it.

    Attributes:
        property_name: Dotted name of the property that failed, e.g.
            ``"findings[skeleton].concentration"``.
        value: The offending value.
        lower: Inclusive lower bound of the expected interval.
        upper: Inclusive upper bound of the expected interval.
    """

    def __init__(self, property_name: str, value: float, lower: float = 0.0, upper: float = 1.0) -> None:
        """Record the failing property and the interval it escaped."""
        self.property_name = property_name
        self.value = value
        self.lower = lower
        self.upper = upper
        super().__init__(f"{property_name} = {value!r} is not in [{lower}, {upper}]")
