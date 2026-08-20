# P91 - Currency mismatch as a structural rather than a market quantity

**Track P - Shadow Finance, Capital Flows and Currency**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Market structure researcher |
| **Upstream** | Discussion 5.3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Currency mismatch is conventionally measured as a balance-sheet quantity - liabilities in one unit, assets in another. The framework holds no balance sheets. Either there is a structural expression of mismatch, or the concept joins the list of things the framework must decline, and the list is getting long enough that its length is itself a finding about the framework's reach.

## 2. Purpose

Attempt the structural expression, rule on it, and then step back and audit how many core financial concepts the framework has now declined - because that count is a fact about the framework's scope.

## 3. Scope

**In scope**

- An attempted structural expression of mismatch as a dependency-kind asymmetry.
- A ruling.
- A running audit of concepts the framework has declined, across all charters.

**Out of scope**

- Balance-sheet, exposure or valuation quantities of any kind.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Attempt the expression honestly: a system whose circulatory dependency runs to an out-of-boundary source under a different regulatory regime has a structural asymmetry, and whether that is 'mismatch' is the question.
2. Test whether the structural version retains what makes mismatch dangerous - that the two sides move differently under stress - and note that movement is precisely what the framework does not represent.
3. Rule. A negative is likely and is acceptable.
4. Then do the wider audit: collect every concept declined across the charter set - liquidity measurement, capital flows, exposures, abuse detection, mismatch - and count them.
5. Present the count as a scope statement rather than as a failure. A framework that declines cleanly is more useful than one that approximates everything.
6. Feed the audit into P128, which owns the scale-and-resolution question.

## 5. Task board

- [ ] Attempt the structural expression.
- [ ] Test whether it retains the dangerous property.
- [ ] Rule.
- [ ] Audit all declined concepts across the charter set.
- [ ] Present the count as a scope statement.
- [ ] Publish `docs/taxonomies/currency_mismatch.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Attempt the structural expression and test whether it retains the mechanism.
- **Inputs:** The AMF model.
- **Output artifact:** A formal attempt with a verdict.
- **Stop condition:** The attempt succeeds or fails for a stated reason.

### `taxonomy-cartographer`

- **Mandate:** Audit every concept declined across the charter set and count them.
- **Inputs:** All charters.
- **Output artifact:** A declined-concept register.
- **Stop condition:** Every decline is recorded with the charter that ruled it.

### `spec-drafter`

- **Mandate:** Present the count as a scope statement.
- **Inputs:** The register.
- **Output artifact:** `docs/taxonomies/currency_mismatch.md` plus a scope section.
- **Stop condition:** The scope statement is neutral in tone and factual in content.

**Hand-off order:** `math-formalizer` -> `taxonomy-cartographer` -> `spec-drafter`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-boundary-check` | A mismatch construct is proposed | Rejects balance-sheet and valuation inputs. |
| `amf-taxonomy-builder` | The declined register is built | Builds it with the ruling charter cited per entry. |
| `amf-doc-page` | The scope statement is published | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/taxonomies/currency_mismatch.md`
- A formal attempt and ruling
- A declined-concept register
- A scope statement

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The structural attempt succeeds or fails for a stated reason.
- [ ] Every declined concept is registered with its ruling charter.
- [ ] The scope statement is factual rather than defensive.
- [ ] No balance-sheet or valuation quantity appears.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Eichengreen, B. (2011). *Exorbitant Privilege: The Rise and Fall of the Dollar and the Future of the International Monetary System*. Oxford University Press.
- Farhi, E., & Maggiori, M. (2018). "A Model of the International Monetary System." *Quarterly Journal of Economics* 133(1), 295-355.
- Obstfeld, M., Shambaugh, J. C., & Taylor, A. M. (2005). "The Trilemma in History: Tradeoffs Among Exchange Rates, Monetary Policies, and Capital Mobility." *Review of Economics and Statistics* 87(3), 423-438.
- Calvo, G. A. (1998). "Capital Flows and Capital-Market Crises: The Simple Economics of Sudden Stops." *Journal of Applied Economics* 1(1), 35-54.
- Rey, H. (2015). "Dilemma not Trilemma: The Global Financial Cycle and Monetary Policy Independence." NBER Working Paper 21162.
- Minsky, H. P. (1986). *Stabilizing an Unstable Economy*. Yale University Press.
- Weisberg, M. (2013). *Simulation and Similarity: Using Models to Understand the World*. Oxford University Press.

## 11. Commit protocol

Commits from this project use the scope `p91`:

```text
docs(p91): attempt a structural expression of currency mismatch and rule
docs(p91): register every concept the framework has declined
docs(p91): present the declined set as a scope statement
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

