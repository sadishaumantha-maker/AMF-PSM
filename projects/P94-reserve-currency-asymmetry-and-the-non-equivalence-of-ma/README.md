# P94 - Reserve currency asymmetry and the non-equivalence of markets

**Track P - Shadow Finance, Capital Flows and Currency**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Comparative regulation researcher |
| **Upstream** | Discussion 5.3; Discussion 7.1 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework treats markets as instances of one model differing only in their metric values. The international monetary literature describes a structural asymmetry that is not a difference of degree: some markets issue the asset others hold as a reserve. If that asymmetry is real, then two markets with identical AMF representations can occupy entirely different positions in the wider system, and the model cannot see it.

## 2. Purpose

Determine whether reserve-issuer asymmetry is representable, and if not, state clearly that AMF scores are not comparable across markets occupying different positions.

## 3. Scope

**In scope**

- A structural characterisation of the asymmetry.
- A test of whether the model can express it.
- A comparability rule for scores across markets.

**Out of scope**

- Ranking currencies or predicting reserve status change.
- Reserve holdings or exchange-rate data.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Characterise the asymmetry structurally: it is a dependency that runs one way across many markets at once, which is a property of the wider system rather than of any single modelled market.
2. Test expressibility. The framework models one market at a time with a fixed boundary, so a property defined across markets is, on its face, outside it.
3. Draw the comparability conclusion carefully. If the model cannot see position, then equal scores do not mean equal resilience, and that is a limitation on *comparison*, not on the score itself.
4. Write the comparability rule so it appears wherever two markets' scores could be placed side by side.
5. Note the connection to sanctions and chokepoints in Track R - the same asymmetry is what makes financial coercion possible, so the two charters share a mechanism.
6. Keep the treatment neutral; this is a structural observation, not a political one.

## 5. Task board

- [ ] Characterise the asymmetry structurally.
- [ ] Test expressibility within a single-market model.
- [ ] Derive the comparability rule.
- [ ] Place the rule where scores are compared.
- [ ] Link the mechanism to Track R.
- [ ] Publish `docs/policy/reserve_asymmetry.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the asymmetry from primary international-monetary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** The mechanism is sourced, not asserted.

### `math-formalizer`

- **Mandate:** Test whether a cross-market property is expressible in a single-market model.
- **Inputs:** The AMF model and `MarketBoundary` semantics from P82.
- **Output artifact:** An expressibility verdict.
- **Stop condition:** The verdict follows from the model's stated semantics.

### `spec-drafter`

- **Mandate:** Write the comparability rule and place it where scores meet.
- **Inputs:** The verdict.
- **Output artifact:** `docs/policy/reserve_asymmetry.md` plus a renderer note.
- **Stop condition:** The rule appears wherever two markets' scores can be compared.

### `red-team-critic`

- **Mandate:** Check the treatment reads as structural rather than political.
- **Inputs:** The draft.
- **Output artifact:** A neutrality critique.
- **Stop condition:** No sentence takes a political position.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A jurisdiction's monetary position is described | Records it with source and vintage, neutrally. |
| `amf-doc-page` | The comparability rule is published | Enforces documentation conventions and neutrality. |
| `amf-red-team` | Scores are compared across markets | Tests whether the comparison implies equivalence the model cannot support. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/reserve_asymmetry.md`
- A structural characterisation
- An expressibility verdict
- A cross-market comparability rule

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The asymmetry is characterised structurally and neutrally.
- [ ] The expressibility verdict follows from the model's stated semantics.
- [ ] The comparability rule appears wherever scores can be compared.
- [ ] No reserve-holding or exchange-rate quantity appears.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Eichengreen, B. (2011). *Exorbitant Privilege: The Rise and Fall of the Dollar and the Future of the International Monetary System*. Oxford University Press.
- Farhi, E., & Maggiori, M. (2018). "A Model of the International Monetary System." *Quarterly Journal of Economics* 133(1), 295-355.
- Rey, H. (2015). "Dilemma not Trilemma: The Global Financial Cycle and Monetary Policy Independence." NBER Working Paper 21162.
- Farrell, H., & Newman, A. L. (2019). "Weaponized Interdependence: How Global Economic Networks Shape State Coercion." *International Security* 44(1), 42-79.
- McDowell, D. (2023). *Bucking the Buck: US Financial Sanctions and the International Backlash against the Dollar*. Oxford University Press.
- Obstfeld, M., Shambaugh, J. C., & Taylor, A. M. (2005). "The Trilemma in History: Tradeoffs Among Exchange Rates, Monetary Policies, and Capital Mobility." *Review of Economics and Statistics* 87(3), 423-438.
- Hirschman, A. O. (1945). *National Power and the Structure of Foreign Trade*. University of California Press.

## 11. Commit protocol

Commits from this project use the scope `p94`:

```text
docs(p94): characterise reserve-issuer asymmetry structurally
docs(p94): rule on expressibility within a single-market model
docs(p94): restrict cross-market score comparison where position differs
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

