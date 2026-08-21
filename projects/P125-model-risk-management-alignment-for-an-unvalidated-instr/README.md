# P125 - Model risk management alignment for an unvalidated instrument

**Track U - Method, Epistemics and External Validation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Research lead |
| **Upstream** | SR 11-7 / OCC 2011-12; `CLAUDE.md` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Supervisory model-risk guidance sets expectations for any model used in decision-making: development evidence, independent validation, outcomes analysis and governance. The framework meets almost none of them and says so. The dispute is whether the guidance is therefore irrelevant, or whether it is the standard the framework should be measured against and is currently failing.

## 2. Purpose

Assess the framework against the published expectations honestly, and record the gap as a roadmap rather than as a disqualification.

## 3. Scope

**In scope**

- An assessment against each element of the published guidance.
- A gap register with a route to closure per gap.
- A statement of what the framework may and may not be used for given the gaps.

**Out of scope**

- Claiming compliance.
- Using the guidance to justify current practice.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Take the guidance's elements directly: conceptual soundness, ongoing monitoring, outcomes analysis, independent validation and governance.
2. Assess each with repository evidence. Conceptual soundness is arguably the strongest, since the charter set exists to document reasoning; outcomes analysis is absent because there are no outcomes.
3. Be precise about independent validation: everything in this repository has been produced by the same process, and independence means a party with no stake in the conclusion.
4. Write the use statement, which is the practical deliverable: given the gaps, the framework is suitable for structured reasoning and unsuitable for any decision with a consequence.
5. Record a route to closure per gap so the assessment is a roadmap rather than a verdict.
6. Connect to P126, which owns external review, as the route for the validation gap.

## 5. Task board

- [ ] Assess against each guidance element with evidence.
- [ ] Distinguish conceptual soundness from validation carefully.
- [ ] Write the permitted-use statement.
- [ ] Record a closure route per gap.
- [ ] Link the validation gap to P126.
- [ ] Publish `docs/methods/model_risk_assessment.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Take the guidance elements from the official publication.
- **Inputs:** The guidance text.
- **Output artifact:** An element inventory.
- **Stop condition:** Elements are quoted from the official source.

### `spec-drafter`

- **Mandate:** Assess each element with repository evidence and write the use statement.
- **Inputs:** The inventory and the repository.
- **Output artifact:** `docs/methods/model_risk_assessment.md`.
- **Stop condition:** Every assessment cites repository evidence, not intent.

### `red-team-critic`

- **Mandate:** Attack any assessment that credits the framework beyond its evidence.
- **Inputs:** The draft.
- **Output artifact:** An over-crediting report.
- **Stop condition:** No element is rated above what the evidence supports.

**Hand-off order:** `literature-scout` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-source-vetting` | The guidance is cited | Requires the official publication. |
| `amf-doc-page` | The use statement is published | Enforces the illustrative-not-validated rule. |
| `amf-red-team` | An element is assessed | Checks the rating against the cited evidence. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/model_risk_assessment.md`
- A per-element assessment
- A gap register with closure routes
- A permitted-use statement

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every element is assessed against repository evidence.
- [ ] No element is rated above what the evidence supports.
- [ ] The permitted-use statement is specific about what is excluded.
- [ ] Every gap has a route to closure.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Board of Governors of the Federal Reserve System & OCC (2011). *Supervisory Guidance on Model Risk Management* (SR 11-7 / OCC Bulletin 2011-12).
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- Box, G. E. P. (1976). "Science and Statistics." *Journal of the American Statistical Association* 71(356), 791-799.
- Derman, E. (1996). "Model Risk." Goldman Sachs Quantitative Strategies Research Notes.
- Manski, C. F. (2013). *Public Policy in an Uncertain World: Analysis and Decisions*. Harvard University Press.
- Saltelli, A., et al. (2020). "Five ways to ensure that models serve society: a manifesto." *Nature* 582, 482-484.
- Grimm, V., et al. (2020). "The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update." *Journal of Artificial Societies and Social Simulation* 23(2), 7.

## 11. Commit protocol

Commits from this project use the scope `p125`:

```text
docs(p125): assess the framework against published model risk expectations
docs(p125): record a gap register with a closure route per element
docs(p125): state what the framework may and may not be used for
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
