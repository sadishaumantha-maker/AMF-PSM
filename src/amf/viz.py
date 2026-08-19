"""Dependency-free visual renderers for markets and simulation traces.

Like :mod:`amf.report`, everything here is a pure formatting helper: each
function takes a :class:`~amf.market.Market` or a result object and returns a
string -- Graphviz DOT, Mermaid, or a self-contained SVG document -- performing
no I/O. The SVG renderers lay the seven systems out on a circle and draw the
stress timeline with nothing but the standard library, so the package stays
free of third-party dependencies.

All colours encode *structural* quantities only (severity bands, coupling
kinds, dimensionless stress); there is nothing financial in these pictures.
"""

from __future__ import annotations

import math
from html import escape
from typing import TYPE_CHECKING

from amf.models import DependencyKind, Severity, SystemKind

if TYPE_CHECKING:
    from amf.market import Market
    from amf.models import DiagnosticReport, SimulationTrace

# Node fill per diagnostic severity band, plus a neutral fill used when no
# report is supplied. Muted pastels keep black labels readable.
_SEVERITY_FILL: dict[Severity, str] = {
    Severity.LOW: "#a5d6a7",
    Severity.MODERATE: "#ffe082",
    Severity.ELEVATED: "#ffb74d",
    Severity.CRITICAL: "#ef9a9a",
}
_NEUTRAL_FILL = "#cfd8dc"
_NODE_STROKE = "#37474f"

# Edge colour per dependency kind; an edge that aggregates several kinds is
# drawn in a neutral slate.
_KIND_COLOR: dict[DependencyKind, str] = {
    DependencyKind.STRUCTURAL: "#455a64",
    DependencyKind.INFORMATIONAL: "#1e88e5",
    DependencyKind.CAPITAL: "#8e24aa",
    DependencyKind.REGULATORY: "#00897b",
}
_MIXED_KIND_COLOR = "#607d8b"

# One fixed, distinguishable line colour per system for the stress timeline.
_SYSTEM_COLOR: dict[SystemKind, str] = {
    SystemKind.SKELETON: "#546e7a",
    SystemKind.CIRCULATORY: "#d81b60",
    SystemKind.NERVOUS: "#1e88e5",
    SystemKind.MUSCULATURE: "#8e24aa",
    SystemKind.ORGANS: "#fb8c00",
    SystemKind.IMMUNE: "#43a047",
    SystemKind.METABOLISM: "#6d4c41",
}

_FOOTNOTE = "Illustrative structural model - not a market forecast or advice."

_ORDER: tuple[SystemKind, ...] = tuple(SystemKind)


def _edges(market: Market) -> list[tuple[SystemKind, SystemKind, float, tuple[DependencyKind, ...]]]:
    """Return one drawable edge per coupled *pair*, in deterministic order.

    A pair coupled by several dependency kinds is drawn once, with its
    aggregate weight and every recorded kind, rather than as overlapping
    arrows -- so this aggregates over
    :meth:`~amf.graph.DependencyGraph.dependencies`, which is per kind.

    Args:
        market: The market whose graph is being rendered.

    Returns:
        ``(source, target, weight, kinds)`` tuples ordered by system rank.
    """
    return [
        (source, target, market.graph.edge_weight(source, target), market.graph.edge_kinds(source, target))
        for source in _ORDER
        for target in market.graph.dependencies_of(source)
    ]


def _severities(report: DiagnosticReport | None) -> dict[SystemKind, Severity]:
    """Return each system's severity band from a report (empty when ``None``)."""
    if report is None:
        return {}
    return {finding.system: finding.severity for finding in report.findings}


def _scores(report: DiagnosticReport | None) -> dict[SystemKind, float]:
    """Return each system's weakness score from a report (empty when ``None``)."""
    if report is None:
        return {}
    return {finding.system: finding.score for finding in report.findings}


def _fill(kind: SystemKind, severities: dict[SystemKind, Severity]) -> str:
    """Return the node fill colour for a system."""
    severity = severities.get(kind)
    return _NEUTRAL_FILL if severity is None else _SEVERITY_FILL[severity]


def _edge_color(kinds: tuple[DependencyKind, ...]) -> str:
    """Return the stroke colour for an edge given its aggregated kinds."""
    if len(kinds) == 1:
        return _KIND_COLOR.get(kinds[0], _MIXED_KIND_COLOR)
    return _MIXED_KIND_COLOR


def _dot_quote(text: str) -> str:
    """Escape a string for use inside a double-quoted DOT attribute."""
    return text.replace("\\", "\\\\").replace('"', '\\"')


