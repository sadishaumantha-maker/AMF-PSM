# P19 - Percentile estimator selection and uncertainty on ensemble output

**Track C - Numerical Correctness & Determinism**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 4 days |
| **Lead role** | Statistician |
| **Upstream** | `ResilienceDistribution`; "percentiles computed in-house by linear interpolation, no numpy" |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The ensemble reports percentiles from a single in-house linear-interpolation rule. There are nine recognised sample-quantile definitions in common statistical use, and they disagree materially in small samples - exactly the regime a hundred-run ensemble occupies. Reporting a percentile without naming the estimator is not reproducible, and reporting it without an interval overstates precision.

## 2. Purpose

Name the estimator explicitly against the standard taxonomy, justify the choice for small samples, and attach an uncertainty interval to every reported percentile.

## 3. Scope

**In scope**

- Identification of the current rule within the standard nine-type taxonomy.
- A small-sample comparison of candidate types at the ensemble sizes actually used.
- Bootstrap intervals for reported percentiles, implemented with the standard library only.

**Out of scope**

- Adding scipy or numpy.
- Reporting any quantity that is not a dimensionless structural measure.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Read the current implementation and place it exactly within the standard sample-quantile taxonomy.
2. State the properties that matter here: continuity in the data, median-unbiasedness, and behaviour at the extremes of a small sample.
3. Compare candidate estimators at run counts of 30, 100 and 1000 against a known reference distribution.
4. Select one, document why, and make the estimator name part of the reported output so the number is reproducible.
5. Implement a bootstrap interval for each reported percentile; keep it seeded and deterministic.
6. Ensure `render_json` remains machine-parseable and that only `render_json` serialises a distribution, per the existing renderer contract.

## 5. Task board

- [ ] Identify the current estimator type.
- [ ] Write the small-sample comparison.
- [ ] Select and document the estimator.
- [ ] Expose the estimator name in the output.
- [ ] Implement seeded bootstrap intervals.
- [ ] Add tests including known-answer cases.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Place the current rule in the standard taxonomy and state its small-sample properties.
- **Inputs:** `simulation.py` percentile code.
- **Output artifact:** `docs/numerics/quantile_estimator.md`.
- **Stop condition:** The rule is identified by type number with a worked example.

### `benchmark-runner`

- **Mandate:** Compare estimators against a reference distribution at realistic ensemble sizes.
- **Inputs:** Candidate estimators.
- **Output artifact:** A comparison table with reproduction commands.
- **Stop condition:** Bias and variance are reported at three sample sizes.

### `algorithm-implementer`

- **Mandate:** Implement the selected estimator and seeded bootstrap intervals without new dependencies.
- **Inputs:** The selection.
- **Output artifact:** A diff under `src/amf/simulation.py` and `models.py`.
- **Stop condition:** `mypy` strict passes and `ResilienceDistribution.to_dict()` round-trips.

### `unit-test-author`

- **Mandate:** Add known-answer tests where the correct quantile is analytically determined.
- **Inputs:** The implementation.
- **Output artifact:** Cases in `tests/unit/test_simulation.py`.
- **Stop condition:** At least three known-answer cases pass exactly.

**Hand-off order:** `math-formalizer` -> `benchmark-runner` -> `algorithm-implementer` -> `unit-test-author`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-ensemble-stats` | Percentiles or intervals are computed | Applies the selected estimator and produces seeded bootstrap intervals. |
| `amf-schema-roundtrip` | A field is added to a result type | Proves `to_dict`/`from_dict` remains a fixed point. |
| `amf-invariant-spec` | An estimator property is claimed | Writes it into the docstring and mirrors it as a test. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/numerics/quantile_estimator.md`
- The selected estimator, named in output
- Seeded bootstrap intervals
- Known-answer tests

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The estimator is identified by its standard type and named in the output.
- [ ] Every reported percentile carries an interval.
- [ ] Bootstrap intervals are deterministic under a fixed seed.
- [ ] No numpy or scipy dependency is introduced.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Hyndman, R. J., & Fan, Y. (1996). "Sample Quantiles in Statistical Packages." *The American Statistician* 50(4), 361-365.
- Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC.
- Robert, C. P., & Casella, G. (2004). *Monte Carlo Statistical Methods* (2nd ed.). Springer.
- Spiegelhalter, D., Pearson, M., & Short, I. (2011). "Visualizing Uncertainty About the Future." *Science* 333(6048), 1393-1400.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.

## 11. Commit protocol

Commits from this project use the scope `p19`:

```text
docs(p19): identify and justify the sample-quantile estimator
feat(p19): report percentiles with seeded bootstrap intervals
test(p19): add known-answer quantile cases
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

