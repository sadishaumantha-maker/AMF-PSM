# P37 - Multi-wave shocks and timing-independent normalisation

**Track F - Shock Propagation, Cascades & Resilience**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Simulation engineer |
| **Upstream** | `Shock.at_step`; "amplification/absorption use total injected load as a timing-independent denominator" |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Multi-wave shocks extend the horizon to cover the last injection, and amplification and absorption are normalised by total injected load so that the metric does not depend on timing. But the *trajectory* certainly depends on timing: two waves arriving together and two waves arriving far apart produce different peaks. A timing-independent denominator with a timing-dependent numerator needs an argument.

## 2. Purpose

State precisely what the normalisation makes comparable and what it does not, and add a timing-explicit companion metric so that wave spacing is visible rather than normalised away.

## 3. Scope

**In scope**

- A formal statement of the normalisation and the comparison it licenses.
- Measurement of how peak stress varies with wave spacing at constant total injected load.
- A companion metric that exposes timing sensitivity.

**Out of scope**

- Removing the existing metrics.
- Exposing multi-wave shocks through the CLI - they remain a Python API feature.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the normalisation formally and identify exactly which comparisons it makes valid.
2. Design an experiment holding total injected load constant while varying wave spacing from simultaneous to fully separated.
3. Measure peak stress, settling time and absorbed fraction across that spacing sweep.
4. Where the normalised metric is flat and the trajectory is not, that is the finding: report a timing-sensitivity companion.
5. Extend `examples/cascade_scenario.py` with a spacing demonstration if it clarifies the point.
6. Add the example to `tests/integration/test_examples.py` if it becomes a covered example.

## 5. Task board

- [ ] Formalise the normalisation and its licensed comparisons.
- [ ] Implement the constant-load spacing sweep.
- [ ] Measure trajectory metrics across spacing.
- [ ] Add a timing-sensitivity companion metric.
- [ ] Extend the cascade example if warranted.
- [ ] Publish `docs/simulation/multiwave.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State the normalisation and the exact comparison class it licenses.
- **Inputs:** `simulation.py`.
- **Output artifact:** `docs/simulation/multiwave.md`.
- **Stop condition:** The document names at least one comparison the normalisation does not license.

### `benchmark-runner`

- **Mandate:** Run the constant-load spacing sweep and report trajectory variation.
- **Inputs:** The simulator.
- **Output artifact:** A spacing sensitivity table.
- **Stop condition:** Peak stress variation is reported across at least six spacing levels.

### `algorithm-implementer`

- **Mandate:** Add the timing-sensitivity companion metric.
- **Inputs:** The measurements.
- **Output artifact:** A diff under `src/amf/simulation.py` and `models.py`.
- **Stop condition:** The new field round-trips through `to_dict()` and `mypy` strict passes.

### `unit-test-author`

- **Mandate:** Pin the constant-load invariance of the normalised metrics with a test.
- **Inputs:** The implementation.
- **Output artifact:** Cases in `tests/unit/test_simulation.py`.
- **Stop condition:** Normalised metrics are invariant to spacing at constant load, and the companion metric is not.

**Hand-off order:** `math-formalizer` -> `benchmark-runner` -> `algorithm-implementer` -> `unit-test-author`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | A normalisation invariance is claimed | Writes it into the docstring and mirrors it as a test. |
| `amf-schema-roundtrip` | A metric is added | Proves `to_dict`/`from_dict` remains a fixed point. |
| `amf-property-harness` | Invariance is claimed over a family of inputs | Scaffolds the hypothesis property. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/simulation/multiwave.md`
- A spacing sensitivity table
- A timing-sensitivity companion metric
- Invariance tests

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The normalisation names at least one comparison it does not license.
- [ ] Spacing sensitivity is measured at constant total injected load.
- [ ] Normalised metrics are provably spacing-invariant; the companion metric is not.
- [ ] Multi-wave shocks remain a Python API feature, not a CLI flag.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Gai, P., & Kapadia, S. (2010). "Contagion in financial networks." *Proceedings of the Royal Society A* 466(2120), 2401-2423.
- Acemoglu, D., Ozdaglar, A., & Tahbaz-Salehi, A. (2015). "Systemic Risk and Stability in Financial Networks." *American Economic Review* 105(2), 564-608.
- Watts, D. J. (2002). "A simple model of global cascades on random networks." *PNAS* 99(9), 5766-5771.
- Strogatz, S. H. (2015). *Nonlinear Dynamics and Chaos* (2nd ed.). Westview Press.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- Grimm, V., et al. (2020). "The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update." *Journal of Artificial Societies and Social Simulation* 23(2), 7.

## 11. Commit protocol

Commits from this project use the scope `p37`:

```text
docs(p37): state what the timing-independent normalisation does and does not license
test(p37): measure trajectory sensitivity to wave spacing at constant load
feat(p37): report a timing-sensitivity companion metric
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

