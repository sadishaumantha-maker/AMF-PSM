# P128 - Scale and resolution limits of the seven-system model

**Track U - Method, Epistemics and External Validation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Research lead |
| **Upstream** | P56; P91; P104; P106; P107; P109 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Six separate charters have run into the same wall from different directions: seven nodes is too few for betweenness to discriminate, a step has no duration, universal dependence is invisible, boundary-crossing loops are unenumerable, and sub-minute episodes have no representation. These are not six problems. They are one property of the model appearing six times, and it has never been stated as a property.

## 2. Purpose

State the model's resolution envelope once - in nodes, in time, in scope - so that a future proposal is checked against it before work starts rather than after.

## 3. Scope

**In scope**

- A single statement of the model's resolution in each dimension.
- A consolidation of the findings from the charters that hit the wall.
- A pre-flight check for future proposals.

**Out of scope**

- Changing the model's resolution; this charter states it, others may propose changing it.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Collect the findings rather than re-deriving them: each contributing charter has already established its limit, and this charter's value is in seeing them as one.
2. State the envelope in each dimension: structural resolution is seven fixed systems; temporal resolution is an undefined step with no calibration; scope resolution is one market with a fixed boundary; and measurement is relative, so anything universal is invisible.
3. Derive the general rule from the four: the model resolves *differential structure within one market at one time*, and nothing else.
4. Test the rule against the six contributing charters and confirm it predicts each of their findings; if it does not predict one, the rule is wrong.
5. Write the pre-flight check as a short list a proposer answers before starting, so the seventh charter does not rediscover the wall.
6. Place the envelope where a reader of any score will encounter it.

## 5. Task board

- [ ] Collect the limit findings from the contributing charters.
- [ ] State the envelope in each dimension.
- [ ] Derive the general rule.
- [ ] Test the rule against all six findings.
- [ ] Write the pre-flight check.
- [ ] Publish `docs/methods/resolution_envelope.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `taxonomy-cartographer`

- **Mandate:** Collect and tabulate the limit findings from the contributing charters.
- **Inputs:** P56, P91, P104, P106, P107, P109.
- **Output artifact:** A consolidated findings table.
- **Stop condition:** Every contributing finding is recorded with its source charter.

### `math-formalizer`

- **Mandate:** State the envelope formally and derive the general rule.
- **Inputs:** The findings table.
- **Output artifact:** A formal envelope statement.
- **Stop condition:** The rule predicts all six findings, or is revised until it does.

### `spec-drafter`

- **Mandate:** Write the pre-flight check and place the envelope where scores are read.
- **Inputs:** The envelope.
- **Output artifact:** `docs/methods/resolution_envelope.md`.
- **Stop condition:** The check is short enough to actually be used.

### `red-team-critic`

- **Mandate:** Find a seventh limitation the rule does not predict.
- **Inputs:** The rule and the framework.
- **Output artifact:** A prediction-failure report.
- **Stop condition:** No unpredicted limitation is found, or the rule is revised.

**Hand-off order:** `taxonomy-cartographer` -> `math-formalizer` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-doc-page` | The envelope is published | Enforces documentation conventions and placement rules. |
| `amf-invariant-spec` | A resolution limit is stated | Writes it into the docstring where the relevant capability lives. |
| `amf-red-team` | The general rule is proposed | Searches for a limitation the rule fails to predict. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/resolution_envelope.md`
- A consolidated findings table
- A formal envelope statement
- A pre-flight check for new proposals

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every contributing finding is recorded with its source charter.
- [ ] The general rule predicts all six findings.
- [ ] The pre-flight check is short enough to be used.
- [ ] The envelope is placed where a score reader will encounter it.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Simon, H. A. (1962). "The Architecture of Complexity." *Proceedings of the American Philosophical Society* 106(6), 467-482.
- Weisberg, M. (2013). *Simulation and Similarity: Using Models to Understand the World*. Oxford University Press.
- Bailer-Jones, D. M. (2009). *Scientific Models in Philosophy of Science*. University of Pittsburgh Press.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.
- Grimm, V., et al. (2020). "The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update." *Journal of Artificial Societies and Social Simulation* 23(2), 7.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- Levin, S. A. (1998). "Ecosystems and the Biosphere as Complex Adaptive Systems." *Ecosystems* 1, 431-436.
- Box, G. E. P. (1976). "Science and Statistics." *Journal of the American Statistical Association* 71(356), 791-799.

## 11. Commit protocol

Commits from this project use the scope `p128`:

```text
docs(p128): consolidate six independently discovered resolution limits
docs(p128): state the model's resolution envelope and derive the general rule
docs(p128): add a pre-flight resolution check for new proposals
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
