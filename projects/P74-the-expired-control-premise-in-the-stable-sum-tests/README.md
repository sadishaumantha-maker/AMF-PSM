# P74 - The expired control premise in the stable_sum tests

**Track M - Live Defects and the Green-Main Obligation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 days |
| **Lead role** | Test engineer |
| **Upstream** | `tests/unit/test_numeric.py`; CI red on py3.12 and py3.13 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Two tests in `tests/unit/test_numeric.py` use the built-in `sum()` as a *control* - they assert it misbehaves so that `stable_sum` has something to be better than. CPython 3.12 changed `sum()` to use Neumaier compensated summation for float inputs, so on 3.12 and 3.13 the control is simply false: `sum([0.1, 0.2, 0.3])` is `0.6` for every permutation, and `sum([1.0, 1e100, 1.0, -1e100])` is `2.0` rather than `0.0`. The test suite is red on two of the three supported versions. The tests are not wrong about `stable_sum`; their assumption about the baseline expired underneath them.

## 2. Purpose

Fix the tests without weakening what they check, and then answer the larger question the incident raises: how many other claims in this repository are anchored to a standard-library behaviour that is free to change?

## 3. Scope

**In scope**

- A version-correct fix for both failing tests in `tests/unit/test_numeric.py`.
- A review of `amf/numeric.py`'s docstring, which states the rationale in terms of the old baseline.
- An inventory of every other test or docstring that asserts a standard-library behaviour rather than an AMF behaviour.

**Out of scope**

- Deleting the tests. The property they defend is real; only the control is stale.
- Dropping Python 3.11 or 3.12 from the CI matrix to make the problem go away.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Reproduce on each supported version before changing anything: 3.11 shows the old behaviour, 3.12 and 3.13 the new one. Record the actual values, because they are the evidence.
2. Decide the fix on principle. A test of `stable_sum` should assert what `stable_sum` promises - exact rounding against a `Fraction` reference - and must not depend on the built-in being bad. The existing `test_stable_sum_is_exactly_rounded` already does this correctly and is the model.
3. Where a contrast with the naive baseline is genuinely illustrative, express it against an explicit left-to-right fold written in the test, not against `sum()`, so the control cannot drift again.
4. Re-read `amf/numeric.py`'s module docstring: it argues for `stable_sum` partly from `sum()`'s order sensitivity, which is now only true below 3.12. Correct the rationale without weakening the conclusion - `stable_sum` is still exactly rounded and the built-in still is not.
5. Note the second half of that docstring's claim about `x ** 2` versus `x * x` is unaffected and remains correct; do not disturb it.
6. Sweep the suite for the same pattern: any assertion whose subject is the standard library rather than `amf`.

## 5. Task board

- [ ] Record the measured behaviour of `sum()` on 3.11, 3.12 and 3.13.
- [ ] Rewrite both failing tests against an explicit fold, not `sum()`.
- [ ] Correct the `amf/numeric.py` docstring rationale.
- [ ] Inventory other standard-library-dependent assertions.
- [ ] Confirm the suite is green on all three CI versions.
- [ ] Record the fix in `CHANGELOG.md` under `Fixed`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `benchmark-runner`

- **Mandate:** Measure the built-in's behaviour on each supported version and record the exact values.
- **Inputs:** Python 3.11, 3.12, 3.13.
- **Output artifact:** A version-behaviour table with the reproduction command.
- **Stop condition:** Both disputed expressions are recorded per version.

### `unit-test-author`

- **Mandate:** Rewrite the two tests so they depend only on `amf` behaviour and an explicit in-test fold.
- **Inputs:** The measurement table.
- **Output artifact:** A diff to `tests/unit/test_numeric.py`.
- **Stop condition:** The suite passes on all three versions and still fails if `stable_sum` is replaced by a naive fold.

### `numerics-auditor`

- **Mandate:** Correct the module docstring's rationale without weakening its conclusion.
- **Inputs:** `src/amf/numeric.py`.
- **Output artifact:** A docstring diff.
- **Stop condition:** Every numeric claim in the docstring is true on 3.11, 3.12 and 3.13.

### `red-team-critic`

- **Mandate:** Find any other assertion in the suite whose subject is the standard library rather than the package.
- **Inputs:** `tests/`.
- **Output artifact:** An inventory of version-fragile assertions.
- **Stop condition:** Every occurrence is listed with a verdict of fix, guard or accept.

**Hand-off order:** `benchmark-runner` -> `unit-test-author` -> `numerics-auditor` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-float-audit` | A numeric claim is restated | Checks the claim against an exact reference on each supported version. |
| `amf-coverage-gate` | Tests change | Confirms the 100% statement and branch gate still holds. |
| `amf-changelog-entry` | The fix lands | Records it under `Fixed` with the version-behaviour evidence. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- Green tests on 3.11, 3.12 and 3.13
- A corrected `amf/numeric.py` rationale
- A version-fragile assertion inventory
- A `CHANGELOG.md` entry

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] `python -m pytest` passes on all three supported versions.
- [ ] The rewritten tests still fail if `stable_sum` is replaced by a naive left-to-right fold.
- [ ] No claim in `amf/numeric.py` is false on any supported version.
- [ ] Every other version-fragile assertion has a written verdict.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Neumaier, A. (1974). "Rundungsfehleranalyse einiger Verfahren zur Summation endlicher Summen." *Zeitschrift fur Angewandte Mathematik und Mechanik* 54(1), 39-51.
- Ogita, T., Rump, S. M., & Oishi, S. (2005). "Accurate Sum and Dot Product." *SIAM Journal on Scientific Computing* 26(6), 1955-1988.
- Shewchuk, J. R. (1997). "Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates." *Discrete & Computational Geometry* 18(3), 305-363.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms* (2nd ed.). SIAM.
- Goldberg, D. (1991). "What Every Computer Scientist Should Know About Floating-Point Arithmetic." *ACM Computing Surveys* 23(1), 5-48.
- IEEE (2019). *IEEE Standard for Floating-Point Arithmetic* (IEEE Std 754-2019).
- CPython issue gh-100425 / bpo tracker. "Improve accuracy of builtin sum() for float inputs" - the Neumaier compensated-summation change shipped in CPython 3.12.
- Python Software Foundation. *PEP 387: Backwards Compatibility Policy*.

## 11. Commit protocol

Commits from this project use the scope `p74`:

```text
test(p74): record built-in sum() behaviour across the supported versions
fix(p74): assert stable_sum against an explicit fold, not the built-in
docs(p74): correct the numeric rationale for CPython 3.12 compensated sum
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

