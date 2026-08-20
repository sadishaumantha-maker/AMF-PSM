# P58 - Topological data analysis of structural change

**Track J - Advanced Methods: Topology, Learning, Information & Quantum**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Applied mathematician |
| **Upstream** | `docs/QUANTUM_NEURAL_RESEARCH.md` Discussion H2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Persistent homology is proposed as a way to detect structural change. Topological data analysis is a serious method with genuine financial applications, but it is usually applied to point clouds derived from time series. AMF has a seven-node graph and no time series. Whether there is anything for persistence to compute here is an open question, not an assumption.

## 2. Purpose

Determine whether persistent homology has anything to say about a seven-node weighted dependency graph, and either implement it with a stated interpretation or record a reasoned refusal.

## 3. Scope

**In scope**

- A filtration definition over the dependency graph by edge weight.
- Computation of persistence for the resulting filtration on example markets.
- An interpretation statement: what a persistent feature means structurally, if anything.

**Out of scope**

- Applying TDA to price or return series - forbidden.
- Adding a TDA library dependency to the runtime package.
- Reporting a persistence diagram without an interpretation.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Define the filtration explicitly: order edges by weight and build the clique complex as the threshold sweeps down.
2. Note that with seven nodes the homology is low-dimensional and finite, so exact computation is trivial - the question is meaning, not tractability.
3. Compute persistence on the example markets and on the P26 null models, because a feature is only interesting relative to a null.
4. Write the interpretation: a persistent one-dimensional class corresponds to a robust cycle in the dependency structure, which the framework already enumerates directly as feedback loops.
5. Confront that overlap honestly - if persistence tells you what feedback-loop enumeration already tells you, it adds nothing here.
6. Publish the finding either way; a reasoned refusal is a valid outcome and is more useful than an unused implementation.

## 5. Task board

- [ ] Define the weight filtration.
- [ ] Implement exact persistence for the small complex (standard library only).
- [ ] Compute on example markets and null models.
- [ ] Write the interpretation and the overlap analysis against feedback loops.
- [ ] Decide implement or refuse.
- [ ] Publish `docs/methods/tda.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish persistent homology and its financial applications from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** The summary states what TDA is applied to in the cited financial work.

### `math-formalizer`

- **Mandate:** Define the filtration and state what each homology class means for a dependency graph.
- **Inputs:** The graph model.
- **Output artifact:** A filtration and interpretation section.
- **Stop condition:** Each persistent class has a structural meaning or is marked meaningless here.

### `algorithm-implementer`

- **Mandate:** Implement exact persistence for the seven-node complex with no dependencies.
- **Inputs:** The filtration definition.
- **Output artifact:** A prototype under `docs/methods/_prototype/` or a rejected note.
- **Stop condition:** Results reproduce exactly, or the implementation is abandoned with a reason.

### `red-team-critic`

- **Mandate:** Argue that feedback-loop enumeration already provides everything persistence would.
- **Inputs:** Both outputs on the same markets.
- **Output artifact:** An overlap analysis.
- **Stop condition:** The overlap is quantified and the adopt-or-refuse decision follows from it.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `algorithm-implementer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-graph-algorithm` | A topological statistic is computed | Verifies the construction against its source and records complexity. |
| `amf-red-team` | A new method is proposed | Argues an existing simpler method already suffices. |
| `amf-doc-page` | The finding is published | Enforces documentation conventions including the negative-result rule. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/tda.md`
- A filtration definition
- Persistence results against null models
- An adopt-or-refuse decision with overlap analysis

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The filtration is defined explicitly and reproducibly.
- [ ] Persistence is computed against null models, not in isolation.
- [ ] The overlap with feedback-loop enumeration is quantified.
- [ ] A reasoned refusal is published if that is the outcome.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Carlsson, G. (2009). "Topology and Data." *Bulletin of the American Mathematical Society* 46(2), 255-308.
- Edelsbrunner, H., & Harer, J. L. (2010). *Computational Topology: An Introduction*. American Mathematical Society.
- Ghrist, R. (2008). "Barcodes: The persistent topology of data." *Bulletin of the American Mathematical Society* 45(1), 61-75.
- Gidea, M., & Katz, Y. (2018). "Topological data analysis of financial time series: Landscapes of crashes." *Physica A* 491, 820-834.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- Johnson, D. B. (1975). "Finding all the elementary circuits of a directed graph." *SIAM Journal on Computing* 4(1), 77-84.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.

## 11. Commit protocol

Commits from this project use the scope `p58`:

```text
docs(p58): define the edge-weight filtration for topological analysis
test(p58): compute persistence against null models on example markets
docs(p58): decide on adopting topological data analysis with overlap evidence
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
