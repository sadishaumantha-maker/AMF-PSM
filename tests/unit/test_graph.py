"""Unit tests for the dependency / feedback graph."""

from __future__ import annotations

import itertools
import math

import pytest

from amf.errors import InvalidConfigError, InvalidDependencyError
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


@pytest.mark.parametrize("alpha", [0.0, 1.0, 1.5, 10.0, -0.4, float("nan"), float("inf")])
def test_centrality_rejects_out_of_range_alpha(alpha: float):
    # At alpha >= 1 the influence series grows without bound; by alpha = 10 it
    # overflows to infinity and max-normalisation turns every result into NaN,
    # which used to be returned silently. At alpha <= 0 the series is dead and
    # every system scores 0, indistinguishable from a graph with no edges.
    graph = DependencyGraph([_dep(SystemKind.NERVOUS, SystemKind.SKELETON)])
    with pytest.raises(InvalidConfigError, match="alpha must be in"):
        graph.centrality(alpha=alpha)


def test_centrality_rejects_a_non_positive_iteration_budget():
    graph = DependencyGraph([_dep(SystemKind.NERVOUS, SystemKind.SKELETON)])
    with pytest.raises(InvalidConfigError, match="iterations must be at least 1"):
        graph.centrality(iterations=0)


@pytest.mark.parametrize("tolerance", [-1e-12, float("nan"), float("inf")])
def test_centrality_rejects_an_invalid_tolerance(tolerance: float):
    graph = DependencyGraph([_dep(SystemKind.NERVOUS, SystemKind.SKELETON)])
    with pytest.raises(InvalidConfigError, match="tolerance must be"):
        graph.centrality(tolerance=tolerance)


def _complete_bipartite(left: list[SystemKind], right: list[SystemKind]) -> DependencyGraph:
    """Every system on one side coupled to every system on the other, both ways."""
    return DependencyGraph([dep for a in left for b in right for dep in (_dep(a, b, 1.0), _dep(b, a, 1.0))])


_UNEQUAL_SIDES = (
    [SystemKind.SKELETON, SystemKind.CIRCULATORY, SystemKind.NERVOUS, SystemKind.MUSCULATURE],
    [SystemKind.ORGANS, SystemKind.IMMUNE],
)


def test_centrality_rejects_a_graph_whose_ranking_never_settles():
    # A complete bipartite market with unequal sides has two modes of equal
    # magnitude, so the normalised ranking cycles between two states forever and
    # the reported answer is decided by whichever step the budget stopped on.
    # Previously this returned one of the two silently.
    with pytest.raises(InvalidDependencyError, match="no single dominant mode"):
        _complete_bipartite(*_UNEQUAL_SIDES).centrality()


@pytest.mark.parametrize("iterations", [199, 200, 201])
def test_the_oscillating_case_is_rejected_whatever_the_budget(iterations: int):
    # The bug this guards was precisely a parity dependence: at 200 iterations the
    # four left-hand systems scored 0.7222 and at 199 or 201 they scored 0.6923.
    # Rejecting must not itself depend on where the budget lands.
    with pytest.raises(InvalidDependencyError, match="no single dominant mode"):
        _complete_bipartite(*_UNEQUAL_SIDES).centrality(iterations=iterations)


def test_centrality_still_answers_when_the_series_diverges_but_the_ranking_holds():
    # Divergence alone is not a defect: above the Katz bound the max-normalised
    # result settles on the dominant-eigenvector direction, which is still a
    # meaningful "most depended upon" ranking. A guard keyed on divergence rather
    # than on stability would wrongly reject both of these.
    every_pair = DependencyGraph([_dep(s, t, 1.0) for s in SystemKind for t in SystemKind if s is not t])
    symmetric = every_pair.centrality()
    assert symmetric == {kind: pytest.approx(1.0) for kind in SystemKind}

    order = list(SystemKind)
    acyclic = DependencyGraph(
        [_dep(order[i], order[j], 1.0) for i in range(len(order)) for j in range(i + 1, len(order))]
    )
    ranked = acyclic.centrality()
    assert ranked[order[-1]] == pytest.approx(1.0)
    assert all(0.0 <= v <= 1.0 for v in ranked.values())


def test_centrality_stays_bounded_over_a_long_diverging_run():
    # Two dense clusters joined by one weak coupling: the two dominant modes are
    # near-degenerate, so the ranking drifts for a long time while the underlying
    # series grows. The accumulator is rescaled as it grows, so the result stays
    # finite and normalised however long the caller iterates.
    order = list(SystemKind)
    pairs = [(0, 1), (1, 0), (0, 2), (2, 0), (1, 2), (2, 1), (3, 4), (4, 3), (3, 5), (5, 3), (4, 5), (5, 4)]
    graph = DependencyGraph([_dep(order[a], order[b], 1.0) for a, b in pairs] + [_dep(order[2], order[3], 0.001)])
    result = graph.centrality(alpha=0.99, iterations=60)
    assert all(math.isfinite(v) for v in result.values())
    assert all(0.0 <= v <= 1.0 for v in result.values())
    assert max(result.values()) == pytest.approx(1.0)


def test_pair_weight_does_not_depend_on_the_order_kinds_were_added():
    # Floating-point addition is not associative, so summing a pair's kinds in
    # insertion order made `edge_weight` -- and every score derived from it --
    # depend on the order the dependencies happened to be listed in. These weights
    # are chosen so the two orders genuinely differ in the last bits.
    kinds = (DependencyKind.STRUCTURAL, DependencyKind.INFORMATIONAL, DependencyKind.CAPITAL)
    weights = (0.1, 0.2, 0.30000000000000004)
    edges = [
        Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, kind, weight)
        for kind, weight in zip(kinds, weights, strict=True)
    ]
    forwards = DependencyGraph(edges).edge_weight(SystemKind.NERVOUS, SystemKind.SKELETON)
    backwards = DependencyGraph(reversed(edges)).edge_weight(SystemKind.NERVOUS, SystemKind.SKELETON)
    # Exact equality, not approx: approx is what let this through.
    assert forwards == backwards


def test_centrality_is_identical_under_every_ordering_of_the_same_edges():
    # Regression, exhaustive rather than sampled: the influence propagation used
    # to accumulate into the target while iterating the pair-weight dict, which
    # is keyed in insertion order. Because float addition is not associative,
    # feeding the identical edges in a different order shifted the published
    # centralities by an ulp. All 720 orderings of these six edges must now agree
    # exactly -- not approximately.
    edges = [
        Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.8),
        Dependency(SystemKind.NERVOUS, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.5),
        Dependency(SystemKind.IMMUNE, SystemKind.SKELETON, DependencyKind.REGULATORY, 0.3),
        Dependency(SystemKind.ORGANS, SystemKind.CIRCULATORY, DependencyKind.CAPITAL, 0.6),
        Dependency(SystemKind.MUSCULATURE, SystemKind.CIRCULATORY, DependencyKind.CAPITAL, 0.7),
        Dependency(SystemKind.METABOLISM, SystemKind.ORGANS, DependencyKind.STRUCTURAL, 0.4),
    ]
    results = {
        tuple(sorted(DependencyGraph(ordering).centrality().items(), key=lambda kv: kv[0].value))
        for ordering in itertools.permutations(edges)
    }
    assert len(results) == 1


def test_centrality_is_max_normalised():
    # The guard in amf.invariants relies on this: a non-empty influence vector is
    # divided through by its own maximum, so the peak is exactly 1.
    graph = DependencyGraph([_dep(SystemKind.CIRCULATORY, SystemKind.SKELETON, 0.8)])
    assert max(graph.centrality().values()) == 1.0
