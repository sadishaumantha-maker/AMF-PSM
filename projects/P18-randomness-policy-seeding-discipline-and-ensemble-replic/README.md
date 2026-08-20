# P18 - Randomness policy, seeding discipline and ensemble replication

**Track C - Numerical Correctness & Determinism**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Simulation engineer |
| **Upstream** | `SimulationConfig.jitter` / `seed`; `ShockSimulator.ensemble` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Ensemble replication `i` uses `base_seed + i`. Sequential seeding of a single generator is a known source of correlated streams in Monte Carlo work, and the repository's own determinism guarantee makes the choice of generator a published property rather than an implementation detail. The dispute is whether `base_seed + i` is defensible for an instrument that reports percentiles.

## 2. Purpose

Set an explicit randomness policy: which generator, how streams are derived per replication, what statistical evidence supports independence, and how a published percentile is reproduced exactly.

## 3. Scope

**In scope**

- An analysis of stream-derivation strategies: sequential seeds, splitting, and counter-based generation.
- Empirical independence checks across replication streams at the ensemble sizes actually used.
- A documented reproduction recipe for any published percentile.

**Out of scope**

- Adding numpy or any external RNG library.
- Making the default configuration non-deterministic.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Document the current behaviour exactly, including that `jitter` has no effect unless `seed` is set.
2. Review the generator guarantees of the standard library implementation actually used, and state them.
3. Compare sequential seeding against stream splitting on correlation between replications at realistic run counts.
4. Run empirical tests for inter-stream correlation; report effect sizes rather than pass/fail alone.
5. If sequential seeding survives the evidence, document why. If not, implement splitting and record the changed numbers.
6. Write the reproduction recipe: given a published percentile, the exact inputs that regenerate it.

## 5. Task board

- [ ] Document current seeding behaviour precisely.
- [ ] Write the stream-derivation comparison.
- [ ] Implement the inter-stream correlation test harness.
- [ ] Report measured correlations at realistic ensemble sizes.
- [ ] Implement splitting if the evidence requires it.
- [ ] Publish `docs/numerics/randomness_policy.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `numerics-auditor`

- **Mandate:** State the generator's guarantees and the risk profile of sequential seeding.
- **Inputs:** `simulation.py`, the reading list.
- **Output artifact:** A generator guarantee note.
- **Stop condition:** The note names the generator, its period and its known weaknesses.

### `benchmark-runner`

- **Mandate:** Measure inter-stream correlation across replications at the ensemble sizes in use.
- **Inputs:** The ensemble implementation.
- **Output artifact:** A measurement table with reproduction commands.
- **Stop condition:** Correlation estimates are reported with uncertainty, at more than one ensemble size.

### `algorithm-implementer`

- **Mandate:** Implement stream splitting only if the measurements justify it.
- **Inputs:** Measurements.
- **Output artifact:** A diff under `src/amf/simulation.py`.
- **Stop condition:** The default configuration remains fully deterministic with `jitter=0.0`.

### `determinism-prover`

- **Mandate:** Prove that a seeded ensemble reproduces exactly across runs and platforms in the tested matrix.
- **Inputs:** The implementation.
- **Output artifact:** Reproduction tests.
- **Stop condition:** The same seed yields identical percentiles on 3.11, 3.12 and 3.13.

**Hand-off order:** `numerics-auditor` -> `benchmark-runner` -> `algorithm-implementer` -> `determinism-prover`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-ensemble-stats` | Ensemble machinery changes | Recomputes percentiles with the documented estimator and checks reproduction. |
| `amf-determinism-audit` | Any seeded path changes | Verifies identical output for identical seeds across the test matrix. |
| `amf-changelog-entry` | Any published percentile changes | Records the change and the measurement that drove it. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/numerics/randomness_policy.md`
- A correlation measurement table
- Any implemented stream-splitting change
- Cross-version reproduction tests

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The generator and stream-derivation strategy are documented as public properties.
- [ ] Inter-stream correlation is measured, not assumed.
- [ ] The default configuration remains fully deterministic.
- [ ] The same seed reproduces identical percentiles across the CI Python matrix.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Matsumoto, M., & Nishimura, T. (1998). "Mersenne Twister: a 623-dimensionally equidistributed uniform pseudo-random number generator." *ACM TOMACS* 8(1), 3-30.
- L'Ecuyer, P., & Simard, R. (2007). "TestU01: A C library for empirical testing of random number generators." *ACM Transactions on Mathematical Software* 33(4), 22.
- O'Neill, M. E. (2014). "PCG: A Family of Simple Fast Space-Efficient Statistically Good Algorithms for Random Number Generation." Harvey Mudd College Technical Report HMC-CS-2014-0905.
- Robert, C. P., & Casella, G. (2004). *Monte Carlo Statistical Methods* (2nd ed.). Springer.
- Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC.
- Sandve, G. K., Nekrutenko, A., Taylor, J., & Hovig, E. (2013). "Ten Simple Rules for Reproducible Computational Research." *PLoS Computational Biology* 9(10), e1003285.

## 11. Commit protocol

Commits from this project use the scope `p18`:

```text
docs(p18): publish the randomness and seeding policy for ensembles
test(p18): measure inter-stream correlation across replications
fix(p18): derive replication streams by splitting rather than sequential seeds
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
