# P83 - Backstops and the lender of last resort as immune structure

**Track N - Policy-Market Contagion and Systemic Indicators**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Policy researcher |
| **Upstream** | PR #42 (immune system as a layered policy stack); Discussion 3.1 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The immune system is modelled as a layered policy stack - rules that constrain. A backstop is a different kind of object: it does not constrain, it absorbs, and it is deliberately ambiguous about when it will act. Modelling it as another rule layer misses what makes it work, and modelling it as guaranteed capacity misses that its deterrent value depends on not being guaranteed.

## 2. Purpose

Establish how a backstop is represented in the seven-system model, and confront the fact that constructive ambiguity is a designed feature that a deterministic model cannot express.

## 3. Scope

**In scope**

- A structural characterisation of a backstop and how it differs from a constraint.
- A treatment of constructive ambiguity within a deterministic framework.
- A ruling on representation, with the moral-hazard consequence noted.

**Out of scope**

- Modelling any specific central bank's reaction function.
- Any claim about whether a backstop would be deployed.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Characterise the backstop as absorptive capacity that is conditional rather than standing, and note that the framework's `absorptive_capacity` is unconditional by construction.
2. Read the classical lender-of-last-resort statement and the modern treatment together; the doctrine is old, precise, and states conditions that are structural rather than discretionary.
3. Confront constructive ambiguity directly: a deterministic model must either assume the backstop acts or assume it does not, and both are wrong. State which the framework assumes and what that costs.
4. Note the moral-hazard consequence: representing a backstop as standing capacity makes every system it covers look more resilient, which is precisely the distortion the doctrine warns about.
5. Rule on representation, and if the ruling is that a backstop is modelled as an `Intervention` rather than as capacity, state why that is the more honest placement.
6. Coordinate with P38, which owns intervention semantics.

## 5. Task board

- [ ] Characterise a backstop against the constraint model.
- [ ] Review the lender-of-last-resort doctrine from its primary statement.
- [ ] Treat constructive ambiguity explicitly.
- [ ] State the moral-hazard consequence of each representation.
- [ ] Rule and coordinate with P38.
- [ ] Publish `docs/policy/backstops.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect the lender-of-last-resort doctrine and its modern treatment from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** The classical conditions are quoted, not paraphrased.

### `spec-drafter`

- **Mandate:** Rule on representation and state the moral-hazard consequence of each option.
- **Inputs:** The summary and the AMF model.
- **Output artifact:** `docs/policy/backstops.md`.
- **Stop condition:** Each candidate representation has its distortion named.

### `red-team-critic`

- **Mandate:** Show what a resilience score does when a backstop is modelled as standing capacity.
- **Inputs:** The simulator and a constructed market.
- **Output artifact:** A demonstration.
- **Stop condition:** The distortion is demonstrated numerically, not only argued.

**Hand-off order:** `literature-scout` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A backstop's statutory basis is cited | Records the instrument and its conditions. |
| `amf-cascade-calibration` | The distortion is demonstrated | Sweeps the parameter space and reports the affected region. |
| `amf-red-team` | A representation is proposed | Demonstrates its distortion on a constructed market. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/backstops.md`
- A structural characterisation
- A constructive-ambiguity treatment
- A numeric demonstration of the distortion

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The backstop is distinguished from a constraint structurally.
- [ ] The framework's assumption about backstop deployment is stated explicitly.
- [ ] The moral-hazard distortion is demonstrated numerically.
- [ ] The ruling is consistent with P38's intervention semantics.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Bagehot, W. (1873). *Lombard Street: A Description of the Money Market*. Henry S. King. (lender of last resort)
- Goodhart, C. A. E. (1988). *The Evolution of Central Banks*. MIT Press.
- Financial Stability Board (2010). *Reducing the moral hazard posed by systemically important financial institutions: FSB Recommendations and Time Lines*.
- Diamond, D. W., & Dybvig, P. H. (1983). "Bank Runs, Deposit Insurance, and Liquidity." *Journal of Political Economy* 91(3), 401-419.
- Acharya, V., Drechsler, I., & Schnabl, P. (2014). "A Pyrrhic Victory? Bank Bailouts and Sovereign Credit Risk." *Journal of Finance* 69(6), 2689-2739.
- Brunnermeier, M. K. (2009). "Deciphering the Liquidity and Credit Crunch 2007-2008." *Journal of Economic Perspectives* 23(1), 77-100.
- Minsky, H. P. (1986). *Stabilizing an Unstable Economy*. Yale University Press.
- Blinder, A. S. (1998). *Central Banking in Theory and Practice*. MIT Press.

## 11. Commit protocol

Commits from this project use the scope `p83`:

```text
docs(p83): characterise backstops as conditional rather than standing capacity
test(p83): demonstrate the resilience distortion from standing-capacity modelling
docs(p83): rule on backstop representation and its moral-hazard consequence
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
