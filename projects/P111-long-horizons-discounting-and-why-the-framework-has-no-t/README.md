# P111 - Long horizons, discounting and why the framework has no time preference

**Track S - Climate, Nature and Long-Horizon Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Quantitative methodologist |
| **Upstream** | Discussion 8.1; P107 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Long-horizon risk analysis turns on discounting, and the choice of discount rate dominates the conclusion - a fact that produced one of the sharpest disagreements in modern economics. The framework has no discount rate, no time preference and no way to weigh a distant structural failure against a near one. Whether that is a limitation or a feature has never been stated.

## 2. Purpose

State the framework's temporal-weighting position explicitly: it treats a failure at step fifty as equivalent to one at step one, and that is a choice with consequences.

## 3. Scope

**In scope**

- An explicit statement of the framework's implicit temporal weighting.
- The consequence for settling time and the resilience composite.
- A decision on whether to keep the flat weighting.

**Out of scope**

- Adopting a discount rate or any monetary valuation.
- Adjudicating the economic dispute over social discounting.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State what the framework currently does: the resilience composite penalises slow settling, which is a temporal preference, but an implicit and unexamined one.
2. Make it explicit. A settling-time penalty says a slow recovery is worse than a fast one, which is a value judgement embedded in a weight, and P39 owns the weight but not the judgement.
3. Present the discounting dispute fairly without adjudicating it; the disagreement is about ethics as much as economics and the framework has no standing in it.
4. Note the framework's advantage here: because its quantities are dimensionless and structural, it can decline discounting entirely - which is a legitimate position, unlike declining it in a monetary model.
5. Decide whether the flat weighting stays, and if so document it as a stated choice rather than an absence.
6. Feed the result into P39, which owns the composite.

## 5. Task board

- [ ] State the implicit temporal weighting.
- [ ] Make the settling-time value judgement explicit.
- [ ] Present the discounting dispute without adjudicating.
- [ ] Decide on the flat weighting.
- [ ] Document it as a choice.
- [ ] Publish `docs/simulation/temporal_weighting.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Present the discounting disagreement fairly from both principal positions.
- **Inputs:** The reading list.
- **Output artifact:** An annotated two-position summary.
- **Stop condition:** Neither position is presented as settled.

### `math-formalizer`

- **Mandate:** Express the framework's implicit temporal weighting formally.
- **Inputs:** `simulation.py` and the resilience composite.
- **Output artifact:** A formal statement.
- **Stop condition:** The settling-time penalty is expressed as a temporal preference.

### `spec-drafter`

- **Mandate:** Decide and document the weighting as a stated choice.
- **Inputs:** The formal statement.
- **Output artifact:** `docs/simulation/temporal_weighting.md`.
- **Stop condition:** The choice is documented where the composite is defined.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `spec-drafter`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-sensitivity-design` | The settling penalty is examined | Measures how much the composite depends on it. |
| `amf-invariant-spec` | The weighting choice is stated | Writes it into the docstring at the composite's definition. |
| `amf-doc-page` | The position is published | Enforces documentation conventions and neutrality. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/simulation/temporal_weighting.md`
- A formal statement of the implicit weighting
- A fair two-position summary
- A documented weighting choice

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The settling-time penalty is expressed as a temporal preference.
- [ ] The discounting dispute is presented without adjudication.
- [ ] The flat weighting is documented as a choice, not an absence.
- [ ] No discount rate or monetary quantity is introduced.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Stern, N. (2007). *The Economics of Climate Change: The Stern Review*. Cambridge University Press.
- Nordhaus, W. D. (2013). *The Climate Casino: Risk, Uncertainty, and Economics for a Warming World*. Yale University Press.
- Weitzman, M. L. (2009). "On Modeling and Interpreting the Economics of Catastrophic Climate Change." *Review of Economics and Statistics* 91(1), 1-19.
- Dasgupta, P. (2021). *The Economics of Biodiversity: The Dasgupta Review*. HM Treasury.
- Manski, C. F. (2013). *Public Policy in an Uncertain World: Analysis and Decisions*. Harvard University Press.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- OECD & European Commission JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.

## 11. Commit protocol

Commits from this project use the scope `p111`:

```text
docs(p111): express the framework's implicit temporal weighting formally
docs(p111): present the discounting dispute without adjudicating it
docs(p111): document the flat weighting as a stated choice
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

