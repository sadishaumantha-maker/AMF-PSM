"""Unit tests for the dependency / feedback graph."""

from __future__ import annotations

import pytest

from amf.errors import InvalidDependencyError
from amf.graph import DependencyGraph
from amf.models import Dependency, DependencyKind, SystemKind


def _dep(source: SystemKind, target: SystemKind, weight: float = 0.5) -> Dependency:
    return Dependency(source=source, target=target, weight=weight)


def _two_kinds(structural: float = 0.3, capital: float = 0.2) -> DependencyGraph:
    """One pair coupled by two kinds -- the shape that can double-count."""
    return DependencyGraph(
        [
            Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.STRUCTURAL, structural),
            Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.CAPITAL, capital),
        ]
    )


def test_self_loop_rejected():
    with pytest.raises(InvalidDependencyError):
        DependencyGraph([_dep(SystemKind.SKELETON, SystemKind.SKELETON)])


@pytest.mark.parametrize("weight", [0.0, -0.1, 1.5])
def test_invalid_weight_rejected(weight: float):
    with pytest.raises(InvalidDependencyError):
        DependencyGraph([_dep(SystemKind.NERVOUS, SystemKind.SKELETON, weight)])


def test_edge_weights_aggregate_and_cap():
    graph = DependencyGraph(
        [
            _dep(SystemKind.NERVOUS, SystemKind.SKELETON, 0.7),
            _dep(SystemKind.NERVOUS, SystemKind.SKELETON, 0.6),
        ]
    )
    # 0.7 + 0.6 capped at 1.0
    assert graph.edge_weight(SystemKind.NERVOUS, SystemKind.SKELETON) == pytest.approx(1.0)


def test_edge_kinds_returns_recorded_kind():
    graph = DependencyGraph([Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.5)])
    assert graph.edge_kinds(SystemKind.CIRCULATORY, SystemKind.SKELETON) == (DependencyKind.CAPITAL,)


def test_edge_kinds_accumulate_across_aggregated_edges():
    graph = DependencyGraph(
        [
            Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.REGULATORY, 0.3),
            Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.INFORMATIONAL, 0.4),
        ]
    )
    # Both kinds are recorded, in DependencyKind declaration order.
    assert graph.edge_kinds(SystemKind.NERVOUS, SystemKind.SKELETON) == (
        DependencyKind.INFORMATIONAL,
        DependencyKind.REGULATORY,
    )


def test_edge_kinds_empty_for_absent_edge():
    assert DependencyGraph().edge_kinds(SystemKind.NERVOUS, SystemKind.SKELETON) == ()


def test_dependencies_and_dependents():
    graph = DependencyGraph(
        [
            _dep(SystemKind.NERVOUS, SystemKind.SKELETON),
            _dep(SystemKind.CIRCULATORY, SystemKind.SKELETON),
        ]
    )
    assert graph.dependencies_of(SystemKind.NERVOUS) == [SystemKind.SKELETON]
    assert set(graph.dependents_of(SystemKind.SKELETON)) == {
        SystemKind.NERVOUS,
        SystemKind.CIRCULATORY,
    }


def test_feedback_loops_finds_single_cycle():
    graph = DependencyGraph(
        [
            _dep(SystemKind.CIRCULATORY, SystemKind.NERVOUS),
            _dep(SystemKind.NERVOUS, SystemKind.MUSCULATURE),
            _dep(SystemKind.MUSCULATURE, SystemKind.CIRCULATORY),
        ]
    )
    loops = graph.feedback_loops()
    assert loops == [(SystemKind.CIRCULATORY, SystemKind.NERVOUS, SystemKind.MUSCULATURE)]


def test_no_feedback_loops_in_acyclic_graph():
    graph = DependencyGraph(
        [
            _dep(SystemKind.NERVOUS, SystemKind.SKELETON),
            _dep(SystemKind.CIRCULATORY, SystemKind.SKELETON),
        ]
    )
    assert graph.feedback_loops() == []


