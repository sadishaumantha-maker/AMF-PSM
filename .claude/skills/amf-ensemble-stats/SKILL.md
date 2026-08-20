---
name: amf-ensemble-stats
description: Compute percentiles and seeded bootstrap intervals with the documented estimator, standard library only. Use whenever an ensemble result is summarised.
---

# amf-ensemble-stats

A percentile without its estimator is not reproducible; a percentile without an interval overstates
precision.

## Procedure

1. **Name the estimator** by its standard sample-quantile type and include the name in the reported output.
   The nine common definitions disagree materially in small samples, and a hundred-run ensemble is a small
   sample.
2. **Compute in-house** - linear interpolation with the standard library. No numpy, no scipy.
3. **Attach an interval** to every reported percentile, by seeded bootstrap.
4. **Seed everything.** Replication `i` derives its stream from the base seed; the derivation must be
   documented and reproduce exactly across the CI Python matrix.
5. **Report sample size** alongside every figure.
6. **Respect the renderer contract** - `ResilienceDistribution` is deliberately excluded from the text and
   Markdown renderers; only `render_json` serialises one.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
