# P27 - Derivation and defence of the fragility formula

**Track E - Diagnostics, Sensitivity & Leverage**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Quantitative methodologist |
| **Upstream** | `src/amf/diagnostics.py`; `CLAUDE.md` -> Diagnostics |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Per-system fragility is `criticality x (1 - health) x (1 - redundancy)`, a product of three terms. A product means any single term at zero zeroes the whole score: a fully redundant system is declared perfectly non-fragile no matter how critical or how unhealthy it is. Nobody has argued that this annihilation property is the intended semantics rather than an artefact of choosing multiplication.

## 2. Purpose

Derive the fragility functional form from stated axioms, test the annihilation property against the robustness literature, and either defend the product form explicitly or replace it with a form whose boundary behaviour is intended.

## 3. Scope

**In scope**

- A written axiom set for fragility (monotonicity, boundary behaviour, scale).
- A comparison of multiplicative, additive and mixed aggregations against those axioms.
- Measured effect of the choice on rankings across generated markets.

**Out of scope**

- Changing the blend weights across components - that is P29.
- Introducing any market-data quantity.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Write the axioms first: what must be true of fragility as each input moves, and what must happen at each boundary.
2. Check the product form against every axiom, especially the three annihilation cases (`criticality = 0`, `health = 1`, `redundancy = 1`).
3. Consult the biological and engineering robustness literature on whether redundancy fully substitutes for integrity; it generally does not, because redundant components share failure modes.
4. Compare candidate forms on the axioms, then measure ranking changes across generated markets.
5. Choose the form that satisfies the axioms, not the one that preserves existing numbers.
6. If the ranking changes, record it as a behavioural change with the axiom that forced it.

## 5. Task board

- [ ] Write the fragility axiom set.
- [ ] Evaluate the product form against each axiom.
- [ ] Survey redundancy substitution in the robustness literature.
- [ ] Compare candidate aggregations.
- [ ] Measure ranking impact across generated markets.
- [ ] Publish `docs/diagnostics/fragility_derivation.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State the axioms and test each candidate form against them.
- **Inputs:** `diagnostics.py`, the reading list.
- **Output artifact:** `docs/diagnostics/fragility_derivation.md`.
- **Stop condition:** Every axiom is either satisfied by the chosen form or explicitly waived with a reason.

### `literature-scout`

- **Mandate:** Find the primary evidence on whether redundancy substitutes for integrity in coupled systems.
- **Inputs:** The reading list.
- **Output artifact:** An annotated evidence table.
- **Stop condition:** At least three primary sources address common-mode failure in redundant components.

### `benchmark-runner`

- **Mandate:** Measure ranking changes under each candidate form.
- **Inputs:** Generated market corpus.
- **Output artifact:** A ranking-impact table.
- **Stop condition:** Rank correlation between forms is reported across at least one hundred markets.

### `red-team-critic`

- **Mandate:** Construct a market the chosen form scores absurdly.
- **Inputs:** The chosen form.
- **Output artifact:** A falsification attempt.
- **Stop condition:** No absurd case survives, or the form is revised.

**Hand-off order:** `math-formalizer` -> `literature-scout` -> `benchmark-runner` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | An axiom is adopted | Writes it into the docstring and mirrors it as a property test. |
| `amf-property-harness` | Monotonicity or boundary behaviour is claimed | Scaffolds the hypothesis property over the admissible box. |
| `amf-red-team` | A functional form is chosen | Searches for inputs where the form gives an indefensible score. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/diagnostics/fragility_derivation.md`
- An axiom-conformance table
- A ranking-impact measurement
- Any implemented form change

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every axiom is satisfied or explicitly waived with a written reason.
- [ ] The annihilation cases are addressed directly, not left implicit.
- [ ] Ranking impact is measured across at least one hundred generated markets.
- [ ] Scores remain inside `[0, 1]` for every admissible input.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Kitano, H. (2004). "Biological robustness." *Nature Reviews Genetics* 5, 826-837.
- Csete, M. E., & Doyle, J. C. (2002). "Reverse Engineering of Biological Complexity." *Science* 295(5560), 1664-1669.
- Carlson, J. M., & Doyle, J. (2002). "Complexity and robustness." *PNAS* 99(suppl 1), 2538-2545.
- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies*. Princeton University Press.
- OECD & European Commission JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. Wiley.
- Holling, C. S. (1973). "Resilience and Stability of Ecological Systems." *Annual Review of Ecology and Systematics* 4, 1-23.

## 11. Commit protocol

Commits from this project use the scope `p27`:

```text
docs(p27): derive the fragility axioms and test the product form against them
test(p27): measure ranking impact of candidate fragility aggregations
fix(p27): adopt the axiom-conforming fragility form
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
