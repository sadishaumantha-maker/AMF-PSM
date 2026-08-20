# P23 - Centrality selection: Katz against betweenness, eigenvector and DebtRank

**Track D - Graph & Network Theory of Market Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Network scientist |
| **Upstream** | `CLAUDE.md`: "Nothing in the scoring pipeline consumes centrality; it is a standalone query." |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Katz centrality was chosen over eigenvector centrality because it is well defined on acyclic graphs. But nothing consumes it, so the choice has never been tested against its purpose. Financial-network research uses several different centralities for different questions, and at least one - DebtRank - was designed specifically for propagation of distress rather than for status.

## 2. Purpose

Decide what question centrality is meant to answer in AMF, evaluate the candidate measures against that question on the framework's own graphs, and either wire the winner into the pipeline or document why centrality remains a standalone diagnostic.

## 3. Scope

**In scope**

- A statement of the question centrality answers in this framework.
- A comparative evaluation of Katz, betweenness, eigenvector and a DebtRank-style propagation measure.
- Rank-correlation analysis across the example markets and generated variants.
- A decision: adopt into the pipeline, keep standalone, or remove.

**Out of scope**

- Introducing any measure that requires prices, returns or exposures - forbidden by the non-trading rule.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Write down the question first. "Which system's failure propagates furthest" and "which system is most depended upon" are different questions with different right answers.
2. Implement each candidate as a structural measure on the dependency graph, using weights only, never market data.
3. Compare rankings using rank correlation across the example market and at least fifty generated variants.
4. Check agreement with the framework's own shock simulation: does the measure predict which single-system shock produces the largest peak stress?
5. Choose on that agreement, not on elegance.
6. If no measure predicts well, that is the finding - report it rather than adopting one anyway.

## 5. Task board

- [ ] State the question centrality must answer.
- [ ] Implement the candidate measures as structural queries.
- [ ] Run rank-correlation comparison across generated markets.
- [ ] Test agreement against simulated peak stress.
- [ ] Decide adopt / keep standalone / remove.
- [ ] Publish `docs/graph/centrality_selection.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect the primary sources for each candidate measure and the financial-network results that use them.
- **Inputs:** The reading list.
- **Output artifact:** An annotated source table.
- **Stop condition:** Every candidate has a primary source, not a secondary summary.

### `algorithm-implementer`

- **Mandate:** Implement each candidate as a pure structural query with no market data.
- **Inputs:** Primary sources.
- **Output artifact:** Implementations plus a comparison harness.
- **Stop condition:** The non-trading naming guard passes for every new name.

### `benchmark-runner`

- **Mandate:** Measure rank correlation and agreement with simulated peak stress.
- **Inputs:** Implementations and generated markets.
- **Output artifact:** A measurement table with reproduction commands.
- **Stop condition:** At least fifty generated markets are covered with reported uncertainty.

### `red-team-critic`

- **Mandate:** Argue that centrality should be removed entirely, and see whether the evidence defeats the argument.
- **Inputs:** The measurements.
- **Output artifact:** A dissent section.
- **Stop condition:** The dissent is either adopted or answered with measurement.

**Hand-off order:** `literature-scout` -> `algorithm-implementer` -> `benchmark-runner` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-centrality-diagnostics` | Any centrality is computed | Validates convergence and reports the measure's stated question. |
| `amf-boundary-check` | New measures are named | Runs the non-trading naming guard against the forbidden substring list. |
| `amf-red-team` | Before adopting a measure | Argues for removal and forces the evidence to answer. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/graph/centrality_selection.md`
- Candidate implementations
- A rank-correlation and predictive-agreement table
- The adoption decision

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The question centrality answers is stated before any measure is compared.
- [ ] Agreement with simulated peak stress is measured across at least fifty markets.
- [ ] The decision cites the measurement, and the negative result is reportable.
- [ ] No candidate uses prices, returns or exposures.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Katz, L. (1953). "A new status index derived from sociometric analysis." *Psychometrika* 18(1), 39-43.
- Bonacich, P. (1987). "Power and Centrality: A Family of Measures." *American Journal of Sociology* 92(5), 1170-1182.
- Freeman, L. C. (1977). "A Set of Measures of Centrality Based on Betweenness." *Sociometry* 40(1), 35-41.
- Battiston, S., Puliga, M., Kaushik, R., Tasca, P., & Caldarelli, G. (2012). "DebtRank: Too Central to Fail? Financial Networks, the FED and Systemic Risk." *Scientific Reports* 2, 541.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- Jackson, M. O. (2008). *Social and Economic Networks*. Princeton University Press.
- Glasserman, P., & Young, H. P. (2016). "Contagion in Financial Networks." *Journal of Economic Literature* 54(3), 779-831.

## 11. Commit protocol

Commits from this project use the scope `p23`:

```text
docs(p23): state the question centrality must answer in AMF
test(p23): compare candidate centralities against simulated peak stress
docs(p23): record the centrality adoption decision with its measurements
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
