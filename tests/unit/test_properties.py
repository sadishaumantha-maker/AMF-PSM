"""Property-based tests for the invariants the docstrings promise.

The example-based tests pin specific values; these check that the stated
invariants hold across arbitrary valid markets. Strategies are defined here
rather than reusing the conftest fixtures because hypothesis rejects
function-scoped fixtures inside ``@given``.
"""

from __future__ import annotations

import itertools

from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from amf.diagnostics import DiagnosticConfig, DiagnosticEngine
from amf.graph import DependencyGraph
from amf.market import Market
from amf.models import Dependency, DependencyKind, MarketBoundary, Shock, SystemKind
from amf.simulation import ShockSimulator, SimulationConfig
from amf.systems import SYSTEM_FACTORIES

_BOUNDARY = MarketBoundary(asset_class="equities", geography="US", timeframe="intraday")
_ORDER = list(SystemKind)
_PAIRS = [(s, t) for s in SystemKind for t in SystemKind if s is not t]

_metric = st.floats(min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False)
_weight = st.floats(min_value=0.01, max_value=1.0, allow_nan=False, allow_infinity=False)


@st.composite
def _dependencies(draw: st.DrawFn) -> list[Dependency]:
    pairs = draw(st.lists(st.sampled_from(_PAIRS), max_size=12))
    return [
        Dependency(source, target, draw(st.sampled_from(list(DependencyKind))), draw(_weight))
        for source, target in pairs
    ]


@st.composite
def _markets(draw: st.DrawFn) -> Market:
    systems = [
        SYSTEM_FACTORIES[kind](
            integrity=draw(_metric),
            redundancy=draw(_metric),
            criticality=draw(_metric),
            load=draw(_metric),
        )
        for kind in _ORDER
    ]
    return Market.assemble(_BOUNDARY, systems, draw(_dependencies()))


def _brute_force_cycles(pairs: set[tuple[SystemKind, SystemKind]]) -> set[tuple[SystemKind, ...]]:
    """Every simple directed cycle, canonicalised to start at its lowest system."""
    index = {kind: i for i, kind in enumerate(_ORDER)}
    cycles: set[tuple[SystemKind, ...]] = set()
    for length in range(2, len(_ORDER) + 1):
        for combo in itertools.permutations(_ORDER, length):
            if combo[0] != min(combo, key=lambda k: index[k]):
                continue
            if all((combo[i], combo[(i + 1) % length]) in pairs for i in range(length)):
                cycles.add(combo)
    return cycles


# Deadline is disabled because coverage line-tracing makes a 7-system, 50-step
# run unpredictably slow on CI runners; the assertions do not depend on timing.
_SETTINGS = settings(deadline=None, max_examples=50, suppress_health_check=[HealthCheck.too_slow])


@given(market=_markets(), target=st.sampled_from(_ORDER), magnitude=_weight)
@_SETTINGS
def test_stress_stays_in_the_unit_interval(market: Market, target: SystemKind, magnitude: float):
    # Replaces 20 parametrised cases that varied only the shock against one fixed
    # market and asserted a single boolean each. This varies the market too, and
    # checks the range invariant those cases never looked at.
    #
    # Note it does NOT assert convergence: the step map is not a contraction for
    # every market, and a stable but slowly-settling one can exhaust max_steps.
    # See test_convergence_is_reported_against_the_step_budget below.
    trace = ShockSimulator(market).propagate(Shock(target, magnitude))
    for step in trace.steps:
        assert set(step) == set(SystemKind)
        for value in step.values():
            assert 0.0 <= value <= 1.0
    assert trace.resilience is not None
    assert 0.0 <= trace.resilience.value <= 1.0
    assert 0.0 <= trace.resilience.peak_stress <= 1.0
    assert 0.0 <= trace.resilience.absorbed_fraction <= 1.0
    assert trace.resilience.amplification_factor >= 0.0


@given(market=_markets(), target=st.sampled_from(_ORDER), magnitude=_weight)
@_SETTINGS
def test_convergence_is_reported_against_the_step_budget(market: Market, target: SystemKind, magnitude: float):
    # What `converged` actually means: the final step moved less than eps, and if
    # it did not, the whole budget was spent.
    config = SimulationConfig()
    trace = ShockSimulator(market, config).propagate(Shock(target, magnitude))
    final_delta = max(abs(trace.steps[-1][k] - trace.steps[-2][k]) for k in SystemKind)

    if trace.converged:
        assert final_delta < config.convergence_eps
        assert trace.resilience is not None
        assert trace.resilience.settling_time == len(trace.steps) - 1
    else:
        assert len(trace.steps) - 1 == config.max_steps
        assert final_delta >= config.convergence_eps
        assert trace.resilience is not None
        assert trace.resilience.settling_time == -1


@given(
    market=_markets(),
    fragility=st.floats(min_value=0.0, max_value=5.0),
    concentration=st.floats(min_value=0.0, max_value=5.0),
    feedback=st.floats(min_value=0.0, max_value=5.0),
)
@_SETTINGS
def test_diagnostic_scores_stay_in_the_unit_interval(
    market: Market, fragility: float, concentration: float, feedback: float
):
    config = DiagnosticConfig(fragility, concentration, feedback)
    report = DiagnosticEngine(config).diagnose(market)
    assert 0.0 <= report.overall_index <= 1.0
    for finding in report.findings:
        assert 0.0 <= finding.score <= 1.0
        assert 0.0 <= finding.fragility <= 1.0
        assert 0.0 <= finding.concentration <= 1.0
        assert 0.0 <= finding.feedback <= 1.0


@given(market=_markets())
@_SETTINGS
def test_serialisation_is_a_fixed_point(market: Market):
    # Generalises the round-trip guard: dependency kinds, multi-kind pairs, and
    # canonical ordering must all survive, for any valid market.
    data = market.to_dict()
    restored = Market.from_dict(data)
    assert restored.graph.dependencies() == market.graph.dependencies()
    assert restored.to_dict() == data


@given(market=_markets())
@_SETTINGS
def test_diagnosis_survives_a_round_trip(market: Market):
    engine = DiagnosticEngine()
    before = engine.diagnose(market)
    after = engine.diagnose(Market.from_dict(market.to_dict()))
    assert after.to_dict() == before.to_dict()


@given(dependencies=_dependencies())
@_SETTINGS
def test_aggregated_edge_weights_stay_in_the_unit_interval(dependencies: list[Dependency]):
    graph = DependencyGraph(dependencies)
    for source in SystemKind:
        for target in graph.dependencies_of(source):
            assert 0.0 < graph.edge_weight(source, target) <= 1.0
    for dependency in graph.dependencies():
        assert 0.0 < dependency.weight <= 1.0


@given(dependencies=_dependencies())
@settings(deadline=None, max_examples=25, suppress_health_check=[HealthCheck.too_slow])
def test_feedback_loops_match_a_brute_force_enumeration(dependencies: list[Dependency]):
    graph = DependencyGraph(dependencies)
    loops = graph.feedback_loops()
    pairs = {(d.source, d.target) for d in graph.dependencies()}
    assert set(loops) == _brute_force_cycles(pairs)
    # Each cycle exactly once, and canonicalised to start at its lowest system.
    assert len(loops) == len(set(loops))
    for loop in loops:
        assert loop[0] == min(loop, key=_ORDER.index)
