"""Unit tests for the shock-propagation simulation engine."""

from __future__ import annotations

import pytest

from amf.errors import InvalidConfigError, InvalidShockError
from amf.market import Market
from amf.models import Dependency, DependencyKind, Intervention, Severity, Shock, SystemKind
from amf.simulation import ShockSimulator, SimulationConfig


def _total_stress(trace) -> float:
    """Sum of stress across every system and timestep of a trace."""
    return sum(v for step in trace.steps for v in step.values())


_CASCADE = SimulationConfig(cascade_threshold=0.2, cascade_gain=1.0)


def _fragile_dense_market(market_factory) -> Market:
    """A tightly coupled market with almost no absorptive capacity.

    Every system is degraded (absorptive capacity 0.5*0 + 0.3*0.15 + 0.2*0.1 =
    0.065) and every ordered pair is coupled at full weight, so an injected shock
    is amplified rather than absorbed.
    """
    weak = {"integrity": 0.15, "redundancy": 0.0, "load": 0.9}
    deps = [
        Dependency(source, target, DependencyKind.STRUCTURAL, 1.0)
        for source in SystemKind
        for target in SystemKind
        if source is not target
    ]
    return market_factory(deps, **{kind.value: weak for kind in SystemKind})


def _hub_market(market_factory) -> Market:
    """Every system depends on skeleton; nothing depends on metabolism."""
    deps = [
        Dependency(source, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 1.0)
        for source in SystemKind
        if source is not SystemKind.SKELETON
    ]
    return market_factory(deps)


def test_invalid_shock_magnitude_raises(healthy_market: Market):
    sim = ShockSimulator(healthy_market)
    for magnitude in (0.0, -0.2, 1.5):
        with pytest.raises(InvalidShockError, match="magnitude"):
            sim.propagate(Shock(SystemKind.SKELETON, magnitude))


def test_empty_shock_list_raises(healthy_market: Market):
    with pytest.raises(InvalidShockError, match="at least one shock"):
        ShockSimulator(healthy_market).propagate([])


def test_isolated_system_dissipates_shock(healthy_market: Market):
    # No couplings => stress only decays; it is fully absorbed and never amplified.
    result = ShockSimulator(healthy_market).resilience(Shock(SystemKind.SKELETON, 0.8))
    assert result.amplification_factor == pytest.approx(1.0)
    assert result.absorbed_fraction == pytest.approx(1.0, abs=1e-3)
    assert result.value > 0.9


def test_deterministic_without_seed(stressed_market: Market):
    sim = ShockSimulator(stressed_market)
    first = sim.propagate(Shock(SystemKind.CIRCULATORY, 0.8))
    second = sim.propagate(Shock(SystemKind.CIRCULATORY, 0.8))
    assert first.steps == second.steps
    assert first.resilience == second.resilience


def test_seeded_jitter_is_reproducible(stressed_market: Market):
    config = SimulationConfig(seed=42, jitter=0.05)
    a = ShockSimulator(stressed_market, config).propagate(Shock(SystemKind.CIRCULATORY, 0.8))
    b = ShockSimulator(stressed_market, config).propagate(Shock(SystemKind.CIRCULATORY, 0.8))
    assert a.steps == b.steps


def test_converges_within_budget(stressed_market: Market):
    trace = ShockSimulator(stressed_market).propagate(Shock(SystemKind.SKELETON, 0.9))
    assert trace.converged is True
    assert trace.resilience is not None
    assert 0.0 <= trace.resilience.value <= 1.0


def test_stress_test_covers_all_systems(stressed_market: Market):
    profile = ShockSimulator(stressed_market).stress_test(magnitude=0.7)
    assert set(profile) == set(SystemKind)
    assert all(0.0 <= score.value <= 1.0 for score in profile.values())


def test_multiple_simultaneous_shocks(stressed_market: Market):
    trace = ShockSimulator(stressed_market).propagate(
        [Shock(SystemKind.SKELETON, 0.6), Shock(SystemKind.CIRCULATORY, 0.9)]
    )
    assert trace.steps[0][SystemKind.SKELETON] == pytest.approx(0.6)
    assert trace.steps[0][SystemKind.CIRCULATORY] == pytest.approx(0.9)
    # dominant shock (circulatory) labels the resilience score
    assert trace.resilience is not None
    assert trace.resilience.target is SystemKind.CIRCULATORY


