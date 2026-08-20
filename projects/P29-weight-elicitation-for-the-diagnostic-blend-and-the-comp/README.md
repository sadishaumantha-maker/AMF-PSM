# P29 - Weight elicitation for the diagnostic blend and the composite-index audit

**Track E - Diagnostics, Sensitivity & Leverage**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Quantitative methodologist |
| **Upstream** | `DiagnosticConfig` weights `0.4 / 0.3 / 0.3`; `CLAUDE.md` -> Diagnostics |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The three diagnostic components are combined with weights `0.4 / 0.3 / 0.3`, normalised by their sum. No source is given. A composite index whose weights are undocumented is not reproducible science, and the standard guidance on composite indicators requires that weighting be stated, justified and accompanied by an uncertainty analysis.

## 2. Purpose

Bring the diagnostic index into line with established composite-indicator methodology: document the weighting scheme, run the required uncertainty and sensitivity analysis, and report how much of the final ranking is driven by the weights rather than by the data.

## 3. Scope

**In scope**

- A documented weighting rationale, including equal weighting as the explicit null.
- An uncertainty analysis over the weight simplex, reporting rank stability.
- A variance-based sensitivity analysis attributing ranking variation to each component.

**Out of scope**

- Adding new components to the blend.
- Any weighting derived from market outcomes - that would make the index a predictive claim.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the current weights, their provenance, and the normalisation.
2. Adopt the standard composite-indicator workflow: theoretical framework, sub-indicator selection, normalisation, weighting, aggregation, uncertainty, sensitivity, back to the data.
3. Sample the weight simplex and measure how often the top-ranked finding changes.
4. Run a variance-based sensitivity analysis to attribute ranking variance to each component.
5. If rankings are unstable across the simplex, report that as the headline result - it means the index is weight-driven and must be presented as such.
6. Publish the uncertainty analysis alongside the index so no reader sees a rank without its stability.

## 5. Task board

- [ ] Document current weights and provenance.
- [ ] Implement weight-simplex sampling (seeded, deterministic).
- [ ] Measure rank stability across the simplex.
- [ ] Run variance-based attribution per component.
- [ ] Publish the uncertainty and sensitivity analysis.
- [ ] Add rank stability to the rendered report if it can be stated without implying validation.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Apply the composite-indicator construction workflow step by step and record each decision.
- **Inputs:** `diagnostics.py`, the reading list.
- **Output artifact:** `docs/diagnostics/weighting.md`.
- **Stop condition:** Every workflow step has a recorded decision, including the ones left at default.

### `benchmark-runner`

- **Mandate:** Sample the weight simplex and measure rank stability deterministically.
- **Inputs:** The index implementation.
- **Output artifact:** A rank-stability table with seeds and commands.
- **Stop condition:** Stability is reported for the top-1 and top-3 findings across the simplex.

### `math-formalizer`

- **Mandate:** Run the variance-based attribution and state its assumptions.
- **Inputs:** Sampling output.
- **Output artifact:** A sensitivity attribution section.
- **Stop condition:** First-order and total-effect indices are reported per component with their estimator.

### `docs-synthesizer`

- **Mandate:** Present the result so a reader cannot mistake a weight-driven rank for a data-driven one.
- **Inputs:** Both analyses.
- **Output artifact:** A published uncertainty section.
- **Stop condition:** Every reported rank appears with its stability figure.

**Hand-off order:** `spec-drafter` -> `benchmark-runner` -> `math-formalizer` -> `docs-synthesizer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-sensitivity-design` | A weighted index is analysed | Designs the simplex sampling and variance-based attribution experiment. |
| `amf-ensemble-stats` | Stability is summarised | Applies the documented estimator and seeded intervals. |
| `amf-doc-page` | Publishing the analysis | Enforces documentation conventions and the illustrative-not-validated rule. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/diagnostics/weighting.md`
- A rank-stability analysis over the weight simplex
- A variance-based attribution
- Reported stability alongside ranks

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The weighting scheme is documented with its provenance and its null alternative.
- [ ] Rank stability is measured over the weight simplex, deterministically.
- [ ] Variance-based indices are reported per component with their estimator named.
- [ ] No rank is published without its stability figure.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- OECD & European Commission JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. Wiley.
- Sobol', I. M. (2001). "Global sensitivity indices for nonlinear mathematical models and their Monte Carlo estimates." *Mathematics and Computers in Simulation* 55(1-3), 271-280.
- Morris, M. D. (1991). "Factorial Sampling Plans for Preliminary Computational Experiments." *Technometrics* 33(2), 161-174.
- Saltelli, A., et al. (2020). "Five ways to ensure that models serve society: a manifesto." *Nature* 582, 482-484.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- Spiegelhalter, D., Pearson, M., & Short, I. (2011). "Visualizing Uncertainty About the Future." *Science* 333(6048), 1393-1400.

## 11. Commit protocol

Commits from this project use the scope `p29`:

```text
docs(p29): document the diagnostic weighting scheme and its provenance
test(p29): measure rank stability across the weight simplex
docs(p29): publish variance-based attribution of ranking variance
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

