"""Example: model the immune system as a layered regulatory stack.

Builds an illustrative six-tier stack, prints its structural profile, and derives
the market's immune system from it rather than asserting four loose metrics.

The layer names below are generic placeholders. Nothing here describes any real
jurisdiction's rulebook, and the numbers are interpretable choices, not estimates.

Run with::

    python examples/policy_layers.py
"""

from __future__ import annotations

from amf import PolicyLayer, PolicyStack, PolicyTier
from amf.report import render_text


def build_stack() -> PolicyStack:
    """An illustrative regulatory stack resting on slow, entrenched foundations."""
    return PolicyStack(
        [
            PolicyLayer(
                tier=PolicyTier.CONSTITUTIVE,
                name="Entrenched mandate of the monetary authority",
                entrenchment=0.95,
                coverage=0.25,
                binding_force=1.0,
                amendment_latency=12,
            ),
            PolicyLayer(
                tier=PolicyTier.STATUTORY,
                name="Primary market-conduct act",
                entrenchment=0.70,
                coverage=0.55,
                binding_force=1.0,
                amendment_latency=6,
            ),
            PolicyLayer(
                tier=PolicyTier.DELEGATED,
                name="Regulatory technical standards",
                entrenchment=0.35,
                coverage=0.45,
                binding_force=0.9,
                amendment_latency=2,
            ),
            PolicyLayer(
                tier=PolicyTier.SUPERVISORY,
                name="Supervisory guidelines and Q&A",
                entrenchment=0.15,
                coverage=0.40,
                binding_force=0.4,
                amendment_latency=1,
            ),
            PolicyLayer(
                tier=PolicyTier.SELF_REGULATORY,
                name="Venue rulebook",
                entrenchment=0.20,
                coverage=0.30,
                binding_force=0.7,
                amendment_latency=1,
            ),
            PolicyLayer(
                tier=PolicyTier.INTERNAL,
                name="Firm risk limits and mandates",
                entrenchment=0.05,
                coverage=0.35,
                binding_force=0.5,
                amendment_latency=0,
            ),
        ]
    )


def main() -> None:
    """Profile the stack, then derive the immune system it implies."""
    stack = build_stack()
    print(render_text(stack.profile()))

    system = stack.to_immune_system(name="Illustrative regulatory regime")
    print()
    print("Derived immune system:")
    print(f"  integrity  {system.integrity:.3f}   (binding coverage of the perimeter)")
    print(f"  redundancy {system.redundancy:.3f}   (tiers populated, out of {len(PolicyTier)})")
    print(f"  load       {system.load:.3f}   (coverage stranded in unresponsive layers)")
    print(f"  health     {system.health():.3f}")
    print(f"  absorptive capacity {system.absorptive_capacity():.3f}")


if __name__ == "__main__":
    main()