def render_dot(market: Market, report: DiagnosticReport | None = None) -> str:
    """Render the dependency graph as Graphviz DOT.

    Args:
        market: The market to draw.
        report: Optional diagnostic report; when given, nodes are filled by
            their severity band and carry a score tooltip.

    Returns:
        A complete ``digraph`` document renderable with ``dot -Tsvg``.
    """
    severities = _severities(report)
    scores = _scores(report)
    b = market.boundary
    lines = [
        "digraph amf_market {",
        f'  label="{_dot_quote(f"{b.asset_class} / {b.geography} / {b.timeframe}")}";',
        '  labelloc="t";',
        "  rankdir=LR;",
        f'  node [shape=ellipse style=filled fontname="Helvetica" color="{_NODE_STROKE}"];',
    ]
    for kind in _ORDER:
        tooltip = f"weakness {scores[kind]:.3f} ({severities[kind].value})" if kind in severities else kind.value
        lines.append(f'  "{kind.value}" [fillcolor="{_fill(kind, severities)}" tooltip="{_dot_quote(tooltip)}"];')
    for source, target, weight, kinds in _edges(market):
        lines.append(
            f'  "{source.value}" -> "{target.value}" '
            f'[penwidth={0.5 + 3.0 * weight:.2f} color="{_edge_color(kinds)}" label="{weight:.2f}" fontsize=10];'
        )
    lines.append("}")
    return "\n".join(lines)


def render_mermaid(market: Market, report: DiagnosticReport | None = None) -> str:
    """Render the dependency graph as a Mermaid flowchart.

    Args:
        market: The market to draw.
        report: Optional diagnostic report; when given, nodes are filled by
            their severity band.

    Returns:
        A ``graph LR`` document accepted by Mermaid renderers.
    """
    severities = _severities(report)
    lines = ["graph LR"]
    for kind in _ORDER:
        lines.append(f'  {kind.value}["{kind.value}"]')
    edges = _edges(market)
    for source, target, weight, _kinds in edges:
        lines.append(f"  {source.value} -->|{weight:.2f}| {target.value}")
    for kind in _ORDER:
        lines.append(f"  style {kind.value} fill:{_fill(kind, severities)},stroke:{_NODE_STROKE}")
    for i, (_source, _target, weight, kinds) in enumerate(edges):
        lines.append(f"  linkStyle {i} stroke:{_edge_color(kinds)},stroke-width:{0.5 + 3.0 * weight:.2f}px")
    return "\n".join(lines)