def test_budget_exhausted_without_convergence(stressed_market: Market):
    # A one-step budget cannot settle, so the run reports non-convergence and an
    # undefined (-1) settling time.
    config = SimulationConfig(max_steps=1)
    trace = ShockSimulator(stressed_market, config).propagate(Shock(SystemKind.CIRCULATORY, 0.9))
    assert trace.converged is False
    assert trace.resilience is not None
    assert trace.resilience.settling_time == -1


# --- Extension 1: threshold / cascade dynamics -----------------------------


def test_cascade_tips_systems_and_default_does_not(stressed_market: Market):
    baseline = ShockSimulator(stressed_market).resilience(Shock(SystemKind.CIRCULATORY, 0.9))
    cascade = ShockSimulator(stressed_market, _CASCADE).resilience(Shock(SystemKind.CIRCULATORY, 0.9))
    # Linear default reports no tipping; cascade mode tips at least the shocked hub.
    assert baseline.tipped_systems == ()
    assert SystemKind.CIRCULATORY in cascade.tipped_systems
    # Impairment can only add stress, so cascade peak >= baseline peak.
    assert cascade.peak_stress >= baseline.peak_stress - 1e-9


def test_cascade_can_amplify_beyond_baseline(stressed_market: Market):
    # Total accumulated stress under cascade is at least the linear baseline.
    base = ShockSimulator(stressed_market).propagate(Shock(SystemKind.CIRCULATORY, 0.9))
    casc = ShockSimulator(stressed_market, _CASCADE).propagate(Shock(SystemKind.CIRCULATORY, 0.9))
    assert _total_stress(casc) >= _total_stress(base) - 1e-9


# --- Extension 2: Monte Carlo ensemble -------------------------------------


def test_ensemble_is_deterministic_and_ordered(stressed_market: Market):
    sim = ShockSimulator(stressed_market)
    a = sim.ensemble(Shock(SystemKind.CIRCULATORY, 0.8), runs=30, base_seed=7, jitter=0.05)
    b = sim.ensemble(Shock(SystemKind.CIRCULATORY, 0.8), runs=30, base_seed=7, jitter=0.05)
    assert a.to_dict() == b.to_dict()
    assert a.runs == 30
    assert a.target is SystemKind.CIRCULATORY
    for stats in (a.value, a.amplification_factor, a.peak_stress, a.absorbed_fraction):
        assert stats.minimum <= stats.p10 <= stats.p50 <= stats.p90 <= stats.maximum
    assert 0.0 <= a.value.mean <= 1.0


def test_ensemble_rejects_nonpositive_runs(stressed_market: Market):
    with pytest.raises(InvalidShockError, match="runs must be"):
        ShockSimulator(stressed_market).ensemble(Shock(SystemKind.SKELETON, 0.8), runs=0)


def test_ensemble_single_run_collapses_to_a_point(stressed_market: Market):
    dist = ShockSimulator(stressed_market).ensemble(Shock(SystemKind.SKELETON, 0.8), runs=1)
    # A single sample makes every percentile equal to that sample.
    assert dist.value.minimum == dist.value.p10 == dist.value.p50 == dist.value.p90 == dist.value.maximum


def test_ensemble_percentile_lands_exactly_on_a_sample(stressed_market: Market):
    # With three runs the p50 rank is exactly 1.0, so it falls on a sample index
    # rather than between two and is taken straight from the sorted values
    # instead of being interpolated.
    dist = ShockSimulator(stressed_market).ensemble(Shock(SystemKind.SKELETON, 0.8), runs=3, base_seed=3)
    assert dist.runs == 3
    assert dist.value.minimum <= dist.value.p50 <= dist.value.maximum


def test_intervention_to_dict_round_trips():
    payload = Intervention(SystemKind.CIRCULATORY, 0.4, at_step=3).to_dict()
    assert payload == {"target": "circulatory", "absorptive_boost": 0.4, "at_step": 3}


# --- Extension 3: time-scheduled / multi-wave shocks -----------------------


def test_scheduled_shock_injects_at_its_step(healthy_market: Market):
    # With no couplings the first shock decays toward zero, then a second wave at
    # step 5 makes circulatory jump.
    trace = ShockSimulator(healthy_market).propagate(
        [Shock(SystemKind.SKELETON, 0.5, at_step=0), Shock(SystemKind.CIRCULATORY, 0.9, at_step=5)]
    )
    assert len(trace.steps) > 5
    assert trace.steps[5][SystemKind.CIRCULATORY] > trace.steps[4][SystemKind.CIRCULATORY]
    assert trace.steps[5][SystemKind.CIRCULATORY] >= 0.5


