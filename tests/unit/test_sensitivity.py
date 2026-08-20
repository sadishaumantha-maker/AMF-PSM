"""Unit tests for sensitivity and leverage analysis."""

from __future__ import annotations

import json

import pytest

from amf.diagnostics import DiagnosticConfig, DiagnosticEngine
from amf.errors import IncompleteMarketError, InvalidConfigError
from amf.models import SystemKind, SystemMetric
from amf.report import render_json
from amf.sensitivity import SensitivityAnalyzer, SensitivityConfig

METRIC_COUNT = len(SystemMetric)
SYSTEM_COUNT = len(SystemKind)


@pytest.fixture
def analyzer():
    return SensitivityAnalyzer()


class TestSensitivityConfig:
    @pytest.mark.parametrize("step", [0.0, -0.1, 1.5])
    def test_step_outside_unit_interval_is_rejected(self, step):
        with pytest.raises(InvalidConfigError, match="step"):
            SensitivityConfig(step=step)

    @pytest.mark.parametrize("step", [0.01, 0.5, 1.0])
    def test_valid_step_accepted(self, step):
        assert SensitivityConfig(step=step).step == step

    def test_defaults(self):
        config = SensitivityConfig()
        assert 0.0 < config.step <= 1.0
        assert config.include_criticality is True


class TestSensitivity:
    def test_raising_integrity_lowers_weakness(self, analyzer, stressed_market):
        s = analyzer.sensitivity(stressed_market, SystemKind.SKELETON, SystemMetric.INTEGRITY)
        assert s.gradient < 0.0

    def test_raising_redundancy_lowers_weakness(self, analyzer, stressed_market):
        s = analyzer.sensitivity(stressed_market, SystemKind.SKELETON, SystemMetric.REDUNDANCY)
        assert s.gradient < 0.0

    def test_raising_load_raises_weakness(self, analyzer, stressed_market):
        s = analyzer.sensitivity(stressed_market, SystemKind.SKELETON, SystemMetric.LOAD)
        assert s.gradient > 0.0

    def test_reports_baseline_value(self, analyzer, stressed_market):
        s = analyzer.sensitivity(stressed_market, SystemKind.CIRCULATORY, SystemMetric.LOAD)
        assert s.baseline_value == stressed_market.system(SystemKind.CIRCULATORY).load

    def test_central_difference_uses_full_span(self, analyzer, stressed_market):
        # skeleton integrity is 0.7, so a 0.05 step has room on both sides.
        s = analyzer.sensitivity(stressed_market, SystemKind.SKELETON, SystemMetric.INTEGRITY)
        assert s.span == pytest.approx(2 * analyzer.config.step)

    def test_span_shrinks_at_upper_boundary(self, analyzer, healthy_market):
        # healthy_market has integrity 1.0, so only the downward half is available.
        s = analyzer.sensitivity(healthy_market, SystemKind.SKELETON, SystemMetric.INTEGRITY)
        assert s.span == pytest.approx(analyzer.config.step)

    def test_span_shrinks_at_lower_boundary(self, analyzer, healthy_market):
        # healthy_market has load 0.0, so only the upward half is available.
        s = analyzer.sensitivity(healthy_market, SystemKind.SKELETON, SystemMetric.LOAD)
        assert s.span == pytest.approx(analyzer.config.step)

    def test_gradient_is_delta_over_span(self, analyzer, stressed_market):
        s = analyzer.sensitivity(stressed_market, SystemKind.NERVOUS, SystemMetric.INTEGRITY)
        assert s.gradient == pytest.approx(s.index_delta / s.span)

    def test_does_not_mutate_the_market(self, analyzer, stressed_market):
        before = stressed_market.system(SystemKind.SKELETON).integrity
        analyzer.sensitivity(stressed_market, SystemKind.SKELETON, SystemMetric.INTEGRITY)
        assert stressed_market.system(SystemKind.SKELETON).integrity == before


