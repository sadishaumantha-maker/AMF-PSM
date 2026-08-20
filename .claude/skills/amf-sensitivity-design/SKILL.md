---
name: amf-sensitivity-design
description: Design a perturbation experiment - one-at-a-time, elementary effects or variance-based - and report rank stability. Use whenever a weight, threshold or parameter's influence is in question.
---

# amf-sensitivity-design

One-at-a-time designs explore a thin cross through the input space and miss interactions. AMF's diagnostic
score is an explicit product of interacting terms, so interactions are the mechanism, not a footnote.

## Procedure

1. **State the question**: which output, which inputs, and over what domain.
2. **Choose the design**:
   - *one-at-a-time* for a quick local gradient - the current `SensitivityAnalyzer` behaviour;
   - *elementary effects* for screening with interaction detection at modest cost;
   - *variance-based indices* where the input dimension is small enough, which at seven systems and four
     metrics it usually is.
3. **Report the span**, not only the gradient. The difference is central where the metric has room on both
   sides and one-sided near a bound, so the interval actually explored must be reported.
4. **Report rank stability**, not only index values. If the top-ranked finding changes across the weight
   simplex, the ranking is weight-driven and must be presented as such.
5. **Report interactions explicitly**: a large total effect with a small first-order effect is the finding.
6. **Seed and reproduce.** State sample size and estimator for every index.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
