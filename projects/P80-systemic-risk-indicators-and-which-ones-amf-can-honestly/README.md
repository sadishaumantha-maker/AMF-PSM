# P80 - Systemic risk indicators and which ones AMF can honestly compute

**Track N - Policy-Market Contagion and Systemic Indicators**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Systemic risk researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 3.3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The established systemic-risk measures - conditional value-at-risk contributions, marginal expected shortfall, connectedness from variance decompositions, DebtRank - are almost all built from market data or balance-sheet exposures. The framework forbids both. Either there is a structural subset it can compute, or the framework's relationship to the systemic-risk literature is rhetorical rather than methodological.

## 2. Purpose

Audit the published indicator set against what AMF is permitted and able to compute, and state the result honestly - including the possibility that most of the literature is out of reach by construction.

## 3. Scope

**In scope**

- A survey of the principal published systemic-risk indicators and their exact data requirements.
- A per-indicator verdict: computable structurally, computable with a stated structural proxy, or out of reach.
- Implementation of any indicator that is genuinely computable.

**Out of scope**

- Any indicator requiring returns, prices, exposures or balance-sheet data.
- Claiming a structural proxy measures what the market-data indicator measures.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Take each indicator from its originating paper, and write down its inputs exactly - most require a return series or an exposure matrix.
2. Apply the non-trading boundary as a hard filter, before considering whether a proxy is possible.
3. Where a purely structural analogue exists, note that DebtRank is the closest, because it propagates distress over a network rather than over returns - and check what it needs that the framework lacks.
4. For each proxy proposed, state what it does *not* capture relative to the original, and require that statement to travel with the number.
5. Implement only what survives. An honest short list beats a long list of proxies that quietly change meaning.
6. Report the negative result prominently: if most of the literature is out of reach, that is the framework's position and should be stated rather than obscured.

## 5. Task board

- [ ] Survey the indicators and record exact input requirements.
- [ ] Apply the non-trading filter per indicator.
- [ ] Assess structural analogues, DebtRank in particular.
- [ ] State per proxy what it does not capture.
- [ ] Implement the survivors.
- [ ] Publish `docs/research/systemic_indicators.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect each indicator from its originating paper with its exact inputs.
- **Inputs:** The reading list.
- **Output artifact:** An indicator input table.
- **Stop condition:** Every indicator's inputs are taken from the source, not from a survey summary.

### `boundary-sentinel`

- **Mandate:** Filter the indicator set against the non-trading boundary before any proxy is considered.
- **Inputs:** The input table.
- **Output artifact:** A filtered set with verdicts.
- **Stop condition:** Every indicator is marked computable, proxy-possible or out of reach.

### `algorithm-implementer`

- **Mandate:** Implement only the indicators that survive, with no new dependencies.
- **Inputs:** The filtered set.
- **Output artifact:** A diff under `src/amf/`.
- **Stop condition:** `mypy` strict passes and every new public name clears the naming guard.

### `red-team-critic`

- **Mandate:** Check that no structural proxy is presented as equivalent to its market-data original.
- **Inputs:** The draft.
- **Output artifact:** An equivalence-claim report.
- **Stop condition:** Every proxy carries its non-capture statement.

**Hand-off order:** `literature-scout` -> `boundary-sentinel` -> `algorithm-implementer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-boundary-check` | An indicator is assessed | Applies the forbidden-substring filter and rejects market-data inputs. |
| `amf-graph-algorithm` | A network indicator is implemented | Verifies it against its source paper and states complexity. |
| `amf-source-vetting` | An indicator is cited | Requires the originating paper, not a survey. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/research/systemic_indicators.md`
- An indicator input and verdict table
- Implementations of the survivors
- A prominent statement of what is out of reach

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every indicator's inputs come from its originating paper.
- [ ] Every indicator has a verdict of computable, proxy-possible or out of reach.
- [ ] Every implemented proxy carries a statement of what it does not capture.
- [ ] The out-of-reach result is stated prominently, not buried.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Adrian, T., & Brunnermeier, M. K. (2016). "CoVaR." *American Economic Review* 106(7), 1705-1741.
- Acharya, V. V., Pedersen, L. H., Philippon, T., & Richardson, M. (2017). "Measuring Systemic Risk." *Review of Financial Studies* 30(1), 2-47.
- Billio, M., Getmansky, M., Lo, A. W., & Pelizzon, L. (2012). "Econometric measures of connectedness and systemic risk in the finance and insurance sectors." *Journal of Financial Economics* 104(3), 535-559.
- Diebold, F. X., & Yilmaz, K. (2014). "On the network topology of variance decompositions: Measuring the connectedness of financial firms." *Journal of Econometrics* 182(1), 119-134.
- Battiston, S., Puliga, M., Kaushik, R., Tasca, P., & Caldarelli, G. (2012). "DebtRank: Too Central to Fail? Financial Networks, the FED and Systemic Risk." *Scientific Reports* 2, 541.
- Glasserman, P., & Young, H. P. (2016). "Contagion in Financial Networks." *Journal of Economic Literature* 54(3), 779-831.
- Basel Committee on Banking Supervision (2013). *Global systemically important banks: updated assessment methodology and the higher loss absorbency requirement*. Bank for International Settlements.
- Cont, R., Moussa, A., & Santos, E. B. (2013). "Network structure and systemic risk in banking systems." In Fouque, J.-P. & Langsam, J. (eds.), *Handbook on Systemic Risk*. Cambridge University Press.

## 11. Commit protocol

Commits from this project use the scope `p80`:

```text
docs(p80): survey systemic risk indicators against their exact input requirements
docs(p80): rule per indicator on structural computability
feat(p80): implement the indicators that survive the non-trading filter
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
