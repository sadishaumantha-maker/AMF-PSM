# P96 - Machine learning in finance as a systemic risk channel

**Track Q - Technology, Fintech and AI Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Research lead |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 6.3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Discussion 6.3 treats machine learning in finance as an opportunity with attendant risks. The systemic-risk literature identifies a specific structural channel that the opportunity framing misses: widely shared models produce correlated behaviour, which converts idiosyncratic events into common ones. That is a structural claim about coupling, which is exactly the kind of thing this framework exists to represent.

## 2. Purpose

Isolate the structural channel - shared models as an invisible coupling - and determine whether the framework can represent a dependency that exists through common tooling rather than through a contract.

## 3. Scope

**In scope**

- A structural characterisation of model-mediated coupling.
- An assessment against the `DependencyKind` vocabulary.
- A ruling with the consequence for coupling measurement stated.

**Out of scope**

- Evaluating any model's predictive performance.
- Any return or price series.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Characterise the channel: two participants using the same model respond identically to the same input, which is a dependency with no edge - neither relies on the other, yet they move together.
2. Recognise this is the same structure P87 proves indistinguishable from coordination, and make the two treatments consistent.
3. Test the vocabulary: `informational` is the closest existing kind, and whether it fits is the question rather than the assumption.
4. State the consequence for measurement: if coupling can exist without an edge, then every concentration and feedback score computed from edges alone understates coupling by an unknown amount.
5. Draw on the endogenous-risk and diversity-diversification work, which establishes that homogeneity of method is itself a systemic exposure.
6. Rule, and if the channel is unrepresentable, record it in P91's declined register with its consequence.

## 5. Task board

- [ ] Characterise model-mediated coupling.
- [ ] Reconcile with P87's indistinguishability result.
- [ ] Test the `informational` dependency kind.
- [ ] State the consequence for edge-based measurement.
- [ ] Rule and register any decline.
- [ ] Publish `docs/research/model_coupling.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the homogeneity and endogenous-risk channel from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated evidence table.
- **Stop condition:** The channel is evidenced from peer-reviewed and official-sector work.

### `math-formalizer`

- **Mandate:** Express coupling-without-an-edge formally and state what it does to edge-based scores.
- **Inputs:** The graph model.
- **Output artifact:** A formal treatment.
- **Stop condition:** The understatement of coupling is expressed, not merely noted.

### `spec-drafter`

- **Mandate:** Rule on representability and register any decline.
- **Inputs:** The formal treatment.
- **Output artifact:** `docs/research/model_coupling.md`.
- **Stop condition:** The ruling is consistent with P87.

### `boundary-sentinel`

- **Mandate:** Reject any construct requiring model outputs or return series.
- **Inputs:** The proposals.
- **Output artifact:** A boundary report.
- **Stop condition:** Only structural constructs survive.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `spec-drafter` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-boundary-check` | A coupling construct is proposed | Rejects return, price and model-output inputs. |
| `amf-graph-algorithm` | Edge-based measurement is assessed | Verifies which queries would understate coupling. |
| `amf-red-team` | A ruling is drafted | Argues the channel is representable and forces an answer. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/research/model_coupling.md`
- An evidence table
- A formal treatment of coupling without an edge
- A ruling consistent with P87

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The channel is characterised structurally and evidenced.
- [ ] The understatement of edge-based coupling is expressed formally.
- [ ] The ruling is consistent with P87's indistinguishability result.
- [ ] Any decline is registered with its consequence.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Danielsson, J., Macrae, R., & Uthemann, A. (2022). "Artificial intelligence and systemic risk." *Journal of Banking & Finance* 140, 106290.
- Danielsson, J., Shin, H. S., & Zigrand, J.-P. (2012). "Endogenous and Systemic Risk." In Haubrich, J. G. & Lo, A. W. (eds.), *Quantifying Systemic Risk*. University of Chicago Press.
- Wagner, W. (2011). "Systemic Liquidation Risk and the Diversity-Diversification Trade-Off." *Journal of Finance* 66(4), 1141-1175.
- Financial Stability Board (2017). *Artificial intelligence and machine learning in financial services: Market developments and financial stability implications*.
- Bikhchandani, S., & Sharma, S. (2000). "Herd Behavior in Financial Markets." *IMF Staff Papers* 47(3), 279-310.
- Calvano, E., Calzolari, G., Denicolo, V., & Pastorello, S. (2020). "Artificial Intelligence, Algorithmic Pricing, and Collusion." *American Economic Review* 110(10), 3267-3297.
- Acemoglu, D., Ozdaglar, A., & Tahbaz-Salehi, A. (2015). "Systemic Risk and Stability in Financial Networks." *American Economic Review* 105(2), 564-608.
- Rudin, C. (2019). "Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead." *Nature Machine Intelligence* 1, 206-215.

## 11. Commit protocol

Commits from this project use the scope `p96`:

```text
docs(p96): characterise shared models as coupling without a dependency edge
docs(p96): express how edge-based scores understate model-mediated coupling
docs(p96): rule on representability consistently with the coordination limit
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
