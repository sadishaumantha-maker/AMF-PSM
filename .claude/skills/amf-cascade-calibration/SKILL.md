---
name: amf-cascade-calibration
description: Sweep the cascade parameter plane, locate the sensitive region and flag knife-edge configurations. Use whenever cascade or recovery parameters are set or changed.
---

# amf-cascade-calibration

Cascade dynamics are opt-in and their defaults must reproduce the linear model exactly.

## Procedure

1. **Map the parameters** onto published threshold-cascade models. `cascade_threshold`, `cascade_gain` and
   `cascade_absorption_drop` each correspond to a named quantity in the literature, or are AMF-specific and
   must be marked so.
2. **Sweep** the threshold-gain plane deterministically at a stated grid resolution, recording cascade
   extent and `tipped_systems`.
3. **Locate the sensitive region** where a small parameter change produces a large extent change. Published
   cascade models show non-monotonic behaviour in connectivity, with a window where global cascades occur.
4. **Flag knife-edge configurations** in the reported output, so a user cannot quote a knife-edge result as
   robust.
5. **Note non-convergence** - under cascade dynamics convergence is not guaranteed and the trajectory may
   settle at a persistent non-zero state. Report that as computed state, not as a documentation caveat.
6. **Verify defaults** still reproduce the linear model exactly, so existing tests stay green.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
