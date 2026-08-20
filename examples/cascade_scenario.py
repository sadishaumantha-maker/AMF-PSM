"""Example: the extended simulation -- cascade, multi-wave, ensemble, intervention.

Run with::

    python examples/cascade_scenario.py
"""

from __future__ import annotations

from amf import (
    Intervention,
    Shock,
    ShockSimulator,
    SimulationConfig,
    SystemKind,
)
from amf.report import render_distribution, render_text
from equity_market import build_market


def main() -> None:
    """Contrast linear vs. cascade dynamics, then show multi-wave and ensemble."""
    market = build_market()
    shock = Shock(target=SystemKind.CIRCULATORY, magnitude=0.9, label="liquidity freeze")

    # 1. Linear (default) vs. nonlinear cascade dynamics.
    linear = ShockSimulator(market).propagate(shock)
    cascade_cfg = SimulationConfig(cascade_threshold=0.2, cascade_gain=1.0)
    cascade = ShockSimulator(market, cascade_cfg).propagate(shock)
    print("== Linear dynamics ==")
    print(render_text(linear))
    print("\n== Cascade dynamics (opt-in) ==")
    print(render_text(cascade))

    # 2. A second wave hitting a still-stressed market.
    print("\n== Multi-wave (second shock at step 5) ==")
    multi = ShockSimulator(market).propagate(
        [shock, Shock(SystemKind.NERVOUS, 0.8, at_step=5, label="information shock")]
    )
    print(render_text(multi))

    # 3. Containment: boost the circulatory system's absorptive capacity.
    print("\n== Intervention comparison (cascade) ==")
    sim = ShockSimulator(market, cascade_cfg)
    contained = sim.propagate(shock, interventions=[Intervention(SystemKind.CIRCULATORY, 0.5)])
    assert cascade.resilience is not None
    assert contained.resilience is not None
    print(f"  resilience without intervention: {cascade.resilience.value:.3f}")
    print(f"  resilience with intervention:    {contained.resilience.value:.3f}")

    # 4. Monte Carlo ensemble over jittered replications.
    print("\n== Monte Carlo ensemble ==")
    dist = ShockSimulator(market).ensemble(shock, runs=200, base_seed=0, jitter=0.05)
    print(render_distribution(dist))


if __name__ == "__main__":
    main()