def render_graph_svg(market: Market, report: DiagnosticReport | None = None, *, size: int = 640) -> str:
    """Render the dependency graph as a self-contained SVG document.

    The seven systems are placed on a circle; each dependency is a straight
    arrow whose width scales with its weight and whose colour encodes its kind.
    When a report is supplied, nodes are filled by severity and annotated with
    their weakness score.

    Args:
        market: The market to draw.
        report: Optional diagnostic report used to colour and annotate nodes.
        size: Width and height of the (square) image in SVG user units.

    Returns:
        A complete ``<svg>`` document.
    """
    severities = _severities(report)
    scores = _scores(report)
    center = size / 2.0
    ring = size / 2.0 - 96.0
    node_r = 34.0

    positions: dict[SystemKind, tuple[float, float]] = {}
    for i, kind in enumerate(_ORDER):
        angle = -math.pi / 2.0 + 2.0 * math.pi * i / len(_ORDER)
        positions[kind] = (center + ring * math.cos(angle), center + ring * math.sin(angle))

    b = market.boundary
    title = escape(f"AMF dependency graph - {b.asset_class} / {b.geography} / {b.timeframe}")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
        f'font-family="Helvetica, Arial, sans-serif">',
        "<defs>",
        '<marker id="amf-arrow" viewBox="0 0 8 6" refX="8" refY="3" markerWidth="8" markerHeight="6" orient="auto">',
        f'<path d="M0,0 L8,3 L0,6 z" fill="{_MIXED_KIND_COLOR}"/>',
        "</marker>",
        "</defs>",
        f'<text x="{center:.1f}" y="26" text-anchor="middle" font-size="14" fill="{_NODE_STROKE}">{title}</text>',
    ]

    for source, target, weight, kinds in _edges(market):
        sx, sy = positions[source]
        tx, ty = positions[target]
        dx, dy = tx - sx, ty - sy
        length = math.hypot(dx, dy) or 1.0
        ux, uy = dx / length, dy / length
        # Shift paired opposite edges sideways so they do not overlap.
        if market.graph.edge_weight(target, source) > 0.0:
            px, py = -uy * 7.0, ux * 7.0
        else:
            px, py = 0.0, 0.0
        x1, y1 = sx + ux * node_r + px, sy + uy * node_r + py
        x2, y2 = tx - ux * (node_r + 9.0) + px, ty - uy * (node_r + 9.0) + py
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{_edge_color(kinds)}" stroke-width="{1.0 + 3.0 * weight:.2f}" '
            f'opacity="0.85" marker-end="url(#amf-arrow)"/>'
        )
        mx, my = (x1 + x2) / 2.0 - uy * 11.0, (y1 + y2) / 2.0 + ux * 11.0
        parts.append(
            f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" font-size="10" fill="#546e7a" '
            f'paint-order="stroke" stroke="#ffffff" stroke-width="3">{weight:.2f}</text>'
        )

    for kind in _ORDER:
        x, y = positions[kind]
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{node_r:.0f}" '
            f'fill="{_fill(kind, severities)}" stroke="{_NODE_STROKE}" stroke-width="1.5"/>'
        )
        if kind in scores:
            parts.append(
                f'<text x="{x:.1f}" y="{y - 2:.1f}" text-anchor="middle" font-size="10.5" '
                f'font-weight="bold" fill="{_NODE_STROKE}">{kind.value}</text>'
            )
            parts.append(
                f'<text x="{x:.1f}" y="{y + 11:.1f}" text-anchor="middle" font-size="9" '
                f'fill="{_NODE_STROKE}">{scores[kind]:.2f} {severities[kind].value}</text>'
            )
        else:
            parts.append(
                f'<text x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle" font-size="10.5" '
                f'font-weight="bold" fill="{_NODE_STROKE}">{kind.value}</text>'
            )

    parts.append(
        f'<text x="{center:.1f}" y="{size - 10}" text-anchor="middle" font-size="9" '
        f'fill="#90a4ae">{escape(_FOOTNOTE)}</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)


def render_timeline_svg(trace: SimulationTrace, *, width: int = 760, height: int = 380) -> str:
    """Render a shock-propagation trace as an SVG line chart.

    One line per anatomical system plots its dimensionless stress level over
    the simulation steps, with a legend and a fixed ``[0, 1]`` stress axis.

    Args:
        trace: The simulation trace to plot.
        width: Image width in SVG user units.
        height: Image height in SVG user units.

    Returns:
        A complete ``<svg>`` document.
    """
    ml, mr, mt, mb = 48.0, 168.0, 44.0, 36.0
    pw, ph = width - ml - mr, height - mt - mb
    steps = trace.steps
    n = len(steps)

    def x_at(i: int) -> float:
        return ml + (pw * i / (n - 1) if n > 1 else pw / 2.0)

    def y_at(v: float) -> float:
        return mt + (1.0 - v) * ph

    shocks = ", ".join(f"{s.target.value} {s.magnitude:.2f}" for s in trace.shocks)
    title = escape(f"Stress propagation - shock: {shocks}")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="Helvetica, Arial, sans-serif">',
        f'<text x="{ml:.1f}" y="24" font-size="14" fill="{_NODE_STROKE}">{title}</text>',
    ]

    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = y_at(tick)
        parts.append(
            f'<line x1="{ml:.1f}" y1="{y:.1f}" x2="{ml + pw:.1f}" y2="{y:.1f}" stroke="#eceff1" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{ml - 8:.1f}" y="{y + 3:.1f}" text-anchor="end" font-size="10" fill="#78909c">{tick:.2f}</text>'
        )

    stride = max(1, math.ceil(n / 8))
    for i in range(0, n, stride):
        x = x_at(i)
        parts.append(
            f'<text x="{x:.1f}" y="{mt + ph + 16:.1f}" text-anchor="middle" font-size="10" fill="#78909c">{i}</text>'
        )
    parts.append(
        f'<text x="{ml + pw / 2:.1f}" y="{height - 6:.1f}" text-anchor="middle" '
        f'font-size="10" fill="#78909c">step</text>'
    )
    parts.append(
        f'<line x1="{ml:.1f}" y1="{mt:.1f}" x2="{ml:.1f}" y2="{mt + ph:.1f}" stroke="#b0bec5" stroke-width="1"/>'
    )
    parts.append(
        f'<line x1="{ml:.1f}" y1="{mt + ph:.1f}" x2="{ml + pw:.1f}" y2="{mt + ph:.1f}" '
        f'stroke="#b0bec5" stroke-width="1"/>'
    )

    for kind in _ORDER:
        points = " ".join(f"{x_at(i):.1f},{y_at(step.get(kind, 0.0)):.1f}" for i, step in enumerate(steps))
        parts.append(
            f'<polyline points="{points}" fill="none" stroke="{_SYSTEM_COLOR[kind]}" '
            f'stroke-width="1.8" stroke-linejoin="round"/>'
        )

    lx = ml + pw + 18.0
    for i, kind in enumerate(_ORDER):
        y = mt + 10.0 + i * 18.0
        parts.append(
            f'<line x1="{lx:.1f}" y1="{y - 3:.1f}" x2="{lx + 18:.1f}" y2="{y - 3:.1f}" '
            f'stroke="{_SYSTEM_COLOR[kind]}" stroke-width="3"/>'
        )
        parts.append(f'<text x="{lx + 24:.1f}" y="{y:.1f}" font-size="10.5" fill="{_NODE_STROKE}">{kind.value}</text>')

    parts.append(
        f'<text x="{width - 8}" y="{height - 6}" text-anchor="end" font-size="9" '
        f'fill="#90a4ae">{escape(_FOOTNOTE)}</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts)
