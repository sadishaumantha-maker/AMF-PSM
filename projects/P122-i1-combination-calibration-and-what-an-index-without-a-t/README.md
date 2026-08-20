# P122 - I1 - combination, calibration, and what an index without a target can be scored against

**Track T - The Promised Research Modules**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2.5 weeks |
| **Lead role** | Forecast-evaluation researcher |
| **Upstream** | `docs/discussions/README.md` module I1 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

I1 promises a unified architecture built on forecast combination, proper scoring and calibration. Every one of those techniques scores a stated quantity against a realised outcome, and the framework has no realised outcome: its resilience index is a construct with no observable counterpart. The dispute is whether the module can be written at all, or whether it must first establish what the index would be scored against - and that question, once asked, is the most important one in the whole discussion directory.

## 2. Purpose

Establish what the framework's outputs could be scored against, and write the combination and calibration content only for whatever survives that test.

## 3. Scope

**In scope**

- The scoring-rule and calibration definitions stated exactly, including what each requires of its target.
- An enumeration of every quantity the framework emits and what, if anything, each could be scored against.
- A ruling per quantity: scoreable, scoreable only against a synthetic ground truth, or unscoreable.
- Combination content written only for the scoreable subset.

**Out of scope**

- Scoring anything against realised market outcomes.
- Any claim of validated performance, which the standing constraints forbid outright.
- A combination implementation in `src/amf/`.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Start with the enumeration, not the theory. Walk `report.Renderable` and list every quantity the framework publishes - the overall index, per-system scores, resilience, peak stress, settling time, sensitivities, leverage points - and ask of each what a correct value would even be.
2. Draw the distinction that resolves most cases: a quantity computed by definition from inputs is not scoreable, it is just the function's value, and calling it a prediction is a category error. Sensitivity gradients are different - they approximate a derivative that has a true value, so they can be checked against an analytic or higher-precision computation.
3. State the proper-scoring definitions exactly, because 'proper' is a technical property - the score is optimised by reporting one's true belief - and it has no content without a probability and an outcome.
4. Handle calibration honestly. Calibration is about probability statements, and the framework issues none; the severity bands are deterministic thresholds on a deterministic score. Say so plainly, because presenting a threshold as a calibrated probability would be the most damaging error the framework could make.
5. Write the combination content only where a target exists, which by the end of the enumeration will be a short list, and be explicit that it is short.
6. Hand the surviving evaluation questions to I2 rather than answering them here, and name the charter that owns it.

## 5. Task board

- [ ] Enumerate every published quantity from `report.Renderable`.
- [ ] Rule per quantity: scoreable, synthetic-only, or unscoreable.
- [ ] State the proper-scoring and calibration definitions exactly.
- [ ] Write the severity-bands-are-not-probabilities finding.
- [ ] Write combination content for the scoreable subset only.
- [ ] Publish `docs/discussions/I1-unified-framework-architecture.md` and relink it.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `api-surface-reviewer`

- **Mandate:** Enumerate every published quantity from the public surface, missing none.
- **Inputs:** `report.py`, `models.py`, `amf/__init__.py`.
- **Output artifact:** A complete quantity inventory.
- **Stop condition:** Every field of every result type appears in the inventory.

### `math-formalizer`

- **Mandate:** State proper scoring and calibration exactly and rule per quantity.
- **Inputs:** The inventory, the primary sources.
- **Output artifact:** A per-quantity ruling table.
- **Stop condition:** The definitional-versus-predictive distinction is applied to every row.

### `literature-scout`

- **Mandate:** Assemble the scoring, calibration and combination primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated bibliography.
- **Stop condition:** Propriety is cited to a source that defines it, not one that uses it.

### `spec-drafter`

- **Mandate:** Write the module and hand the evaluation questions to the I2 charter by name.
- **Inputs:** All of the above.
- **Output artifact:** `docs/discussions/I1-unified-framework-architecture.md`.
- **Stop condition:** The severity-bands finding is stated plainly and early.

### `red-team-critic`

- **Mandate:** Attack any presentation of a deterministic threshold as a calibrated probability.
- **Inputs:** The draft, `models.py`.
- **Output artifact:** An adversarial report.
- **Stop condition:** No band, score or index is described in probabilistic language.

**Hand-off order:** `api-surface-reviewer` -> `math-formalizer` -> `literature-scout` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-ensemble-stats` | Distributional output is discussed | Checks the percentile and summary conventions the package already uses. |
| `amf-invariant-spec` | Scoring properties are stated | Records what each definition requires of its target. |
| `amf-literature-brief` | The sources are assembled | Produces the annotated brief. |
| `amf-red-team` | The module is drafted | Scans for probabilistic language attached to deterministic output. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/discussions/I1-unified-framework-architecture.md`
- A complete published-quantity inventory
- A per-quantity scoreability ruling
- The severity-bands-are-not-probabilities finding

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The inventory covers every field of every published result type.
- [ ] Each quantity receives an explicit scoreability ruling.
- [ ] Propriety is defined, not assumed.
- [ ] The severity-bands finding appears early and plainly.
- [ ] Combination content is confined to the scoreable subset.
- [ ] The index link resolves.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Spiegelhalter, D., Pearson, M., & Short, I. (2011). "Visualizing Uncertainty About the Future." *Science* 333(6048), 1393-1400.
- Gigerenzer, G., Gaissmaier, W., Kurz-Milcke, E., Schwartz, L. M., & Woloshin, S. (2007). "Helping Doctors and Patients Make Sense of Health Statistics." *Psychological Science in the Public Interest* 8(2), 53-96.
- Manski, C. F. (2013). *Public Policy in an Uncertain World: Analysis and Decisions*. Harvard University Press.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press.
- Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC.
- Hyndman, R. J., & Fan, Y. (1996). "Sample Quantiles in Statistical Packages." *The American Statistician* 50(4), 361-365.
- Box, G. E. P. (1976). "Science and Statistics." *Journal of the American Statistical Association* 71(356), 791-799.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.
- Mitchell, M., et al. (2019). "Model Cards for Model Reporting." *Proceedings of the Conference on Fairness, Accountability, and Transparency*, 220-229.

## 11. Commit protocol

Commits from this project use the scope `p122`:

```text
docs(p122): inventory every published quantity and rule on its scoreability
docs(p122): record that the severity bands are thresholds, not probabilities
docs(p122): publish the I1 module and relink it from the index
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

