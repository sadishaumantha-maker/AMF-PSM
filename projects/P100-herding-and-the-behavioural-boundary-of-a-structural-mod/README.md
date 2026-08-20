# P100 - Herding and the behavioural boundary of a structural model

**Track Q - Technology, Fintech and AI Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Complex systems analyst |
| **Upstream** | Discussion 6.3; P96 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Herding is behavioural: participants act alike because they observe each other. The framework models structure, not behaviour, and has repeatedly declined behavioural constructs. But herding produces a structural signature - transient coupling that does not exist in the dependency graph - and the framework has no way to say that its graph is a partial picture of the coupling that actually obtains.

## 2. Purpose

Draw the behavioural boundary once, explicitly, for the whole framework, rather than re-litigating it in every charter that runs into it.

## 3. Scope

**In scope**

- A general statement of the behavioural boundary and why it is where it is.
- A catalogue of the constructs already declined for being behavioural.
- A standing rule for future proposals.

**Out of scope**

- Modelling any behavioural mechanism.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Recognise the pattern: P81 declined uncertainty as behavioural, P96 confronted model-mediated coupling, P87 proved coordination indistinguishable, and this charter faces herding. One boundary is being drawn four times.
2. State it once, generally: the framework represents arrangements that persist independently of what participants believe, and declines mechanisms that operate through belief.
3. Test the statement against the four cases and against the framework's existing content - absorptive capacity, for instance, is arguably partly behavioural, and if so the boundary is already crossed and should be admitted.
4. Catalogue the declined constructs from P91's register and classify which were declined for being behavioural rather than for lacking data.
5. Write the standing rule so a future proposal is evaluated against it rather than argued afresh.
6. State plainly that the graph is a lower bound on coupling, since behavioural coupling exists and is not represented.

## 5. Task board

- [ ] State the behavioural boundary generally.
- [ ] Test it against the four existing cases.
- [ ] Check whether existing content already crosses it.
- [ ] Classify the declined register by reason.
- [ ] Write the standing rule.
- [ ] Publish `docs/methods/behavioural_boundary.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** State the boundary once and test it against the existing cases.
- **Inputs:** P81, P87, P91, P96 and the model.
- **Output artifact:** `docs/methods/behavioural_boundary.md`.
- **Stop condition:** The statement classifies all four cases consistently.

### `red-team-critic`

- **Mandate:** Find existing framework content that already crosses the stated boundary.
- **Inputs:** `src/amf/` and the boundary statement.
- **Output artifact:** A crossing report.
- **Stop condition:** Every crossing is admitted or the boundary is restated.

### `taxonomy-cartographer`

- **Mandate:** Classify the declined register by reason for decline.
- **Inputs:** P91's register.
- **Output artifact:** A classified register.
- **Stop condition:** Every decline is marked behavioural, data-unavailable or out-of-model.

**Hand-off order:** `spec-drafter` -> `red-team-critic` -> `taxonomy-cartographer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-boundary-check` | A construct is evaluated | Applies the naming guard and now the behavioural rule. |
| `amf-red-team` | The boundary is stated | Searches existing content for crossings. |
| `amf-doc-page` | The rule is published | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/behavioural_boundary.md`
- A general boundary statement
- A crossing report
- A classified declined register

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The boundary statement classifies all four existing cases consistently.
- [ ] Any existing crossing is admitted rather than explained away.
- [ ] The declined register is classified by reason.
- [ ] The graph is stated to be a lower bound on coupling.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Bikhchandani, S., & Sharma, S. (2000). "Herd Behavior in Financial Markets." *IMF Staff Papers* 47(3), 279-310.
- Danielsson, J., Shin, H. S., & Zigrand, J.-P. (2012). "Endogenous and Systemic Risk." In Haubrich, J. G. & Lo, A. W. (eds.), *Quantifying Systemic Risk*. University of Chicago Press.
- Calvano, E., Calzolari, G., Denicolo, V., & Pastorello, S. (2020). "Artificial Intelligence, Algorithmic Pricing, and Collusion." *American Economic Review* 110(10), 3267-3297.
- Soros, G. (2013). "Fallibility, reflexivity, and the human uncertainty principle." *Journal of Economic Methodology* 20(4), 309-329.
- Merton, R. K. (1948). "The Self-Fulfilling Prophecy." *The Antioch Review* 8(2), 193-210.
- Arthur, W. B. (2015). *Complexity and the Economy*. Oxford University Press.
- LeBaron, B. (2006). "Agent-based Computational Finance." In Tesfatsion, L. & Judd, K. L. (eds.), *Handbook of Computational Economics, Vol. 2*. North-Holland.
- Weisberg, M. (2013). *Simulation and Similarity: Using Models to Understand the World*. Oxford University Press.

## 11. Commit protocol

Commits from this project use the scope `p100`:

```text
docs(p100): state the behavioural boundary once for the whole framework
docs(p100): report where existing content already crosses it
docs(p100): classify the declined register by reason for decline
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
