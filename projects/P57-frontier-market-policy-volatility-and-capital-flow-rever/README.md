# P57 - Frontier market policy volatility and capital-flow reversal

**Track I - Empirical Case Studies & Forensic Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Emerging markets researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Track 5 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The discussion treats frontier markets as a category defined by instability. That is an outcome-based definition dressed as a structural one, and it risks encoding a prejudice rather than a property. The framework needs frontier status defined by structure - which institutions exist, which do not - if the category is to be analytically useful.

## 2. Purpose

Define frontier market status structurally, and study policy volatility and capital-flow reversal as structural phenomena with an established theoretical literature rather than as a national characteristic.

## 3. Scope

**In scope**

- A structural definition of frontier status: which of the seven systems are present, absent or thin.
- A structural reading of sudden-stop dynamics and the policy trilemma.
- A jurisdiction set positioned structurally, with sources and vintages.

**Out of scope**

- Capital-flow volumes, exchange rates or reserve figures.
- Any characterisation of a country as risky, unstable or badly governed.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Define frontier status by structural presence and thinness, never by realised volatility.
2. Read the sudden-stop literature and express its mechanism structurally: an external funding dependency withdrawing, with no domestic substitute available.
3. Express the policy trilemma structurally: it constrains which immune-system configurations are simultaneously available.
4. Position the jurisdiction set on structural dimensions using published, dated sources from P50.
5. Write with the neutrality discipline established in P45; no country is characterised.
6. Note explicitly where informal and shadow finance make the structural picture incomplete, and link to that work.

## 5. Task board

- [ ] Write the structural definition of frontier status.
- [ ] Express sudden-stop dynamics structurally.
- [ ] Express the policy trilemma as an immune-system constraint.
- [ ] Position the jurisdiction set with dated sources.
- [ ] Run the neutrality review.
- [ ] Publish `docs/case_studies/frontier_markets.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish sudden stops and the trilemma from primary economic sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated mechanism summary.
- **Stop condition:** Both mechanisms are sourced from primary research.

### `regime-comparativist`

- **Mandate:** Position the jurisdiction set on structural dimensions with dated sources.
- **Inputs:** P50 profiles and official sources.
- **Output artifact:** A structural positioning table.
- **Stop condition:** Every position carries a source and a vintage.

### `spec-drafter`

- **Mandate:** Write the structural definition and the trilemma-as-constraint framing.
- **Inputs:** Mechanism summary and positioning.
- **Output artifact:** `docs/case_studies/frontier_markets.md`.
- **Stop condition:** Frontier status is defined without reference to realised volatility.

### `red-team-critic`

- **Mandate:** Scan for any sentence that characterises a country rather than a structure.
- **Inputs:** The draft.
- **Output artifact:** A neutrality critique.
- **Stop condition:** No country is characterised.

**Hand-off order:** `literature-scout` -> `regime-comparativist` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A jurisdiction is positioned | Produces the dated structural profile with citations. |
| `amf-case-dossier` | An episode is documented | Applies the protocol with source ranking and uncertainty. |
| `amf-red-team` | The document is drafted | Scans for country characterisation and outcome-based definitions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/case_studies/frontier_markets.md`
- A structural frontier definition
- A structural reading of sudden stops and the trilemma
- A dated positioning table

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Frontier status is defined structurally, never by realised volatility.
- [ ] No capital-flow, exchange-rate or reserve figure appears.
- [ ] No country is characterised as risky or badly governed.
- [ ] Every structural position carries a source and a vintage.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Calvo, G. A. (1998). "Capital Flows and Capital-Market Crises: The Simple Economics of Sudden Stops." *Journal of Applied Economics* 1(1), 35-54.
- Rey, H. (2015). "Dilemma not Trilemma: The Global Financial Cycle and Monetary Policy Independence." NBER Working Paper 21162.
- Obstfeld, M., Shambaugh, J. C., & Taylor, A. M. (2005). "The Trilemma in History: Tradeoffs Among Exchange Rates, Monetary Policies, and Capital Mobility." *Review of Economics and Statistics* 87(3), 423-438.
- Farhi, E., & Maggiori, M. (2018). "A Model of the International Monetary System." *Quarterly Journal of Economics* 133(1), 295-355.
- Pozsar, Z., Adrian, T., Ashcraft, A., & Boesky, H. (2013). "Shadow Banking." *FRBNY Economic Policy Review* 19(2), 1-16.
- Financial Stability Board (2011). *Shadow Banking: Scoping the Issues*. FSB Background Note.
- Demirguc-Kunt, A., Klapper, L., Singer, D., Ansar, S., & Hess, J. (2018). *The Global Findex Database 2017*. World Bank.
- Kaufmann, D., Kraay, A., & Mastruzzi, M. (2010). "The Worldwide Governance Indicators: Methodology and Analytical Issues." World Bank Policy Research Working Paper 5430.

## 11. Commit protocol

Commits from this project use the scope `p57`:

```text
docs(p57): define frontier market status structurally
docs(p57): express sudden stops and the trilemma as structural constraints
docs(p57): position jurisdictions with dated structural sources
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

