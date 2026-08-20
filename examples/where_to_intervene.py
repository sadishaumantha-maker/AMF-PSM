"""Example: find which structural metrics the diagnosis is most sensitive to.

Sweeps every metric of every system, ranks them by how steeply the overall
weakness index responds, and lists the adjustments that would improve the index
most. The numbers describe this illustrative model only.

Run with::

    python examples/where_to_intervene.py
"""

from __future__ import annotations

from amf import SensitivityAnalyzer, SensitivityConfig
from amf.report import render_text
from equity_market import build_market


def main() -> None:
    """Rank metric sensitivities and candidate interventions for the sample market."""
    market = build_market()

    # A larger step describes a more substantial intervention than the default.
    analyzer = SensitivityAnalyzer(config=SensitivityConfig(step=0.1))
    report = analyzer.analyse(market)
    print(render_text(report))

    if report.leverage_points:
        best = report.leverage_points[0]
        print()
        print(
            f"Largest single improvement: raise {best.system.value} {best.metric.value} "
            f"from {best.baseline_value:.2f} to {best.adjusted_value:.2f}, "
            f"moving the index {best.index_before:.3f} -> {best.index_after:.3f}."
        )


if __name__ == "__main__":
    main()
