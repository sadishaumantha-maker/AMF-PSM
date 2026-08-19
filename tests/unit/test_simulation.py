"""Unit tests for the shock-propagation simulation engine."""

from __future__ import annotations

import random

import pytest

from amf.errors import InvalidShockError
from amf.market import Market
from amf.models import Intervention, Shock, SystemKind
from amf.simulation import ShockSimulator, SimulationConfig


def _total_stress(trace) -> float:
    """Sum of stress across every system and timestep of a trace."""
    return sum(v for step in trace.steps for v in step.values())


_CASCADE = SimulationConfig(cascade_threshold=0.2, cascade_gain=1.0)


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
