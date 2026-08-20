"""Unit tests for the immune system's policy stack."""

from __future__ import annotations

import json

import pytest

from amf.errors import IncompleteMarketError, InvalidConfigError
from amf.models import ChangeMode, PolicyLayer, PolicyTier, SystemKind
from amf.policy import ENTRENCHED_THRESHOLD, PolicyStack
from amf.report import render_json, render_markdown, render_text


def layer(tier: PolicyTier, **kwargs) -> PolicyLayer:
    """A policy layer with sensible defaults, overridable per test."""
    defaults = {"name": tier.value, "entrenchment": 0.5, "coverage": 0.5, "binding_force": 1.0}
    return PolicyLayer(tier=tier, **{**defaults, **kwargs})


@pytest.fixture
def stack() -> PolicyStack:
    """A five-tier stack resting mostly on slow, entrenched layers."""
    return PolicyStack(
        [
            layer(PolicyTier.CONSTITUTIVE, entrenchment=0.95, coverage=0.25, amendment_latency=12),
            layer(PolicyTier.STATUTORY, entrenchment=0.70, coverage=0.55, amendment_latency=6),
            layer(PolicyTier.DELEGATED, entrenchment=0.35, coverage=0.45, binding_force=0.9, amendment_latency=2),
            layer(PolicyTier.SUPERVISORY, entrenchment=0.15, coverage=0.40, binding_force=0.4),
            layer(PolicyTier.SELF_REGULATORY, entrenchment=0.20, coverage=0.30, binding_force=0.7),
        ]
    )


class TestPolicyTier:
    def test_every_tier_names_an_amending_authority(self):
        for tier in PolicyTier:
            assert tier.amending_authority().strip()

    def test_tiers_are_declared_hardest_to_amend_first(self):
        order = list(PolicyTier)
        assert order[0] is PolicyTier.CONSTITUTIVE
        assert order[-1] is PolicyTier.INTERNAL


class TestPolicyLayer:
    def test_responsiveness_falls_with_entrenchment(self):
        soft = layer(PolicyTier.INTERNAL, entrenchment=0.1)
        hard = layer(PolicyTier.INTERNAL, entrenchment=0.9)
        assert soft.responsiveness() > hard.responsiveness()

    def test_responsiveness_falls_with_latency(self):
        quick = layer(PolicyTier.INTERNAL, entrenchment=0.2, amendment_latency=0)
        slow = layer(PolicyTier.INTERNAL, entrenchment=0.2, amendment_latency=9)
        assert quick.responsiveness() > slow.responsiveness()

    def test_a_non_derogable_layer_is_wholly_unresponsive(self):
        assert layer(PolicyTier.CONSTITUTIVE, entrenchment=1.0).responsiveness() == pytest.approx(0.0)

    def test_effective_coverage_discounts_soft_law(self):
        hard = layer(PolicyTier.STATUTORY, coverage=0.8, binding_force=1.0)
        soft = layer(PolicyTier.SUPERVISORY, coverage=0.8, binding_force=0.25)
        assert hard.effective_coverage() == pytest.approx(0.8)
        assert soft.effective_coverage() == pytest.approx(0.2)

    def test_to_dict_records_the_amending_authority(self):
        payload = layer(PolicyTier.STATUTORY).to_dict()
        assert payload["amending_authority"] == PolicyTier.STATUTORY.amending_authority()
        assert payload["tier"] == "statutory"


class TestPolicyStackValidation:
    def test_duplicate_tier_is_rejected(self):
        with pytest.raises(InvalidConfigError, match="duplicate"):
            PolicyStack([layer(PolicyTier.STATUTORY), layer(PolicyTier.STATUTORY)])

    @pytest.mark.parametrize("field", ["entrenchment", "coverage", "binding_force"])
    @pytest.mark.parametrize("value", [-0.1, 1.5])
    def test_out_of_range_metric_is_rejected(self, field, value):
        with pytest.raises(InvalidConfigError, match=field):
            PolicyStack([layer(PolicyTier.STATUTORY, **{field: value})])

    def test_negative_latency_is_rejected(self):
        with pytest.raises(InvalidConfigError, match="amendment_latency"):
            PolicyStack([layer(PolicyTier.STATUTORY, amendment_latency=-1)])

    def test_blank_name_is_rejected(self):
        with pytest.raises(InvalidConfigError, match="name"):
            PolicyStack([layer(PolicyTier.STATUTORY, name="   ")])

    def test_bad_entrenchment_threshold_is_rejected(self, stack):
        with pytest.raises(InvalidConfigError, match="threshold"):
            stack.entrenched_core(threshold=1.5)


