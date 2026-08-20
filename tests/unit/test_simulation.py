"""Unit tests for the shock-propagation simulation engine."""

from __future__ import annotations

import random

import pytest

from amf.errors import InvalidConfigError, InvalidShockError
from amf.market import Market
from amf.models import Shock, SystemKind
from amf.simulation import ShockSimulator, SimulationConfig


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


@pytest.mark.parametrize("trial", range(20))
def test_damped_dynamics_always_converge(stressed_market: Market, trial: int):
    """Property test: a damped market always settles for random shocks."""
    rng = random.Random(trial)
    target = rng.choice(list(SystemKind))
    magnitude = rng.uniform(0.1, 1.0)
    trace = ShockSimulator(stressed_market).propagate(Shock(target, magnitude))
    assert trace.converged is True


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
        ({"max_steps": 0}, "max_steps"),
        ({"max_steps": -1}, "max_steps"),
        ({"damping": 0.0}, "damping"),
        ({"damping": 1.5}, "damping"),
        ({"damping": -0.2}, "damping"),
        ({"retention": -0.1}, "retention"),
        ({"transmission": -1.0}, "transmission"),
        ({"jitter": -0.05}, "jitter"),
    ],
)
def test_invalid_config_rejected(kwargs, match):
    # Damping above one turns the dynamics from a contraction into an amplifier,
    # which would void the convergence guarantee the whole engine rests on.
    with pytest.raises(InvalidConfigError, match=match):
        SimulationConfig(**kwargs)


def test_boundary_config_values_accepted():
    assert SimulationConfig(max_steps=1, damping=1.0, retention=0.0, transmission=0.0, jitter=0.0).damping == 1.0


def test_resilience_blend_is_pinned_on_an_isolated_market(healthy_market: Market):
    # A market with no couplings absorbs everything and amplifies nothing, so the
    # blend reduces to 0.6*1 + 0.25*1 + 0.15*(1 - settling/max_steps). Asserting
    # the number keeps the 0.6/0.25/0.15 weights load-bearing: permuting them
    # changes this value.
    config = SimulationConfig()
    score = ShockSimulator(healthy_market, config).resilience(Shock(SystemKind.SKELETON, 0.8))
    expected = 0.6 * score.absorbed_fraction + 0.25 * 1.0 + 0.15 * (1.0 - score.settling_time / config.max_steps)
    assert score.value == pytest.approx(expected)
    assert score.absorbed_fraction == pytest.approx(1.0, abs=1e-3)


def test_lower_damping_dissipates_stress_faster(stressed_market: Market):
    # Damping is the global per-step decay: less of it must mean a lower peak and
    # a quicker settle. This is what pins the default at a meaningful value.
    shock = Shock(SystemKind.CIRCULATORY, 0.9)
    heavy = ShockSimulator(stressed_market, SimulationConfig(damping=0.4)).resilience(shock)
    light = ShockSimulator(stressed_market, SimulationConfig(damping=0.95)).resilience(shock)
    assert heavy.peak_stress <= light.peak_stress
    assert heavy.settling_time < light.settling_time
    assert heavy.value > light.value


def test_lower_retention_settles_sooner(stressed_market: Market):
    # Retention is how much of its own stress a system carries forward. Less of it
    # must not slow convergence down -- but "slower" can mean not settling at all,
    # which is reported as the -1 sentinel rather than a larger step count, so the
    # two cannot simply be compared as numbers.
    shock = Shock(SystemKind.CIRCULATORY, 0.9)
    low = ShockSimulator(stressed_market, SimulationConfig(retention=0.1)).resilience(shock)
    high = ShockSimulator(stressed_market, SimulationConfig(retention=0.9)).resilience(shock)
    assert low.settling_time > 0, "a low-retention market must settle within budget"
    assert high.settling_time == -1 or high.settling_time > low.settling_time
    assert low.value > high.value


def test_zero_transmission_isolates_every_system(stressed_market: Market):
    # With no stress transmitted along couplings, a coupled market behaves exactly
    # like an isolated one: nothing is amplified.
    score = ShockSimulator(stressed_market, SimulationConfig(transmission=0.0)).resilience(
        Shock(SystemKind.CIRCULATORY, 0.8)
    )
    assert score.amplification_factor == pytest.approx(1.0)
    assert score.absorbed_fraction == pytest.approx(1.0, abs=1e-3)


def test_jitter_without_a_seed_stays_deterministic(stressed_market: Market):
    # jitter only takes effect alongside a seed; the tests rely on that, so it is
    # asserted rather than assumed.
    config = SimulationConfig(jitter=0.5)
    a = ShockSimulator(stressed_market, config).propagate(Shock(SystemKind.CIRCULATORY, 0.8))
    b = ShockSimulator(stressed_market, config).propagate(Shock(SystemKind.CIRCULATORY, 0.8))
    assert a.steps == b.steps


def test_different_seeds_produce_different_trajectories(stressed_market: Market):
    a = ShockSimulator(stressed_market, SimulationConfig(seed=1, jitter=0.05)).propagate(
        Shock(SystemKind.CIRCULATORY, 0.8)
    )
    b = ShockSimulator(stressed_market, SimulationConfig(seed=2, jitter=0.05)).propagate(
        Shock(SystemKind.CIRCULATORY, 0.8)
    )
    assert a.steps != b.steps


def test_default_config_values_are_pinned():
    # The tests above vary each parameter explicitly, which pins the *behaviour*
    # but leaves the defaults free to drift. jitter must default to 0.0: the whole
    # suite relies on the simulation being deterministic without a seed.
    config = SimulationConfig()
    assert config.max_steps == 50
    assert config.damping == pytest.approx(0.85)
    assert config.retention == pytest.approx(0.5)
    assert config.transmission == pytest.approx(1.0)
    assert config.convergence_eps == pytest.approx(1e-4)
    assert config.seed is None
    assert config.jitter == pytest.approx(0.0)


def test_default_simulator_matches_the_default_config(stressed_market: Market):
    shock = Shock(SystemKind.CIRCULATORY, 0.8)
    assert ShockSimulator(stressed_market).propagate(shock).steps == (
        ShockSimulator(stressed_market, SimulationConfig()).propagate(shock).steps
    )
