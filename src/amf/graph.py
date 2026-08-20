"""Dependency and feedback graph over the seven anatomical systems (AMF Step 3).

The :class:`DependencyGraph` is a directed, weighted graph whose edges encode
"``source`` depends on ``target``". Because the market has only seven systems,
the classic graph algorithms it needs (simple-cycle enumeration, articulation
points, eigenvector centrality) are implemented directly here with no third-party
dependency, which keeps the core fully typed and self-contained.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

from amf.errors import InvalidConfigError, InvalidDependencyError
from amf.invariants import check_centrality
from amf.models import Dependency, DependencyKind, SystemKind
from amf.numeric import clip_unit, stable_sum

if TYPE_CHECKING:
    from collections.abc import Iterable

# A stable ordering of the seven systems, used to canonicalise cycles and index
# the coupling matrix deterministically.
_ORDER: tuple[SystemKind, ...] = tuple(SystemKind)
_INDEX: dict[SystemKind, int] = {k: i for i, k in enumerate(_ORDER)}
_KIND_ORDER: tuple[DependencyKind, ...] = tuple(DependencyKind)
_KIND_INDEX: dict[DependencyKind, int] = {k: i for i, k in enumerate(_KIND_ORDER)}

# Rescale the influence accumulator once it passes this magnitude. Above the Katz
# bound the series grows without limit, so this keeps its magnitude bounded however
# long the caller iterates. The result is max-normalised at the end, so dividing
# through changes nothing observable.
_RESCALE_AT = 1e12
# How many past normalised states to remember when looking for a repeat. A cycle
# on seven systems has period at most seven, so this window covers every one.
_CYCLE_WINDOW = 8


@dataclass(frozen=True, slots=True)
class CouplingMatrix:
    """A 7x7 stress-transmission matrix between anatomical systems.

    Entry ``(transmitter, receiver)`` is the strength with which stress flows from
    ``transmitter`` to ``receiver``. Stress flows opposite to dependency: if a
    receiver depends on a transmitter, a stressed transmitter loads the receiver.

    Attributes:
        order: The systems in row/column order.
        data: Nested mapping ``data[transmitter][receiver] -> weight``.
    """

    order: tuple[SystemKind, ...]
    data: dict[SystemKind, dict[SystemKind, float]]

    def get(self, transmitter: SystemKind, receiver: SystemKind) -> float:
        """Return the stress-transmission weight from ``transmitter`` to ``receiver``."""
        return self.data.get(transmitter, {}).get(receiver, 0.0)


class DependencyGraph:
    """A directed, weighted graph of dependencies between anatomical systems.

    An edge is identified by ``(source, target, kind)``: the same pair of systems
    may be coupled by more than one :class:`~amf.models.DependencyKind`, and each
    such coupling is retained separately so it survives serialisation. Adding the
    same triple twice aggregates its weight, capped at ``1.0``.

    Every *pair-level* query -- :meth:`edge_weight`, :meth:`dependencies_of`,
    :meth:`dependents_of`, :meth:`coupling_matrix`, :meth:`centrality`,
    :meth:`feedback_loops`, and :meth:`articulation_points` -- aggregates across
    kinds, so structural analysis sees one coupling per pair regardless of how
    many kinds describe it.
    """

    def __init__(self, dependencies: Iterable[Dependency] = ()) -> None:
        """Build a graph from an iterable of dependencies.

        Args:
            dependencies: The directed couplings to add.
        """
        # Weight per (source, target, kind) triple, each capped at 1.0. This is
        # the source of truth and the only place ``kind`` is retained.
        self._edges: dict[tuple[SystemKind, SystemKind, DependencyKind], float] = {}
        # Derived per-pair total, also capped at 1.0. Every structural algorithm
        # reads this rather than ``_edges``, so a pair coupled by several kinds is
        # never counted more than once.
        self._pair_weights: dict[tuple[SystemKind, SystemKind], float] = {}
        for dep in dependencies:
            self.add(dep)

    def add(self, dependency: Dependency) -> None:
        """Add a dependency, aggregating the weight if the same edge already exists.

        Args:
            dependency: The coupling to add.

        Raises:
            InvalidDependencyError: If the weight is outside ``(0, 1]`` or the edge
                is a self-loop.
        """
        if dependency.source == dependency.target:
            msg = f"a system cannot depend on itself: {dependency.source}"
            raise InvalidDependencyError(msg)
        if not 0.0 < dependency.weight <= 1.0:
            msg = f"dependency weight must be in (0, 1], got {dependency.weight!r}"
            raise InvalidDependencyError(msg)
        key = (dependency.source, dependency.target, dependency.kind)
        self._edges[key] = min(1.0, self._edges.get(key, 0.0) + dependency.weight)
        source, target = dependency.source, dependency.target
        # Sum across kinds in DependencyKind declaration order rather than in the
        # order the edges were added. Floating-point addition is not associative,
        # so summing insertion-first made a pair's weight -- and every score
        # derived from it -- depend on the order the dependencies were listed in.
        self._pair_weights[source, target] = clip_unit(
            stable_sum(
                self._edges[source, target, kind] for kind in _KIND_ORDER if (source, target, kind) in self._edges
            )
        )

    def dependencies(self) -> list[Dependency]:
        """Return every dependency, one per ``(source, target, kind)``, in canonical order.

        Ordering follows system declaration order then dependency-kind declaration
        order, so the result -- and anything derived from it, such as
        :meth:`~amf.market.Market.to_dict` -- does not depend on the order the
        dependencies were added in.
        """
        return [
            Dependency(source=source, target=target, kind=kind, weight=weight)
            for (source, target, kind), weight in sorted(
                self._edges.items(),
                key=lambda item: (_INDEX[item[0][0]], _INDEX[item[0][1]], _KIND_INDEX[item[0][2]]),
            )
        ]

    def edge_weight(self, source: SystemKind, target: SystemKind) -> float:
        """Return the total dependency weight of ``source`` on ``target``, across all kinds."""
        return self._pair_weights.get((source, target), 0.0)

    def edge_kinds(self, source: SystemKind, target: SystemKind) -> tuple[DependencyKind, ...]:
        """Return the coupling kinds recorded for the ``source`` -> ``target`` edge.

        Kinds accumulate as edges aggregate: coupling the same pair twice with
        different kinds records both.

        Returns:
            The recorded kinds in :class:`~amf.models.DependencyKind` declaration
            order, or an empty tuple if the edge does not exist.
        """
        recorded = {kind for (s, t, kind) in self._edges if (s, t) == (source, target)}
        return tuple(kind for kind in _KIND_ORDER if kind in recorded)

    def dependencies_of(self, system: SystemKind) -> list[SystemKind]:
        """Return the systems that ``system`` depends on (its outgoing edges), once each.

        Sorted by system declaration order. Callers such as
        :meth:`~amf.diagnostics.DiagnosticEngine.concentration` sum over this list,
        and floating-point addition is not associative, so a canonical order keeps
        results identical no matter what order the dependencies were added in.
        """
        return sorted((t for (s, t) in self._pair_weights if s == system), key=lambda k: _INDEX[k])

    def dependents_of(self, system: SystemKind) -> list[SystemKind]:
        """Return the systems that depend on ``system`` (its incoming edges), once each.

        Sorted by system declaration order, for the same reason as
        :meth:`dependencies_of`.
        """
        return sorted((s for (s, t) in self._pair_weights if t == system), key=lambda k: _INDEX[k])

    def _out_adjacency(self) -> dict[SystemKind, list[SystemKind]]:
        """Return source -> sorted list of distinct targets."""
        adj: dict[SystemKind, list[SystemKind]] = {k: [] for k in _ORDER}
        for s, t in self._pair_weights:
            adj[s].append(t)
        for targets in adj.values():
            targets.sort(key=lambda k: _INDEX[k])
        return adj

    def _incoming_influence(self) -> dict[SystemKind, tuple[tuple[SystemKind, float], ...]]:
        """Return, per target, the ``(dependent source, weight)`` pairs in canonical order.

        ``_pair_weights`` is keyed in insertion order, so iterating it directly
        makes any accumulation depend on the order the dependencies were added.
        Sorting by system declaration order removes that, which is what keeps
        :meth:`centrality` identical for two markets that compare equal.
        """
        incoming: dict[SystemKind, list[tuple[SystemKind, float]]] = {k: [] for k in _ORDER}
        for (source, target), weight in self._pair_weights.items():
            incoming[target].append((source, weight))
        return {
            target: tuple(sorted(sources, key=lambda item: _INDEX[item[0]])) for target, sources in incoming.items()
        }

    def feedback_loops(self) -> list[tuple[SystemKind, ...]]:
        """Return all simple directed cycles (circular dependencies).

        Each cycle is returned once, as a tuple of systems in traversal order
        starting at the cycle's lowest-ordered system. Cycles are the AMF
        "feedback loops" that can amplify a shock.

        Returns:
            A list of cycles, each a tuple such as
            ``(NERVOUS, MUSCULATURE, CIRCULATORY)`` meaning
            ``NERVOUS -> MUSCULATURE -> CIRCULATORY -> NERVOUS``.
        """
        adj = self._out_adjacency()
        cycles: list[tuple[SystemKind, ...]] = []

        def dfs(start: SystemKind, node: SystemKind, path: list[SystemKind]) -> None:
            for nxt in adj[node]:
                if nxt == start:
                    cycles.append(tuple(path))
                elif _INDEX[nxt] > _INDEX[start] and nxt not in path:
                    dfs(start, nxt, [*path, nxt])

        # Restricting traversal to nodes ordered after ``start`` guarantees each
        # cycle is enumerated exactly once, with its minimum node first.
        for start in _ORDER:
            dfs(start, start, [start])
        return cycles

    def coupling_matrix(self) -> CouplingMatrix:
        """Return the 7x7 stress-transmission matrix derived from dependencies."""
        data: dict[SystemKind, dict[SystemKind, float]] = {k: {} for k in _ORDER}
        for (source, target), weight in self._pair_weights.items():
            # ``source`` depends on ``target`` => stress flows target -> source.
            data[target][source] = weight
        return CouplingMatrix(order=_ORDER, data=data)

    def centrality(
        self, alpha: float = 0.4, iterations: int = 200, tolerance: float = 1e-12
    ) -> dict[SystemKind, float]:
        """Return Katz-style "being depended upon" centrality, scaled to ``[0, 1]``.

        Each system seeds a unit of influence that flows, with attenuation
        ``alpha`` per hop, from dependents toward the systems they rely on. A
        system therefore scores highly when many systems -- directly or
        transitively -- depend on it. Unlike plain eigenvector centrality this is
        well defined on acyclic graphs (it does not collapse to zero), and an
        isolated graph yields all zeros.

        Below ``alpha = 1 / spectral radius`` this is the Katz sum proper. Above it
        the underlying series grows without bound, but the *max-normalised* result
        still settles -- on the dominant-eigenvector direction rather than a Katz
        total. Both are meaningful rankings of "how much is depended upon", so
        neither is rejected; the accumulator is rescaled as it grows so its
        magnitude stays bounded either way.

        What is *not* meaningful is a graph with no single dominant mode. There the
        normalised vector never settles: it cycles between two or more states
        forever, and the answer would be decided by whichever step the iteration
        budget happened to stop on. A complete bipartite market with unequal sides
        does exactly this. That case raises rather than returning a coin flip.

        Args:
            alpha: Per-hop attenuation in ``(0, 1)``.
            iterations: Maximum propagation steps. Exhausting the budget on a
                trajectory that is still settling returns the partial result, as
                a truncated run is what the caller asked for.
            tolerance: Threshold on the per-step change in the max-normalised
                vector. Being scale-free, it means the same thing whether the
                underlying series converges or grows.

        Returns:
            A mapping from system to centrality in ``[0, 1]`` (max-normalised).

        Raises:
            InvalidConfigError: If ``alpha`` is outside ``(0, 1)``, ``iterations``
                is below ``1``, or ``tolerance`` is negative or not finite.
            InvalidDependencyError: If the dependency structure has no single
                dominant mode, so the ranking oscillates instead of settling and
                no stable centrality exists to report.
        """
        if not math.isfinite(alpha) or not 0.0 < alpha < 1.0:
            msg = f"alpha must be in (0, 1), got {alpha!r}"
            raise InvalidConfigError(msg)
        if iterations < 1:
            msg = f"iterations must be at least 1, got {iterations!r}"
            raise InvalidConfigError(msg)
        if not math.isfinite(tolerance) or tolerance < 0.0:
            msg = f"tolerance must be a finite, non-negative number, got {tolerance!r}"
            raise InvalidConfigError(msg)

        influence: dict[SystemKind, float] = dict.fromkeys(_ORDER, 0.0)
        frontier: dict[SystemKind, float] = dict.fromkeys(_ORDER, 1.0)
        normalised: dict[SystemKind, float] = dict.fromkeys(_ORDER, 0.0)
        history: list[dict[SystemKind, float]] = []

        incoming = self._incoming_influence()

        for _ in range(iterations):
            # Influence flows from a dependent ``source`` to its ``target``. The
            # per-target reduction is exactly rounded and taken in declaration
            # order, so the ranking cannot depend on assembly order.
            nxt: dict[SystemKind, float] = {
                target: alpha * stable_sum(weight * frontier[source] for source, weight in sources)
                for target, sources in incoming.items()
            }
            for k in _ORDER:
                influence[k] += nxt[k]
            frontier = nxt

            peak = max(influence.values())
            if peak > _RESCALE_AT:
                influence = {k: v / peak for k, v in influence.items()}
                frontier = {k: v / peak for k, v in frontier.items()}
                peak = max(influence.values())
            normalised = dict.fromkeys(_ORDER, 0.0) if peak <= 0.0 else {k: influence[k] / peak for k in _ORDER}

            if history:
                # Settled: the ranking stopped moving, whether the underlying
                # series converged or merely stabilised in direction.
                if _within(normalised, history[-1], tolerance):
                    return check_centrality(normalised)
                # Returned to a state older than the previous one: the ranking is
                # cycling and will never settle, so no answer exists to report.
                if any(_within(normalised, earlier, tolerance) for earlier in history[:-1]):
                    msg = (
                        "dependency structure has no single dominant mode: the centrality "
                        "ranking cycles instead of settling, so it would be decided by where "
                        "the iteration budget stopped"
                    )
                    raise InvalidDependencyError(msg)
            history.append(normalised)
            if len(history) > _CYCLE_WINDOW:
                history.pop(0)

        # Budget spent on a trajectory that is still settling: a truncated run is
        # what was asked for, so return what it reached.
        return check_centrality(normalised)

    def articulation_points(self) -> set[SystemKind]:
        """Return systems whose removal disconnects the (undirected) dependency graph.

        These are structural cut vertices: candidates for single points of failure.
        """
        neighbours: dict[SystemKind, set[SystemKind]] = {k: set() for k in _ORDER}
        for s, t in self._pair_weights:
            neighbours[s].add(t)
            neighbours[t].add(s)

        present = [k for k in _ORDER if neighbours[k]]
        if not present:
            return set()

        visited: set[SystemKind] = set()
        disc: dict[SystemKind, int] = {}
        low: dict[SystemKind, int] = {}
        articulation: set[SystemKind] = set()
        timer = [0]

        def dfs(node: SystemKind, parent: SystemKind | None) -> None:
            visited.add(node)
            disc[node] = low[node] = timer[0]
            timer[0] += 1
            children = 0
            for nb in sorted(neighbours[node], key=lambda k: _INDEX[k]):
                if nb == parent:
                    continue
                if nb in visited:
                    low[node] = min(low[node], disc[nb])
                    continue
                children += 1
                dfs(nb, node)
                low[node] = min(low[node], low[nb])
                if parent is not None and low[nb] >= disc[node]:
                    articulation.add(node)
            if parent is None and children > 1:
                articulation.add(node)

        for start in present:
            if start not in visited:
                dfs(start, None)
        return articulation


def _within(a: dict[SystemKind, float], b: dict[SystemKind, float], tolerance: float) -> bool:
    """Return whether two normalised vectors agree within ``tolerance``."""
    return max(abs(a[k] - b[k]) for k in _ORDER) <= tolerance