def test_coupling_matrix_direction_is_target_to_source():
    # circulatory depends on skeleton => stress flows skeleton -> circulatory.
    graph = DependencyGraph([_dep(SystemKind.CIRCULATORY, SystemKind.SKELETON, 0.8)])
    matrix = graph.coupling_matrix()
    assert matrix.get(SystemKind.SKELETON, SystemKind.CIRCULATORY) == pytest.approx(0.8)
    assert matrix.get(SystemKind.CIRCULATORY, SystemKind.SKELETON) == 0.0


def test_centrality_highest_for_most_depended_upon():
    graph = DependencyGraph(
        [
            _dep(SystemKind.NERVOUS, SystemKind.SKELETON),
            _dep(SystemKind.CIRCULATORY, SystemKind.SKELETON),
            _dep(SystemKind.MUSCULATURE, SystemKind.SKELETON),
        ]
    )
    centrality = graph.centrality()
    assert centrality[SystemKind.SKELETON] == pytest.approx(1.0)
    assert all(centrality[k] <= centrality[SystemKind.SKELETON] for k in SystemKind)


def test_centrality_all_zero_without_edges():
    centrality = DependencyGraph().centrality()
    assert all(value == 0.0 for value in centrality.values())


def test_centrality_normalises_when_iteration_budget_exhausted():
    # With a one-step budget the influence series cannot converge below the
    # tolerance, so the loop exits by exhausting ``iterations`` rather than by
    # breaking early. The result must still be max-normalised to [0, 1].
    graph = DependencyGraph(
        [
            _dep(SystemKind.NERVOUS, SystemKind.SKELETON),
            _dep(SystemKind.CIRCULATORY, SystemKind.SKELETON),
        ]
    )
    centrality = graph.centrality(iterations=1)
    assert centrality[SystemKind.SKELETON] == pytest.approx(1.0)
    assert all(0.0 <= v <= 1.0 for v in centrality.values())


def test_feedback_loops_finds_multiple_disjoint_cycles():
    graph = DependencyGraph(
        [
            # cycle A: skeleton <-> circulatory
            _dep(SystemKind.SKELETON, SystemKind.CIRCULATORY),
            _dep(SystemKind.CIRCULATORY, SystemKind.SKELETON),
            # cycle B: nervous <-> musculature
            _dep(SystemKind.NERVOUS, SystemKind.MUSCULATURE),
            _dep(SystemKind.MUSCULATURE, SystemKind.NERVOUS),
        ]
    )
    # Length is checked on the raw list, not a set: a set would silently collapse
    # a cycle that was enumerated more than once.
    loops = graph.feedback_loops()
    assert len(loops) == 2
    assert (SystemKind.SKELETON, SystemKind.CIRCULATORY) in set(loops)
    assert (SystemKind.NERVOUS, SystemKind.MUSCULATURE) in set(loops)


def test_dependencies_of_is_in_canonical_order():
    # Insertion order must not leak into the result: diagnostics sums over this
    # list, and float addition is not associative.
    deps = [
        _dep(SystemKind.NERVOUS, SystemKind.ORGANS),
        _dep(SystemKind.NERVOUS, SystemKind.SKELETON),
        _dep(SystemKind.NERVOUS, SystemKind.CIRCULATORY),
    ]
    expected = [SystemKind.SKELETON, SystemKind.CIRCULATORY, SystemKind.ORGANS]
    assert DependencyGraph(deps).dependencies_of(SystemKind.NERVOUS) == expected
    assert DependencyGraph(reversed(deps)).dependencies_of(SystemKind.NERVOUS) == expected


def test_dependents_of_is_in_canonical_order():
    deps = [
        _dep(SystemKind.ORGANS, SystemKind.SKELETON),
        _dep(SystemKind.CIRCULATORY, SystemKind.SKELETON),
    ]
    expected = [SystemKind.CIRCULATORY, SystemKind.ORGANS]
    assert DependencyGraph(deps).dependents_of(SystemKind.SKELETON) == expected
    assert DependencyGraph(reversed(deps)).dependents_of(SystemKind.SKELETON) == expected


def test_edge_weights_aggregate_below_the_cap():
    graph = DependencyGraph(
        [
            _dep(SystemKind.NERVOUS, SystemKind.SKELETON, 0.2),
            _dep(SystemKind.NERVOUS, SystemKind.SKELETON, 0.3),
        ]
    )
    assert graph.edge_weight(SystemKind.NERVOUS, SystemKind.SKELETON) == pytest.approx(0.5)