def test_run_extends_to_cover_late_shock(healthy_market: Market):
    # A late shock must fire even though the pre-shock trajectory is already flat.
    trace = ShockSimulator(healthy_market).propagate(Shock(SystemKind.SKELETON, 0.8, at_step=6))
    assert trace.steps[6][SystemKind.SKELETON] >= 0.7


# --- Extension 4: recovery / intervention ----------------------------------


def test_recovery_reduces_total_stress(stressed_market: Market):
    base = ShockSimulator(stressed_market).propagate(Shock(SystemKind.CIRCULATORY, 0.9))
    healed = ShockSimulator(stressed_market, SimulationConfig(recovery_rate=0.1)).propagate(
        Shock(SystemKind.CIRCULATORY, 0.9)
    )
    assert _total_stress(healed) < _total_stress(base)


def test_intervention_improves_resilience(stressed_market: Market):
    sim = ShockSimulator(stressed_market, _CASCADE)
    without = sim.propagate(Shock(SystemKind.NERVOUS, 0.9))
    with_iv = sim.propagate(
        Shock(SystemKind.NERVOUS, 0.9),
        interventions=[Intervention(SystemKind.CIRCULATORY, 0.5, at_step=0)],
    )
    assert without.resilience is not None
    assert with_iv.resilience is not None
    assert with_iv.resilience.value >= without.resilience.value - 1e-9
    assert _total_stress(with_iv) <= _total_stress(without) + 1e-9


def test_a_delayed_intervention_absorbs_less_than_an_immediate_one(stressed_market: Market):
    # Before its at_step the intervention is inactive, so a containment measure
    # that arrives late leaves more total stress behind than the same measure
    # applied from the start -- while still helping relative to no measure.
    sim = ShockSimulator(stressed_market, _CASCADE)
    shock = Shock(SystemKind.NERVOUS, 0.9)
    without = _total_stress(sim.propagate(shock))
    delayed = _total_stress(sim.propagate(shock, interventions=[Intervention(SystemKind.CIRCULATORY, 0.5, at_step=4)]))
    immediate = _total_stress(
        sim.propagate(shock, interventions=[Intervention(SystemKind.CIRCULATORY, 0.5, at_step=0)])
    )
    assert immediate <= delayed + 1e-9
    assert delayed <= without + 1e-9


def test_a_stable_market_can_still_exhaust_the_step_budget(market_factory):
    # `converged` is reported against max_steps, not against stability. This
    # market is decaying steadily but too slowly to settle within 50 steps, so it
    # reports converged=False and a settling time of -1 -- and therefore takes the
    # full settling penalty, exactly as a market that never settles would.
    # Replaces 20 parametrised cases that asserted convergence always holds; it
    # does not, and the property test now covers the invariants that do.
    weak = {"integrity": 0.0, "redundancy": 0.0, "criticality": 0.0, "load": 0.0}
    deps = [
        Dependency(SystemKind.ORGANS, SystemKind.NERVOUS, DependencyKind.STRUCTURAL, 0.598),
        Dependency(SystemKind.SKELETON, SystemKind.MUSCULATURE, DependencyKind.STRUCTURAL, 0.584),
        Dependency(SystemKind.SKELETON, SystemKind.IMMUNE, DependencyKind.STRUCTURAL, 0.462),
        Dependency(SystemKind.IMMUNE, SystemKind.METABOLISM, DependencyKind.STRUCTURAL, 0.842),
        Dependency(SystemKind.METABOLISM, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.945),
        Dependency(SystemKind.MUSCULATURE, SystemKind.NERVOUS, DependencyKind.STRUCTURAL, 0.479),
        Dependency(SystemKind.MUSCULATURE, SystemKind.ORGANS, DependencyKind.STRUCTURAL, 0.668),
        Dependency(SystemKind.MUSCULATURE, SystemKind.IMMUNE, DependencyKind.STRUCTURAL, 0.07),
    ]
    market = market_factory(deps, **{kind.value: weak for kind in SystemKind})
    trace = ShockSimulator(market).propagate(Shock(SystemKind.IMMUNE, 1.0))

    assert trace.converged is False
    assert len(trace.steps) - 1 == SimulationConfig().max_steps
    assert trace.resilience is not None
    assert trace.resilience.settling_time == -1
    # Still decaying when the budget ran out, not oscillating or diverging.
    peaks = [max(step.values()) for step in trace.steps]
    assert peaks[-1] < peaks[-2] < peaks[-3]
    assert peaks[-1] < 0.05


