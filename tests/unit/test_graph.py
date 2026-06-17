"""Unit tests for the dependency / feedback graph."""

from __future__ import annotations

import pytest

from amf.errors import InvalidDependencyError
from amf.graph import DependencyGraph
from amf.models import Dependency, SystemKind


def _dep(source: SystemKind, target: SystemKind, weight: float = 0.5) -> Dependency:
    return Dependency(source=source, target=target, weight=weight)


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
    loops = set(graph.feedback_loops())
    assert (SystemKind.SKELETON, SystemKind.CIRCULATORY) in loops
    assert (SystemKind.NERVOUS, SystemKind.MUSCULATURE) in loops
    assert len(loops) == 2


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
