"""Policy layers of the immune system (AMF analytical Step 2, immune system).

The AMF's immune system is "risk management and regulation". In practice that is
not one thing but a *stack*: entrenched provisions at the top that almost nothing
moves, primary legislation below them, delegated acts and technical standards
below that, then supervisory guidance, self-regulatory and venue rulebooks, and
finally firm-level policy. Each layer answers a different set of the questions an
analyst asks of a regulatory regime -- who may amend it, how fast, how bindingly,
and over how much of the perimeter.

:class:`PolicyStack` models that structure and reduces it to the metrics the rest
of the toolkit already speaks, so a regulatory regime can *parameterise* the
immune system rather than being asserted as four loose numbers.

Vocabulary is taken from established sources rather than invented:

* The ``STATUTORY`` / ``DELEGATED`` / ``SUPERVISORY`` tiers correspond to the
  three Lamfalussy levels of EU financial-services rulemaking.
* :class:`~amf.models.ChangeMode` names the four modes of gradual institutional
  change from Streeck and Thelen, *Beyond Continuity* (2005): displacement,
  layering, drift, and conversion.
* The idea that some commitments resist argument almost entirely -- the
  ``CONSTITUTIVE`` tier here -- parallels the "deep core" of Sabatier's Advocacy
  Coalition Framework. Note that the ACF's further prediction, that policy-core
  beliefs are more stable than secondary ones, has found only weak empirical
  support, so this module does not encode it.

Everything here remains **illustrative**. The thresholds and weights below are
interpretable choices, not calibrated estimates, and no part of this module
describes any real jurisdiction's rulebook.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from amf.errors import IncompleteMarketError, InvalidConfigError
from amf.models import ChangeMode, PolicyLayer, PolicyProfile, PolicyTier
from amf.systems import immune

if TYPE_CHECKING:
    from collections.abc import Iterable

    from amf.systems import AnatomicalSystem

# Tiers in amendment-hardness order, hardest first. Used to order a stack
# deterministically regardless of the order layers were supplied in.
_TIER_ORDER: tuple[PolicyTier, ...] = tuple(PolicyTier)

# A layer at or above this entrenchment is treated as part of the stack's
# invariant core: the provisions that do not move with time, personnel, or a
# change of decision-maker.
ENTRENCHED_THRESHOLD = 0.75

# A stack whose binding coverage is mostly carried by unresponsive layers is
# exposed to drift at or above this level.
_HIGH_DRIFT = 0.5

# Below this aggregate coverage, the perimeter has gaps a new layer would fill.
_LOW_COVERAGE = 0.7


class PolicyStack:
    """The layered regulatory regime standing behind a market's immune system."""

    def __init__(self, layers: Iterable[PolicyLayer] = ()) -> None:
        """Build a stack from its layers.

        Args:
            layers: The policy layers, in any order; at most one per tier.

        Raises:
            InvalidConfigError: If a tier appears twice, or a layer's metrics fall
                outside their documented ranges.
        """
        mapping: dict[PolicyTier, PolicyLayer] = {}
        for layer in layers:
            if layer.tier in mapping:
                msg = f"duplicate policy layer for tier {layer.tier.value}"
                raise InvalidConfigError(msg)
            _validate(layer)
            mapping[layer.tier] = layer
        self._layers = mapping

    @property
    def layers(self) -> tuple[PolicyLayer, ...]:
        """Return the layers, ordered hardest-to-amend first."""
        return tuple(self._layers[t] for t in _TIER_ORDER if t in self._layers)

    def layer(self, tier: PolicyTier) -> PolicyLayer | None:
        """Return the layer at ``tier``, or ``None`` if the tier is unpopulated."""
        return self._layers.get(tier)

    def depth(self) -> int:
        """Return how many tiers are populated -- the stack's defence in depth."""
        return len(self._layers)

    def aggregate_coverage(self) -> float:
        """Return the perimeter covered by at least one binding layer, in ``[0, 1]``.

        Layers are treated as independently leaky, so the uncovered share is the
        product of each layer's uncovered share. Coverage therefore accumulates
        with diminishing returns and never reaches ``1`` through soft guidance
        alone -- adding a layer helps most where the perimeter is thin.
        """
        uncovered = 1.0
        for layer in self._layers.values():
            uncovered *= 1.0 - layer.effective_coverage()
        return 1.0 - uncovered

    def nominal_coverage(self) -> float:
        """Return the perimeter addressed by any layer, ignoring binding force.

        The counterpart to :meth:`aggregate_coverage`: how much ground the rules
        *speak to*, rather than how much they bindingly constrain. The gap
        between the two is the room available for
        :attr:`~amf.models.ChangeMode.CONVERSION`, where broad but soft text is
        redeployed to new ends instead of being amended.
        """
        unaddressed = 1.0
        for layer in self._layers.values():
            unaddressed *= 1.0 - layer.coverage
        return 1.0 - unaddressed

    def drift_exposure(self) -> float:
        """Return the share of binding coverage carried by unresponsive layers.

        This is exposure to :attr:`~amf.models.ChangeMode.DRIFT`: rules that stay
        fixed while conditions move around them. A stack whose coverage rests on
        entrenched, slow-to-amend layers scores high even though nothing about it
        is formally deficient. Returns ``0`` for an empty or wholly non-binding
        stack, where there is no binding coverage to strand.
        """
        weight = sum(layer.effective_coverage() for layer in self._layers.values())
        if weight <= 0.0:
            return 0.0
        stranded = sum(layer.effective_coverage() * (1.0 - layer.responsiveness()) for layer in self._layers.values())
        return stranded / weight

    def entrenched_core(self, threshold: float = ENTRENCHED_THRESHOLD) -> tuple[PolicyLayer, ...]:
        """Return the layers that resist amendment at or above ``threshold``.

        These are the provisions that do not move with time, personnel, or a
        change of decision-maker -- the part of the regime an analyst can treat
        as fixed over the horizon in question.

        Raises:
            InvalidConfigError: If ``threshold`` is outside ``[0, 1]``.
        """
        if not 0.0 <= threshold <= 1.0:
            msg = f"entrenchment threshold must be in [0, 1], got {threshold!r}"
            raise InvalidConfigError(msg)
        return tuple(layer for layer in self.layers if layer.entrenchment >= threshold)

    def dominant_mode(self) -> tuple[ChangeMode, str]:
        """Infer which mode of gradual change the stack's shape most invites.

        The mapping is interpretable rather than estimated:

        * A perimeter with gaps that the entrenched core blocks anyone from
          reworking invites **layering** -- new rules piled on top of old.
        * Binding coverage stranded in unresponsive layers invites **drift**.
        * Broad but weakly binding coverage invites **conversion** -- the same
          text redeployed to new ends, since reinterpreting costs less than
          amending.
        * Otherwise the stack is pliable enough for **displacement**.

        Returns:
            The inferred :class:`~amf.models.ChangeMode` and a one-line rationale.
        """
        coverage = self.aggregate_coverage()
        drift = self.drift_exposure()
        core = self.entrenched_core()

        if coverage < _LOW_COVERAGE and core:
            return (
                ChangeMode.LAYERING,
                f"coverage is {coverage:.2f} but {len(core)} entrenched layer(s) block rework, "
                "so new rules accumulate on top of the old",
            )
        if drift >= _HIGH_DRIFT:
            return (
                ChangeMode.DRIFT,
                f"{drift:.0%} of binding coverage sits in layers that cannot readily adapt",
            )
        if self.nominal_coverage() >= _LOW_COVERAGE and self._weakly_binding():
            # Tested against nominal rather than binding coverage on purpose:
            # weak binding force lowers `aggregate_coverage`, so testing that
            # would make the two halves of this condition contradict each other
            # and conversion unreachable.
            return (
                ChangeMode.CONVERSION,
                "the rules address a broad perimeter but bind weakly, so reinterpretation costs less than amendment",
            )
        return (
            ChangeMode.DISPLACEMENT,
            "no entrenched core and responsive layers, so existing rules can be replaced outright",
        )

    def _weakly_binding(self) -> bool:
        """Return whether the stack's coverage-weighted binding force is below half.

        The division is safe because the only caller reaches this after
        :meth:`nominal_coverage` has cleared a positive threshold, which cannot
        happen unless some layer has non-zero coverage.
        """
        weight = sum(layer.coverage for layer in self._layers.values())
        mean_force = sum(layer.coverage * layer.binding_force for layer in self._layers.values()) / weight
        return mean_force < 0.5

    def profile(self) -> PolicyProfile:
        """Return the full structural summary of the stack."""
        mode, rationale = self.dominant_mode()
        return PolicyProfile(
            layers=self.layers,
            depth=self.depth(),
            aggregate_coverage=self.aggregate_coverage(),
            drift_exposure=self.drift_exposure(),
            entrenched_core=self.entrenched_core(),
            dominant_mode=mode,
            mode_rationale=rationale,
        )

    def to_immune_system(self, name: str | None = None) -> AnatomicalSystem:
        """Derive the market's immune system from this regulatory stack.

        This is the bridge into the rest of the toolkit: rather than asserting the
        immune system's four metrics directly, they follow from the regime's
        structure.

        * ``integrity`` is :meth:`aggregate_coverage` -- how completely the
          perimeter is bindingly covered.
        * ``redundancy`` is the populated share of the tiers, since a regime
          defended at several levels retains a fallback when one gives way.
        * ``load`` is :meth:`drift_exposure` -- coverage the regime is carrying
          but can no longer adjust is a standing burden on it.
        * ``criticality`` keeps the immune system's default, which describes how
          load-bearing the system is for the market rather than anything about
          the stack.

        Args:
            name: Optional concrete counterpart for the derived system.

        Returns:
            An :class:`~amf.systems.AnatomicalSystem` of kind
            :attr:`~amf.models.SystemKind.IMMUNE`.

        Raises:
            IncompleteMarketError: If the stack has no layers, since a regime with
                no policy at all cannot parameterise an immune system.
        """
        if not self._layers:
            msg = "an empty policy stack cannot describe an immune system"
            raise IncompleteMarketError(msg)
        return immune(
            name=name,
            components=[layer.name for layer in self.layers],
            integrity=self.aggregate_coverage(),
            redundancy=self.depth() / len(_TIER_ORDER),
            load=self.drift_exposure(),
        )


def _validate(layer: PolicyLayer) -> None:
    """Validate one layer's metrics.

    Raises:
        InvalidConfigError: If a unit-interval metric is out of range, the
            latency is negative, or the name is blank.
    """
    if not layer.name.strip():
        msg = f"policy layer for tier {layer.tier.value} must have a name"
        raise InvalidConfigError(msg)
    for field in ("entrenchment", "coverage", "binding_force"):
        value = getattr(layer, field)
        if not 0.0 <= value <= 1.0:
            msg = f"{field} must be in [0, 1], got {value!r}"
            raise InvalidConfigError(msg)
    if layer.amendment_latency < 0:
        msg = f"amendment_latency must be non-negative, got {layer.amendment_latency!r}"
        raise InvalidConfigError(msg)