def test_the_step_map_is_not_always_a_contraction(market_factory):
    # Full-weight coupling with almost no absorptive capacity gives a per-step
    # gain of 0.85 * (0.5 + 1.0 * 0.8) = 1.105, so stress grows until it
    # saturates at the clip rather than contracting.
    weak = {"integrity": 0.0, "redundancy": 0.0, "criticality": 0.0, "load": 0.0}
    deps = [
        Dependency(SystemKind.SKELETON, SystemKind.CIRCULATORY, DependencyKind.STRUCTURAL, 1.0),
        Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 1.0),
    ]
    market = market_factory(deps, **{kind.value: weak for kind in SystemKind})
    steps = ShockSimulator(market).propagate(Shock(SystemKind.SKELETON, 1.0)).steps

    # circulatory starts unstressed and is driven up to the clip, not damped down.
    circulatory = [step[SystemKind.CIRCULATORY] for step in steps]
    assert circulatory[0] == pytest.approx(0.0)
    assert circulatory[-1] == pytest.approx(1.0)
    assert max(step[SystemKind.SKELETON] for step in steps) == pytest.approx(1.0)


def test_advance_matches_hand_computed_dynamics(market_factory):
    # Default systems everywhere: absorptive capacity = 0.5*0.5 + 0.3*1.0 + 0.2*1.0 = 0.75.
    # One edge: circulatory depends on skeleton at 0.8, so stress flows skeleton -> circulatory.
    # Defaults: damping 0.85, retention 0.5, transmission 1.0.
    market = market_factory([Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.8)])
    steps = ShockSimulator(market).propagate(Shock(SystemKind.SKELETON, 0.5)).steps

    assert steps[0][SystemKind.SKELETON] == pytest.approx(0.5)
    assert steps[0][SystemKind.CIRCULATORY] == pytest.approx(0.0)

    # skeleton receives nothing: 0.85 * (0.5 * 0.5) = 0.2125
    assert steps[1][SystemKind.SKELETON] == pytest.approx(0.2125)
    # circulatory: 0.85 * (0.5 * 0.8 * 1.0 * (1 - 0.75)) = 0.085
    assert steps[1][SystemKind.CIRCULATORY] == pytest.approx(0.085)
    assert steps[1][SystemKind.NERVOUS] == pytest.approx(0.0)

    # 0.85 * (0.2125 * 0.5) = 0.0903125
    assert steps[2][SystemKind.SKELETON] == pytest.approx(0.0903125)
    # 0.85 * (0.085 * 0.5 + 0.2125 * 0.8 * 0.25) = 0.07225
    assert steps[2][SystemKind.CIRCULATORY] == pytest.approx(0.07225)


def test_dense_fragile_market_amplifies_the_shock(market_factory):
    # The amplification branch of the resilience score is otherwise never exercised.
    score = ShockSimulator(_fragile_dense_market(market_factory)).resilience(Shock(SystemKind.CIRCULATORY, 0.6))

    assert score.amplification_factor > 1.0
    assert score.peak_stress == pytest.approx(1.0)
    assert score.absorbed_fraction == pytest.approx(0.0)
    assert score.severity is Severity.CRITICAL
    # With absorbed == 0 and the amplification penalty saturated at 1, the blend
    # collapses to its settling-time term alone, pinning the whole formula.
    assert score.value == pytest.approx(0.15 * (1.0 - score.settling_time / 50))


def test_shocking_a_hub_is_less_resilient_than_shocking_a_leaf(market_factory):
    profile = ShockSimulator(_hub_market(market_factory)).stress_test(magnitude=0.8)
    # Everything depends on skeleton; nothing depends on metabolism.
    assert profile[SystemKind.SKELETON].value < profile[SystemKind.METABOLISM].value
    assert profile[SystemKind.METABOLISM].amplification_factor == pytest.approx(1.0)
    assert profile[SystemKind.SKELETON].amplification_factor > 1.0


def test_more_redundancy_gives_more_resilience(market_factory):
    deps = [Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.9)]
    shock = Shock(SystemKind.SKELETON, 0.8)
    brittle = ShockSimulator(market_factory(deps, circulatory={"redundancy": 0.0})).resilience(shock)
    robust = ShockSimulator(market_factory(deps, circulatory={"redundancy": 1.0})).resilience(shock)
    assert robust.value > brittle.value


