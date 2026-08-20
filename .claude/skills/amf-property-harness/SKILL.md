---
name: amf-property-harness
description: Scaffold a hypothesis property test for a universally quantified claim, using the importable build_market() helper. Use when a claim must hold for all admissible inputs.
---

# amf-property-harness

Scaffold the property that would find the counterexample.

## Mechanics

- Hypothesis cannot use function-scoped fixtures under `@given`. Import `build_market()` from
  `tests/conftest.py` as a plain function. The `market_factory` fixture is for everything else.
- One property per claim. A property with two possible failure causes tells you nothing when it fails.
- Bias generation toward boundaries: metric values at 0.0 and 1.0, weights at the `(0, 1]` endpoints, empty
  and complete dependency sets, and configurations at their domain endpoints.

## Existing properties to extend rather than duplicate

Stress stays in `[0, 1]` at every step; diagnostic scores stay in `[0, 1]` for any blend of config weights;
`to_dict`/`from_dict` is a fixed point; feedback-loop enumeration matches brute-force simple-cycle search; a
market diagnoses identically under any permutation of its assembly order.

## Verification

Break the claim deliberately and confirm hypothesis finds a counterexample within the example budget.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
