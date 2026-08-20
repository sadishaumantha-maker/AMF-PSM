# P20 - Feedback loop enumeration: correctness and complexity against Johnson's algorithm

**Track D - Graph & Network Theory of Market Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Algorithms engineer |
| **Upstream** | `src/amf/graph.py` -> feedback-loop (simple-cycle) enumeration |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Feedback amplification is one of three components of every diagnostic score, and it is computed by enumerating simple cycles. The current property test compares against a brute-force search on small graphs. The dispute is whether that is evidence of correctness or only evidence of agreement on small inputs, and whether the enumeration's complexity is acceptable as market graphs densify.

## 2. Purpose

Establish the enumeration's correctness against the published algorithm for elementary circuits, state its complexity bound explicitly, and characterise the input sizes at which it stops being usable.

## 3. Scope

**In scope**

- A written specification of what counts as a feedback loop in AMF terms, including self-loops and multi-kind edges.
- Correctness verification against Johnson's elementary-circuit algorithm.
- A complexity statement and a measured growth curve up to a documented refusal threshold.

**Out of scope**

- Changing how loop weight enters the diagnostic score - that is P27 and P29.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Write the AMF definition of a feedback loop precisely: directed, simple, and how multi-kind parallel edges collapse.
2. State the reference algorithm and its bound in terms of vertices, edges and the number of elementary circuits.
3. Verify agreement with an independent implementation on exhaustively enumerated small digraphs, not only random ones.
4. Measure runtime growth on synthetic graphs of increasing density up to and beyond the seven-system case.
5. Define and implement a documented refusal threshold: beyond it, the query raises rather than hanging.
6. Record the complexity statement in the module docstring so the cost is visible at the call site.

## 5. Task board

- [ ] Write the AMF feedback-loop specification.
- [ ] Implement an independent reference enumerator for testing.
- [ ] Verify agreement over all digraphs up to a fixed small order.
- [ ] Measure and plot the growth curve.
- [ ] Implement the refusal threshold with a typed error.
- [ ] Publish `docs/graph/feedback_loops.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Write the precise definition and the complexity statement.
- **Inputs:** `graph.py`, the reading list.
- **Output artifact:** `docs/graph/feedback_loops.md`.
- **Stop condition:** The definition resolves self-loops and parallel multi-kind edges unambiguously.

### `algorithm-implementer`

- **Mandate:** Provide an independent reference enumerator and the refusal threshold.
- **Inputs:** The specification.
- **Output artifact:** A test-only reference plus a guarded production path.
- **Stop condition:** Exhaustive agreement holds up to the chosen order and the threshold raises a typed error.

### `benchmark-runner`

- **Mandate:** Measure the growth curve and identify the practical refusal point.
- **Inputs:** Synthetic graph generator.
- **Output artifact:** A measurement table.
- **Stop condition:** Runtime is characterised across at least four density levels.

### `property-test-author`

- **Mandate:** Encode agreement with the reference as a hypothesis property.
- **Inputs:** Both implementations.
- **Output artifact:** A property in `tests/unit/test_properties.py`.
- **Stop condition:** No counterexample is found within the example budget.

**Hand-off order:** `math-formalizer` -> `algorithm-implementer` -> `benchmark-runner` -> `property-test-author`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-graph-algorithm` | A graph query is added or changed | Checks the implementation against its source paper and states the complexity bound. |
| `amf-property-harness` | Agreement with a reference is claimed | Scaffolds the differential property test. |
| `amf-config-validator` | A refusal threshold is introduced | Adds validation raising `InvalidConfigError` with boundary tests. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/graph/feedback_loops.md`
- A test-only reference enumerator
- A growth-curve measurement table
- A guarded refusal threshold

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Exhaustive agreement with the reference holds for all digraphs up to the stated order.
- [ ] The complexity bound appears in the module docstring.
- [ ] Inputs beyond the threshold raise a typed `AMFError` rather than hanging.
- [ ] The 100% coverage gate still passes.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Johnson, D. B. (1975). "Finding all the elementary circuits of a directed graph." *SIAM Journal on Computing* 4(1), 77-84.
- Tarjan, R. (1972). "Depth-First Search and Linear Graph Algorithms." *SIAM Journal on Computing* 1(2), 146-160.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- Jackson, M. O. (2008). *Social and Economic Networks*. Princeton University Press.
- Claessen, K., & Hughes, J. (2000). "QuickCheck: a lightweight tool for random testing of Haskell programs." *ICFP '00*, 268-279.

## 11. Commit protocol

Commits from this project use the scope `p20`:

```text
docs(p20): specify feedback loops and state the enumeration complexity bound
test(p20): verify cycle enumeration against an independent reference
feat(p20): refuse feedback-loop enumeration beyond the documented threshold
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