def test_stronger_coupling_gives_less_resilience(market_factory):
    shock = Shock(SystemKind.SKELETON, 0.8)
    weak_link = [Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.1)]
    strong_link = [Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 1.0)]
    loose = ShockSimulator(market_factory(weak_link)).resilience(shock)
    tight = ShockSimulator(market_factory(strong_link)).resilience(shock)
    assert tight.value < loose.value


def test_larger_shocks_never_reduce_peak_stress(stressed_market: Market):
    sim = ShockSimulator(stressed_market)
    peaks = [sim.resilience(Shock(SystemKind.CIRCULATORY, m)).peak_stress for m in (0.2, 0.5, 0.8, 1.0)]
    assert peaks == sorted(peaks)


def test_two_shocks_on_the_same_target_clamp_at_one(stressed_market: Market):
    trace = ShockSimulator(stressed_market).propagate(
        [Shock(SystemKind.SKELETON, 0.7), Shock(SystemKind.SKELETON, 0.8)]
    )
    assert trace.steps[0][SystemKind.SKELETON] == pytest.approx(1.0)


def test_stress_test_labels_each_score_with_its_own_target(stressed_market: Market):
    # A _score that always reported the first shock's target would pass the
    # existing coverage test, which only checks the key set.
    profile = ShockSimulator(stressed_market).stress_test()
    assert all(score.target is kind for kind, score in profile.items())


def test_high_resilience_scores_as_low_severity(market_factory):
    # Severity is from_score(1 - value), so it must invert the resilience. The
    # amplifying test only covers the CRITICAL end, where a sign error looks the
    # same; this pins the other end.
    score = ShockSimulator(market_factory()).resilience(Shock(SystemKind.SKELETON, 0.8))
    assert score.value > 0.9
    assert score.severity is Severity.LOW


def test_absorbed_fraction_is_exact_when_partly_absorbed(market_factory):
    # Absorbed fraction is only ever exactly 1.0 or exactly 0.0 elsewhere in the
    # suite, which leaves `1 - final / injected` under-determined. Truncating the
    # budget stops the decay part-way and pins the formula on a real fraction.
    # Uncoupled defaults decay by damping * retention = 0.85 * 0.5 = 0.425 a step,
    # so after three steps the residual is 0.425**3 of what was injected.
    config = SimulationConfig(max_steps=3)
    score = ShockSimulator(market_factory(), config).resilience(Shock(SystemKind.SKELETON, 0.8))
    assert score.absorbed_fraction == pytest.approx(1.0 - 0.425**3)
    assert 0.0 < score.absorbed_fraction < 1.0
    assert score.amplification_factor == pytest.approx(1.0)


def test_seeded_jitter_perturbs_the_trajectory_by_an_exact_amount(market_factory):
    # The other jitter tests only assert that trajectories differ or repeat, which
    # leaves the perturbation itself unpinned.
    market = market_factory([Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.8)])
    shock = Shock(SystemKind.SKELETON, 0.5)
    jittered = ShockSimulator(market, SimulationConfig(seed=42, jitter=0.05)).propagate(shock)
    assert jittered.steps[1][SystemKind.CIRCULATORY] == pytest.approx(0.08438761609929381)
    # ... against 0.085 with no jitter, i.e. a real but small perturbation.
    plain = ShockSimulator(market).propagate(shock)
    assert plain.steps[1][SystemKind.CIRCULATORY] == pytest.approx(0.085)


def test_jitter_changes_the_trajectory(stressed_market: Market):
    # Without this, test_seeded_jitter_is_reproducible would still pass if jitter
    # were removed from the dynamics entirely.
    jittered = ShockSimulator(stressed_market, SimulationConfig(seed=42, jitter=0.05))
    plain = ShockSimulator(stressed_market, SimulationConfig(seed=42, jitter=0.0))
    shock = Shock(SystemKind.CIRCULATORY, 0.8)
    assert jittered.propagate(shock).steps != plain.propagate(shock).steps


def test_different_seeds_give_different_trajectories(stressed_market: Market):
    shock = Shock(SystemKind.CIRCULATORY, 0.8)
    first = ShockSimulator(stressed_market, SimulationConfig(seed=1, jitter=0.05)).propagate(shock)
    second = ShockSimulator(stressed_market, SimulationConfig(seed=2, jitter=0.05)).propagate(shock)
    assert first.steps != second.steps


