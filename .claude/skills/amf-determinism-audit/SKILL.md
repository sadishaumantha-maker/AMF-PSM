---
name: amf-determinism-audit
description: Run permutation, repetition and cross-version invariance checks over the AMF public API. Use after any change that could affect ordering, iteration or output.
---

# amf-determinism-audit

Prove that equal inputs give byte-identical output.

## Checks

1. **Repeat-run identity** - run the same input twice; outputs must be byte-identical in every format.
2. **Permutation invariance** - build the same market with systems and dependencies added in a different
   order; every rendered output must match exactly.
3. **Tie stress** - construct markets where ranking ties occur. `musculature` and `metabolism` share a
   criticality of 0.60, so this is the routine case, not the exotic one.
4. **Canonical key coverage** - for every iteration over a collection on the path from `Market.from_dict` to
   the renderers, name the canonical key that orders it. An unnamed iteration is a defect.
5. **Cross-version** - verify on 3.11, 3.12 and 3.13; the CI matrix covers all three.
6. **Seed discipline** - confirm the default configuration is fully deterministic. `jitter` must have no
   effect unless `seed` is also set.

## Why this matters

Floating-point addition is not associative. Insertion-ordered traversal once made a diagnosis differ in its
last bits, because the concentration HHI sums over an ordered list. A dict-insertion-order tie-break is a
bug, not a detail.

## Failure

Report the exact pair of inputs that differ and the first differing byte.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