class TestLeveragePoint:
    def test_criticality_is_not_a_lever(self, analyzer, stressed_market):
        assert analyzer.leverage_point(stressed_market, SystemKind.SKELETON, SystemMetric.CRITICALITY) is None

    def test_no_headroom_at_full_integrity(self, analyzer, healthy_market):
        assert analyzer.leverage_point(healthy_market, SystemKind.SKELETON, SystemMetric.INTEGRITY) is None

    def test_no_headroom_at_zero_load(self, analyzer, healthy_market):
        assert analyzer.leverage_point(healthy_market, SystemKind.SKELETON, SystemMetric.LOAD) is None

    def test_integrity_adjustment_moves_upward(self, analyzer, stressed_market):
        p = analyzer.leverage_point(stressed_market, SystemKind.SKELETON, SystemMetric.INTEGRITY)
        assert p is not None
        assert p.adjusted_value > p.baseline_value

    def test_load_adjustment_moves_downward(self, analyzer, stressed_market):
        p = analyzer.leverage_point(stressed_market, SystemKind.CIRCULATORY, SystemMetric.LOAD)
        assert p is not None
        assert p.adjusted_value < p.baseline_value

    def test_improvement_is_index_reduction(self, analyzer, stressed_market):
        p = analyzer.leverage_point(stressed_market, SystemKind.SKELETON, SystemMetric.INTEGRITY)
        assert p is not None
        assert p.improvement == pytest.approx(p.index_before - p.index_after)
        assert p.improvement > 0.0

    def test_adjustment_is_clipped_to_unit_interval(self, stressed_market):
        analyzer = SensitivityAnalyzer(config=SensitivityConfig(step=1.0))
        p = analyzer.leverage_point(stressed_market, SystemKind.SKELETON, SystemMetric.INTEGRITY)
        assert p is not None
        assert p.adjusted_value == 1.0


class TestAnalyse:
    def test_sweeps_every_system_and_metric(self, analyzer, stressed_market):
        report = analyzer.analyse(stressed_market)
        assert len(report.sensitivities) == SYSTEM_COUNT * METRIC_COUNT
        assert {s.system for s in report.sensitivities} == set(SystemKind)

    def test_criticality_can_be_excluded(self, stressed_market):
        analyzer = SensitivityAnalyzer(config=SensitivityConfig(include_criticality=False))
        report = analyzer.analyse(stressed_market)
        assert len(report.sensitivities) == SYSTEM_COUNT * (METRIC_COUNT - 1)
        assert all(s.metric is not SystemMetric.CRITICALITY for s in report.sensitivities)

    def test_sensitivities_sorted_by_absolute_gradient(self, analyzer, stressed_market):
        gradients = [abs(s.gradient) for s in analyzer.analyse(stressed_market).sensitivities]
        assert gradients == sorted(gradients, reverse=True)

    def test_leverage_points_sorted_by_improvement(self, analyzer, stressed_market):
        improvements = [p.improvement for p in analyzer.analyse(stressed_market).leverage_points]
        assert improvements == sorted(improvements, reverse=True)

    def test_leverage_points_never_include_criticality(self, analyzer, stressed_market):
        report = analyzer.analyse(stressed_market)
        assert all(p.metric is not SystemMetric.CRITICALITY for p in report.leverage_points)

    def test_criticality_still_reported_as_sensitive(self, analyzer, stressed_market):
        report = analyzer.analyse(stressed_market)
        assert any(s.metric is SystemMetric.CRITICALITY for s in report.sensitivities)

    def test_baseline_matches_the_diagnostic_index(self, analyzer, stressed_market):
        report = analyzer.analyse(stressed_market)
        assert report.baseline_index == pytest.approx(DiagnosticEngine().diagnose(stressed_market).overall_index)

    def test_carries_boundary_and_step(self, analyzer, stressed_market):
        report = analyzer.analyse(stressed_market)
        assert report.boundary == stressed_market.boundary
        assert report.step == analyzer.config.step

    def test_healthy_market_offers_only_redundancy_leverage(self, analyzer, healthy_market):
        # Every system sits at integrity 1.0 and load 0.0, leaving redundancy as
        # the only metric with headroom in its improving direction.
        report = analyzer.analyse(healthy_market)
        assert {p.metric for p in report.leverage_points} == {SystemMetric.REDUNDANCY}
        assert len(report.leverage_points) == SYSTEM_COUNT

    def test_deterministic(self, analyzer, stressed_market):
        assert analyzer.analyse(stressed_market).to_dict() == analyzer.analyse(stressed_market).to_dict()

    def test_incomplete_market_is_rejected(self, analyzer, stressed_market):
        del stressed_market.systems[SystemKind.IMMUNE]
        with pytest.raises(IncompleteMarketError, match="missing systems"):
            analyzer.analyse(stressed_market)

    def test_custom_engine_weights_are_honoured(self, stressed_market):
        # Scoring purely on fragility ignores concentration and feedback, so the
        # analysis of that engine must differ from the default blend.
        fragility_only = DiagnosticEngine(
            DiagnosticConfig(fragility_weight=1.0, concentration_weight=0.0, feedback_weight=0.0)
        )
        default = SensitivityAnalyzer().analyse(stressed_market)
        custom = SensitivityAnalyzer(engine=fragility_only).analyse(stressed_market)
        assert custom.baseline_index != default.baseline_index

    def test_report_is_json_serialisable(self, analyzer, stressed_market):
        payload = json.loads(render_json(analyzer.analyse(stressed_market)))
        assert payload["sensitivities"]
        assert payload["leverage_points"]
        assert payload["baseline_severity"] in {"low", "moderate", "elevated", "critical"}
