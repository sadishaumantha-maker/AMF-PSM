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

from amf.errors import IncompleteMarketError, MarketParseError
from amf.graph import DependencyGraph
from amf.models import Dependency, DependencyKind, MarketBoundary, SystemKind
from amf.systems import AnatomicalSystem

if TYPE_CHECKING:
    from collections.abc import Iterable


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
        market = cls(boundary=boundary, systems=mapping, graph=DependencyGraph(dependencies))
        market.require_complete()
        return market

    def require_complete(self) -> None:
        """Ensure all seven systems are present.

        Raises:
            IncompleteMarketError: If any :class:`~amf.models.SystemKind` is absent.
        """
        missing = [k.value for k in SystemKind if k not in self.systems]
        if missing:
            msg = f"market is missing systems: {', '.join(missing)}"
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
        """Return a JSON-serialisable representation of the market."""
        return {
            "boundary": self.boundary.to_dict(),
            "systems": {
                kind.value: {
                    "name": system.name,
                    "components": list(system.components),
                    "integrity": system.integrity,
                    "redundancy": system.redundancy,
                    "criticality": system.criticality,
                    "load": system.load,
                }
                for kind, system in self.systems.items()
            },
            "dependencies": [
                Dependency(
                    source=source,
                    target=target,
                    weight=self.graph.edge_weight(source, target),
                ).to_dict()
                for source in SystemKind
                for target in self.graph.dependencies_of(source)
            ],
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
        except (KeyError, TypeError, AttributeError) as exc:
            msg = f"malformed market description: {exc}"
            raise MarketParseError(msg) from exc
        try:
            return cls.assemble(boundary, systems, dependencies)
        except IncompleteMarketError as exc:
            raise MarketParseError(str(exc)) from exc


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
    """Parse one system entry into an :class:`AnatomicalSystem`."""
    kind = _parse_kind(name)
    return AnatomicalSystem(
        kind=kind,
        name=str(body.get("name", kind.value)),
        components=[str(c) for c in body.get("components", [])],
        integrity=float(body.get("integrity", 1.0)),
        redundancy=float(body.get("redundancy", 0.5)),
        criticality=float(body.get("criticality", 0.5)),
        load=float(body.get("load", 0.0)),
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
