"""The :class:`Market` aggregate root that ties the AMF model together.

A market is a :class:`~amf.models.MarketBoundary`, exactly one
:class:`~amf.systems.AnatomicalSystem` of each of the seven kinds, and a
:class:`~amf.graph.DependencyGraph` describing how they couple. The
:meth:`Market.from_dict` / :meth:`Market.to_dict` pair defines the JSON schema
consumed by the command-line interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from amf.errors import AMFError, IncompleteMarketError, MarketParseError
from amf.graph import DependencyGraph
from amf.models import Dependency, DependencyKind, MarketBoundary, SystemKind
from amf.systems import SYSTEM_FACTORIES

if TYPE_CHECKING:
    from collections.abc import Iterable

    from amf.systems import AnatomicalSystem

# Metric fields a system entry may carry; everything else is a name, components,
# or an error.
_SYSTEM_METRICS = ("integrity", "redundancy", "criticality", "load")


@dataclass(slots=True)
class Market:
    """A complete market anatomy: a boundary, seven systems, and their couplings.

    Attributes:
        boundary: The scope of the market under analysis.
        systems: Exactly one system per :class:`~amf.models.SystemKind`.
        graph: The dependency graph coupling the systems.
    """

    boundary: MarketBoundary
    systems: dict[SystemKind, AnatomicalSystem]
    graph: DependencyGraph

    @classmethod
    def assemble(
        cls,
        boundary: MarketBoundary,
        systems: Iterable[AnatomicalSystem],
        dependencies: Iterable[Dependency] = (),
    ) -> Market:
        """Assemble and validate a market from its parts.

        Args:
            boundary: The market boundary.
            systems: The anatomical systems (must cover all seven kinds exactly once).
            dependencies: The couplings between systems.

        Returns:
            A validated :class:`Market`.

        Raises:
            IncompleteMarketError: If a kind is missing or duplicated.
        """
        mapping: dict[SystemKind, AnatomicalSystem] = {}
        for system in systems:
            if system.kind in mapping:
                msg = f"duplicate system for kind {system.kind}"
                raise IncompleteMarketError(msg)
            mapping[system.kind] = system
        # Store in SystemKind declaration order, not the order the caller happened
        # to supply. Everything that iterates ``systems`` -- ``to_dict``, the
        # diagnostic engine's per-system maps, the tie-break between equally
        # weak systems -- then reads the same canonical order, so two markets
        # that compare equal also render and rank identically.
        ordered = {kind: mapping[kind] for kind in SystemKind if kind in mapping}
        market = cls(boundary=boundary, systems=ordered, graph=DependencyGraph(dependencies))
        market.require_complete()
        return market

    def require_complete(self) -> None:
        """Ensure all seven systems are present and filed under their own kind.

        Raises:
            IncompleteMarketError: If any :class:`~amf.models.SystemKind` is absent,
                or a system is stored under a key that is not its own ``kind``.
        """
        missing = [k.value for k in SystemKind if k not in self.systems]
        if missing:
            msg = f"market is missing systems: {', '.join(missing)}"
            raise IncompleteMarketError(msg)
        # ``systems`` is a plain mutable dict, so a caller can file a system under
        # the wrong key after assembly. Every engine trusts the key for a
        # finding's label and the value for its metrics, so a mismatch would
        # silently attribute one system's weaknesses to another.
        mismatched = [
            f"{k.value} holds a {self.systems[k].kind.value} system"
            for k in SystemKind
            if self.systems[k].kind is not k
        ]
        if mismatched:
            msg = f"market has misfiled systems: {', '.join(mismatched)}"
            raise IncompleteMarketError(msg)

    def system(self, kind: SystemKind) -> AnatomicalSystem:
        """Return the system of the given kind.

        Raises:
            IncompleteMarketError: If the kind is not present.
        """
        try:
            return self.systems[kind]
        except KeyError as exc:
            msg = f"market has no {kind} system"
            raise IncompleteMarketError(msg) from exc

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable representation of the market.

        Systems are emitted in :class:`~amf.models.SystemKind` declaration order
        and dependencies in the graph's canonical order, so the rendered JSON
        depends only on the market's content, never on how it was built.
        """
        return {
            "boundary": self.boundary.to_dict(),
            "systems": {kind.value: _system_to_dict(self.systems[kind]) for kind in SystemKind if kind in self.systems},
            "dependencies": [dependency.to_dict() for dependency in self.graph.dependencies()],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Market:
        """Build a market from a parsed JSON mapping.

        Args:
            data: A mapping with ``boundary``, ``systems``, and ``dependencies`` keys.

        Returns:
            A validated :class:`Market`.

        Raises:
            MarketParseError: If the structure or any value is malformed.
        """
        try:
            boundary = _parse_boundary(data["boundary"])
            systems = [_parse_system(name, body) for name, body in data["systems"].items()]
            dependencies = [_parse_dependency(item) for item in data.get("dependencies", [])]
            return cls.assemble(boundary, systems, dependencies)
        except MarketParseError:
            raise
        except (KeyError, TypeError, AttributeError, ValueError) as exc:
            # ValueError covers non-numeric metrics and weights (``float("abc")``),
            # which would otherwise escape the documented MarketParseError contract.
            msg = f"malformed market description: {exc}"
            raise MarketParseError(msg) from exc
        except AMFError as exc:
            # Domain validation failed: an out-of-range metric, a bad dependency, or
            # a missing/duplicated system. Surface it as a parse error per the schema.
            raise MarketParseError(str(exc)) from exc


def _system_to_dict(system: AnatomicalSystem) -> dict[str, Any]:
    """Return a JSON-serialisable representation of one anatomical system."""
    return {
        "name": system.name,
        "components": list(system.components),
        "integrity": system.integrity,
        "redundancy": system.redundancy,
        "criticality": system.criticality,
        "load": system.load,
    }


def _parse_boundary(body: dict[str, Any]) -> MarketBoundary:
    """Parse a boundary mapping into a :class:`MarketBoundary`."""
    return MarketBoundary(
        asset_class=str(body["asset_class"]),
        geography=str(body["geography"]),
        timeframe=str(body["timeframe"]),
        notes=str(body.get("notes", "")),
    )


def _parse_kind(value: str) -> SystemKind:
    """Parse a system-kind string, raising :class:`MarketParseError` if unknown."""
    try:
        return SystemKind(value)
    except ValueError as exc:
        msg = f"unknown system kind {value!r}"
        raise MarketParseError(msg) from exc


def _parse_system(name: str, body: dict[str, Any]) -> AnatomicalSystem:
    """Parse one system entry into an :class:`AnatomicalSystem`.

    Delegates to the system factories so that a field omitted from the JSON gets
    exactly the same default as the equivalent factory call.

    Raises:
        MarketParseError: If the body carries an unrecognised field.
    """
    kind = _parse_kind(name)
    unknown = set(body) - {"name", "components", *_SYSTEM_METRICS}
    if unknown:
        msg = f"unknown field(s) for system {kind.value!r}: {', '.join(sorted(unknown))}"
        raise MarketParseError(msg)
    metrics = {metric: float(body[metric]) for metric in _SYSTEM_METRICS if metric in body}
    return SYSTEM_FACTORIES[kind](
        name=str(body["name"]) if "name" in body else None,
        components=[str(c) for c in body.get("components", [])],
        **metrics,
    )


def _parse_dependency(item: dict[str, Any]) -> Dependency:
    """Parse one dependency entry into a :class:`Dependency`."""
    kind_value = str(item.get("kind", DependencyKind.STRUCTURAL.value))
    try:
        kind = DependencyKind(kind_value)
    except ValueError as exc:
        msg = f"unknown dependency kind {kind_value!r}"
        raise MarketParseError(msg) from exc
    return Dependency(
        source=_parse_kind(str(item["source"])),
        target=_parse_kind(str(item["target"])),
        kind=kind,
        weight=float(item.get("weight", 0.5)),
    )
