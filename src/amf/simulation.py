"""Shock-propagation simulation engine.

The :class:`ShockSimulator` models how a *structural* stress injected into one
system cascades through the dependency graph and whether the market's anatomy
absorbs or amplifies it. The single state variable is **stress** -- a
dimensionless load in ``[0, 1]`` -- not a price, return, or order. The dynamics
are a damped, capacity-gated linear diffusion that is guaranteed to converge.

For a stress vector ``x_t`` over the seven systems, coupling matrix ``W`` (entry
``W[i][j]`` is the stress transmitted from ``i`` to ``j``) and per-system
absorptive capacity ``a_j``::

    incoming_j  = sum_i  x_t[i] * W[i][j] * transmission
    x_{t+1}[j]  = clip( damping * (x_t[j] * retention + incoming_j * (1 - a_j)), 0, 1 )

iterated until the trajectory settles or a step budget is exhausted.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING

from amf.errors import InvalidShockError
from amf.models import (
    ResilienceScore,
    Severity,
    Shock,
    SimulationTrace,
    SystemKind,
)

if TYPE_CHECKING:
    from amf.market import Market

_ORDER: tuple[SystemKind, ...] = tuple(SystemKind)


@dataclass(frozen=True, slots=True)
class SimulationConfig:
    """Parameters controlling the shock-propagation dynamics.

    Attributes:
        max_steps: Maximum number of timesteps to simulate.
        damping: Global per-step decay in ``(0, 1]``; lower means faster dissipation.
        retention: Fraction of a system's own stress carried to the next step.
        transmission: Global scaler on stress transmitted along couplings.
        convergence_eps: L-infinity change below which the trajectory is settled.
        seed: If set, enables small deterministic Gaussian jitter on transmission.
        jitter: Standard deviation of the optional transmission jitter.
    """

    max_steps: int = 50
    damping: float = 0.85
    retention: float = 0.5
    transmission: float = 1.0
    convergence_eps: float = 1e-4
    seed: int | None = None
    jitter: float = 0.0


class ShockSimulator:
    """Propagates structural shocks through a market's dependency graph."""

    def __init__(self, market: Market, config: SimulationConfig | None = None) -> None:
        """Initialise the simulator.

        Args:
            market: The market to simulate (must be complete).
            config: Dynamics parameters; defaults to :class:`SimulationConfig`.
        """
        market.require_complete()
        self.market = market
        self.config = config or SimulationConfig()
        self._coupling = market.graph.coupling_matrix()
        self._absorption = {k: market.system(k).absorptive_capacity() for k in _ORDER}
        self._criticality = {k: market.system(k).criticality for k in _ORDER}
        self._crit_total = sum(self._criticality.values()) or 1.0

    def propagate(self, shock: Shock | list[Shock]) -> SimulationTrace:
        """Propagate one or more shocks and return the full trajectory.

        Args:
            shock: A single shock or a list applied simultaneously at ``t = 0``.

        Returns:
            A :class:`SimulationTrace` including per-step stress and resilience.

        Raises:
            InvalidShockError: If any shock magnitude is outside ``(0, 1]``.
        """
        shocks = [shock] if isinstance(shock, Shock) else list(shock)
        if not shocks:
            msg = "at least one shock is required"
            raise InvalidShockError(msg)

        state: dict[SystemKind, float] = dict.fromkeys(_ORDER, 0.0)
        for sk in shocks:
            if not 0.0 < sk.magnitude <= 1.0:
                msg = f"shock magnitude must be in (0, 1], got {sk.magnitude!r}"
                raise InvalidShockError(msg)
            state[sk.target] = min(1.0, state[sk.target] + sk.magnitude)

        rng = random.Random(self.config.seed) if self.config.seed is not None else None
        steps: list[dict[SystemKind, float]] = [dict(state)]
        injected = self._aggregate(state)
        converged = False

        for _ in range(self.config.max_steps):
            nxt = self._advance(state, rng)
            steps.append(nxt)
            delta = max(abs(nxt[k] - state[k]) for k in _ORDER)
            state = nxt
            if delta < self.config.convergence_eps:
                converged = True
                break

        resilience = self._score(shocks, steps, injected)
        return SimulationTrace(
            shocks=tuple(shocks),
            steps=tuple(steps),
            converged=converged,
            resilience=resilience,
        )

    def resilience(self, shock: Shock) -> ResilienceScore:
        """Return just the resilience metrics for a single shock."""
        trace = self.propagate(shock)
        assert trace.resilience is not None  # propagate always populates it
        return trace.resilience

    def stress_test(self, magnitude: float = 0.8) -> dict[SystemKind, ResilienceScore]:
        """Shock each system in turn and return the systemic resilience profile.

        Args:
            magnitude: The stress magnitude applied to each system.

        Returns:
            A mapping from shocked system to its :class:`ResilienceScore`.
        """
        return {
            kind: self.resilience(Shock(target=kind, magnitude=magnitude, label=f"stress-{kind.value}"))
            for kind in _ORDER
        }

    def _advance(self, state: dict[SystemKind, float], rng: random.Random | None) -> dict[SystemKind, float]:
        """Compute the next stress vector from the current one."""
        cfg = self.config
        nxt: dict[SystemKind, float] = {}
        for receiver in _ORDER:
            incoming = 0.0
            for transmitter in _ORDER:
                weight = self._coupling.get(transmitter, receiver)
                if weight <= 0.0:
                    continue
                factor = cfg.transmission
                if rng is not None and cfg.jitter > 0.0:
                    factor = max(0.0, factor + rng.gauss(0.0, cfg.jitter))
                incoming += state[transmitter] * weight * factor
            value = cfg.damping * (state[receiver] * cfg.retention + incoming * (1.0 - self._absorption[receiver]))
            nxt[receiver] = min(1.0, max(0.0, value))
        return nxt

    def _aggregate(self, state: dict[SystemKind, float]) -> float:
        """Return the criticality-weighted aggregate stress in ``[0, 1]``."""
        return sum(self._criticality[k] * state[k] for k in _ORDER) / self._crit_total

    def _score(
        self,
        shocks: list[Shock],
        steps: list[dict[SystemKind, float]],
        injected: float,
    ) -> ResilienceScore:
        """Derive resilience metrics from a completed trajectory."""
        aggregates = [self._aggregate(s) for s in steps]
        peak = max(aggregates)
        final = aggregates[-1]

        absorbed = 1.0 - (final / injected) if injected > 0.0 else 1.0
        absorbed = min(1.0, max(0.0, absorbed))
        amplification = peak / injected if injected > 0.0 else 1.0

        settling_time = self._settling_time(steps)
        amp_penalty = min(1.0, max(0.0, amplification - 1.0))
        settle_penalty = settling_time / self.config.max_steps if settling_time >= 0 else 1.0
        value = min(
            1.0,
            max(0.0, 0.6 * absorbed + 0.25 * (1.0 - amp_penalty) + 0.15 * (1.0 - settle_penalty)),
        )

        # Pick the dominant shock target for labelling the score.
        target = max(shocks, key=lambda s: s.magnitude).target
        return ResilienceScore(
            target=target,
            value=value,
            severity=Severity.from_score(1.0 - value),
            peak_stress=peak,
            settling_time=settling_time,
            absorbed_fraction=absorbed,
            amplification_factor=amplification,
        )

    def _settling_time(self, steps: list[dict[SystemKind, float]]) -> int:
        """Return the first step index at which the trajectory settled, else ``-1``."""
        eps = self.config.convergence_eps
        for i in range(1, len(steps)):
            delta = max(abs(steps[i][k] - steps[i - 1][k]) for k in _ORDER)
            if delta < eps:
                return i
        return -1
