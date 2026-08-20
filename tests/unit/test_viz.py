"""Unit tests for the dependency-free visual renderers."""

from __future__ import annotations

import xml.etree.ElementTree as ET

import pytest

from amf.diagnostics import DiagnosticEngine
from amf.models import Shock, SimulationTrace, SystemKind
from amf.simulation import ShockSimulator
from amf.viz import render_dot, render_graph_svg, render_mermaid, render_timeline_svg

ALL_KINDS = [k.value for k in SystemKind]


@pytest.fixture
def report(stressed_market):
    return DiagnosticEngine().diagnose(stressed_market)


@pytest.fixture
def trace(stressed_market):
    return ShockSimulator(stressed_market).propagate(Shock(target=SystemKind.CIRCULATORY, magnitude=0.8))


def _svg_root(document):
    root = ET.fromstring(document)
    assert root.tag.endswith("svg")
    return root


class TestRenderDot:
    def test_contains_all_systems_and_edges(self, stressed_market):
        dot = render_dot(stressed_market)
        assert dot.startswith("digraph")
        for kind in ALL_KINDS:
            assert f'"{kind}"' in dot
        assert dot.count("->") == 8

    def test_healthy_market_has_no_edges(self, healthy_market):
        assert "->" not in render_dot(healthy_market)

    def test_report_colours_nodes_and_adds_tooltips(self, stressed_market, report):
        dot = render_dot(stressed_market, report)
        assert "weakness" in dot
        assert "fillcolor" in dot

    def test_edge_weight_scales_penwidth(self, stressed_market):
        dot = render_dot(stressed_market)
        # The circulatory -> skeleton edge has weight 0.8 => penwidth 2.90.
        assert "penwidth=2.90" in dot

    def test_boundary_label_is_escaped(self):
        from amf.market import Market
        from amf.models import MarketBoundary
        from amf.systems import circulatory, immune, metabolism, musculature, nervous, organs, skeleton

        boundary = MarketBoundary(asset_class='equi"ties', geography="US", timeframe="intraday")
        market = Market.assemble(
            boundary,
            [skeleton(), circulatory(), nervous(), musculature(), organs(), immune(), metabolism()],
        )
        assert '\\"' in render_dot(market)

    def test_deterministic(self, stressed_market, report):
        assert render_dot(stressed_market, report) == render_dot(stressed_market, report)


class TestRenderMermaid:
    def test_structure(self, stressed_market):
        mermaid = render_mermaid(stressed_market)
        assert mermaid.startswith("graph LR")
        for kind in ALL_KINDS:
            assert f'{kind}["{kind}"]' in mermaid
        assert mermaid.count("-->") == 8
        assert mermaid.count("linkStyle") == 8
        assert mermaid.count("style ") == 7

    def test_report_changes_fill(self, stressed_market, report):
        neutral = render_mermaid(stressed_market)
        coloured = render_mermaid(stressed_market, report)
        assert neutral != coloured

    def test_deterministic(self, stressed_market):
        assert render_mermaid(stressed_market) == render_mermaid(stressed_market)


class TestRenderGraphSvg:
    def test_is_wellformed_with_seven_nodes(self, stressed_market, report):
        root = _svg_root(render_graph_svg(stressed_market, report))
        circles = [el for el in root.iter() if el.tag.endswith("circle")]
        lines = [el for el in root.iter() if el.tag.endswith("line")]
        assert len(circles) == 7
        assert len(lines) == 8

    def test_without_report_uses_neutral_fill(self, healthy_market):
        svg = render_graph_svg(healthy_market)
        assert "#cfd8dc" in svg

    def test_title_names_the_boundary(self, stressed_market):
        svg = render_graph_svg(stressed_market)
        assert "equities / US / intraday" in svg

    def test_governance_footnote_present(self, stressed_market):
        assert "not a market forecast" in render_graph_svg(stressed_market)

    def test_deterministic(self, stressed_market, report):
        assert render_graph_svg(stressed_market, report) == render_graph_svg(stressed_market, report)

    def test_reciprocal_edges_are_offset_apart(self, boundary):
        from amf.market import Market
        from amf.models import Dependency, DependencyKind
        from amf.systems import circulatory, immune, metabolism, musculature, nervous, organs, skeleton

        market = Market.assemble(
            boundary,
            [skeleton(), circulatory(), nervous(), musculature(), organs(), immune(), metabolism()],
            [
                Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.6),
                Dependency(SystemKind.SKELETON, SystemKind.CIRCULATORY, DependencyKind.STRUCTURAL, 0.4),
            ],
        )
        root = _svg_root(render_graph_svg(market))
        lines = [el for el in root.iter() if el.tag.endswith("line")]
        assert len(lines) == 2
        # The two opposite arrows must not lie on top of each other.
        assert {line.get("x1") for line in lines} != {line.get("x2") for line in lines}


class TestRenderTimelineSvg:
    def test_is_wellformed_with_seven_polylines(self, trace):
        root = _svg_root(render_timeline_svg(trace))
        polylines = [el for el in root.iter() if el.tag.endswith("polyline")]
        assert len(polylines) == 7

    def test_title_names_the_shock(self, trace):
        svg = render_timeline_svg(trace)
        assert "Stress propagation" in svg
        assert "circulatory 0.80" in svg

    def test_legend_lists_all_systems(self, trace):
        svg = render_timeline_svg(trace)
        for kind in ALL_KINDS:
            assert kind in svg

    def test_single_step_trace_does_not_crash(self):
        trace = SimulationTrace(
            shocks=(Shock(target=SystemKind.SKELETON, magnitude=0.5),),
            steps=(dict.fromkeys(SystemKind, 0.0),),
        )
        _svg_root(render_timeline_svg(trace))

    def test_governance_footnote_present(self, trace):
        assert "not a market forecast" in render_timeline_svg(trace)


class TestEdgeColouring:
    def test_single_kind_edge_uses_its_own_colour(self, stressed_market):
        # circulatory -> nervous is purely informational (#1e88e5).
        assert "#1e88e5" in render_graph_svg(stressed_market)

    def test_mixed_kind_edge_uses_neutral_colour(self, boundary):
        from amf.market import Market
        from amf.models import Dependency, DependencyKind
        from amf.systems import circulatory, immune, metabolism, musculature, nervous, organs, skeleton

        market = Market.assemble(
            boundary,
            [skeleton(), circulatory(), nervous(), musculature(), organs(), immune(), metabolism()],
            [
                Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.STRUCTURAL, 0.3),
                Dependency(SystemKind.CIRCULATORY, SystemKind.SKELETON, DependencyKind.CAPITAL, 0.3),
            ],
        )
        root = _svg_root(render_graph_svg(market))
        lines = [el for el in root.iter() if el.tag.endswith("line")]
        assert [line.get("stroke") for line in lines] == ["#607d8b"]
