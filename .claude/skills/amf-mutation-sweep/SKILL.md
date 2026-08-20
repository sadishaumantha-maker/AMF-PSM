---
name: amf-mutation-sweep
description: Run the pinned mutation-testing configuration over src/amf and triage every surviving mutant. Use to find gaps that 100% coverage hides.
---

# amf-mutation-sweep

Coverage says a line ran. Mutation says the test would have noticed if it were wrong.

## Procedure

1. **Pin** the tool version and configuration. An unreproducible mutation score is not a measurement.
2. **Run** the full baseline over `src/amf/` and store the mutant inventory per module.
3. **Triage** every survivor into exactly one of:
   - *killed by new test* - write the minimal behavioural test that detects it;
   - *equivalent* - argue why no observable behaviour differs; assumption is not argument;
   - *accepted* - with a written reason and a named owner.
4. **Respect the boundary** - new tests must pass `tests/unit/test_non_trading_boundary.py` with no new
   allowlist entries.
5. **Measure runtime** and report it. Gating decisions need cost, not enthusiasm.

## Never

Weaken an existing test to raise the score. Add a test that asserts implementation detail rather than
behaviour.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
