"""The seven anatomical systems domain model (AMF analytical Step 2).

An :class:`AnatomicalSystem` captures the *structural* state of one of the seven
systems of a market. Every metric is a dimensionless quantity in ``[0, 1]`` that
describes robustness, redundancy, load-bearing importance, or current stress.
There are no prices, volumes, or trade concepts here by design.

Convenience factories (:func:`skeleton`, :func:`circulatory`, ...) build a system
of each kind with AMF-aligned default criticality, so callers can assemble a full
market anatomy quickly.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from amf.errors import InvalidSystemError
from amf.models import SystemKind

# Default load-bearing importance (criticality) per system, reflecting how much
# the rest of the market structurally depends on it. Infrastructure and capital
# flow are the most load-bearing; participants and metabolism the least.
_DEFAULT_CRITICALITY: dict[SystemKind, float] = {
    SystemKind.SKELETON: 0.90,
    SystemKind.CIRCULATORY: 0.85,
    SystemKind.IMMUNE: 0.75,
    SystemKind.NERVOUS: 0.70,
    SystemKind.ORGANS: 0.65,
    SystemKind.MUSCULATURE: 0.60,
    SystemKind.METABOLISM: 0.60,
}

_DEFAULT_NAME: dict[SystemKind, str] = {
    SystemKind.SKELETON: "Market infrastructure",
    SystemKind.CIRCULATORY: "Capital flow",
    SystemKind.NERVOUS: "Information & signals",
    SystemKind.MUSCULATURE: "Active participants",
    SystemKind.ORGANS: "Functional subsystems",
    SystemKind.IMMUNE: "Risk management & regulation",
    SystemKind.METABOLISM: "Value creation & destruction",
}


def _check_unit(name: str, value: float) -> None:
    """Raise :class:`InvalidSystemError` if ``value`` is not in ``[0, 1]``."""
    if not 0.0 <= value <= 1.0:
        msg = f"{name} must be in [0, 1], got {value!r}"
        raise InvalidSystemError(msg)


@dataclass(slots=True)
class AnatomicalSystem:
    """One of the seven anatomical systems of a market.

    Attributes:
        kind: Which anatomical system this is.
        name: Concrete real-world counterpart (e.g. ``"NYSE + DTCC"``).
        components: Named sub-components belonging to this system.
        integrity: How intact and robust the system is now, in ``[0, 1]``.
        redundancy: Availability of fallbacks or alternatives, in ``[0, 1]``.
        criticality: How load-bearing the system is for the market, in ``[0, 1]``.
        load: Current stress level, in ``[0, 1]``.
    """

    kind: SystemKind
    name: str
    components: list[str] = field(default_factory=list)
    integrity: float = 1.0
    redundancy: float = 0.5
    criticality: float = 0.5
    load: float = 0.0

    def __post_init__(self) -> None:
        """Validate the system on construction."""
        self.validate()

    def validate(self) -> None:
        """Validate that all metrics are in range and the name is non-empty.

        Raises:
            InvalidSystemError: If any metric is out of ``[0, 1]`` or the name is
                blank.
        """
        if not self.name.strip():
            msg = "system name must not be empty"
            raise InvalidSystemError(msg)
        _check_unit("integrity", self.integrity)
        _check_unit("redundancy", self.redundancy)
        _check_unit("criticality", self.criticality)
        _check_unit("load", self.load)

    def health(self) -> float:
        """Return composite structural health in ``[0, 1]``.

        Health degrades both as intrinsic integrity falls and as current load
        rises: ``health = integrity * (1 - load)``.
        """
        return self.integrity * (1.0 - self.load)

    def absorptive_capacity(self) -> float:
        """Return the fraction of incoming stress this system dampens, in ``[0, 1]``.

        A system absorbs more stress when it has redundancy (fallbacks), high
        integrity, and spare capacity (low load). The weights below are a fixed,
        interpretable blend; they always yield a value in ``[0, 1]`` because each
        term is in ``[0, 1]`` and the weights sum to one.
        """
        return 0.5 * self.redundancy + 0.3 * self.integrity + 0.2 * (1.0 - self.load)


def _make(kind: SystemKind, name: str | None, components: list[str] | None, **metrics: float) -> AnatomicalSystem:
    """Build a system of ``kind`` with AMF-aligned defaults."""
    return AnatomicalSystem(
        kind=kind,
        name=name if name is not None else _DEFAULT_NAME[kind],
        components=list(components) if components is not None else [],
        criticality=metrics.pop("criticality", _DEFAULT_CRITICALITY[kind]),
        integrity=metrics.pop("integrity", 1.0),
        redundancy=metrics.pop("redundancy", 0.5),
        load=metrics.pop("load", 0.0),
    )


def skeleton(name: str | None = None, components: list[str] | None = None, **metrics: float) -> AnatomicalSystem:
    """Build the skeleton (market infrastructure) system."""
    return _make(SystemKind.SKELETON, name, components, **metrics)


def circulatory(name: str | None = None, components: list[str] | None = None, **metrics: float) -> AnatomicalSystem:
    """Build the circulatory (capital flow) system."""
    return _make(SystemKind.CIRCULATORY, name, components, **metrics)


def nervous(name: str | None = None, components: list[str] | None = None, **metrics: float) -> AnatomicalSystem:
    """Build the nervous (information & signals) system."""
    return _make(SystemKind.NERVOUS, name, components, **metrics)


def musculature(name: str | None = None, components: list[str] | None = None, **metrics: float) -> AnatomicalSystem:
    """Build the musculature (active participants) system."""
    return _make(SystemKind.MUSCULATURE, name, components, **metrics)


def organs(name: str | None = None, components: list[str] | None = None, **metrics: float) -> AnatomicalSystem:
    """Build the organs (functional subsystems) system."""
    return _make(SystemKind.ORGANS, name, components, **metrics)


def immune(name: str | None = None, components: list[str] | None = None, **metrics: float) -> AnatomicalSystem:
    """Build the immune (risk management & regulation) system."""
    return _make(SystemKind.IMMUNE, name, components, **metrics)


def metabolism(name: str | None = None, components: list[str] | None = None, **metrics: float) -> AnatomicalSystem:
    """Build the metabolism (value creation & destruction) system."""
    return _make(SystemKind.METABOLISM, name, components, **metrics)
