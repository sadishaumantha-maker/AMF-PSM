# P31 - From one-at-a-time perturbation to a defensible sensitivity design

**Track E - Diagnostics, Sensitivity & Leverage**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Sensitivity analyst |
| **Upstream** | `SensitivityAnalyzer`; `SensitivityConfig.step` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Sensitivity is computed by moving one metric of one system at a time and re-diagnosing. One-at-a-time designs are known to explore only a thin cross through the input space and to miss interactions entirely. Since the diagnostic score is an explicit product of interacting terms, interactions are not a theoretical worry here - they are the mechanism.

## 2. Purpose

Upgrade the sensitivity design from one-at-a-time to a method that can detect interactions, while keeping the result deterministic, dependency-free and cheap enough to run in CI.

## 3. Scope

**In scope**

- A written critique of the current design against established sensitivity-analysis practice.
- Implementation of an elementary-effects screening design with the standard library only.
- Optional variance-based indices where the cost is affordable at seven systems and four metrics.
- Preservation of the existing gradient and span reporting for continuity.

**Out of scope**

- Adding SALib, numpy or scipy.
- Removing the existing one-at-a-time output before the replacement is validated.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the current design precisely, including that the difference is central where the metric has room on both sides and one-sided near a bound, which is why `span` is reported.
2. Set out the known limitations of one-at-a-time designs and why they bite for a multiplicative score.
3. Implement elementary-effects screening with a deterministic trajectory design and a seeded generator.
4. Where affordable, add variance-based first-order and total-effect indices; the input dimension here is small enough to make this feasible.
5. Report interactions explicitly: a large total effect with a small first-order effect is the finding.
6. Keep the existing gradient output so downstream consumers are not broken while the new design is validated.

## 5. Task board

- [ ] Write the design critique.
- [ ] Implement elementary-effects screening deterministically.
- [ ] Implement variance-based indices where affordable.
- [ ] Report interaction findings explicitly.
- [ ] Validate against the existing gradients on a known case.
- [ ] Publish `docs/sensitivity/design.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect the primary methodological sources for screening and variance-based designs.
- **Inputs:** The reading list.
- **Output artifact:** An annotated source table.
- **Stop condition:** Each method has its originating paper, not a textbook summary alone.

### `algorithm-implementer`

- **Mandate:** Implement the designs with the standard library only, preserving determinism.
- **Inputs:** The methodological sources.
- **Output artifact:** A diff under `src/amf/sensitivity.py`.
- **Stop condition:** Repeat runs with a fixed seed produce identical indices; `mypy` strict passes.

### `math-formalizer`

- **Mandate:** State each estimator, its bias and its convergence behaviour at the sample sizes used.
- **Inputs:** The implementation.
- **Output artifact:** An estimator section in the docs.
- **Stop condition:** Every reported index names its estimator and sample size.

### `benchmark-runner`

- **Mandate:** Validate the new design against the existing gradients on a case with a known analytic answer.
- **Inputs:** Both designs.
- **Output artifact:** A validation table.
- **Stop condition:** The methods agree where they should and the disagreement is explained where they do not.

**Hand-off order:** `literature-scout` -> `algorithm-implementer` -> `math-formalizer` -> `benchmark-runner`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-sensitivity-design` | A perturbation experiment is designed | Selects the design, sets the sample size and generates the deterministic trajectory. |
| `amf-ensemble-stats` | Indices are summarised | Applies the documented estimator and seeded intervals. |
| `amf-config-validator` | New sensitivity knobs are added | Adds `InvalidConfigError` validation with boundary tests. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/sensitivity/design.md`
- An elementary-effects implementation
- Variance-based indices where affordable
- A validation table against the existing gradients

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Interactions are detectable and are reported explicitly.
- [ ] Every index names its estimator and sample size.
- [ ] Results reproduce exactly under a fixed seed.
- [ ] No new runtime dependency; the existing gradient output still works.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Morris, M. D. (1991). "Factorial Sampling Plans for Preliminary Computational Experiments." *Technometrics* 33(2), 161-174.
- Sobol', I. M. (2001). "Global sensitivity indices for nonlinear mathematical models and their Monte Carlo estimates." *Mathematics and Computers in Simulation* 55(1-3), 271-280.
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. Wiley.
- Saltelli, A., et al. (2020). "Five ways to ensure that models serve society: a manifesto." *Nature* 582, 482-484.
- OECD & European Commission JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- Robert, C. P., & Casella, G. (2004). *Monte Carlo Statistical Methods* (2nd ed.). Springer.

## 11. Commit protocol

Commits from this project use the scope `p31`:

```text
docs(p31): critique the one-at-a-time sensitivity design against established practice
feat(p31): add deterministic elementary-effects screening
feat(p31): report variance-based indices and explicit interaction findings
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
