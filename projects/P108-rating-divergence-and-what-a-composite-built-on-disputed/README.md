# P108 - Rating divergence and what a composite built on disputed inputs inherits

**Track S - Climate, Nature and Long-Horizon Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Research lead |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 8.2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The published research on sustainability ratings finds substantial divergence between providers rating the same entity - they disagree on measurement, on scope and on weighting. Any framework consuming such ratings inherits that divergence. The framework's own composite indices have exactly the same structure, which makes this a mirror the framework should look into rather than a topic about someone else.

## 2. Purpose

Use the rating-divergence findings as a diagnostic for the framework's own composite construction, and decide whether AMF's indices would survive the same scrutiny.

## 3. Scope

**In scope**

- A summary of the measured divergence and its decomposed causes.
- An application of the same decomposition to AMF's own composites.
- A ruling on whether AMF indices should be reported as single numbers at all.

**Out of scope**

- Consuming any rating product.
- Rating any entity.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Take the divergence decomposition from the primary work: measurement, scope and weight divergence are distinct causes with different remedies.
2. Apply each to AMF. Measurement divergence corresponds to the metric definitions; scope to which systems are included; weight to P29's and P39's blend weights, whose stability is already known to be untested.
3. This is the uncomfortable part and the point of the charter: if independent teams implementing the framework would produce materially different indices, then the index is a convention rather than a measurement.
4. Design the test: have two people independently populate the same market from the same description and compare the resulting indices. That is a direct measure of the framework's own inter-rater divergence.
5. Rule on single-number reporting, informed by P29's weight-simplex stability results.
6. Report the outcome plainly whichever way it falls.

## 5. Task board

- [ ] Summarise the divergence decomposition from the primary work.
- [ ] Apply each cause to AMF's composites.
- [ ] Design and run the inter-rater exercise.
- [ ] Combine with P29's weight-stability results.
- [ ] Rule on single-number reporting.
- [ ] Publish `docs/research/composite_divergence.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Recover the divergence decomposition from the primary study.
- **Inputs:** The reading list.
- **Output artifact:** An annotated decomposition.
- **Stop condition:** The three causes are taken from the source with their measured contributions.

### `benchmark-runner`

- **Mandate:** Run the inter-rater exercise and report the divergence.
- **Inputs:** A market description and two independent populations of it.
- **Output artifact:** A divergence measurement.
- **Stop condition:** Index divergence between independent populations is reported with the exercise design.

### `spec-drafter`

- **Mandate:** Rule on single-number reporting using both evidence sources.
- **Inputs:** The measurement and P29's stability results.
- **Output artifact:** `docs/research/composite_divergence.md`.
- **Stop condition:** The ruling cites both the inter-rater and the weight-stability evidence.

### `red-team-critic`

- **Mandate:** Argue the framework's index is a convention rather than a measurement.
- **Inputs:** The evidence.
- **Output artifact:** A dissent section.
- **Stop condition:** The dissent is answered with measurement or conceded.

**Hand-off order:** `literature-scout` -> `benchmark-runner` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-sensitivity-design` | Divergence is decomposed | Designs the attribution across measurement, scope and weight. |
| `amf-ensemble-stats` | Divergence is summarised | Applies the documented estimator and seeded intervals. |
| `amf-red-team` | A single-number report is proposed | Argues the number is a convention and demands evidence. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/research/composite_divergence.md`
- An applied divergence decomposition
- An inter-rater divergence measurement
- A ruling on single-number reporting

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The three divergence causes are applied to AMF's own composites.
- [ ] Inter-rater divergence is measured, not estimated.
- [ ] The ruling cites both inter-rater and weight-stability evidence.
- [ ] The outcome is reported plainly even if unflattering.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Berg, F., Koelbel, J. F., & Rigobon, R. (2022). "Aggregate Confusion: The Divergence of ESG Ratings." *Review of Finance* 26(6), 1315-1344.
- OECD & European Commission JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. Wiley.
- Saltelli, A., et al. (2020). "Five ways to ensure that models serve society: a manifesto." *Nature* 582, 482-484.
- Krueger, P., Sautner, Z., & Starks, L. T. (2020). "The Importance of Climate Risks for Institutional Investors." *Review of Financial Studies* 33(3), 1067-1111.
- Bingler, J. A., Kraus, M., Leippold, M., & Webersinke, N. (2022). "Cheap talk and cherry-picking: What ClimateBert has to say on corporate climate risk disclosures." *Finance Research Letters* 47, 102776.
- Gelman, A., & Loken, E. (2014). "The Statistical Crisis in Science." *American Scientist* 102(6), 460-465.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.

## 11. Commit protocol

Commits from this project use the scope `p108`:

```text
docs(p108): apply the rating-divergence decomposition to AMF's own composites
test(p108): measure inter-rater divergence on independently populated markets
docs(p108): rule on whether AMF indices may be reported as single numbers
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
