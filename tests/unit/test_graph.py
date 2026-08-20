"""Unit tests for the dependency / feedback graph."""

from __future__ import annotations

import pytest

from amf.errors import InvalidDependencyError
from amf.graph import DependencyGraph
from amf.models import Dependency, DependencyKind, SystemKind


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


def test_centrality_alpha_controls_per_hop_attenuation():
    # alpha attenuates influence per hop, so raising it must lift a system that is
    # only reached transitively. skeleton is two hops from musculature.
    graph = DependencyGraph(
        [
            _dep(SystemKind.MUSCULATURE, SystemKind.NERVOUS),
            _dep(SystemKind.NERVOUS, SystemKind.SKELETON),
            _dep(SystemKind.CIRCULATORY, SystemKind.SKELETON),
        ]
    )
    low = graph.centrality(alpha=0.1)
    high = graph.centrality(alpha=0.8)
    # Nervous is one hop from its dependents; skeleton also collects two-hop flow,
    # so a higher alpha widens skeleton's lead over nervous.
    assert high[SystemKind.NERVOUS] < low[SystemKind.NERVOUS]
    assert all(0.0 <= v <= 1.0 for v in low.values())
    assert all(0.0 <= v <= 1.0 for v in high.values())


def test_centrality_is_max_normalised_to_one():
    graph = DependencyGraph([_dep(SystemKind.NERVOUS, SystemKind.SKELETON)])
    for alpha in (0.1, 0.4, 0.9):
        centrality = graph.centrality(alpha=alpha)
        assert max(centrality.values()) == pytest.approx(1.0)


def test_centrality_ranks_transitive_dependence_above_none():
    # A chain metabolism -> organs -> circulatory: circulatory is depended upon
    # both directly and transitively, so it must outrank organs.
    graph = DependencyGraph(
        [
            _dep(SystemKind.METABOLISM, SystemKind.ORGANS),
            _dep(SystemKind.ORGANS, SystemKind.CIRCULATORY),
        ]
    )
    centrality = graph.centrality()
    assert centrality[SystemKind.CIRCULATORY] > centrality[SystemKind.ORGANS]
    assert centrality[SystemKind.METABOLISM] == pytest.approx(0.0)


def test_feedback_loops_enumerates_each_cycle_once_in_a_dense_graph():
    # Two cycles share an edge; each must still be reported exactly once, with its
    # lowest-ordered system first.
    graph = DependencyGraph(
        [
            _dep(SystemKind.SKELETON, SystemKind.CIRCULATORY),
            _dep(SystemKind.CIRCULATORY, SystemKind.SKELETON),
            _dep(SystemKind.CIRCULATORY, SystemKind.NERVOUS),
            _dep(SystemKind.NERVOUS, SystemKind.SKELETON),
        ]
    )
    loops = graph.feedback_loops()
    assert len(loops) == len(set(loops))
    assert set(loops) == {
        (SystemKind.SKELETON, SystemKind.CIRCULATORY),
        (SystemKind.SKELETON, SystemKind.CIRCULATORY, SystemKind.NERVOUS),
    }
    for loop in loops:
        assert loop[0] == min(loop, key=list(SystemKind).index)


def test_centrality_default_alpha_is_pinned():
    # The default attenuation is documented as 0.4; the alpha tests above pass it
    # explicitly, which would leave the default free to drift.
    graph = DependencyGraph(
        [
            _dep(SystemKind.METABOLISM, SystemKind.ORGANS),
            _dep(SystemKind.ORGANS, SystemKind.CIRCULATORY),
        ]
    )
    assert graph.centrality() == pytest.approx(graph.centrality(alpha=0.4))
    assert graph.centrality() != pytest.approx(graph.centrality(alpha=0.9))
