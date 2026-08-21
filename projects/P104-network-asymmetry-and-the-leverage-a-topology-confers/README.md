# P104 - Network asymmetry and the leverage a topology confers

**Track R - Geopolitics, Sanctions and Fragmentation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Network scientist |
| **Upstream** | Discussion 7.1; P23; P101 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

P23 asked which centrality answers the framework's question. Chokepoint structure asks a different question again: not which system is most depended upon, but which position in the topology confers the ability to deny access to others. Betweenness is the classical measure of that, and the framework has never computed it, so the question has never been testable here.

## 2. Purpose

Determine whether a denial-capability measure is meaningful on a seven-node market graph, and either implement it or record why the graph is too small for the question.

## 3. Scope

**In scope**

- A statement of the question a denial measure answers.
- An assessment of whether seven nodes can support it.
- Implementation or a reasoned refusal.

**Out of scope**

- Any application to a real jurisdiction or participant.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the question precisely: which node lies on the paths others must use, which is what betweenness measures and what the framework's Katz centrality does not.
2. Confront the size problem immediately. On seven nodes, path structure is extremely limited, and a measure designed for large networks may be degenerate here - check before implementing.
3. Compute betweenness on the example markets and on P26's null models, and see whether the values discriminate at all or collapse to a few ties.
4. If they collapse, that is the answer: the question is not answerable at this scale, and the finding belongs in P128's resolution-limits work.
5. If they discriminate, implement it as a standalone query following P23's precedent, and state the question it answers in the docstring.
6. Keep it structural and unapplied; no jurisdiction, no participant.

## 5. Task board

- [ ] State the denial question formally.
- [ ] Assess whether seven nodes can support the measure.
- [ ] Compute on example markets and nulls.
- [ ] Test for degeneracy and ties.
- [ ] Implement or refuse with reasons.
- [ ] Publish `docs/graph/denial_capability.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State the question and the measure that answers it, from the primary source.
- **Inputs:** The reading list and `graph.py`.
- **Output artifact:** A formal statement.
- **Stop condition:** The question is distinguished from the one Katz centrality answers.

### `benchmark-runner`

- **Mandate:** Compute the measure on example markets and nulls and test for degeneracy.
- **Inputs:** The implementation and P26's nulls.
- **Output artifact:** A discrimination table.
- **Stop condition:** Tie frequency and value spread are reported.

### `algorithm-implementer`

- **Mandate:** Implement only if the measure discriminates, with no new dependencies.
- **Inputs:** The discrimination result.
- **Output artifact:** A diff or a rejection note.
- **Stop condition:** `mypy` strict passes, or the refusal is recorded with its evidence.

### `red-team-critic`

- **Mandate:** Argue the measure is degenerate at this scale and force the data to answer.
- **Inputs:** The results.
- **Output artifact:** A dissent section.
- **Stop condition:** The dissent is answered with the discrimination table.

**Hand-off order:** `math-formalizer` -> `benchmark-runner` -> `algorithm-implementer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-graph-algorithm` | The measure is implemented | Verifies against the source paper and states complexity. |
| `amf-centrality-diagnostics` | A centrality-family measure is added | Records the question it answers and its convergence properties. |
| `amf-ensemble-stats` | Discrimination is summarised | Applies the documented estimator and seeded intervals. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/graph/denial_capability.md`
- A formal question statement
- A discrimination table
- An implementation or a reasoned refusal

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The question is distinguished from the one Katz centrality answers.
- [ ] Degeneracy at seven nodes is tested, not assumed either way.
- [ ] Implementation happens only if the measure discriminates.
- [ ] A refusal, if that is the outcome, feeds P128's resolution-limits work.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Freeman, L. C. (1977). "A Set of Measures of Centrality Based on Betweenness." *Sociometry* 40(1), 35-41.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- Jackson, M. O. (2008). *Social and Economic Networks*. Princeton University Press.
- Barabasi, A.-L. (2016). *Network Science*. Cambridge University Press.
- Farrell, H., & Newman, A. L. (2019). "Weaponized Interdependence: How Global Economic Networks Shape State Coercion." *International Security* 44(1), 42-79.
- Albert, R., Jeong, H., & Barabasi, A.-L. (2000). "Error and attack tolerance of complex networks." *Nature* 406, 378-382.
- Callaway, D. S., Newman, M. E. J., Strogatz, S. H., & Watts, D. J. (2000). "Network Robustness and Fragility: Percolation on Random Graphs." *Physical Review Letters* 85(25), 5468-5471.

## 11. Commit protocol

Commits from this project use the scope `p104`:

```text
docs(p104): state the denial-capability question and the measure that answers it
test(p104): test betweenness for degeneracy on seven-node market graphs
docs(p104): implement or refuse the measure on the discrimination evidence
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
