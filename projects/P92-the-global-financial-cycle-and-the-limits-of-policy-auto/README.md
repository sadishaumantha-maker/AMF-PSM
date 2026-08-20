# P92 - The global financial cycle and the limits of policy autonomy

**Track P - Shadow Finance, Capital Flows and Currency**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Comparative regulation researcher |
| **Upstream** | Discussion 5.3; Discussion 7.2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework treats each market's policy stack as its own. The global-financial-cycle literature argues that policy autonomy is far more constrained than the classical trilemma implies - that a market's immune system is partly set elsewhere. If so, modelling a market's policy stack as endogenous overstates its independence, and the framework's regime profiles describe less than they appear to.

## 2. Purpose

Establish what portion of a market's policy configuration is genuinely local, and record the constraint where regime profiles are read.

## 3. Scope

**In scope**

- The trilemma and its dilemma revision, stated from primary sources with the disagreement intact.
- A structural expression of externally-constrained policy capacity.
- A recorded constraint attached to the P50 regime profiles.

**Out of scope**

- Any claim about a specific jurisdiction's current autonomy.
- Interest-rate or exchange-rate data.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Present both positions fairly - the classical trilemma and the dilemma revision disagree substantively, and the framework should not adjudicate an open question in international macroeconomics.
2. Express the structural residue: whichever position holds, some configurations of the immune system are jointly unavailable, and joint unavailability is a structural constraint the framework can represent.
3. Attach the constraint to the P50 regime profiles, so a reader of a profile sees which dimensions are not freely set.
4. Do not resolve the underlying economic dispute; record it as contested and represent only what both positions agree on.
5. Note the consequence for comparison: two jurisdictions with the same profile may have very different room to change it.
6. Keep every quantity structural.

## 5. Task board

- [ ] State both positions from primary sources.
- [ ] Express joint unavailability structurally.
- [ ] Attach the constraint to the regime profiles.
- [ ] Record the dispute as contested.
- [ ] State the consequence for cross-jurisdiction comparison.
- [ ] Publish `docs/policy/policy_autonomy.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Present the trilemma and its revision with the disagreement intact.
- **Inputs:** The reading list.
- **Output artifact:** An annotated two-position summary.
- **Stop condition:** Neither position is presented as settled.

### `math-formalizer`

- **Mandate:** Express joint unavailability of policy configurations structurally.
- **Inputs:** The two positions.
- **Output artifact:** A formal constraint statement.
- **Stop condition:** The constraint holds under both positions.

### `regime-comparativist`

- **Mandate:** Attach the constraint to the P50 profiles.
- **Inputs:** The constraint and the profiles.
- **Output artifact:** An amended profile schema.
- **Stop condition:** Every profile shows which dimensions are externally constrained.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `regime-comparativist`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A profile is amended | Records constraints with source and vintage. |
| `amf-source-vetting` | A macroeconomic position is cited | Requires the primary paper and records the state of the dispute. |
| `amf-doc-page` | The constraint is published | Enforces documentation conventions and neutrality. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/policy_autonomy.md`
- A two-position summary
- A formal joint-unavailability constraint
- Amended regime profiles

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Both positions are presented without adjudication.
- [ ] The structural constraint holds under either position.
- [ ] Every regime profile marks its externally constrained dimensions.
- [ ] No interest-rate or exchange-rate quantity appears.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Rey, H. (2015). "Dilemma not Trilemma: The Global Financial Cycle and Monetary Policy Independence." NBER Working Paper 21162.
- Obstfeld, M., Shambaugh, J. C., & Taylor, A. M. (2005). "The Trilemma in History: Tradeoffs Among Exchange Rates, Monetary Policies, and Capital Mobility." *Review of Economics and Statistics* 87(3), 423-438.
- Farhi, E., & Maggiori, M. (2018). "A Model of the International Monetary System." *Quarterly Journal of Economics* 133(1), 295-355.
- Eichengreen, B. (2011). *Exorbitant Privilege: The Rise and Fall of the Dollar and the Future of the International Monetary System*. Oxford University Press.
- Kaufmann, D., Kraay, A., & Mastruzzi, M. (2010). "The Worldwide Governance Indicators: Methodology and Analytical Issues." World Bank Policy Research Working Paper 5430.
- Alesina, A., & Summers, L. H. (1993). "Central Bank Independence and Macroeconomic Performance." *Journal of Money, Credit and Banking* 25(2), 151-162.
- International Monetary Fund (2023). "Geoeconomic Fragmentation and the Future of Multilateralism." IMF Staff Discussion Note SDN/2023/001.

## 11. Commit protocol

Commits from this project use the scope `p92`:

```text
docs(p92): state the trilemma and its dilemma revision without adjudicating
docs(p92): express jointly unavailable policy configurations structurally
docs(p92): mark externally constrained dimensions on the regime profiles
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

