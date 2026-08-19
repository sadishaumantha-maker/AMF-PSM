"""Unit tests for the shock-propagation simulation engine."""

from __future__ import annotations

import random

import pytest

from amf.errors import InvalidShockError
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
