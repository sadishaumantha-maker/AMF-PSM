# P39 - The resilience composite and early-warning signal candidates

**Track F - Shock Propagation, Cascades & Resilience**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Quantitative methodologist |
| **Upstream** | `resilience = 0.6 x absorbed + 0.25 x (1 - amp_penalty) + 0.15 x (1 - settle_penalty)` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Resilience is a three-term weighted composite with weights `0.6 / 0.25 / 0.15` and no stated source. Separately, the resilience literature has well-known candidate early-warning indicators - rising variance, rising autocorrelation, critical slowing down - and the framework already computes a full trajectory from which several of them could be derived, but computes none of them.

## 2. Purpose

Audit the composite as a composite index, and evaluate whether trajectory-derived early-warning indicators are better structural summaries than the current hand-weighted blend.

## 3. Scope

**In scope**

- A composite-index audit of the resilience score, including weight sensitivity.
- Implementation of trajectory-derived indicators, notably a critical-slowing-down proxy.
- A comparison of the composite against the indicators as summaries of the same trajectory.

**Out of scope**

- Claiming any indicator predicts a real market event.
- Adding any indicator that requires time-series market data.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Apply the same composite-index workflow used in P29 to the resilience score.
2. Measure rank stability of stress-test orderings across the resilience weight simplex.
3. Implement critical-slowing-down proxies computable from the framework's own trajectory: recovery rate after perturbation, and lag-one autocorrelation of the stress path.
4. Compare what each summary tells a reader that the others do not.
5. Report indicators alongside the composite rather than replacing it, unless the comparison clearly favours replacement.
6. State plainly that these are model-internal indicators, with no validated relationship to real market transitions.

## 5. Task board

- [ ] Audit the resilience composite as a composite index.
- [ ] Measure rank stability across the weight simplex.
- [ ] Implement critical-slowing-down proxies.
- [ ] Compare summaries on the same trajectories.
- [ ] Report indicators alongside the composite.
- [ ] Publish `docs/simulation/resilience_composite.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect the primary early-warning-signal literature and identify which indicators are computable here.
- **Inputs:** The reading list.
- **Output artifact:** An indicator feasibility table.
- **Stop condition:** Each indicator is marked computable, computable-with-changes, or requiring market data.

### `benchmark-runner`

- **Mandate:** Measure resilience rank stability across the weight simplex.
- **Inputs:** The simulator and generated markets.
- **Output artifact:** A stability table.
- **Stop condition:** Stress-test rank stability is reported across the simplex.

### `algorithm-implementer`

- **Mandate:** Implement the feasible indicators with no new dependencies.
- **Inputs:** The feasibility table.
- **Output artifact:** A diff under `src/amf/simulation.py` and `models.py`.
- **Stop condition:** New fields round-trip and `mypy` strict passes.

### `red-team-critic`

- **Mandate:** Check that no indicator is presented as an early warning of a real event.
- **Inputs:** Draft output and documentation.
- **Output artifact:** A wording critique.
- **Stop condition:** Every indicator is explicitly model-internal in every rendered format.

**Hand-off order:** `literature-scout` -> `benchmark-runner` -> `algorithm-implementer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-sensitivity-design` | Composite weights are audited | Designs the simplex sampling and reports rank stability. |
| `amf-ensemble-stats` | Indicators are summarised | Applies the documented estimator and seeded intervals. |
| `amf-red-team` | An indicator is named | Checks the name and surrounding text cannot imply a real-world forecast. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/simulation/resilience_composite.md`
- A weight stability analysis
- Trajectory-derived indicators
- A summary comparison

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The composite is audited under the composite-indicator workflow with published weight sensitivity.
- [ ] At least one critical-slowing-down proxy is implemented and tested.
- [ ] Every indicator is explicitly model-internal in text, markdown and JSON output.
- [ ] No new runtime dependency is added.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Scheffer, M., et al. (2009). "Early-warning signals for critical transitions." *Nature* 461, 53-59.
- Scheffer, M. (2009). *Critical Transitions in Nature and Society*. Princeton University Press.
- Holling, C. S. (1973). "Resilience and Stability of Ecological Systems." *Annual Review of Ecology and Systematics* 4, 1-23.
- OECD & European Commission JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. Wiley.
- May, R. M., Levin, S. A., & Sugihara, G. (2008). "Ecology for bankers." *Nature* 451, 893-895.
- Adrian, T., & Brunnermeier, M. K. (2016). "CoVaR." *American Economic Review* 106(7), 1705-1741.
- Acharya, V. V., Pedersen, L. H., Philippon, T., & Richardson, M. (2017). "Measuring Systemic Risk." *Review of Financial Studies* 30(1), 2-47.

## 11. Commit protocol

Commits from this project use the scope `p39`:

```text
docs(p39): audit the resilience composite under composite-indicator methodology
feat(p39): add trajectory-derived critical-slowing-down proxies
docs(p39): compare the composite against early-warning indicator summaries
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

