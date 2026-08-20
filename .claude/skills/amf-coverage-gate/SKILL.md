---
name: amf-coverage-gate
description: Verify the 100% statement and branch coverage gate and diagnose uncovered branches with reaching inputs. Use whenever tests or coverage configuration change.
---

# amf-coverage-gate

The gate is `--cov-fail-under=100` in `pyproject.toml`, over `src/amf/`, statements and branches.

## Procedure

1. Run `pytest` and read the branch report, not only the statement report.
2. For every uncovered branch, identify the input that reaches it. If no input reaches it, the branch is
   dead code - remove it rather than testing it.
3. Never lower the threshold. The fix for a failing gate is a test.
4. Never add an exclusion pragma without a written justification and human sign-off.
5. Whenever you report a coverage figure, state that full coverage is not full testing. This repository's own
   history proves it - `tests/unit/test_packaging.py` and the mutation-driven tests exist because full
   coverage was hiding real gaps.

## Output

Pass, or a list of uncovered branches with the reaching input for each.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
