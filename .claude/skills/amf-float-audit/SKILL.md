---
name: amf-float-audit
description: Locate floating-point accumulations, bound their error and compare against an extended-precision reference. Use whenever a reported number's precision is in question.
---

# amf-float-audit

Quantify finite-precision error in `src/amf/`.

## Procedure

1. **Inventory** the accumulations: the concentration HHI share sum, the criticality-weighted mean, feedback
   edge-weight products, the stress-vector inner loop, and the percentile machinery.
2. **Bound** each with the standard forward error result for summation, in terms of the condition number and
   the term count. With seven systems the term count is small - the condition number, not the length, is
   usually the risk.
3. **Reference** - build an exact-rational or extended-precision oracle for tests only.
4. **Search** for the adversarial input inside the admissible `[0, 1]` box that maximises observed relative
   error.
5. **Decide** - implement compensated (Kahan-Neumaier) summation only where the measured error can change a
   reported digit or flip a `Severity` band. A change with no measured effect is not made.
6. **Degenerate paths** - identify NaN and infinity fall-throughs. NaN compares false against every
   threshold, so a threshold chain has a silent default branch that must be intentional.

## Constraint

Standard library only. No numpy.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
