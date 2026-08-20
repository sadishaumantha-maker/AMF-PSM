---
name: amf-invariant-spec
description: Write a claimed invariant into the docstring and mirror it as a test that fails when the invariant is removed. Use whenever a project asserts something must always hold.
---

# amf-invariant-spec

An invariant that is only written in prose is a wish.

## Procedure

1. **State it formally** - the quantities, their domains, and the relation that must hold.
2. **Put it in the docstring** at the point of use, in Google style, so a reader sees it where it matters.
3. **Mirror it as a test.** Deterministic boundary cases go in `tests/unit/test_<module>.py`; universally
   quantified claims go in `tests/unit/test_properties.py` as a hypothesis property.
4. **Verify the test bites** - break the invariant deliberately on a scratch branch and confirm the test
   turns red. A test that passes on broken code defends nothing.
5. **Record the waiver** if the invariant is deliberately not enforced, with the reason.

## Common AMF invariants

- Every score stays in `[0, 1]`; `Severity.from_score` and `WeaknessFinding` both rely on it.
- `to_dict`/`from_dict` is a fixed point, including every dependency kind.
- Equal markets produce identical output under any assembly permutation.
- Default simulation configuration is fully deterministic.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