def test_edge_weight_sums_across_kinds():
    assert _two_kinds(0.3, 0.2).edge_weight(SystemKind.NERVOUS, SystemKind.SKELETON) == pytest.approx(0.5)


def test_edge_weight_caps_across_kinds():
    assert _two_kinds(0.8, 0.6).edge_weight(SystemKind.NERVOUS, SystemKind.SKELETON) == pytest.approx(1.0)


def test_dependencies_of_deduplicates_across_kinds():
    # List equality, not set: a set would hide the duplicate this guards against.
    assert _two_kinds().dependencies_of(SystemKind.NERVOUS) == [SystemKind.SKELETON]


def test_dependents_of_deduplicates_across_kinds():
    assert _two_kinds().dependents_of(SystemKind.SKELETON) == [SystemKind.NERVOUS]


def test_coupling_matrix_sums_kinds_for_one_pair():
    # Last-write-wins would give 0.3 or 0.2; only summing gives 0.5.
    matrix = _two_kinds(0.3, 0.2).coupling_matrix()
    assert matrix.get(SystemKind.SKELETON, SystemKind.NERVOUS) == pytest.approx(0.5)


def test_centrality_matches_the_single_equivalent_edge():
    split = _two_kinds(0.3, 0.2).centrality()
    single = DependencyGraph([_dep(SystemKind.NERVOUS, SystemKind.SKELETON, 0.5)]).centrality()
    for kind in SystemKind:
        assert split[kind] == pytest.approx(single[kind])


def test_feedback_loops_counted_once_with_multi_kind_edges():
    graph = DependencyGraph(
        [
            Dependency(SystemKind.SKELETON, SystemKind.CIRCULATORY, DependencyKind.STRUCTURAL, 0.5),
            Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.5),
            Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.4),
        ]
    )
    assert len(graph.feedback_loops()) == 1


def test_dependencies_returns_each_kind_separately():
    edges = _two_kinds(0.3, 0.2).dependencies()
    assert [(d.source, d.target, d.kind, d.weight) for d in edges] == [
        (SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.3),
        (SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.2),
    ]


def test_dependencies_order_is_independent_of_insertion_order():
    forward = [
        Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.2),
        Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.4),
    ]
    assert DependencyGraph(forward).dependencies() == DependencyGraph(reversed(forward)).dependencies()


def test_dependencies_aggregates_repeats_of_the_same_triple():
    graph = DependencyGraph(
        [
            Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.2),
            Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.3),
        ]
    )
    assert [(d.kind, d.weight) for d in graph.dependencies()] == [(DependencyKind.CAPITAL, pytest.approx(0.5))]


def test_articulation_points_identify_cut_vertices():
    # immune - skeleton - circulatory - organs - metabolism (a path); the
    # interior nodes are articulation points.
    graph = DependencyGraph(
        [
            _dep(SystemKind.IMMUNE, SystemKind.SKELETON),
            _dep(SystemKind.CIRCULATORY, SystemKind.SKELETON),
            _dep(SystemKind.ORGANS, SystemKind.CIRCULATORY),
            _dep(SystemKind.METABOLISM, SystemKind.ORGANS),
        ]
    )
    points = graph.articulation_points()
    assert SystemKind.SKELETON in points
    assert SystemKind.CIRCULATORY in points
    assert SystemKind.ORGANS in points
    assert SystemKind.IMMUNE not in points
    assert SystemKind.METABOLISM not in points


def test_articulation_points_empty_without_edges():
    assert DependencyGraph().articulation_points() == set()


def test_articulation_points_none_in_a_cycle():
    # A cycle has no cut vertex: removing any single node keeps the rest
    # connected. This also exercises the DFS back-edge (already-visited) path.
    graph = DependencyGraph(
        [
            _dep(SystemKind.SKELETON, SystemKind.CIRCULATORY),
            _dep(SystemKind.CIRCULATORY, SystemKind.NERVOUS),
            _dep(SystemKind.NERVOUS, SystemKind.SKELETON),
        ]
    )
    assert graph.articulation_points() == set()
