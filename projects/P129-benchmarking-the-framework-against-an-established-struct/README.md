# P129 - Benchmarking the framework against an established structural measure

**Track U - Method, Epistemics and External Validation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Quantitative methodologist |
| **Upstream** | P23; P80; P125 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework has never been compared to anything. Its rankings may agree with an established measure, disagree with it, or be uncorrelated, and all three would be informative - agreement suggests it recovers something known, disagreement locates where it differs, and no relationship suggests it measures noise. Without the comparison the framework's outputs have no reference point at all.

## 2. Purpose

Run the comparison against the one established measure that is structural rather than market-data-based, and report the result whatever it is.

## 3. Scope

**In scope**

- Selection of a comparator that is computable without market data.
- A rank-correlation comparison across generated markets.
- An honest report including the uncorrelated outcome.

**Out of scope**

- Comparators requiring returns, exposures or balance sheets.
- Tuning the framework to improve agreement.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Select the comparator from P80's filtered set - a DebtRank-style propagation measure is the strongest candidate because it is defined on a weighted network rather than on returns.
2. Implement the comparator faithfully to its source, and resist adapting it until it agrees; an adapted comparator measures nothing.
3. Compare on rankings rather than levels, since the two measures have no common scale and level comparison would be meaningless.
4. Pre-commit to reporting the result before running it, following P124's pre-registration practice, so a disappointing outcome cannot be quietly reframed.
5. Interpret carefully: agreement does not validate the framework, since both could be wrong in the same way, and this must be stated alongside a positive result.
6. Report the uncorrelated outcome as prominently as any other, because it is the most informative and the least welcome.

## 5. Task board

- [ ] Select and justify the comparator.
- [ ] Implement it faithfully to its source.
- [ ] Pre-commit to the reporting plan.
- [ ] Run the rank comparison across generated markets.
- [ ] State what agreement does and does not establish.
- [ ] Publish `docs/research/benchmark_comparison.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Recover the comparator's definition from its originating paper.
- **Inputs:** The reading list.
- **Output artifact:** A faithful definition.
- **Stop condition:** The definition comes from the source with no adaptation.

### `algorithm-implementer`

- **Mandate:** Implement the comparator without adapting it to improve agreement.
- **Inputs:** The definition.
- **Output artifact:** A test-only implementation.
- **Stop condition:** The implementation matches the source definition exactly.

### `benchmark-runner`

- **Mandate:** Run the rank comparison across generated markets with the plan pre-committed.
- **Inputs:** Both measures.
- **Output artifact:** A rank-correlation table with seeds.
- **Stop condition:** The comparison covers at least two hundred markets with reported uncertainty.

### `red-team-critic`

- **Mandate:** Check that no post-hoc adaptation improved agreement and that the reporting matches the pre-commitment.
- **Inputs:** The implementation history and the plan.
- **Output artifact:** An adaptation audit.
- **Stop condition:** No adaptation occurred after the first result was seen.

**Hand-off order:** `literature-scout` -> `algorithm-implementer` -> `benchmark-runner` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-graph-algorithm` | The comparator is implemented | Verifies it against its source paper and states complexity. |
| `amf-ensemble-stats` | Correlation is summarised | Applies the documented estimator and seeded intervals. |
| `amf-red-team` | The result is reported | Audits for post-hoc adaptation and reporting drift. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/research/benchmark_comparison.md`
- A faithful comparator implementation
- A rank-correlation result
- A pre-committed reporting record

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The comparator matches its source definition with no adaptation.
- [ ] The reporting plan was committed before the first result was seen.
- [ ] The uncorrelated outcome, if it occurs, is reported as prominently as any other.
- [ ] The document states that agreement does not constitute validation.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Battiston, S., Puliga, M., Kaushik, R., Tasca, P., & Caldarelli, G. (2012). "DebtRank: Too Central to Fail? Financial Networks, the FED and Systemic Risk." *Scientific Reports* 2, 541.
- Glasserman, P., & Young, H. P. (2016). "Contagion in Financial Networks." *Journal of Economic Literature* 54(3), 779-831.
- Acemoglu, D., Ozdaglar, A., & Tahbaz-Salehi, A. (2015). "Systemic Risk and Stability in Financial Networks." *American Economic Review* 105(2), 564-608.
- Elliott, M., Golub, B., & Jackson, M. O. (2014). "Financial Networks and Contagion." *American Economic Review* 104(10), 3115-3153.
- Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). "The preregistration revolution." *PNAS* 115(11), 2600-2606.
- Gelman, A., & Loken, E. (2014). "The Statistical Crisis in Science." *American Scientist* 102(6), 460-465.
- Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.

## 11. Commit protocol

Commits from this project use the scope `p129`:

```text
docs(p129): select and justify a structural comparator for benchmarking
test(p129): compare AMF rankings against the comparator across generated markets
docs(p129): report the benchmark outcome against the pre-committed plan
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