class TestPolicyStackStructure:
    def test_layers_are_ordered_hardest_first_regardless_of_input_order(self):
        built = PolicyStack([layer(PolicyTier.INTERNAL), layer(PolicyTier.CONSTITUTIVE)])
        assert [item.tier for item in built.layers] == [PolicyTier.CONSTITUTIVE, PolicyTier.INTERNAL]

    def test_depth_counts_populated_tiers(self, stack):
        assert stack.depth() == 5

    def test_layer_lookup(self, stack):
        assert stack.layer(PolicyTier.STATUTORY) is not None
        assert stack.layer(PolicyTier.INTERNAL) is None

    def test_empty_stack_is_inert(self):
        empty = PolicyStack()
        assert empty.depth() == 0
        assert empty.aggregate_coverage() == pytest.approx(0.0)
        assert empty.drift_exposure() == pytest.approx(0.0)
        assert empty.entrenched_core() == ()


class TestCoverage:
    def test_coverage_accumulates_with_diminishing_returns(self):
        one = PolicyStack([layer(PolicyTier.STATUTORY, coverage=0.5)])
        two = PolicyStack([layer(PolicyTier.STATUTORY, coverage=0.5), layer(PolicyTier.DELEGATED, coverage=0.5)])
        assert two.aggregate_coverage() > one.aggregate_coverage()
        assert two.aggregate_coverage() == pytest.approx(0.75)

    def test_soft_law_covers_less_than_hard_law(self):
        hard = PolicyStack([layer(PolicyTier.STATUTORY, coverage=0.8, binding_force=1.0)])
        soft = PolicyStack([layer(PolicyTier.SUPERVISORY, coverage=0.8, binding_force=0.3)])
        assert hard.aggregate_coverage() > soft.aggregate_coverage()

    def test_nominal_coverage_ignores_binding_force(self):
        soft = PolicyStack([layer(PolicyTier.SUPERVISORY, coverage=0.8, binding_force=0.1)])
        assert soft.nominal_coverage() == pytest.approx(0.8)
        assert soft.aggregate_coverage() < soft.nominal_coverage()

    def test_wholly_non_binding_stack_strands_nothing(self):
        inert = PolicyStack([layer(PolicyTier.SUPERVISORY, coverage=0.9, binding_force=0.0)])
        assert inert.drift_exposure() == pytest.approx(0.0)


class TestDriftExposure:
    def test_responsive_stack_has_low_drift(self):
        quick = PolicyStack([layer(PolicyTier.DELEGATED, entrenchment=0.05, amendment_latency=0)])
        assert quick.drift_exposure() < 0.1

    def test_entrenched_slow_stack_has_high_drift(self):
        stuck = PolicyStack([layer(PolicyTier.CONSTITUTIVE, entrenchment=0.9, amendment_latency=10)])
        assert stuck.drift_exposure() > 0.9

    def test_drift_is_a_share_and_stays_in_unit_interval(self, stack):
        assert 0.0 <= stack.drift_exposure() <= 1.0


class TestEntrenchedCore:
    def test_core_holds_the_layers_that_do_not_move(self, stack):
        core = stack.entrenched_core()
        assert [item.tier for item in core] == [PolicyTier.CONSTITUTIVE]

    def test_threshold_is_inclusive(self):
        built = PolicyStack([layer(PolicyTier.STATUTORY, entrenchment=ENTRENCHED_THRESHOLD)])
        assert len(built.entrenched_core()) == 1

    def test_lowering_the_threshold_widens_the_core(self, stack):
        assert len(stack.entrenched_core(threshold=0.3)) > len(stack.entrenched_core())


