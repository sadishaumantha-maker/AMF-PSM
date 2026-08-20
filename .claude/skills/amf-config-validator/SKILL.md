---
name: amf-config-validator
description: Add or change a validated tuning parameter so it raises InvalidConfigError outside its domain, with both-sided boundary tests. Use for every new or modified configuration knob.
---

# amf-config-validator

A nonsensical knob must fail, not produce a plausible-looking number.

## Procedure

1. **State the domain** and the invariant it protects. The primary invariant is that every score stays in
   `[0, 1]`.
2. **Prove containment** over the whole admissible domain, or narrow the domain until you can. Never widen
   the domain and hope.
3. **Validate on construction**, raising `InvalidConfigError` - never a bare `ValueError`, and never silent
   normalisation into nonsense.
4. **Test both sides of every endpoint**, open and closed.
5. **Preserve documented legal edge cases**, such as the all-zero `DiagnosticConfig` weight triple, which is
   legal and yields zero scores.

## Existing domains for reference

`DiagnosticConfig`: finite, non-negative weights. `SimulationConfig`: `max_steps >= 1`, `damping` in
`(0, 1]`, `retention` in `[0, 1]`, finite non-negative `transmission` and `jitter`, `convergence_eps > 0`,
`cascade_threshold` `None` or in `(0, 1)`. `SensitivityConfig`: `step` in `(0, 1]`.
`DependencyGraph.centrality`: `alpha` in `(0, 1)`, `iterations >= 1`, finite non-negative `tolerance`.

## Why

A negative blend weight once yielded a finding scoring 2.0, and `alpha >= 10` overflowed the influence series
to infinity and returned NaN for every system.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
