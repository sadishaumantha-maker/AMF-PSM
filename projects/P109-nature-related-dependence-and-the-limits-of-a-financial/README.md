# P109 - Nature-related dependence and the limits of a financial-system boundary

**Track S - Climate, Nature and Long-Horizon Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Research lead |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 8.3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The nature-related risk literature argues that the economy is embedded in the biosphere rather than adjacent to it. The framework's boundary places a market inside an economy and stops there. If the embedding claim is right, the framework's outermost dependency is not the outermost dependency, and the model has no way to represent something the whole market depends on.

## 2. Purpose

Decide whether a dependence shared by every system in the market is representable at all, since a dependency on which everything depends equally is invisible to a relative structural measure.

## 3. Scope

**In scope**

- A statement of the universal-dependence problem in structural terms.
- An assessment of what relative measures do when a dependency is universal.
- A ruling with the consequence stated.

**Out of scope**

- Ecological modelling or valuation of natural capital.
- Any claim about ecosystem state.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the structural problem, which is more interesting than the topic: the framework's measures are relative - concentration is a share, centrality is max-normalised, fragility is comparative. A dependency shared equally by all seven systems contributes nothing to any of them.
2. Demonstrate it: add a universal dependency to a market and show the scores do not move. That is a concrete property of the measurement scheme, not a claim about nature.
3. Draw the general lesson - the framework can only see *differential* dependence, and any risk that is common to everything it models is invisible by construction.
4. Note that this generalises beyond nature to any universal substrate, including the third-party dependence of P99 taken to its limit.
5. Rule on representation, and if the answer is that universal dependence is invisible, record it as a first-class limitation.
6. Keep the treatment structural; the review literature supplies the framing without needing ecological modelling.

## 5. Task board

- [ ] State the universal-dependence problem structurally.
- [ ] Demonstrate score invariance under a universal dependency.
- [ ] Generalise the lesson beyond nature.
- [ ] Connect to P99's limiting case.
- [ ] Rule and record the limitation.
- [ ] Publish `docs/research/universal_dependence.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State why relative measures are blind to universal dependence.
- **Inputs:** `diagnostics.py`, `graph.py`.
- **Output artifact:** A formal statement.
- **Stop condition:** The blindness is derived from the measures' definitions.

### `benchmark-runner`

- **Mandate:** Demonstrate score invariance when a universal dependency is added.
- **Inputs:** The engines and a constructed market.
- **Output artifact:** A demonstration table.
- **Stop condition:** Score invariance is shown numerically across the diagnostic and resilience outputs.

### `spec-drafter`

- **Mandate:** Generalise the lesson and record the limitation.
- **Inputs:** The demonstration.
- **Output artifact:** `docs/research/universal_dependence.md`.
- **Stop condition:** The limitation is recorded as first-class, not as a caveat.

### `boundary-sentinel`

- **Mandate:** Reject ecological and valuation constructs.
- **Inputs:** The proposals.
- **Output artifact:** A boundary report.
- **Stop condition:** The treatment remains structural.

**Hand-off order:** `math-formalizer` -> `benchmark-runner` -> `spec-drafter` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | The blindness is stated | Writes it into the docstring and mirrors it as a test. |
| `amf-sensitivity-design` | Invariance is demonstrated | Designs the perturbation and reports the null effect. |
| `amf-doc-page` | The limitation is recorded | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/research/universal_dependence.md`
- A formal blindness statement
- A numeric invariance demonstration
- A first-class recorded limitation

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The blindness is derived from the measures' definitions, not asserted.
- [ ] Score invariance under universal dependence is demonstrated numerically.
- [ ] The lesson is generalised beyond the nature case.
- [ ] No ecological or valuation construct appears.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Dasgupta, P. (2021). *The Economics of Biodiversity: The Dasgupta Review*. HM Treasury.
- IPBES (2019). *Global Assessment Report on Biodiversity and Ecosystem Services*. Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services.
- Rockstrom, J., et al. (2009). "A safe operating space for humanity." *Nature* 461, 472-475.
- Steffen, W., et al. (2015). "Planetary boundaries: Guiding human development on a changing planet." *Science* 347(6223), 1259855.
- Levin, S. A. (1998). "Ecosystems and the Biosphere as Complex Adaptive Systems." *Ecosystems* 1, 431-436.
- May, R. M., Levin, S. A., & Sugihara, G. (2008). "Ecology for bankers." *Nature* 451, 893-895.
- Holling, C. S. (1973). "Resilience and Stability of Ecological Systems." *Annual Review of Ecology and Systematics* 4, 1-23.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.

## 11. Commit protocol

Commits from this project use the scope `p109`:

```text
docs(p109): derive why relative measures are blind to universal dependence
test(p109): demonstrate score invariance under a universal dependency
docs(p109): record universal-dependence blindness as a first-class limitation
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