class TestDominantMode:
    def test_gaps_behind_an_entrenched_core_invite_layering(self):
        built = PolicyStack(
            [
                layer(PolicyTier.CONSTITUTIVE, entrenchment=0.95, coverage=0.3, amendment_latency=10),
                layer(PolicyTier.STATUTORY, entrenchment=0.5, coverage=0.3, amendment_latency=1),
            ]
        )
        mode, why = built.dominant_mode()
        assert mode is ChangeMode.LAYERING
        assert "entrenched" in why

    def test_stranded_binding_coverage_invites_drift(self):
        built = PolicyStack([layer(PolicyTier.STATUTORY, entrenchment=0.8, coverage=0.9, amendment_latency=8)])
        assert built.dominant_mode()[0] is ChangeMode.DRIFT

    def test_broad_but_soft_coverage_invites_conversion(self):
        # Nominal breadth is what matters here: binding-weighted coverage would
        # be dragged down by the very softness that makes conversion likely.
        built = PolicyStack(
            [
                layer(PolicyTier.SUPERVISORY, entrenchment=0.05, coverage=0.85, binding_force=0.3),
                layer(PolicyTier.INTERNAL, entrenchment=0.05, coverage=0.8, binding_force=0.35),
            ]
        )
        assert built.dominant_mode()[0] is ChangeMode.CONVERSION

    def test_pliable_stack_permits_displacement(self):
        built = PolicyStack([layer(PolicyTier.DELEGATED, entrenchment=0.1, coverage=0.8, binding_force=1.0)])
        assert built.dominant_mode()[0] is ChangeMode.DISPLACEMENT

    def test_every_mode_is_reachable(self):
        # A mode the shape rules can never produce would be dead vocabulary.
        shapes = [
            PolicyStack(
                [
                    layer(PolicyTier.CONSTITUTIVE, entrenchment=0.95, coverage=0.3, amendment_latency=10),
                    layer(PolicyTier.STATUTORY, entrenchment=0.5, coverage=0.3, amendment_latency=1),
                ]
            ),
            PolicyStack([layer(PolicyTier.STATUTORY, entrenchment=0.8, coverage=0.9, amendment_latency=8)]),
            PolicyStack(
                [
                    layer(PolicyTier.SUPERVISORY, entrenchment=0.05, coverage=0.85, binding_force=0.3),
                    layer(PolicyTier.INTERNAL, entrenchment=0.05, coverage=0.8, binding_force=0.35),
                ]
            ),
            PolicyStack([layer(PolicyTier.DELEGATED, entrenchment=0.1, coverage=0.8, binding_force=1.0)]),
        ]
        assert {shape.dominant_mode()[0] for shape in shapes} == set(ChangeMode)


class TestImmuneSystemBridge:
    def test_derives_an_immune_system(self, stack):
        system = stack.to_immune_system()
        assert system.kind is SystemKind.IMMUNE

    def test_metrics_follow_the_stack(self, stack):
        system = stack.to_immune_system()
        assert system.integrity == pytest.approx(stack.aggregate_coverage())
        assert system.load == pytest.approx(stack.drift_exposure())
        assert system.redundancy == pytest.approx(stack.depth() / len(PolicyTier))

    def test_criticality_keeps_the_immune_default(self, stack):
        from amf.systems import immune

        assert stack.to_immune_system().criticality == pytest.approx(immune().criticality)

    def test_components_name_the_layers(self, stack):
        assert stack.to_immune_system().components == [item.name for item in stack.layers]

    def test_custom_name_is_used(self, stack):
        assert stack.to_immune_system(name="EU regime").name == "EU regime"

    def test_broader_coverage_yields_a_healthier_system(self):
        thin = PolicyStack([layer(PolicyTier.STATUTORY, coverage=0.2, entrenchment=0.1)])
        broad = PolicyStack([layer(PolicyTier.STATUTORY, coverage=0.9, entrenchment=0.1)])
        assert broad.to_immune_system().health() > thin.to_immune_system().health()

    def test_empty_stack_cannot_describe_an_immune_system(self):
        with pytest.raises(IncompleteMarketError, match="empty policy stack"):
            PolicyStack().to_immune_system()


class TestPolicyRenderers:
    def test_text_names_the_layers_and_mode(self, stack):
        out = render_text(stack.profile())
        assert "Immune System Policy Stack" in out
        assert "Dominant change mode" in out
        for item in stack.layers:
            assert item.tier.value in out

    def test_text_reports_an_absent_entrenched_core(self):
        built = PolicyStack([layer(PolicyTier.INTERNAL, entrenchment=0.1)])
        assert "Entrenched core: none" in render_text(built.profile())

    def test_markdown_is_a_table(self, stack):
        out = render_markdown(stack.profile())
        assert out.startswith("# AMF Immune System Policy Stack")
        assert "| Tier | Name |" in out

    def test_markdown_reports_an_absent_entrenched_core(self):
        built = PolicyStack([layer(PolicyTier.INTERNAL, entrenchment=0.1)])
        assert "none" in render_markdown(built.profile())

    def test_json_round_trips(self, stack):
        payload = json.loads(render_json(stack.profile()))
        assert payload["depth"] == 5
        assert payload["dominant_mode"] in {m.value for m in ChangeMode}
        assert payload["entrenched_core"] == ["constitutive"]
        assert len(payload["layers"]) == 5

    def test_profile_is_deterministic(self, stack):
        assert stack.profile().to_dict() == stack.profile().to_dict()
