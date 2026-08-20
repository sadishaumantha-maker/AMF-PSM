# P21 - Articulation points: verification against Hopcroft-Tarjan and the directed-graph caveat

**Track D - Graph & Network Theory of Market Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 4 days |
| **Lead role** | Algorithms engineer |
| **Upstream** | `src/amf/graph.py` -> articulation points; `DiagnosticEngine` SPOF detection |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

A single point of failure is defined as an articulation point with low redundancy. Articulation points are a property of *undirected* connectivity, while the AMF dependency graph is directed. Applying the undirected notion to a directed dependency structure is a modelling choice that has never been argued in writing, and it changes which systems are flagged.

## 2. Purpose

Verify the implementation against the published linear-time algorithm, and settle explicitly whether the correct structural notion for AMF is an undirected articulation point, a strong articulation point, or a dominator-based cut.

## 3. Scope

**In scope**

- Verification against the standard depth-first articulation-point algorithm.
- A written comparison of undirected articulation points, strong articulation points and dominators for directed dependency graphs.
- A ruling, with the effect on flagged systems measured on the example markets.

**Out of scope**

- Changing the `_LOW_REDUNDANCY` threshold - that is P30.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the algorithm currently implemented and confirm its linear-time behaviour.
2. Verify against an independent reference on exhaustively enumerated small graphs.
3. Set out the three candidate notions and what each means in AMF terms: whose removal disconnects whom.
4. Measure, on `examples/sample_market.json` and generated variants, which systems each notion flags.
5. Choose the notion that matches the framework's semantics of dependency, and document the rejected alternatives.
6. If the ruling changes flagged systems, record it as a behavioural change with the reasoning.

## 5. Task board

- [ ] Confirm and document the implemented algorithm.
- [ ] Verify against a reference implementation exhaustively at small order.
- [ ] Write the three-notion comparison.
- [ ] Measure flagging differences on the example markets.
- [ ] Implement the ruling.
- [ ] Publish `docs/graph/articulation_semantics.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Set out the three candidate cut notions in AMF semantics.
- **Inputs:** `graph.py`, the reading list.
- **Output artifact:** `docs/graph/articulation_semantics.md`.
- **Stop condition:** Each notion states exactly what removal disconnects.

### `algorithm-implementer`

- **Mandate:** Verify the current implementation and implement the ruling.
- **Inputs:** The comparison and ruling.
- **Output artifact:** A diff under `src/amf/graph.py`.
- **Stop condition:** Exhaustive agreement at small order and `mypy` strict passing.

### `benchmark-runner`

- **Mandate:** Measure which systems each notion flags on the example markets.
- **Inputs:** Example markets and generated variants.
- **Output artifact:** A flagging comparison table.
- **Stop condition:** The table covers at least twenty generated market variants.

### `red-team-critic`

- **Mandate:** Construct a market where the chosen notion flags a system that is obviously not a single point of failure.
- **Inputs:** The ruling.
- **Output artifact:** A falsification attempt.
- **Stop condition:** No such market is found, or the ruling is revised.

**Hand-off order:** `math-formalizer` -> `algorithm-implementer` -> `benchmark-runner` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-graph-algorithm` | A connectivity query is changed | Verifies against the source algorithm and records complexity. |
| `amf-red-team` | A structural definition is chosen | Searches for inputs where the definition gives an absurd answer. |
| `amf-changelog-entry` | Flagged systems change | Records the behavioural change and its justification. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/graph/articulation_semantics.md`
- A verified implementation
- A flagging comparison table
- The implemented ruling

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Exhaustive agreement with a reference implementation at small order.
- [ ] The chosen cut notion is documented with the rejected alternatives.
- [ ] Any change to flagged systems is recorded in `CHANGELOG.md`.
- [ ] The red-team critic finds no absurd flagging, or the ruling was revised.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Hopcroft, J., & Tarjan, R. (1973). "Algorithm 447: efficient algorithms for graph manipulation." *Communications of the ACM* 16(6), 372-378.
- Tarjan, R. (1972). "Depth-First Search and Linear Graph Algorithms." *SIAM Journal on Computing* 1(2), 146-160.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- Albert, R., Jeong, H., & Barabasi, A.-L. (2000). "Error and attack tolerance of complex networks." *Nature* 406, 378-382.
- Callaway, D. S., Newman, M. E. J., Strogatz, S. H., & Watts, D. J. (2000). "Network Robustness and Fragility: Percolation on Random Graphs." *Physical Review Letters* 85(25), 5468-5471.

## 11. Commit protocol

Commits from this project use the scope `p21`:

```text
docs(p21): compare articulation, strong articulation and dominator cuts for AMF
test(p21): verify articulation points against a reference implementation
fix(p21): adopt the ruled cut notion for single-point-of-failure detection
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