def test_jitter_without_a_seed_is_ignored(stressed_market: Market):
    # Deliberate: a diagnostic tool must be reproducible by default, so jitter
    # only applies when a seed makes it deterministic.
    shock = Shock(SystemKind.CIRCULATORY, 0.8)
    unseeded = ShockSimulator(stressed_market, SimulationConfig(jitter=0.5)).propagate(shock)
    plain = ShockSimulator(stressed_market, SimulationConfig(jitter=0.0)).propagate(shock)
    assert unseeded.steps == plain.steps


def test_settling_time_is_first_settled_step(stressed_market: Market):
    # settling_time must be the FIRST step whose change falls below the
    # convergence epsilon: the step before it must still exceed the threshold.
    config = SimulationConfig()
    trace = ShockSimulator(stressed_market, config).propagate(Shock(SystemKind.CIRCULATORY, 0.9))
    st = trace.resilience.settling_time
    assert st > 0

    def delta(i: int) -> float:
        return max(abs(trace.steps[i][k] - trace.steps[i - 1][k]) for k in SystemKind)

    assert delta(st) < config.convergence_eps
    assert delta(st - 1) >= config.convergence_eps


def test_larger_shock_is_no_more_resilient(stressed_market: Market):
    # Resilience is monotonically non-increasing in shock magnitude: a bigger
    # shock takes longer to settle and never scores higher than a smaller one.
    sim = ShockSimulator(stressed_market)
    values = [sim.resilience(Shock(SystemKind.CIRCULATORY, m)).value for m in (0.2, 0.5, 0.9)]
    assert values == sorted(values, reverse=True)


@pytest.mark.parametrize("target", list(SystemKind))
def test_amplification_factor_never_below_one(stressed_market: Market, target: SystemKind):
    # Peak aggregate stress includes the injection step, so the damped model can
    # never report a peak below what was injected: amplification is always >= 1.
    score = ShockSimulator(stressed_market).resilience(Shock(target, 0.8))
    assert score.amplification_factor >= 1.0


@pytest.mark.parametrize(
    ("kwargs", "match"),
    [
        ({"max_steps": 0}, "max_steps must be at least 1"),
        ({"max_steps": -5}, "max_steps must be at least 1"),
        ({"damping": 0.0}, "damping must be in"),
        ({"damping": 5.0}, "damping must be in"),
        ({"damping": float("nan")}, "damping must be in"),
        ({"retention": -3.0}, "retention must be in"),
        ({"retention": 1.5}, "retention must be in"),
        ({"transmission": -2.0}, "transmission must be"),
        ({"transmission": float("inf")}, "transmission must be"),
        ({"convergence_eps": 0.0}, "convergence_eps must be"),
        ({"convergence_eps": -1.0}, "convergence_eps must be"),
        ({"jitter": -1.0}, "jitter must be"),
        ({"jitter": float("nan")}, "jitter must be"),
        ({"cascade_threshold": 0.0}, "cascade_threshold must be"),
        ({"cascade_threshold": 1.0}, "cascade_threshold must be"),
        ({"cascade_threshold": float("nan")}, "cascade_threshold must be"),
        ({"cascade_gain": -0.5}, "cascade_gain must be"),
        ({"cascade_gain": float("inf")}, "cascade_gain must be"),
        ({"cascade_absorption_drop": -0.1}, "cascade_absorption_drop must be"),
        ({"cascade_absorption_drop": 1.5}, "cascade_absorption_drop must be"),
        ({"recovery_rate": -0.1}, "recovery_rate must be"),
        ({"recovery_rate": 2.0}, "recovery_rate must be"),
    ],
)
def test_simulation_config_rejects_out_of_range_parameters(kwargs: dict[str, float], match: str):
    # Each of these used to be accepted and produce a plausible-looking but
    # meaningless trajectory: max_steps=0 reported a market as never settling
    # without simulating a single step, damping=5.0 amplified every step
    # globally, and a negative transmission inverted the direction of stress.
    with pytest.raises(InvalidConfigError, match=match):
        SimulationConfig(**kwargs)


def test_simulation_config_accepts_its_documented_boundaries():
    # The validation must not narrow the supported range: damping of exactly 1
    # (no global decay), zero retention, zero transmission and zero jitter are
    # all meaningful settings.
    config = SimulationConfig(max_steps=1, damping=1.0, retention=0.0, transmission=0.0, jitter=0.0)
    assert config.damping == 1.0
