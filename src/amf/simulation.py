"""Shock-propagation simulation engine.

The :class:`ShockSimulator` models how a *structural* stress injected into one
system cascades through the dependency graph and whether the market's anatomy
absorbs or amplifies it. The single state variable is **stress** -- a
dimensionless load in ``[0, 1]`` -- not a price, return, or order.

By default the dynamics are a damped, capacity-gated **linear diffusion**. For a
stress vector ``x_t`` over the seven systems, coupling matrix ``W`` (entry
``W[i][j]`` is the stress transmitted from ``i`` to ``j``) and per-system
absorptive capacity ``a_j``::

    incoming_j  = sum_i  x_t[i] * W[i][j] * transmission
    x_{t+1}[j]  = clip( damping * (x_t[j] * retention + incoming_j * (1 - a_j)), 0, 1 )

Damping and absorptive capacity pull the trajectory down, but they do not make
the step map a contraction for every market: where a system has enough incoming
weight and little capacity to absorb it, the per-step gain exceeds one and stress
grows until it saturates at the ``1.0`` clip. Settling is therefore reported
against the step budget rather than promised in advance -- see
:attr:`SimulationConfig.max_steps` and :attr:`~amf.models.SimulationTrace.converged`.

Four **opt-in** extensions enrich this (all off by default, so the linear model
above is reproduced exactly unless configured):

* **Threshold / cascade dynamics** (``cascade_threshold``): a system whose stress
  exceeds the threshold becomes *impaired* -- it transmits amplified stress and
  absorbs less -- producing tipping and self-reinforcing cascades. This nonlinear
  regime can settle at a persistent non-zero fixed point and pushes the per-step
  gain higher still; the ``max_steps`` budget and ``[0, 1]`` clipping keep it
  bounded.
* **Recovery** (``recovery_rate``): an active per-step healing term.
* **Time-scheduled shocks** (:attr:`~amf.models.Shock.at_step`): inject a shock at a
  later timestep to model a second wave.
* **Interventions** (:class:`~amf.models.Intervention`): time-gated boosts to a
  system's absorptive capacity, modelling containment measures.

The engine also offers a seeded **Monte Carlo ensemble** (:meth:`ShockSimulator.
ensemble`) that summarises resilience over many jittered replications.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from amf.errors import InvalidConfigError, InvalidShockError
from amf.invariants import check_simulation_trace
from amf.models import (
    Intervention,
    MetricStats,
    ResilienceDistribution,
    ResilienceScore,
    Severity,
    Shock,
    SimulationTrace,
    SystemKind,
)
from amf.numeric import clip_unit, stable_sum

if TYPE_CHECKING:
    from collections.abc import Sequence

    from amf.market import Market

_ORDER: tuple[SystemKind, ...] = tuple(SystemKind)


@dataclass(frozen=True, slots=True)
class SimulationConfig:
    """Parameters controlling the shock-propagation dynamics.

    Every parameter is validated on construction: an out-of-range knob otherwise
    produces a plausible-looking but meaningless trajectory rather than an error
    (a negative ``transmission`` inverts stress flow, a ``damping`` above one
    amplifies every step globally, a ``max_steps`` of zero reports a market as
    never settling without simulating anything).

    Attributes:
        max_steps: Maximum number of timesteps to simulate, at least ``1``. A
            trajectory that is still decaying when the budget runs out is
            reported as not converged, with a settling time of ``-1``; a market
            can be perfectly stable and still exhaust the budget if it settles
            slowly.
        damping: Global per-step decay in ``(0, 1]``; lower means faster dissipation.
        retention: Fraction of a system's own stress carried to the next step, in
            ``[0, 1]``.
        transmission: Global scaler on stress transmitted along couplings; finite
            and non-negative.
        convergence_eps: L-infinity change below which the trajectory is settled;
            strictly positive, since a non-positive threshold can never be met.
        seed: If set, enables small deterministic Gaussian jitter on transmission.
        jitter: Standard deviation of the optional transmission jitter; finite and
            non-negative. Has no effect unless ``seed`` is also set: a diagnostic
            tool stays reproducible by default, so jitter is only applied when a
            seed makes it deterministic.
        cascade_threshold: If set (in ``(0, 1)``), enables nonlinear cascade
            dynamics: a system whose stress exceeds this value is impaired.
        cascade_gain: Extra fractional transmission from an impaired system.
        cascade_absorption_drop: Fraction by which an impaired system's absorptive
            capacity is reduced.
        recovery_rate: Active per-step reduction of every system's stress (healing).
    """

    max_steps: int = 50
    damping: float = 0.85
    retention: float = 0.5
    transmission: float = 1.0
    convergence_eps: float = 1e-4
    seed: int | None = None
    jitter: float = 0.0
    cascade_threshold: float | None = None
    cascade_gain: float = 0.5
    cascade_absorption_drop: float = 0.5
    recovery_rate: float = 0.0

    def __post_init__(self) -> None:
        """Validate the dynamics parameters on construction.

        Raises:
            InvalidConfigError: If any parameter is outside its documented range.
        """
        if self.max_steps < 1:
            msg = f"max_steps must be at least 1, got {self.max_steps!r}"
            raise InvalidConfigError(msg)
        if not math.isfinite(self.damping) or not 0.0 < self.damping <= 1.0:
            msg = f"damping must be in (0, 1], got {self.damping!r}"
            raise InvalidConfigError(msg)
        if not math.isfinite(self.retention) or not 0.0 <= self.retention <= 1.0:
            msg = f"retention must be in [0, 1], got {self.retention!r}"
            raise InvalidConfigError(msg)
        if not math.isfinite(self.transmission) or self.transmission < 0.0:
            msg = f"transmission must be a finite, non-negative number, got {self.transmission!r}"
            raise InvalidConfigError(msg)
        if not math.isfinite(self.convergence_eps) or self.convergence_eps <= 0.0:
            msg = f"convergence_eps must be a finite, positive number, got {self.convergence_eps!r}"
            raise InvalidConfigError(msg)
        if not math.isfinite(self.jitter) or self.jitter < 0.0:
            msg = f"jitter must be a finite, non-negative number, got {self.jitter!r}"
            raise InvalidConfigError(msg)
        if self.cascade_threshold is not None and (
            not math.isfinite(self.cascade_threshold) or not 0.0 < self.cascade_threshold < 1.0
        ):
            msg = f"cascade_threshold must be None or in (0, 1), got {self.cascade_threshold!r}"
            raise InvalidConfigError(msg)
        if not math.isfinite(self.cascade_gain) or self.cascade_gain < 0.0:
            msg = f"cascade_gain must be a finite, non-negative number, got {self.cascade_gain!r}"
            raise InvalidConfigError(msg)
        if not math.isfinite(self.cascade_absorption_drop) or not 0.0 <= self.cascade_absorption_drop <= 1.0:
            msg = f"cascade_absorption_drop must be in [0, 1], got {self.cascade_absorption_drop!r}"
            raise InvalidConfigError(msg)
        if not math.isfinite(self.recovery_rate) or not 0.0 <= self.recovery_rate <= 1.0:
            msg = f"recovery_rate must be in [0, 1], got {self.recovery_rate!r}"
            raise InvalidConfigError(msg)


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
        self._crit_total = stable_sum(self._criticality.values()) or 1.0

    def propagate(
        self,
        shock: Shock | list[Shock],
        interventions: Sequence[Intervention] = (),
    ) -> SimulationTrace:
        """Propagate one or more shocks and return the full trajectory.

        Args:
            shock: A single shock or a list. Shocks with ``at_step == 0`` are applied
                at the start; those with a later ``at_step`` are injected then.
            interventions: Optional containment measures that boost a system's
                absorptive capacity from their ``at_step`` onward.

        Returns:
            A :class:`SimulationTrace` including per-step stress and resilience.

        Raises:
            InvalidShockError: If any shock magnitude is outside ``(0, 1]``.
        """
        shocks = [shock] if isinstance(shock, Shock) else list(shock)
        if not shocks:
            msg = "at least one shock is required"
            raise InvalidShockError(msg)
        for sk in shocks:
            if not 0.0 < sk.magnitude <= 1.0:
                msg = f"shock magnitude must be in (0, 1], got {sk.magnitude!r}"
                raise InvalidShockError(msg)

        # Total injected load (timing-independent) gives a stable denominator for
        # the amplification and absorption metrics.
        injected_vec = dict.fromkeys(_ORDER, 0.0)
        for sk in shocks:
            injected_vec[sk.target] = min(1.0, injected_vec[sk.target] + sk.magnitude)
        injected = self._aggregate(injected_vec)

        state: dict[SystemKind, float] = dict.fromkeys(_ORDER, 0.0)
        for sk in shocks:
            if sk.at_step <= 0:
                state[sk.target] = min(1.0, state[sk.target] + sk.magnitude)

        rng = random.Random(self.config.seed) if self.config.seed is not None else None
        threshold = self.config.cascade_threshold
        tipped: set[SystemKind] = set()

        def record_tips(vector: dict[SystemKind, float]) -> None:
            if threshold is not None:
                tipped.update(k for k in _ORDER if vector[k] > threshold)

        steps: list[dict[SystemKind, float]] = [dict(state)]
        record_tips(state)

        last_injection = max((sk.at_step for sk in shocks), default=0)
        horizon = max(self.config.max_steps, last_injection)
        converged = False

        for step in range(1, horizon + 1):
            nxt = self._advance(state, step, rng, interventions)
            for sk in shocks:
                if sk.at_step == step:
                    nxt[sk.target] = min(1.0, nxt[sk.target] + sk.magnitude)
            steps.append(nxt)
            record_tips(nxt)
            delta = max(abs(nxt[k] - state[k]) for k in _ORDER)
            state = nxt
            if delta < self.config.convergence_eps and step >= last_injection:
                converged = True
                break

        tipped_systems = tuple(k for k in _ORDER if k in tipped)
        resilience = self._score(shocks, steps, injected, tipped_systems, horizon)
        return check_simulation_trace(
            SimulationTrace(
                shocks=tuple(shocks),
                steps=tuple(steps),
                converged=converged,
                resilience=resilience,
            )
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

    def ensemble(
        self,
        shock: Shock,
        runs: int = 100,
        base_seed: int = 0,
        jitter: float = 0.05,
    ) -> ResilienceDistribution:
        """Run a seeded Monte Carlo ensemble and summarise the resilience spread.

        Each replication reuses this simulator's configuration but with transmission
        jitter and a distinct derived seed (``base_seed + i``), so the whole ensemble
        is reproducible.

        Args:
            shock: The shock to replicate.
            runs: Number of replications (``>= 1``).
            base_seed: Seed offset; replication ``i`` uses ``base_seed + i``.
            jitter: Standard deviation of the per-replication transmission jitter.

        Returns:
            A :class:`ResilienceDistribution` over the replications.

        Raises:
            InvalidShockError: If ``runs`` is less than 1.
        """
        if runs < 1:
            msg = f"runs must be >= 1, got {runs}"
            raise InvalidShockError(msg)
        scores = [
            ShockSimulator(self.market, replace(self.config, seed=base_seed + i, jitter=jitter)).resilience(shock)
            for i in range(runs)
        ]
        return ResilienceDistribution(
            target=shock.target,
            runs=runs,
            value=_stats([s.value for s in scores]),
            amplification_factor=_stats([s.amplification_factor for s in scores]),
            peak_stress=_stats([s.peak_stress for s in scores]),
            absorbed_fraction=_stats([s.absorbed_fraction for s in scores]),
        )

    def _advance(
        self,
        state: dict[SystemKind, float],
        step: int,
        rng: random.Random | None,
        interventions: Sequence[Intervention],
    ) -> dict[SystemKind, float]:
        """Compute the next stress vector from the current one."""
        cfg = self.config
        threshold = cfg.cascade_threshold

        # Effective absorptive capacity per system: base, raised by any active
        # intervention, lowered if the system is impaired under cascade dynamics.
        a_eff = dict(self._absorption)
        for iv in interventions:
            if step >= iv.at_step:
                a_eff[iv.target] = min(1.0, a_eff[iv.target] + iv.absorptive_boost)

        nxt: dict[SystemKind, float] = {}
        for receiver in _ORDER:
            recv_abs = a_eff[receiver]
            if threshold is not None and state[receiver] > threshold:
                recv_abs *= 1.0 - cfg.cascade_absorption_drop
            # Terms are collected and reduced with ``stable_sum`` rather than
            # accumulated with ``+=``. Iteration stays in declaration order and
            # still draws jitter only for live couplings, so a seeded run
            # consumes exactly the same random stream as before.
            terms: list[float] = []
            for transmitter in _ORDER:
                weight = self._coupling.get(transmitter, receiver)
                if weight <= 0.0:
                    continue
                factor = cfg.transmission
                if rng is not None and cfg.jitter > 0.0:
                    factor = max(0.0, factor + rng.gauss(0.0, cfg.jitter))
                if threshold is not None and state[transmitter] > threshold:
                    factor *= 1.0 + cfg.cascade_gain
                terms.append(state[transmitter] * weight * factor)
            incoming = stable_sum(terms)
            value = cfg.damping * (state[receiver] * cfg.retention + incoming * (1.0 - recv_abs))
            if cfg.recovery_rate > 0.0:
                value -= cfg.recovery_rate
            nxt[receiver] = clip_unit(value)
        return nxt

    def _aggregate(self, state: dict[SystemKind, float]) -> float:
        """Return the criticality-weighted aggregate stress in ``[0, 1]``."""
        return stable_sum(self._criticality[k] * state[k] for k in _ORDER) / self._crit_total

    def _score(
        self,
        shocks: list[Shock],
        steps: list[dict[SystemKind, float]],
        injected: float,
        tipped_systems: tuple[SystemKind, ...],
        horizon: int,
    ) -> ResilienceScore:
        """Derive resilience metrics from a completed trajectory.

        Args:
            shocks: The shocks that were applied.
            steps: The recorded stress vectors, one per timestep.
            injected: Total injected load, used as the timing-independent
                denominator for absorption and amplification.
            tipped_systems: Systems that crossed the cascade threshold.
            horizon: The number of steps the run was actually allowed, which is
                ``max(max_steps, last injection step)``. The settling penalty is
                measured against this rather than against ``max_steps``: a
                multi-wave run extends the horizon past the budget, and dividing
                by the shorter one produced a penalty above ``1`` and drove the
                settling term of the composite negative.
        """
        aggregates = [self._aggregate(s) for s in steps]
        peak = max(aggregates)
        final = aggregates[-1]

        absorbed = clip_unit(1.0 - (final / injected) if injected > 0.0 else 1.0)
        amplification = peak / injected if injected > 0.0 else 1.0

        settling_time = self._settling_time(steps)
        amp_penalty = clip_unit(amplification - 1.0)
        settle_penalty = clip_unit(settling_time / horizon) if settling_time >= 0 else 1.0
        value = clip_unit(0.6 * absorbed + 0.25 * (1.0 - amp_penalty) + 0.15 * (1.0 - settle_penalty))

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
            tipped_systems=tipped_systems,
        )

    def _settling_time(self, steps: list[dict[SystemKind, float]]) -> int:
        """Return the first step index at which the trajectory settled, else ``-1``."""
        eps = self.config.convergence_eps
        for i in range(1, len(steps)):
            delta = max(abs(steps[i][k] - steps[i - 1][k]) for k in _ORDER)
            if delta < eps:
                return i
        return -1


def _percentile(sorted_values: list[float], q: float) -> float:
    """Return the ``q``-th percentile of an ascending list by linear interpolation."""
    if len(sorted_values) == 1:
        return sorted_values[0]
    rank = (q / 100.0) * (len(sorted_values) - 1)
    lo = math.floor(rank)
    hi = math.ceil(rank)
    if lo == hi:
        return sorted_values[lo]
    frac = rank - lo
    return sorted_values[lo] * (1.0 - frac) + sorted_values[hi] * frac


def _stats(values: list[float]) -> MetricStats:
    """Summarise a list of metric samples as a :class:`MetricStats`."""
    ordered = sorted(values)
    mean = sum(ordered) / len(ordered)
    return MetricStats(
        mean=mean,
        minimum=ordered[0],
        maximum=ordered[-1],
        p10=_percentile(ordered, 10.0),
        p50=_percentile(ordered, 50.0),
        p90=_percentile(ordered, 90.0),
    )
