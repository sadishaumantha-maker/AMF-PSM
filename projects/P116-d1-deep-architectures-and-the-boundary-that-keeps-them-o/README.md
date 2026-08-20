# P116 - D1 - deep architectures, and the boundary that keeps them out of the package

**Track T - The Promised Research Modules**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Machine-learning researcher |
| **Upstream** | `docs/discussions/README.md` module D1 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

D1 promises deep architectures for multi-asset forecasting. Two of the repository's hard rules land on that sentence at once: the package takes no runtime dependencies, so no tensor library may enter it, and the package makes no forecasts, so the stated objective is outside its remit whatever the architecture. The dispute is whether the module can say anything useful once both rules are honoured, or whether it exists only to explain why the answer is no.

## 2. Purpose

Write the architectures module as a boundary analysis with real technical content: what each architecture family assumes about its data, which of those assumptions a structural snapshot violates, and what a sidecar - not the package - could legitimately do.

## 3. Scope

**In scope**

- Recurrent gating, self-attention and message passing stated exactly, with their inductive biases named.
- An assumption-by-assumption check against what the framework actually holds.
- A sidecar boundary: what may live outside the package and how it stays outside.
- A statement of the sample-size problem at seven systems.

**Out of scope**

- Any import of a tensor library anywhere under `src/`.
- Forecasting anything, for any asset, over any horizon.
- Training on market data of any kind.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Name the inductive bias of each family before discussing fit: recurrence assumes sequential dependence with shared parameters across time, attention assumes relevance is content-addressable and permutation structure must be supplied, message passing assumes the graph is the right relational prior. These are the load-bearing statements.
2. Check each against the framework's data. A market here is seven systems with four metrics each and a sparse edge set - twenty-eight numbers and a handful of weights. Every architecture in the list is over-parameterised by orders of magnitude for that, and the module must say so with the arithmetic shown.
3. Give message passing its due, because it is the one family whose prior matches: the framework's object is a graph, and graph networks were built for graphs. Then state the sample-size objection anyway - one graph is not a training set.
4. Define the sidecar boundary concretely: a separate repository, never imported by `amf`, with its own dependencies and its own disclaimers, and state exactly what test would catch a violation if someone tried to import it.
5. Do not use forecasting vocabulary anywhere in the module. Structural retrodiction - replaying recorded structural configurations and scoring the resilience index - is the only framing the boundary permits, and even that belongs to I2.
6. Write section 7's propositions about representational adequacy, which is testable, rather than about accuracy, which is not available here.

## 5. Task board

- [ ] State each architecture family's inductive bias precisely.
- [ ] Check each against the framework's twenty-eight numbers and sparse edges.
- [ ] Show the over-parameterisation arithmetic.
- [ ] Define the sidecar boundary and the test that enforces it.
- [ ] Write propositions about representational adequacy.
- [ ] Publish `docs/discussions/D1-deep-learning-architectures.md` and relink it.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Assemble the primary architecture papers and the geometric-deep-learning framing.
- **Inputs:** The reading list.
- **Output artifact:** An annotated bibliography.
- **Stop condition:** Each architecture is cited to the paper that introduced it.

### `math-formalizer`

- **Mandate:** State each inductive bias formally and do the parameter-count arithmetic.
- **Inputs:** The sources, `market.py`, `graph.py`.
- **Output artifact:** A bias-and-capacity note.
- **Stop condition:** The over-parameterisation is shown numerically, not asserted.

### `boundary-sentinel`

- **Mandate:** Define the sidecar boundary and specify the test that catches an import violation.
- **Inputs:** `pyproject.toml`, the dependency rules.
- **Output artifact:** A boundary specification.
- **Stop condition:** A concrete failing condition is named, not a policy sentence.

### `spec-drafter`

- **Mandate:** Write the module as a boundary analysis with technical content.
- **Inputs:** All of the above.
- **Output artifact:** `docs/discussions/D1-deep-learning-architectures.md`.
- **Stop condition:** No forecasting vocabulary appears anywhere in the file.

### `red-team-critic`

- **Mandate:** Attack the module for smuggling a forecasting objective back in.
- **Inputs:** The draft.
- **Output artifact:** An adversarial report.
- **Stop condition:** No sentence describes predicting a future market state.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `boundary-sentinel` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-boundary-check` | The sidecar boundary is defined | Checks names and framing against the non-trading list and the dependency rule. |
| `amf-literature-brief` | The sources are assembled | Produces the annotated brief. |
| `amf-layering-check` | The import rule is specified | Verifies the dependency direction the specification claims. |
| `amf-doc-page` | The module is published | Enforces conventions and disclaimers. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/discussions/D1-deep-learning-architectures.md`
- A bias-and-capacity note with arithmetic
- A sidecar boundary specification
- An enforcement test description

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Each family's inductive bias is stated before its fit is discussed.
- [ ] The over-parameterisation argument shows its arithmetic.
- [ ] The sidecar boundary names a concrete failing condition.
- [ ] No forecasting vocabulary appears in the module.
- [ ] No tensor library is added under `src/`.
- [ ] The index link resolves.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
- LeCun, Y., Bengio, Y., & Hinton, G. (2015). "Deep learning." *Nature* 521, 436-444.
- Vaswani, A., et al. (2017). "Attention Is All You Need." *Advances in Neural Information Processing Systems 30*.
- Scarselli, F., Gori, M., Tsoi, A. C., Hagenbuchner, M., & Monfardini, G. (2009). "The Graph Neural Network Model." *IEEE Transactions on Neural Networks* 20(1), 61-80.
- Kipf, T. N., & Welling, M. (2017). "Semi-Supervised Classification with Graph Convolutional Networks." *ICLR 2017*.
- Velickovic, P., Cucurull, G., Casanova, A., Romero, A., Lio, P., & Bengio, Y. (2018). "Graph Attention Networks." *ICLR 2018*.
- Battaglia, P. W., et al. (2018). "Relational inductive biases, deep learning, and graph networks." arXiv:1806.01261.
- Bronstein, M. M., Bruna, J., Cohen, T., & Velickovic, P. (2021). "Geometric Deep Learning: Grids, Groups, Graphs, Geodesics, and Gauges." arXiv:2104.13478.
- Vapnik, V. N. (1998). *Statistical Learning Theory*. Wiley.
- Sculley, D., et al. (2015). "Hidden Technical Debt in Machine Learning Systems." *Advances in Neural Information Processing Systems 28*.

## 11. Commit protocol

Commits from this project use the scope `p116`:

```text
docs(p116): state the inductive bias of each architecture family
docs(p116): specify the sidecar boundary and its enforcement condition
docs(p116): publish the D1 module and relink it from the index
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

