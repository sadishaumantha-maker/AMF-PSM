"""Example: propagate a capital-flow shock and inspect systemic resilience.

Run with::

    python examples/liquidity_shock.py
"""

from __future__ import annotations

from amf import Shock, ShockSimulator, SystemKind
from amf.report import render_stress_test, render_text
from equity_market import build_market


def main() -> None:
    """Shock the circulatory system, then run a full systemic stress test."""
    market = build_market()
    simulator = ShockSimulator(market)

    shock = Shock(target=SystemKind.CIRCULATORY, magnitude=0.85, label="liquidity withdrawal")
    trace = simulator.propagate(shock)
    print(render_text(trace))
    print()
    print(render_stress_test(simulator.stress_test(magnitude=0.8)))


if __name__ == "__main__":
    main()
