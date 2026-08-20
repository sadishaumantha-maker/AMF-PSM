# P26 - Null models and structural significance for AMF graph findings

**Track D - Graph & Network Theory of Market Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Network scientist |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` -> Theme D: Network Effects |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Every structural finding the framework reports - a feedback loop, an articulation point, a concentration score - is reported without any statement of what would be expected by chance in a comparable graph. Without a null model, a finding of "three feedback loops" carries no information about whether that is many or few for a seven-node dependency structure.

## 2. Purpose

Define null models appropriate to AMF dependency graphs, implement them deterministically, and express structural findings relative to the null so that a reader can tell signal from structure-by-construction.

## 3. Scope

**In scope**

- Selection of null models: degree-preserving rewiring and weight-preserving randomisation.
- A deterministic, seeded implementation with the standard library only.
- Reporting of at least one structural finding relative to its null distribution.

**Out of scope**

- Claiming statistical significance for any real market - the framework is illustrative, not validated.
- Any null model that requires market data.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Choose null models that preserve what is not in question and randomise what is; state both explicitly.
2. Note the constraint that AMF graphs have exactly seven nodes, so asymptotic network results do not apply - use exact or exhaustive enumeration where feasible.
3. Implement seeded randomisation reusing the P18 randomness policy.
4. For the example market, report feedback-loop count and articulation-point count against the null distribution.
5. Write the interpretation rules carefully: this is a structural comparison, never a claim about a real market.
6. Add the null-model context to the report renderers only if it can be stated without implying validation.

## 5. Task board

- [ ] Select and justify the null models.
- [ ] Implement seeded, deterministic randomisation.
- [ ] Compute null distributions for the example market.
- [ ] Report findings relative to null.
- [ ] Write the interpretation rules.
- [ ] Publish `docs/graph/null_models.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect the null-model literature applicable to very small directed weighted graphs.
- **Inputs:** The reading list.
- **Output artifact:** An annotated source table.
- **Stop condition:** At least one source addresses small-graph rather than asymptotic behaviour.

### `algorithm-implementer`

- **Mandate:** Implement seeded null-model generation with no new dependencies.
- **Inputs:** Selected models.
- **Output artifact:** A test-only or clearly separated implementation.
- **Stop condition:** Repeat runs with the same seed produce identical null distributions.

### `benchmark-runner`

- **Mandate:** Compute the null distributions and the observed statistics.
- **Inputs:** The implementation and the example market.
- **Output artifact:** A results table with reproduction commands.
- **Stop condition:** Every reported comparison names the null model and the seed.

### `red-team-critic`

- **Mandate:** Check that no sentence in the output can be read as a validated claim about a real market.
- **Inputs:** Draft output text.
- **Output artifact:** A wording critique.
- **Stop condition:** Every sentence survives the illustrative-not-validated test.

**Hand-off order:** `literature-scout` -> `algorithm-implementer` -> `benchmark-runner` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-graph-algorithm` | A structural statistic is compared to a null | Verifies the statistic and records the null model used. |
| `amf-ensemble-stats` | A null distribution is summarised | Applies the documented quantile estimator and seeded intervals. |
| `amf-red-team` | Any comparative claim is drafted | Tests the wording against the illustrative-not-validated rule. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/graph/null_models.md`
- A seeded null-model implementation
- Null distributions for the example market
- Interpretation rules

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every null model states what it preserves and what it randomises.
- [ ] Null distributions reproduce exactly under a fixed seed.
- [ ] No output sentence claims validated significance for a real market.
- [ ] Small-graph limitations are stated explicitly.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- Barabasi, A.-L. (2016). *Network Science*. Cambridge University Press.
- Jackson, M. O. (2008). *Social and Economic Networks*. Princeton University Press.
- Callaway, D. S., Newman, M. E. J., Strogatz, S. H., & Watts, D. J. (2000). "Network Robustness and Fragility: Percolation on Random Graphs." *Physical Review Letters* 85(25), 5468-5471.
- Albert, R., Jeong, H., & Barabasi, A.-L. (2000). "Error and attack tolerance of complex networks." *Nature* 406, 378-382.
- Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.

## 11. Commit protocol

Commits from this project use the scope `p26`:

```text
docs(p26): select null models appropriate to seven-node dependency graphs
feat(p26): add seeded null-model generation for structural comparison
docs(p26): report example-market structure relative to its null distribution
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
