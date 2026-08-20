---
name: amf-centrality-diagnostics
description: Estimate the graph's spectral radius and validate the Katz attenuation factor against the convergence condition. Use whenever centrality is computed or configured.
---

# amf-centrality-diagnostics

Katz-style influence converges only while the attenuation factor stays below the inverse of the graph's
spectral radius.

## Procedure

1. **Estimate the spectral radius** by power iteration, with a validated iteration cap and tolerance.
2. **Check the condition** before computing. The default `alpha = 0.4` satisfies it on a sparse market but
   not on a densely coupled one, where the influence series diverges *before* max-normalisation and returns
   NaN for every system.
3. **Be conservative** - the estimate has error, so classify borderline graphs as unsafe, not safe.
4. **Fail loudly** - raise `InvalidConfigError` naming the largest admissible `alpha`, rather than returning
   a NaN.
5. **State the question** - Katz answers "how much is this system depended upon", attenuated per hop. It was
   chosen over eigenvector centrality because it is well defined on acyclic graphs. It is a standalone query;
   nothing in the scoring pipeline consumes it.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
